from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import numpy as np
import pandas as pd

from app.services.model_loader import load_model

app = FastAPI(title="Calories per Minute Prediction API")

# Load the trained RandomForest model with preprocessing
model, MODEL_READY = load_model("../../models/random_forest_pipeline.joblib")


class InputData(BaseModel):
    Avg_HR: float
    Max_HR: float
    Distance: float = 0
    Steps: float = 0
    Avg_Stress: float = 0
    Stress_Change: float = 0
    Total_Reps: float = 0
    Total_Poses: float = 0
    Activity_Type: str
    day_of_week: int
    hour: int

@app.get("/health")
def health():
    return {
        "status": "ok" if MODEL_READY else "model_not_loaded"
    }

@app.post("/predict")
def predict(data: InputData):
    """Predykcja kalorii na minutę na podstawie danych treningowych z zegarka Garmin."""

    # Walidacja godziny
    if data.hour is None or not (0 <= data.hour <= 23):
        raise HTTPException(status_code=400, detail="hour must be integer in [0,23]")

    # oblicz reprezentację cykliczną godziny
    hour_sin = np.sin(2 * np.pi * data.hour / 24)
    hour_cos = np.cos(2 * np.pi * data.hour / 24)

    # Mapowanie na nazwy kolumn modelu ML
    df = pd.DataFrame([{
        "Avg HR": data.Avg_HR,
        "Max HR": data.Max_HR,
        "Distance": data.Distance,
        "Steps": data.Steps,
        "Avg Stress": data.Avg_Stress,
        "Stress Change": data.Stress_Change,
        "Total Reps": data.Total_Reps,
        "Total Poses": data.Total_Poses,
        "Activity Type": data.Activity_Type,
        "day_of_week": data.day_of_week,
        "hour_sin": hour_sin,
        "hour_cos": hour_cos
    }])

    try:
        pred = model.predict(df)[0]
        return {"calories_per_min": float(pred)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return RedirectResponse(url="/ui")


@app.get("/ui", response_class=HTMLResponse)
def ui():
    """Zwraca prosty interaktywny interfejs HTML do predykcji kalorii/min."""

    return """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Predykcja intensywności treningu</title>
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            body { background-color: #f2f2f2; }
            .card { background-color: #e6e6e6; border: 1px solid #bfbfbf; }
            .form-control, .form-select { background-color: #f9f9f9; border-color: #bfbfbf; }
            .btn-primary { background-color: #6c757d; border-color: #6c757d; }
            .btn-primary:hover { background-color: #5a6268; }
            .alert-info { background-color: #d9d9d9; color: #333; border-color: #bfbfbf; }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    </head>

    <body>
        <div class="container mt-5">
            <h2 class="mb-4">Predykcja intensywności treningu (kcal/min)</h2>
            <div class="card shadow-sm p-4">
                <form id="predictForm" class="row g-3">

                    <!-- WYBÓR AKTYWNOŚCI -->
                    <div class="col-md-6">
                        <label class="form-label fw-bold">Wybierz typ aktywności</label>
                        <select name="Activity_Type" id="ActivityType" class="form-select" required>
                            <option value="">-- wybierz --</option>
                            <option value="Walking">Chodzenie</option>
                            <option value="Yoga">Joga</option>
                            <option value="Strength">Trening siłowy</option>
                            <option value="Cardio">Kardio</option>
                        </select>
                    </div>

                    <!-- POLA SPECYFICZNE -->
                    <div class="col-md-4 specific-field d-none" id="DistanceField">
                        <label class="form-label">Dystans (km)</label>
                        <input type="number" step="0.01" name="Distance" class="form-control">
                    </div>

                    <div class="col-md-4 specific-field d-none" id="StepsField">
                        <label class="form-label">Liczba kroków</label>
                        <input type="number" name="Steps" class="form-control">
                    </div>

                    <div class="col-md-4 specific-field d-none" id="AvgStressField">
                        <label class="form-label">Średni stres</label>
                        <input type="number" step="0.1" name="Avg_Stress" class="form-control">
                    </div>

                    <div class="col-md-4 specific-field d-none" id="StressChangeField">
                        <label class="form-label">Zmiana stresu</label>
                        <input type="number" step="0.1" name="Stress_Change" class="form-control">
                    </div>

                    <div class="col-md-4 specific-field d-none" id="TotalRepsField">
                        <label class="form-label">Liczba powtórzeń</label>
                        <input type="number" name="Total_Reps" class="form-control">
                    </div>

                    <div class="col-md-4 specific-field d-none" id="TotalPosesField">
                        <label class="form-label">Liczba serii</label>
                        <input type="number" name="Total_Poses" class="form-control">
                    </div>

                    <!-- POLA WSPÓLNE -->
                    <div class="col-md-4 common-field d-none">
                        <label class="form-label">Średnie tętno</label>
                        <input type="number" step="0.1" name="Avg_HR" class="form-control">
                    </div>

                    <div class="col-md-4 common-field d-none">
                        <label class="form-label">Maksymalne tętno</label>
                        <input type="number" step="0.1" name="Max_HR" class="form-control">
                    </div>

                    <div class="col-md-3 common-field d-none">
                        <label class="form-label">Dzień tygodnia (0–6)</label>
                        <input type="number" min="0" max="6" name="day_of_week" class="form-control">
                    </div>

                    <div class="col-md-3 common-field d-none">
                        <label class="form-label">Godzina (0–23)</label>
                        <input type="number" min="0" max="23" name="hour" class="form-control">
                    </div>

                    <!-- PREDYKCJA PRZYCISK-->
                    <div class="col-12 mt-3 d-none" id="PredictButtonWrapper">
                        <button type="submit" class="btn btn-primary">Wykonaj predykcję</button>
                    </div>

                </form>
            </div>

            <!-- WYNIK -->
            <div id="resultBox" class="alert alert-info mt-4 d-none"></div>
        </div>

        <script>
            const activitySelect = document.getElementById("ActivityType");
            const predictButton = document.getElementById("PredictButtonWrapper");
            const form = document.getElementById("predictForm");
            const resultBox = document.getElementById("resultBox");

            const activityFields = {
                "Walking": ["DistanceField", "StepsField"],
                "Yoga": ["AvgStressField", "StressChangeField"],
                "Strength": ["TotalRepsField", "TotalPosesField"],
                "Cardio": []
            };
            
            // Ukrywa wszystkie pasujące elementy i usuwa obowiązek wypełniania ich pól
            function hideFields(selector) {
                document.querySelectorAll(selector).forEach(el => {
                    el.classList.add("d-none");
                    el.querySelectorAll("input, select").forEach(i => i.required = false);
                });
            }
            
            // Pokazuje elementy o podanych ID i ustawia ich pola jako wymagane
            function showFieldsById(ids) {
                ids.forEach(id => {
                    const el = document.getElementById(id);
                    el.classList.remove("d-none");
                    el.querySelectorAll("input, select").forEach(i => i.required = true);
                });
            }
            
            // Reaguje na zmianę aktywności, ukrywa wszystko, pokazuje pola wspólne i specyficzne i przycisk predykcji
            function updateFields() {
                const selected = activitySelect.value;

                hideFields(".specific-field");
                hideFields(".common-field");
                predictButton.classList.add("d-none");

                if (!selected) return;

                document.querySelectorAll(".common-field").forEach(el => {
                    el.classList.remove("d-none");
                    el.querySelectorAll("input, select").forEach(i => i.required = true);
                });

                showFieldsById(activityFields[selected] || []);
                predictButton.classList.remove("d-none");
            }

            activitySelect.addEventListener("change", updateFields);
            
            // przetwarza formularz, zamienia puste pola na 0, wysyła dane do serwera i wyświetla wynik lub błąd
            form.addEventListener("submit", async function (event) {
                event.preventDefault();

                resultBox.className = "alert alert-info mt-4 d-none";

                const formData = new FormData(form);
                const jsonData = Object.fromEntries(formData.entries());

                for (let key in jsonData) {
                    if (jsonData[key] === "") { 
                        jsonData[key] = 0; // domyślna wartość dla ukrytych pól 
                    } else if (!isNaN(jsonData[key])) { 
                    jsonData[key] = Number(jsonData[key]); 
                    }
                }

                try {
                    const response = await axios.post("/predict", jsonData);
                    const value = response.data.calories_per_min.toFixed(4);

                    resultBox.classList.remove("d-none");
                    resultBox.innerHTML =
                        `<strong>Wynik predykcji:</strong> ${value} kcal/min`;

                } catch (error) {
                    resultBox.classList.remove("d-none");
                    resultBox.classList.add("alert-danger");
                    resultBox.innerText =
                        "Błąd: nieprawidłowe dane lub problem z serwerem.";
                }
            });
        </script>

    </body>
    </html>
    """

