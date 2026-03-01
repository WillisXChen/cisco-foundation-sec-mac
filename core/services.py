import asyncio
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import langfuse


from core.config import (
    INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET,
    QDRANT_URL
)
from core.logger import logger
from core.hardware import HardwareMonitor
from core.database import VectorDBManager, MetricsDBManager
from core.llm import LLMManager
from core.assistant_service import AssistantService
from core.schema import _latest_hw_stats_ref

# Initialize Arize Phoenix OpenTelemetry tracing
trace_provider = TracerProvider()
# Phoenix OTLP HTTP endpoint is often on the same port as the UI (6006) in recent versions
trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")))
trace.set_tracer_provider(trace_provider)

tracer = trace.get_tracer("cisco.foundation.sec")

# Initialize Langfuse - Hardcoded Keys to bypass environment loading issues
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-1234567890"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-1234567890"
os.environ["LANGFUSE_HOST"] = "http://localhost:3001"

langfuse_client = langfuse.Langfuse()



# Global dependencies
hw_monitor = HardwareMonitor()
llm_manager = LLMManager()
vector_db = VectorDBManager(url=QDRANT_URL)
assistant_service = AssistantService(llm_manager, vector_db)

# Shared state
metrics_db = None
_monitor_task = None

async def hardware_monitor_task():
    global metrics_db
    if metrics_db is None:
        try:
            metrics_db = MetricsDBManager(
                url=INFLUXDB_URL, token=INFLUXDB_TOKEN, 
                org=INFLUXDB_ORG, bucket=INFLUXDB_BUCKET
            )
            logger.info("✅ Connected to InfluxDB v3 for hardware monitoring.")
        except Exception as e:
            logger.error(f"❌ InfluxDB Connection error: {e}")

    while True:
        try:
            stats = await asyncio.to_thread(hw_monitor.get_stats)
            _latest_hw_stats_ref.update(stats)
            if metrics_db:
                await asyncio.to_thread(metrics_db.write_hardware_stats, stats)
        except Exception as e:
            logger.error(f"Monitor error: {e}")
        await asyncio.sleep(2)

def start_hardware_monitor():
    global _monitor_task
    if _monitor_task is None:
        _monitor_task = asyncio.create_task(hardware_monitor_task())
    return _monitor_task
