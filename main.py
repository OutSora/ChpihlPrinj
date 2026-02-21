from fastapi import FastAPI
from pydantic import BaseModel
from agent import StudyAgent

# OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


# Ресурс — имя сервиса будет видно в Jaeger
resource = Resource(attributes={
    "service.name": "study-agent-service"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# ВАЖНО: используем имя контейнера jaeger
otlp_exporter = OTLPSpanExporter(
    endpoint="jaeger:4317",
    insecure=True
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


app = FastAPI()
agent = StudyAgent()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "AI Study Agent is working"}


@app.post("/ask")
def ask_agent(request: QuestionRequest):

    with tracer.start_as_current_span("agent_request") as span:

        span.set_attribute("user.question", request.question)

        response = agent.run(request.question)

        span.set_attribute("agent.response_length", len(response))

        return {"response": response}