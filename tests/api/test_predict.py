from tests.api.conftest import make_client

KEYS = {"model_name", "model_version", "label", "score", "threshold", "status"}
POSITIVE = {"title": "Great", "text": "Love this game, hours of fun"}
NEGATIVE = {"title": "Broke", "text": "The controller stopped working after a week"}


def test_predict_ok(client, headers):
    r = client.post("/predict", json=POSITIVE, headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert set(body) == KEYS
    assert body["label"] == "positive"
    assert body["status"] == "ok"


def test_predict_negative_label(client, headers):
    r = client.post("/predict", json=NEGATIVE, headers=headers)
    assert r.status_code == 200
    assert r.json()["label"] == "negative"


def test_missing_key_401(client):
    r = client.post("/predict", json=POSITIVE)
    assert r.status_code == 401
    assert "score" not in r.json()


def test_wrong_key_401(client):
    r = client.post("/predict", json=POSITIVE, headers={"x-api-key": "nope"})
    assert r.status_code == 401
    assert "score" not in r.json()


def test_server_without_api_key_fails_closed():
    with make_client(api_key="") as c:
        r = c.post("/predict", json=POSITIVE, headers={"x-api-key": "anything"})
        assert r.status_code == 401
        r = c.post("/predict", json=POSITIVE, headers={"x-api-key": ""})
        assert r.status_code == 401


def test_title_optional(client, headers):
    r = client.post("/predict", json={"text": "Love this game"}, headers=headers)
    assert r.status_code == 200


def test_star_title_same_score_as_empty_title(client, headers):
    a = client.post("/predict", json={"title": "Five Stars", "text": "x"}, headers=headers)
    b = client.post("/predict", json={"text": "x"}, headers=headers)
    assert a.json()["score"] == b.json()["score"]


def _assert_422_on(client, headers, payload, field):
    r = client.post("/predict", json=payload, headers=headers)
    assert r.status_code == 422
    assert field in r.json()["detail"][0]["loc"]


def test_blank_text_422(client, headers):
    _assert_422_on(client, headers, {"text": "   "}, "text")


def test_missing_text_422(client, headers):
    _assert_422_on(client, headers, {"title": "x"}, "text")


def test_long_text_422(client, headers):
    _assert_422_on(client, headers, {"text": "x" * 100_000}, "text")


def test_unknown_field_422(client, headers):
    _assert_422_on(client, headers, {"text": "x", "foo": 1}, "foo")


def test_wrong_type_422(client, headers):
    _assert_422_on(client, headers, {"text": 123}, "text")


def test_openapi_declares_api_key(client):
    schemes = client.get("/openapi.json").json()["components"]["securitySchemes"]
    assert any(s["type"] == "apiKey" and s["name"] == "x-api-key" for s in schemes.values())
