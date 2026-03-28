import numpy as np
import pandas as pd
import pytest
from sklearn.exceptions import NotFittedError

from app.services.prediction import predict, prepare_input_df

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

def test_prepare_input_df_columns_and_values():
    frame = prepare_input_df(VALID_PAYLOAD)

    expected_cols = {
        'Avg HR','Max HR','Distance','Steps','Avg Stress','Stress Change',
        'Total Reps','Total Poses','Activity Type','day_of_week','hour_sin','hour_cos'
    }

    assert set(frame.columns) == expected_cols
    assert int(frame.at[0, 'day_of_week']) == VALID_PAYLOAD['day_of_week']

    hour = VALID_PAYLOAD['hour']
    expected_sin = np.sin(2 * np.pi * hour / 24)
    expected_cos = np.cos(2 * np.pi * hour / 24)

    assert pytest.approx(expected_sin, rel=1e-6) == float(frame.at[0, 'hour_sin'])
    assert pytest.approx(expected_cos, rel=1e-6) == float(frame.at[0, 'hour_cos'])

@pytest.mark.parametrize("bad_hour", [None, "x", 24, -1])
def test_prepare_input_df_invalid_hour(bad_hour):
    payload = VALID_PAYLOAD.copy()
    payload['hour'] = bad_hour
    with pytest.raises(ValueError):
        prepare_input_df(payload)

@pytest.mark.parametrize("bad_day", [None, "y", 7, -1])
def test_prepare_input_df_invalid_day(bad_day):
    payload = VALID_PAYLOAD.copy()
    payload['day_of_week'] = bad_day
    with pytest.raises(ValueError):
        prepare_input_df(payload)


@pytest.mark.parametrize(
    "field,value,expected_message",
    [
        ("Avg_HR", "abc", "must be numeric"),
        ("Max_HR", np.nan, "must be a finite number"),
        ("Distance", np.inf, "must be a finite number"),
        ("Steps", -np.inf, "must be a finite number"),
    ],
)
def test_prepare_input_df_rejects_invalid_numeric_values(field, value, expected_message):
    payload = VALID_PAYLOAD.copy()
    payload[field] = value

    with pytest.raises(ValueError) as exc:
        prepare_input_df(payload)

    assert expected_message in str(exc.value)

def test_predict_success():
    class DummyModel:
        def predict(self, _):
            return np.array([2.5])

    frame = prepare_input_df(VALID_PAYLOAD)
    result = predict(DummyModel(), frame)

    assert isinstance(result, float)
    assert result == pytest.approx(2.5)

def test_predict_model_none_raises():
    with pytest.raises(RuntimeError):
        predict(None, pd.DataFrame())

def test_predict_not_fitted_raises():
    class M:
        def predict(self, _):
            raise NotFittedError("not fitted")

    with pytest.raises(RuntimeError):
        predict(M(), pd.DataFrame())

def test_predict_value_error_propagated():
    class M:
        def predict(self, _):
            raise ValueError("bad shape")

    with pytest.raises(ValueError) as exc:
        predict(M(), pd.DataFrame())

    assert "Invalid input data" in str(exc.value)

def test_predict_unexpected_exception():
    class M:
        def predict(self, _):
            raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        predict(M(), pd.DataFrame())

