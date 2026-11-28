from fastapi import Request

from api.services.predictor import Predictor


def get_predictor(request: Request) -> Predictor:
    return request.app.state.predictor
