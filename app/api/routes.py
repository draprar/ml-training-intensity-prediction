import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.schemas import InputData
from app.config import TEMPLATES_DIR
from app.services.prediction import predict, prepare_input_df

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
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        logger.exception('Runtime error during prediction')
        raise HTTPException(status_code=500, detail='Prediction failed') from e
    except Exception as e:
        logger.exception('Unexpected error during prediction')
        raise HTTPException(status_code=500, detail='Internal server error') from e

@router.get('/', include_in_schema=False)
def root():
    return RedirectResponse(url='/ui')

@router.get('/ui', response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
