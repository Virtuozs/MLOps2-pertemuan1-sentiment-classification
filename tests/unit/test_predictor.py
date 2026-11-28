import re
from pathlib import Path

import pytest

from api.schemas.predict import Label
from api.services.predictor import Predictor

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def predictor() -> Predictor:
    return Predictor(
        ROOT / "models/best_model/model.joblib",
        ROOT / "models/best_model/model_info.json",
        "sentiment-sgd-tfidf",
    )


def test_version_is_12_hex(predictor):
    assert re.fullmatch(r"[0-9a-f]{12}", predictor.version)


def test_positive_review(predictor):
    result = predictor.predict("Great game", "Love it, hours of fun")
    assert result.label == Label.POSITIVE
    assert result.score > predictor.threshold


def test_negative_review(predictor):
    result = predictor.predict("Broke after a week", "The controller stopped working")
    assert result.label == Label.NEGATIVE
    assert result.score <= predictor.threshold
