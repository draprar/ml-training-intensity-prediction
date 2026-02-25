![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

# Training Intensity Prediction (Garmin Data)

End-to-end machine learning pipeline and inference service for predicting training intensity (`kcal/min`) using Garmin activity data.

This project demonstrates a complete ML workflow:
- Data exploration & preprocessing
- Model training (Random Forest pipeline)
- Model serialization
- Production-ready FastAPI inference service
- Lightweight frontend UI

---

## 📌 Project Overview

The goal is to build a reproducible end-to-end machine learning pipeline and deploy it as a REST API with a simple web interface.

The model predicts **calories per minute** based on:
- Heart rate metrics
- Activity type
- Distance / steps
- Stress metrics
- Time-based features (hour, day of week)

The project separates modeling, service layer, configuration, and presentation layer to follow production-ready backend practices.

---

## 📁 Project Structure
```
.
├── app/
│   ├── main.py                # FastAPI app (lifespan-based startup)
│   ├── config.py              # Paths & configuration
│   ├── api/                   # Routes & Pydantic schemas
│   ├── services/              # Model loading & prediction logic
│   ├── core/                  # Logging configuration
│   └── ui/                    # Templates + static files
│
├── data/
│   ├── raw/                   # Private Garmin exports
│   └── processed/             # Model-ready datasets
│
├── models/                    # Serialized model artifacts (not versioned)
├── notebooks/                 # EDA & modeling notebooks
├── tests/                     # Pytest test suite
│
├── requirements.txt
├── requirements-freeze.txt
└── README.md
```
---

## ⚙️ Requirements

- Python 3.9+
- pip
- (recommended) virtual environment
- Uvicorn
- Jupyter Notebook / JupyterLab (for modeling)

---

## 📦 Installation

1. Create virtual environment
```
python -m venv .venv
```

Activate:

**Windows**
```
.venv\Scripts\activate
```
**Linux / macOS**
```
source .venv/bin/activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

If you need exact environment replication:
```
pip install -r requirements-freeze.txt
```

---

## 🧠 Model Training

1. Place your Garmin export file:
```
data/raw/Activities.csv
```

2. Run notebooks in order:
```
notebooks/01_eda_preprocessing.ipynb
notebooks/02_modeling.ipynb
```

This generates:
```
models/random_forest_pipeline.joblib
models/model_metadata.joblib
```

*Model artifacts are not versioned in the repository.*

---

## 🏗 Architecture

- RandomForestRegressor wrapped in full preprocessing Pipeline
- Preprocessing handled via ColumnTransformer
- Model serialized with joblib
- Loaded at startup using FastAPI lifespan
- Stored in app.state for shared access
- REST inference endpoint (/predict)

---
## 🌐 Running the API

Start the application:
```
uvicorn app.main:app --reload
```

Available endpoints:
- UI - http://127.0.0.1:8000/ui
- Health check - http://127.0.0.1:8000/health
- Swagger docs - http://127.0.0.1:8000/docs

---

## 🔌 Example API Request

Example JSON payload

```
{
  "Avg_HR": 120.0,
  "Max_HR": 150.0,
  "Distance": 5.0,
  "Steps": 4000,
  "Avg_Stress": 0.0,
  "Stress_Change": 0.0,
  "Total_Reps": 0,
  "Total_Poses": 0,
  "Activity_Type": "Walking",
  "day_of_week": 2,
  "hour": 12
}
```

Example `curl` request

```
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "Avg_HR": 120.0,
           "Max_HR": 150.0,
           "Distance": 5.0,
           "Steps": 4000,
           "Avg_Stress": 0.0,
           "Stress_Change": 0.0,
           "Total_Reps": 0,
           "Total_Poses": 0,
           "Activity_Type": "Walking",
           "day_of_week": 2,
           "hour": 12
         }'
```

Example response
```
{
  "calories_per_min": 8.1234
}
```

---

## 🖥 UI Features

- Activity selection
- Dynamic form fields
- Client-side validation
- Async prediction (Axios)
- Error handling with status-specific messages
- No page reload

---

## ⚠️ Error Handling

- 400 — validation or input-related error
- 503 — model not loaded
- 500 — internal server error

Errors are logged using structured logging configuration.

---

## 🧪 Running Tests

```
pytest -q
```

Test coverage includes:
- Model loading behavior
- API endpoint responses
- Error handling scenarios

---

## 🧰 Tech Stack

- FastAPI
- Pydantic v2
- scikit-learn
- Pandas / NumPy
- Joblib
- Bootstrap 5
- Axios
- Pytest

---

## 🔒 Data Privacy

Raw Garmin data (`Activities.csv`) is not included in this repository due to personal and health-related information.

To reproduce results:
- Provide your own Garmin export
- Follow the notebook workflow

---

## 📄 License

MIT License.

---

## 👤 Author

Developed as part of an academic project and extended into a production-style ML API.
