from sklearn.exceptions import NotFittedError
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def prepare_input_df(payload: dict) -> pd.DataFrame:
    """
    Convert validated API payload into DataFrame expected by ML pipeline.
    """

    # Validate hour
    try:
        hour = int(payload['hour'])
    except (KeyError, TypeError, ValueError):
        raise ValueError('hour must be an integer')

    if not (0 <= hour <= 23):
        raise ValueError('hour must be in range [0, 23]')

    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)

    # Validate day_of_week
    try:
        day = int(payload['day_of_week'])
    except (KeyError, TypeError, ValueError):
        raise ValueError('day_of_week must be an integer')

    if not (0 <= day <= 6):
        raise ValueError('day_of_week must be in range [0, 6]')

    df = pd.DataFrame([{
        'Avg HR': payload.get('Avg_HR'),
        'Max HR': payload.get('Max_HR'),
        'Distance': payload.get('Distance', 0),
        'Steps': payload.get('Steps', 0),
        'Avg Stress': payload.get('Avg_Stress', 0),
        'Stress Change': payload.get('Stress_Change', 0),
        'Total Reps': payload.get('Total_Reps', 0),
        'Total Poses': payload.get('Total_Poses', 0),
        'Activity Type': payload.get('Activity_Type'),
        'day_of_week': day,
        'hour_sin': hour_sin,
        'hour_cos': hour_cos
    }])

    return df

def predict(model, df):
    if model is None:
        raise RuntimeError('Model is not available')

    try:
        prediction  = model.predict(df)
        return float(prediction [0])

    except NotFittedError as e:
        logger.exception('Model is not fitted')
        raise RuntimeError('Model is not fitted') from e

    except ValueError as e:
        logger.warning('Invalid input to model: %s', e)
        raise ValueError(f"Invalid input data: {e}") from e

    except Exception as e:
        logger.exception('Unexpected error during prediction', e)
        raise RuntimeError('Prediction failed') from e