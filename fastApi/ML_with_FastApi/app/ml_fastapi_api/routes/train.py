from fastapi import APIRouter
from app.models.schemas import TrainModelRequest, ModelMetadata
from app.services.trainer import train_and_save_model

router = APIRouter()

@router.post("/newcaliforniareg", response_model=ModelMetadata)
def train_model(request: TrainModelRequest):
    return train_and_save_model(request)
