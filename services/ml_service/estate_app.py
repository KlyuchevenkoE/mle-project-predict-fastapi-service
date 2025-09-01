from fastapi import FastAPI, Body
from ml_service.fast_api_handler import FastApiHandler

app = FastAPI()
app.handler = FastApiHandler()

@app.post("/howmuch/")
def get_prediction_for_item(
    flat_id: str,
    model_params: dict = Body(...) 
):
    all_params = {
        "flat_id": flat_id,
        "model_params": model_params
    }
    return app.handler.handle(all_params)