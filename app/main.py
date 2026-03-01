from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging

from app.config import MODEL_PATH, STATIC_DIR
from app.core.logging_config import configure_logging
from app.api.routes import router as api_router
from app.services.model_loader import load_model

configure_logging()
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            logger.info('Loading model from %s', MODEL_PATH)
            app.state.model = load_model(MODEL_PATH)
            app.state.model_ready = True
            logger.info('Loaded model from %s', MODEL_PATH)
        except Exception as e:
            app.state.model = None
            app.state.model_ready = False
            logger.error('Failed to load model from %s', e)

        yield

    app = FastAPI(title='Calories per Minute Prediction API', lifespan=lifespan)

    app.include_router(api_router, prefix='')
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    return app

app = create_app()
