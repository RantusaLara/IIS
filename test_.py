from fastapi.testclient import TestClient
from src.serve.server import app
from flask_cors import CORS, cross_origin

#client = TestClient(app)

def test_main():
	request_body ={

		"temperature_2m": -0.1,
        "relativehumidity_2m": 72,        
        "windspeed_10m": 1.3
	
	}
	
	
	#response = client.post('/air/predict/', json = request_body)
	response = app.test_client().post('air/predict/', json = request_body)
	assert response.status_code == 200