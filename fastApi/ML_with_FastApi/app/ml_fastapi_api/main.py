from fastapi import FastAPI
from app.routes import train, predict, model_registry

app = FastAPI(title="Modular California Housing API")

# Include route modules
app.include_router(train.router)
app.include_router(predict.router)
app.include_router(model_registry.router)
