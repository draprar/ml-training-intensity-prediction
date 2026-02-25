from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest_pipeline.joblib"
TEMPLATES_DIR = BASE_DIR / "app" / "ui" / "templates"
STATIC_DIR = BASE_DIR / "app" / "ui" / "static"