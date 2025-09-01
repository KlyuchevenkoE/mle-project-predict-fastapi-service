
import joblib
import numpy as np

class FastApiHandler:
    def __init__(self):

        self.param_types = {
            "flat_id": str,
            "model_params": dict
        }
        
        self.model_path = "models/best_model.joblib"
        self.load_model(self.model_path)
        
        self.required_model_params = [
            'x000', 'x001', 'x003', 'x005', 'x007', 'x009', 'x012', 'x017',
            'x019', 'x023'
            ]

    def load_model(self, model_path: str):
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")


    def how_much(self, model_params: dict) -> float:
        param_values_list = list(model_params.values())
        param_values_list = np.array([param_values_list], dtype=object)
        pred = self.model.predict(param_values_list)
        return float(pred[0])
        
    def check_required_query_params(self, query_params: dict) -> bool:

        if "flat_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["flat_id"], self.param_types["flat_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:

        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    
    def validate_params(self, params: dict) -> bool:

        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
		
    def handle(self, params):

        try:
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                flat_id = params["flat_id"]
                print(f"Predicting for flat_id: {flat_id} and model_params:\n{model_params}")
                cost = self.how_much(model_params)
                response = {
                    "flat_id": flat_id, 
                    "cost": cost
                }
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response

if __name__ == "__main__":

    test_params = {
	    "flat_id": "4742",
        "model_params": {
            'x000':307,
            'x001':9,
            'x003':9,
            'x005':10,
            'x007':82,
            'x009':5.84,
            'x012':9,
            'x017':0,
            'x019':0,
            'x023':0
        }
    }

    # Создаем обработчик запросов для API
    handler = FastApiHandler()

    # Делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")