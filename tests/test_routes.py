from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.api.routes as routes

VALID_PAYLOAD = {
    "Avg_HR": 100.0,
    "Max_HR": 140.0,
    "Distance": 3.5,
    "Steps": 3000,
    "Avg_Stress": 0.1,
    "Stress_Change": 0.0,
    "Total_Reps": 0,
    "Total_Poses": 0,
    "Activity_Type": "Walking",
    "day_of_week": 2,
    "hour": 6
}

def make_app():
    app = FastAPI()
    app.include_router(routes.router)
    return app

def test_health_not_ready():
    app = make_app()
    app.state.model_ready = False
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "model_not_loaded"}

def test_health_ready():
    app = make_app()
    app.state.model_ready = True
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_model_not_ready():
    app = make_app()
    app.state.model_ready = False
    client = TestClient(app)

    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 503
    assert response.json()["detail"] == "Model not available"

def test_predict_success(monkeypatch):
    app = make_app()
    app.state.model_ready = True
    app.state.model = object()

    monkeypatch.setattr(routes, "prepare_input_df", lambda _: "df")
    monkeypatch.setattr(routes, "predict", lambda *_: 3.14)

    client = TestClient(app)
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"calories_per_min": 3.14}

def test_predict_validation_error(monkeypatch):
    app = make_app()
    app.state.model_ready = True
    app.state.model = object()

    def fake_prepare(_):
        raise ValueError("bad input")

    monkeypatch.setattr(routes, "prepare_input_df", fake_prepare)

    client = TestClient(app)
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 400
    assert response.json()["detail"] == "bad input"

def test_predict_runtime_error(monkeypatch):
    app = make_app()
    app.state.model_ready = True
    app.state.model = object()

    monkeypatch.setattr(routes, "prepare_input_df", lambda _: "df")
    monkeypatch.setattr(routes, "predict", lambda *_: (_ for _ in ()).throw(RuntimeError()))

    client = TestClient(app)
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 500
    assert response.json()["detail"] == "Prediction failed"

def test_predict_unexpected_error(monkeypatch):
    app = make_app()
    app.state.model_ready = True
    app.state.model = object()

    monkeypatch.setattr(routes, "prepare_input_df", lambda _: "df")
    monkeypatch.setattr(routes, "predict", lambda *_: (_ for _ in ()).throw(Exception()))

    client = TestClient(app)
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"

def test_root_redirect():
    app = make_app()
    client = TestClient(app)

    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/ui"

def test_ui_renders(monkeypatch):

    class DummyTemplate:
        def TemplateResponse(self, *_):
            return "ok"

    monkeypatch.setattr(routes, "templates", DummyTemplate())

    app = FastAPI()
    app.include_router(routes.router)

    client = TestClient(app)

    r = client.get("/ui")

    assert r.status_code == 200