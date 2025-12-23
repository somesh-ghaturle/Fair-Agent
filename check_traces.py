import os
import django
import sys

# Setup Django environment
sys.path.append('webapp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

from fair_agent_app.models import TraceLog, SpanLog

count = TraceLog.objects.count()
print(f"Total Traces: {count}")

if count > 0:
    last_trace = TraceLog.objects.last()
    print(f"Last Trace ID: {last_trace.trace_id}")
    print(f"Duration: {last_trace.duration_ms}ms")
    print(f"Spans: {last_trace.spans.count()}")
    for span in last_trace.spans.all():
        print(f"  - {span.name}: {span.duration_ms}ms ({span.status})")
else:
    print("No traces found.")
