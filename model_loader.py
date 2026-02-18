import joblib

def load_model(path: str):
    try:
        model = joblib.load(path)
        return model, True
    except Exception as e:
        print(f"Model loading failed: {e}")
        return None, False