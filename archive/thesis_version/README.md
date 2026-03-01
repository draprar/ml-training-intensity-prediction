# Training Intensity Prediction (Garmin Data)

Model uczenia maszynowego do predykcji intensywności treningu (kcal/min) na podstawie danych z zegarka Garmin.  
Projekt obejmuje pełny proces analityczny — od przygotowania danych, przez budowę modelu, aż po wdrożenie usługi predykcyjnej z interfejsem użytkownika.

---

## 📌 Cel projektu

Celem projektu jest opracowanie modelu uczenia maszynowego przewidującego intensywność treningu fizycznego (kcal/min) na podstawie danych pozyskanych z zegarka Garmin.  
Projekt obejmuje kompletny pipeline ML oraz wdrożenie modelu w postaci API z interfejsem użytkownika, umożliwiającym praktyczne wykorzystanie rozwiązania.

---

## 📁 Struktura projektu
```
├── data/  
│   ├── raw/  
│   │   └── Activities.csv (dane prywatne autora) 
│   └── processed/  
│       └── activities_model_ready.parquet (dane przetworzone, zanonimizowane)
│  
├── models/  
│   ├── (artefakty modelu nie są wersjonowane w repozytorium) 
│  
├── notebooks/  
│   ├── 00_quickstart_guide.ipynb  
│   ├── 01_eda_preprocessing.ipynb  
│   └── 02_modeling.ipynb  
│  
├── api.py  
│  
├── requirements.txt  
├── requirements-freeze.txt  
└── README.md  
```
---

## ⚙️ Wymagania

- Python ≥ 3.9  
- pip  
- Jupyter Notebook / JupyterLab  
- Windows / Linux / macOS  
- (opcjonalnie) Uvicorn do uruchomienia API

---

## 📦 Instalacja

Instalacja zależności:
```
pip install -r requirements.txt
```
Plik `requirements-freeze.txt` zawiera pełny snapshot środowiska deweloperskiego i może być użyty do odtworzenia identycznej konfiguracji.

---

## 🧪 Weryfikacja środowiska

Notebook `00_quickstart_guide.ipynb` zawiera komórkę sprawdzającą wersje kluczowych bibliotek:
```
import sys, platform, numpy as np, pandas as pd, sklearn, matplotlib, seaborn as sns

print("Python:", sys.version)  
print("Platform:", platform.platform())  
print("NumPy:", np.__version__)  
print("pandas:", pd.__version__)  
print("scikit-learn:", sklearn.__version__)  
print("Matplotlib:", matplotlib.__version__)  
print("Seaborn:", sns.__version__)  
```

---

## 🧠 Model

Model został wytrenowany jako Random Forest Regressor osadzony w pełnym pipeline’ie preprocessingowym (ColumnTransformer, kodowanie kategorii, imputacja braków).

Artefakty generowane po treningu:

- models/random_forest_pipeline.joblib — kompletny pipeline gotowy do predykcji  
- models/model_metadata.joblib — metadane środowiskowe (wersje bibliotek, opis modelu)

**📈 Wyniki modelu**

Model Random Forest osiąga stabilne wyniki w walidacji krzyżowej.
Najsilniejszym predyktorem intensywności treningu jest średnie tętno (`Avg HR`), natomiast pozostałe zmienne wnoszą dodatkową, choć mniejszą informację predykcyjną.

---

## 🌐 API predykcyjne (FastAPI)

Projekt zawiera usługę predykcyjną dostępną w pliku `api.py`.

### Uruchomienie API:
```
uvicorn api:app --reload
```

### Endpoint `/predict`

- wczytuje pipeline (random_forest_pipeline.joblib),  
- przyjmuje dane wejściowe w formacie JSON,  
- konwertuje je do DataFrame,  
- zwraca przewidywaną intensywność treningu (kcal/min).

---

## 🖥️ Interfejs użytkownika (UI)

UI dostępny jest pod adresem:

http://localhost:8000/

### Funkcjonalności:

- wybór typu aktywności,  
- dynamiczne wyświetlanie wymaganych pól (np. kroki dla chodzenia, stres dla jogi),  
- walidacja danych,  
- predykcja bez przeładowania strony,  
- wynik prezentowany w czytelnym boxie.

**Uwaga:**

Artefakty modelu (.joblib) nie są wersjonowane w repozytorium.
Aby uruchomić API, należy najpierw wytrenować model w notebooku 02_modeling.ipynb, co wygeneruje wymagane pliki w katalogu models/.
---

## 📊 Dane wejściowe

- Surowe dane: `data/raw/Activities.csv`  
- Dane przetworzone: `data/processed/activities_model_ready.parquet`

Dane pochodzą z eksportu aktywności z platformy Garmin Connect.

**Uwaga:**

Surowe dane treningowe (`Activities.csv`) nie są udostępniane publicznie ze względu na prywatny charakter informacji (dane osobowe i zdrowotne).

Aby odtworzyć projekt:
- Umieść własny plik `Activities.csv` w katalogu `data/raw/`.
- Uruchom notebook `01_eda_preprocessing.ipynb`.
- Następnie uruchom `02_modeling.ipynb`.

---

## 📚 Notebooki

1. **00_quickstart_guide.ipynb**  
   Konfiguracja środowiska, instrukcje i informacje organizacyjne.

2. **01_eda_preprocessing.ipynb**  
   Analiza eksploracyjna danych i przygotowanie zbioru do modelowania.

3. **02_modeling.ipynb**  
   Budowa, trenowanie i ewaluacja modeli ML.

---

## 🏁 Podsumowanie

Projekt dostarcza kompletny pipeline analityczny oraz gotowe środowisko inferencyjne umożliwiające wykonywanie predykcji intensywności treningu.  
Dzięki integracji modelu z API i interfejsem użytkownika rozwiązanie może być wykorzystywane zarówno w celach badawczych, jak i praktycznych.

---

## 📄 Licencja

Projekt został opracowany jako część pracy dyplomowej.
