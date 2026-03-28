import logging
from pathlib import Path

import joblib

logger = logging.getLogger(__name__)

class ModelNotLoadedError(Exception):
    pass

def load_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Model file {path} not found.")

    try:
        return joblib.load(path)
    except Exception as e:
        logger.exception('Failed to load model from %s', path)
        raise ModelNotLoadedError (f"Could not load model: {e}") from e
