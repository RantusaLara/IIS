from fastapi.testclient import TestClient
from .api import app

client = TestClient(app)

def test_main():
	response = client.get("/")
	assert response.status_code == 200