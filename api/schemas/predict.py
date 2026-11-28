"""Request and response models of the /predict endpoint."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Label(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(
        default="",
        max_length=500,
        description="Review title (optional). A star-only title such as 'Five Stars' is ignored.",
        examples=["Great game"],
    )
    text: str = Field(
        min_length=1,
        max_length=20000,
        description="Review text (mandatory, must not be blank).",
        examples=["Great game, hours of fun and the story is excellent."],
    )


class PredictResponse(BaseModel):
    # pydantic reserves the `model_` prefix; this response owns such fields on purpose.
    model_config = ConfigDict(
        extra="forbid",
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "model_name": "sentiment-sgd-tfidf",
                "model_version": "9b9c16336560",
                "label": "positive",
                "score": 3.0818533098089436,
                "threshold": 0.0,
                "status": "ok",
            }
        },
    )

    model_name: str
    model_version: str = Field(pattern=r"^[0-9a-f]{12}$")
    label: Label
    score: float
    threshold: float
    status: Literal["ok"] = "ok"
