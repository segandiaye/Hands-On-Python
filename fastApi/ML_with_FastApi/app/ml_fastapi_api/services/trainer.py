import pickle, uuid, os
from datetime import datetime
from sklearn.linear_model import Ridge
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

from app.registry import model_registry
from app.models.schemas import TrainModelRequest, ModelMetadata
from app.storage.file_storage import save_model

def train_and_save_model(request: TrainModelRequest) -> ModelMetadata:
    data = fetch_california_housing()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=(1 - request.train_ratio), random_state=42
    )

    model = Ridge(alpha=request.alpha)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    rse = mean_squared_error(y_test, predictions) / np.var(y_test)

    model_id = str(uuid.uuid4())
    filename = f"{model_id}.pkl"
    save_model(model, filename)

    metadata = {
        "id": model_id,
        "name": request.name,
        "created_at": datetime.utcnow().isoformat(),
        "relative_squared_error": rse,
        "filename": filename
    }

    model_registry[model_id] = metadata
    return ModelMetadata(**metadata)
