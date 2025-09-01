from fastapi import FastAPI, Body, Request
from ml_service.fast_api_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

INFER_LATENCY = Histogram(
    "model_inference_duration_seconds", "Model inference time (seconds)",
    buckets=[0.001,0.003,0.007,0.015,0.03,0.06,0.12,0.25,0.5,1,2],
)
PREDICTIONS = Counter(
    "model_predictions_total", "Predictions by result and cache", ["result","cached"]
)
HTTP_REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests by method/path/status",
    ["method","path","status_code"],
)
app = FastAPI()
app.handler = FastApiHandler()
Instrumentator().instrument(app).expose(app)  

@app.middleware("http")
async def _count_status_mw(request: Request, call_next):
    response = await call_next(request)
    HTTP_REQUESTS.labels(request.method, request.url.path, str(response.status_code)).inc()
    return response

@app.post("/howmuch/")
def get_prediction_for_item(flat_id: str, model_params: dict = Body(...)):
    all_params = {"flat_id": flat_id, "model_params": model_params}
    try:
        with INFER_LATENCY.time():
            result = app.handler.handle(all_params)
        PREDICTIONS.labels("ok","false").inc()
        return result
    except Exception:
        PREDICTIONS.labels("error","false").inc()
        raise
