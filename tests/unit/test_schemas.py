import warnings

import pytest
from pydantic import ValidationError

from api.schemas.model_info import ModelInfo
from api.schemas.predict import PredictRequest, PredictResponse


def test_blank_text_rejected():
    with pytest.raises(ValidationError):
        PredictRequest(text="   ")


def test_title_is_optional():
    assert PredictRequest(text="ok").title == ""


def test_too_long_text_rejected():
    with pytest.raises(ValidationError):
        PredictRequest(text="x" * 20001)


def test_unknown_field_rejected():
    with pytest.raises(ValidationError):
        PredictRequest(text="ok", extra=1)


def test_response_rejects_bad_label_and_version():
    good = dict(
        model_name="m", model_version="0123456789ab", label="positive",
        score=1.0, threshold=0.0,
    )
    assert PredictResponse(**good).status == "ok"
    with pytest.raises(ValidationError):
        PredictResponse(**{**good, "label": "neutral"})
    with pytest.raises(ValidationError):
        PredictResponse(**{**good, "model_version": "xyz"})


def test_response_emits_no_warning():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        PredictResponse(
            model_name="m", model_version="0123456789ab", label="negative",
            score=-1.0, threshold=0.0,
        )


def test_model_info_ignores_other_keys():
    assert ModelInfo.model_validate_json('{"threshold": 0.0, "other": 1}').threshold == 0.0
