from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import logging

from app.config import TEMPLATES_DIR
from app.api.schemas import InputData
from app.services.prediction import prepare_input_df, predict

logger = logging.getLogger(__name__)
router = APIRouter()

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get('/health')
def health(request: Request):
    ready = getattr(request.app.state, 'model_ready', False)
    return {'status': 'ok' if ready else 'model_not_loaded'}

@router.post('/predict')
def predict_endpoint(request: Request, data: InputData):
    if not request.app.state.model_ready:
        raise HTTPException(status_code=503, detail='Model not available')

    try:
        model = request.app.state.model
        payload = data.model_dump()
        df = prepare_input_df(payload)
        calories_per_min = predict(model, df)
        return {'calories_per_min': calories_per_min}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        logger.exception('Runtime error during prediction')
        raise HTTPException(status_code=500, detail='Prediction failed')
    except Exception:
        logger.exception('Unexpected error during prediction')
        raise HTTPException(status_code=500, detail='Internal server error')

@router.get('/', include_in_schema=False)
def root():
    return RedirectResponse(url='/ui')

@router.get('/ui', response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
