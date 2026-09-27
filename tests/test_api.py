from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"

def test_air_quality_endpoint():
    res = client.get("/api/v1/air-quality?city=San%20Francisco")
    assert res.status_code == 200
    assert res.json()["location"]["city"] == "San Francisco"

def test_chat_endpoint():
    res = client.post("/api/v1/chat", json={"message": "What is the air quality in Seattle?"})
    assert res.status_code == 200
    assert "Seattle" in res.json()["location"]
    assert res.json()["grounding_status"] == "PASSED"
