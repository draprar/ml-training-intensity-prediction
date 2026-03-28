from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.api.routes as routes


def make_app():
    app = FastAPI()
    app.include_router(routes.router)
    app.state.model_ready = True
    app.state.model = object()
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


def test_out_of_range_values():
    app = make_app()
    client = TestClient(app)

    bad_payload = {
        "Avg_HR": -1,
        "Max_HR": 300,
        "Activity_Type": "Walking",
        "day_of_week": 8,
        "hour": 24,
    }

    r = client.post("/predict", json=bad_payload)

    assert r.status_code == 422


def test_extra_field_forbidden():
    app = make_app()
    client = TestClient(app)

    payload = {
        "Avg_HR": 100.0,
        "Max_HR": 140.0,
        "Activity_Type": "Walking",
        "day_of_week": 2,
        "hour": 12,
        "unexpected": "x",
    }

    r = client.post("/predict", json=payload)

    assert r.status_code == 422
