"""Wraps the saved joblib model. Knows nothing about FastAPI or HTTP."""

import hashlib
from pathlib import Path

import joblib
from pydantic import BaseModel, ConfigDict

from api.schemas.model_info import ModelInfo
from api.schemas.predict import Label
from api.services.text import build_input


class Prediction(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: Label
    score: float


class Predictor:
    def __init__(self, model_path: Path, info_path: Path, model_name: str) -> None:
        self.name = model_name
        self.version = hashlib.sha256(model_path.read_bytes()).hexdigest()[:12]
        self.threshold = ModelInfo.model_validate_json(info_path.read_text()).threshold
        self._model = joblib.load(model_path)

    def predict(self, title: str, text: str) -> Prediction:
        score = float(self._model.decision_function([build_input(title, text)])[0])
        label = Label.POSITIVE if score > self.threshold else Label.NEGATIVE
        return Prediction(label=label, score=score)
