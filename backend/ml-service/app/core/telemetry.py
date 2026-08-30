"""OpenTelemetry configuration."""
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from app.core.config import settings


def configure_telemetry() -> None:
    """Configure OpenTelemetry tracing."""
    resource = Resource.create({
        "service.name": settings.SERVICE_NAME,
        "service.version": settings.VERSION,
        "service.environment": settings.ENV,
    })

    provider = TracerProvider(resource=resource)

    if settings.ENV != "test":
        try:
            otlp_exporter = OTLPSpanExporter(
                endpoint="http://tempo:4317",
                insecure=True,
            )
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        except Exception:
            pass  # Don't fail startup if telemetry unavailable

    trace.set_tracer_provider(provider)
