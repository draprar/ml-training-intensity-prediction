import pytest
import app.services.model_loader as model_loader

def test_load_model_file_not_found(tmp_path):
    missing = tmp_path / "no_such_model.joblib"
    with pytest.raises(FileNotFoundError):
        model_loader.load_model(missing)

def test_load_model_joblib_raises(monkeypatch, tmp_path):
    model_path = tmp_path / "model.joblib"
    model_path.write_text("dummy")

    def fake_load(_):
        raise Exception("joblib boom")

    monkeypatch.setattr("app.services.model_loader.joblib.load", fake_load)

    with pytest.raises(model_loader.ModelNotLoadedError):
        model_loader.load_model(model_path)

def test_load_model_success(monkeypatch, tmp_path):
    model_path = tmp_path / "model.joblib"
    model_path.write_text("dummy")

    fake_model = {"clf": "dummy"}

    monkeypatch.setattr(
        "app.services.model_loader.joblib.load",
        lambda _: fake_model
    )

    loaded = model_loader.load_model(model_path)
    assert loaded is fake_model

def test_load_model_preserves_exception_chain(monkeypatch, tmp_path):
    model_path = tmp_path / "model.joblib"
    model_path.write_text("dummy")

    original_error = RuntimeError("boom")

    def fake_load(_):
        raise original_error

    monkeypatch.setattr(
        "app.services.model_loader.joblib.load",
        fake_load
    )

    with pytest.raises(model_loader.ModelNotLoadedError) as exc:
        model_loader.load_model(model_path)

    assert exc.value.__cause__ is original_error