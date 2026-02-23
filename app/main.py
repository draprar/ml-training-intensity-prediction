from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from pathlib import Path
import logging

from app.config import MODEL_PATH, TEMPLATES_DIR
from app.core.logging_config import configure_logging
from app.api.routes import api_router
from app.services.model_loader import load_model

configure_logging()
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

def create_app() -> FastAPI:
    app = FastAPI(title='Calories per Minute Prediction API')

    app.include_router(api_router, prefix='')

    @app.on_event('startup')
    def startup_event():
        try:
            logger.info('Loading model from %s', MODEL_PATH)
            app.state.model = load_model(MODEL_PATH)
            app.state.model_ready = True
            logger.info('Loaded model from %s', MODEL_PATH)
        except Exception as e:
            app.state.model = None
            app.state.model_ready = False
            logger.error('Failed to load model from %s', e)

    return app

app = create_app()
