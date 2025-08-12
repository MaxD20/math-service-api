# Maxim Dragos, Data Engineer

from fastapi import FastAPI, Request
from prometheus_client import start_http_server, Counter, Histogram
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse
from math_service.controllers.math_controller import router
# from math_service.controllers import math_controller

# from math_service.services.messaging_service import publish_log

REQUEST_COUNT = Counter(
    "math_api_requests_total",
    "Total number of requests",
    ["method", "endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "math_api_request_latency_seconds",
    "Latency per endpoint",
    ["method", "endpoint", "http_status"],
)

start_http_server(8001)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Math API is running"}


@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code,
    ).inc()

    (REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code,
        ).observe(latency))

    return response

app.include_router(router, prefix="/api")
