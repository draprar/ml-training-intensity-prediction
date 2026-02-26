from fastapi.testclient import TestClient
from app.main import create_app

def test_model_load_success(monkeypatch):
    fake_model = object()

    monkeypatch.setattr(
        "app.main.load_model",
        lambda _: fake_model
    )

    app = create_app()

    with TestClient(app) as client:
        assert app.state.model_ready is True
        assert app.state.model is fake_model

        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}


def test_model_load_failure(monkeypatch):
    def boom(_):
        raise Exception("load failed")

    monkeypatch.setattr(
        "app.main.load_model",
        boom
    )

    app = create_app()

    with TestClient(app) as client:
        assert app.state.model_ready is False
        assert app.state.model is None

        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "model_not_loaded"}