# Tracing and Observability in FAIR-Agent

This document describes the observability system implemented in the FAIR-Agent project. The system provides distributed tracing, metrics collection, and performance monitoring for the LLM pipeline.

## Overview

The observability layer is designed to answer questions like:
- How long did the entire request take?
- Which agent handled the query?
- How many tokens were generated?
- Did the RAG retrieval step fail?

It uses a custom `TelemetryManager` that mimics OpenTelemetry concepts (Traces and Spans) but is lightweight and optimized for this specific architecture.

## Key Components

### 1. Telemetry Manager (`src/observability/telemetry.py`)
The central singleton that manages the lifecycle of traces.
- **Traces**: Represent a full user request (e.g., "User asks about Apple stock").
- **Spans**: Represent individual steps (e.g., "Retrieve Documents", "LLM Inference").

### 2. Context Propagation
We use Python's `contextvars` to propagate the `trace_id` across different modules without passing it as an argument to every function. This allows deep instrumentation of the `Orchestrator`, `Agents`, and `OllamaClient`.

## How to Trace the Model

### Viewing Traces
Traces are currently stored as JSON files in the `logs/telemetry/` directory.

**Example Trace Structure:**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "start_time": 1703251200.0,
  "end_time": 1703251205.5,
  "duration_ms": 5500.0,
  "metadata": {
    "user_id": "user_123",
    "query_domain": "finance"
  },
  "spans": [
    {
      "name": "orchestrator_process",
      "start_time": 1703251200.1,
      "duration_ms": 5400.0,
      "status": "success"
    },
    {
      "name": "llm_inference",
      "start_time": 1703251202.0,
      "duration_ms": 2000.0,
      "metadata": {
        "model": "llama3.2",
        "tokens": 150
      }
    }
  ]
}
```

### Adding New Spans
To trace a new function or component, use the `start_span` method from the global telemetry instance.

```python
from src.observability.telemetry import telemetry_manager

def my_custom_function():
    # Start a span
    span = telemetry_manager.start_span("my_custom_function")
    
    try:
        # Do work...
        result = complex_calculation()
        
        # Add metadata
        span.metadata["result_size"] = len(result)
        span.status = "success"
        
    except Exception as e:
        span.status = "error"
        span.error_message = str(e)
        raise
    finally:
        # Always end the span
        telemetry_manager.end_span(span)
```

## Database Integration (New)

We are migrating trace storage to the SQLite database for better querying.
- **Model**: `TraceLog` and `SpanLog` in `webapp/fair_agent_app/models.py`.
- **Querying**: You can use the Django Admin interface to view and filter traces by latency, status, or domain.

## Metrics

The system also collects aggregated metrics:
- `llm_latency`: Time taken for LLM to generate a response.
- `llm_tokens`: Number of tokens generated.
- `rag_retrieval_time`: Time taken to search the vector database.
