import pytest
from fastapi.testclient import TestClient

from api.core.config import Settings, get_settings
from api.main import create_app

API_KEY = "test-key"


def make_client(api_key: str = API_KEY):
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(api_key=api_key)
    return TestClient(app)


@pytest.fixture(scope="module")
def client():
    with make_client() as c:
        yield c


@pytest.fixture
def headers() -> dict[str, str]:
    return {"x-api-key": API_KEY}
