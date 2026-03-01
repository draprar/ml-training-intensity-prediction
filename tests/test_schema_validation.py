from fastapi import FastAPI
from fastapi.testclient import TestClient
import app.api.routes as routes

def make_app():
    app = FastAPI()
    app.include_router(routes.router)
    setattr(app.state, "model_ready", True)
    setattr(app.state, "model", object())
    return app

def test_missing_required_field():
    app = make_app()
    client = TestClient(app)

    bad_payload = {
        "Avg_HR": 100.0
    }

    r = client.post("/predict", json=bad_payload)

    assert r.status_code == 422

def test_wrong_type():
    app = make_app()
    client = TestClient(app)

    bad_payload = {
        "Avg_HR": "not a float",
        "Max_HR": 140,
        "Activity_Type": "Walk",
        "day_of_week": 2,
        "hour": 12
    }

    r = client.post("/predict", json=bad_payload)

    assert r.status_code == 422