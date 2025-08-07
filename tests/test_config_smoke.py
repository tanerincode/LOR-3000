from fastapi.testclient import TestClient
from main import app


def test_config_endpoint_ok() -> None:
    client = TestClient(app)
    resp = client.get("/api/v1/config")
    assert resp.status_code == 200
    data = resp.json()
    assert "app_name" in data
