# Observability Module

This module provides tracing and metrics for the FAIR-Agent system.

## Components

### TelemetryManager
The central manager for all observability data. It handles:
- **Tracing**: Tracks the execution flow of requests.
- **Metrics**: Collects counters and gauges (latency, tokens).
- **Storage**: Saves traces to `logs/telemetry/` as JSON files.

## Usage

### Tracing
```python
from src.observability.telemetry import get_telemetry

telemetry = get_telemetry()
trace_id = "unique-id"
telemetry.start_trace(trace_id)

try:
    telemetry.start_span("operation_name")
    # Do work...
    telemetry.end_span("operation_name")
finally:
    telemetry.end_trace(trace_id)
```

### Metrics
```python
telemetry.record_metric("latency_ms", 150.5)
telemetry.increment_counter("requests_total")
```

## Data Location
Traces are stored in `logs/telemetry/` in the project root.
