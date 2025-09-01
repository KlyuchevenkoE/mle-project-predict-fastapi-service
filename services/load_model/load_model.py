import mlflow
import os
import joblib
from dotenv import load_dotenv

load_dotenv(".env")

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))              
mlflow.set_registry_uri(os.environ.get("MLFLOW_REGISTRY_URI"))                 

print("tracking:", mlflow.get_tracking_uri())
print("registry:", mlflow.get_registry_uri())

logged_model = 'runs:/63d0ef17c3c84c71b03e0471bed43d46/models'

loaded_model = mlflow.pyfunc.load_model(logged_model)

joblib.dump(loaded_model, "models/best_model.joblib")
