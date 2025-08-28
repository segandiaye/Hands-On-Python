from pydantic import BaseModel

class TrainModelRequest(BaseModel):
    name: str
    alpha: float
    train_ratio: float

class ModelMetadata(BaseModel):
    id: str
    name: str
    created_at: str
    relative_squared_error: float
    filename: str

class HouseFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

class PredictRequest(BaseModel):
    model_id: str
    features: HouseFeatures
