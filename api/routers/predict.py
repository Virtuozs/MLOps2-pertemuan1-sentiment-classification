from fastapi import APIRouter, Depends

from api.core.security import verify_api_key
from api.dependencies import get_predictor
from api.schemas.predict import PredictRequest, PredictResponse
from api.services.predictor import Predictor

router = APIRouter(tags=["predict"])


@router.post(
    "/predict",
    response_model=PredictResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Classify a product review as positive or negative",
)
def predict(
    body: PredictRequest, predictor: Predictor = Depends(get_predictor)
) -> PredictResponse:
    result = predictor.predict(body.title, body.text)
    return PredictResponse(
        model_name=predictor.name,
        model_version=predictor.version,
        label=result.label,
        score=result.score,
        threshold=predictor.threshold,
        status="ok",
    )
