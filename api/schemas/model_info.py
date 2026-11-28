"""The part of models/best_model/model_info.json that the service needs."""

from pydantic import BaseModel, ConfigDict


class ModelInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    threshold: float
