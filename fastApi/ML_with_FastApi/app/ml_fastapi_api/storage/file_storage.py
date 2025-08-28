import pickle, os

MODEL_DIR = "saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)

def save_model(model, filename):
    path = os.path.join(MODEL_DIR, filename)
    with open(path, "wb") as f:
        pickle.dump(model, f)

def load_model(filename):
    path = os.path.join(MODEL_DIR, filename)
    with open(path, "rb") as f:
        return pickle.load(f)
