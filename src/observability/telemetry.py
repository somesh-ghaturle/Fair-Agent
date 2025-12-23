"""
Observability Module for FAIR-Agent

This module provides tracing, metrics, and monitoring capabilities for the LLM system.
It allows tracking request flows, measuring latency/tokens, and monitoring system health.
"""

import time
import logging
import json
import threading
import contextvars
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Context variable for current trace ID
current_trace_id = contextvars.ContextVar('current_trace_id', default=None)

@dataclass
class Span:
    """A single operation within a trace"""
    name: str
    start_time: float
    end_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "running"  # running, success, error
    error_message: Optional[str] = None
    
    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0

@dataclass
class Trace:
    """A complete request trace"""
    trace_id: str
    start_time: float
    end_time: Optional[float] = None
    spans: List[Span] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_span(self, span: Span):
        self.spans.append(span)
        
    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0

class TelemetryManager:
    """
    Central manager for system telemetry (Tracing & Metrics)
    """
    
    def __init__(self, storage_dir: str = "logs/telemetry"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self._traces: Dict[str, Trace] = {}
        self._metrics: Dict[str, List[float]] = {}
        self._counters: Dict[str, int] = {}
        self._lock = threading.Lock()
        
        # Auto-save thread could be added here
        
    def start_trace(self, trace_id: str, metadata: Optional[Dict] = None) -> Trace:
        """Start a new trace"""
        # Set context variable
        current_trace_id.set(trace_id)
        
        with self._lock:
            trace = Trace(
                trace_id=trace_id,
                start_time=time.time(),
                metadata=metadata or {}
            )
            self._traces[trace_id] = trace
            return trace
            
    def end_trace(self, trace_id: Optional[str] = None):
        """End a trace and save it"""
        tid = trace_id or current_trace_id.get()
        if not tid:
            return

        with self._lock:
            if tid in self._traces:
                trace = self._traces[tid]
                trace.end_time = time.time()
                self._save_trace(trace)
                # Keep only recent traces in memory
                if len(self._traces) > 100:
                    oldest = min(self._traces.keys(), key=lambda k: self._traces[k].start_time)
                    del self._traces[oldest]
        
        # Clear context if it matches
        if current_trace_id.get() == tid:
            current_trace_id.set(None)

    def update_trace_metadata(self, trace_id: str, metadata: Dict[str, Any]):
        """Update metadata for an active trace"""
        with self._lock:
            if trace_id in self._traces:
                self._traces[trace_id].metadata.update(metadata)

    def start_span(self, name: str, metadata: Optional[Dict] = None, trace_id: Optional[str] = None) -> Optional[Span]:
        """Start a span within a trace"""
        tid = trace_id or current_trace_id.get()
        if not tid:
            return None
            
        with self._lock:
            if tid in self._traces:
                span = Span(
                    name=name,
                    start_time=time.time(),
                    metadata=metadata or {}
                )
                self._traces[tid].add_span(span)
                return span
        return None

    def end_span(self, span_name: str, status: str = "success", error: Optional[str] = None, trace_id: Optional[str] = None, metadata: Optional[Dict] = None):
        """End a span"""
        tid = trace_id or current_trace_id.get()
        if not tid:
            return

        with self._lock:
            if tid in self._traces:
                trace = self._traces[tid]
                # Find the last span with this name that is running
                for span in reversed(trace.spans):
                    if span.name == span_name and span.end_time is None:
                        span.end_time = time.time()
                        span.status = status
                        span.error_message = error
                        if metadata:
                            span.metadata.update(metadata)
                        break

    def record_metric(self, name: str, value: float):
        """Record a numerical metric (latency, tokens, etc.)"""
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = []
            self._metrics[name].append(value)
            # Keep history limited
            if len(self._metrics[name]) > 1000:
                self._metrics[name] = self._metrics[name][-1000:]

    def increment_counter(self, name: str, value: int = 1):
        """Increment a counter"""
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + value

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        summary = {
            "counters": self._counters.copy(),
            "metrics": {}
        }
        
        for name, values in self._metrics.items():
            if values:
                summary["metrics"][name] = {
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                    "last": values[-1]
                }
        return summary

    def _save_trace(self, trace: Trace):
        """Save trace to disk and database"""
        try:
            # 1. Save to JSON file
            data = {
                "trace_id": trace.trace_id,
                "start_time": datetime.fromtimestamp(trace.start_time).isoformat(),
                "end_time": datetime.fromtimestamp(trace.end_time).isoformat() if trace.end_time else None,
                "duration_ms": trace.duration_ms,
                "metadata": trace.metadata,
                "spans": [
                    {
                        "name": s.name,
                        "duration_ms": s.duration_ms,
                        "status": s.status,
                        "error": s.error_message,
                        "metadata": s.metadata
                    } for s in trace.spans
                ]
            }
            
            filename = self.storage_dir / f"trace_{trace.trace_id}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)

            # 2. Save to SQLite Database (if Django is available)
            try:
                from fair_agent_app.models import TraceLog, SpanLog
                from django.db import transaction
                
                # Use atomic transaction to ensure consistency
                with transaction.atomic():
                    db_trace = TraceLog.objects.create(
                        trace_id=trace.trace_id,
                        start_time=trace.start_time,
                        end_time=trace.end_time,
                        duration_ms=trace.duration_ms,
                        metadata=trace.metadata
                    )
                    
                    for s in trace.spans:
                        SpanLog.objects.create(
                            trace=db_trace,
                            name=s.name,
                            start_time=s.start_time,
                            end_time=s.end_time,
                            duration_ms=s.duration_ms,
                            status=s.status,
                            error_message=s.error_message,
                            metadata=s.metadata
                        )
            except ImportError:
                # Django environment not loaded
                pass
            except Exception as db_err:
                logger.error(f"Failed to save trace to DB: {db_err}")
                
        except Exception as e:
            logger.error(f"Failed to save trace: {e}")

# Global instance
_telemetry = TelemetryManager()

def get_telemetry() -> TelemetryManager:
    return _telemetry
