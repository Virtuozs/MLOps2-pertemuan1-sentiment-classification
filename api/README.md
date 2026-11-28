# Review Sentiment API

A FastAPI service that serves the saved model (`models/best_model/model.joblib`). It classifies an Amazon Video Games review as positive or negative.

## Structure

```
api/
├── main.py            app factory; loads the model once at startup
├── __main__.py        `python -m api` entry point (host and port from config.toml)
├── config.example.toml  template for config.toml (committed)
├── config.toml        your real settings and api_key (git-ignored)
├── dependencies.py    get_predictor
├── core/              config.py (settings), security.py (x-api-key check)
├── schemas/           pydantic request, response and model-info models
├── services/          text.py (input building), predictor.py (wraps the joblib)
├── routers/           predict.py (POST /predict), health.py (GET /health)
└── requirements.txt   slim dependencies for serving (no torch or jupyter)
```

## Setup

1. Copy `api/config.example.toml` to `api/config.toml`, which is git-ignored.
2. Generate a key and set it as `api_key`:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
3. Install and run, from the project root:
   ```bash
   uv run python -m api                       # development, with the full project environment
   # or on a server:
   pip install -r api/requirements.txt && python -m api
   ```

Settings come from `api/config.toml` (`api_key`, `model_path`, `model_info_path`, `model_name`, `host`, `port`). Environment variables such as `API_KEY` override the file. With no key set, every request gets 401. Swagger UI is at `/docs`.

## Endpoints

### `POST /predict`

Needs the header `x-api-key`. `title` is optional, `text` is mandatory (1 to 20,000 characters, not blank). Unknown fields give 422.

```bash
curl -X POST localhost:8000/predict \
  -H "x-api-key: <your key>" -H "content-type: application/json" \
  -d '{"title": "Great game", "text": "Love this game, hours of fun"}'
```

```json
{
  "model_name": "sentiment-sgd-tfidf",
  "model_version": "9b9c16336560",
  "label": "positive",
  "score": 3.0818533098089436,
  "threshold": 0.0,
  "status": "ok"
}
```

- `label` is `positive` when `score` is above `threshold`, otherwise `negative`.
- `score` is the model's decision score. `threshold` is 0.0, the value that scored best on the validation set (notebook Section 9.1).
- `model_version` is the first 12 characters of the SHA-256 of the model file.
- A title that is only a star rating, such as "Five Stars", is ignored, as in training.

| Status | When |
|---|---|
| 200 | prediction returned |
| 401 | `x-api-key` missing or wrong, or no key configured on the server |
| 422 | invalid body (blank or missing `text`, unknown field, wrong type) |

### `GET /health`

Open, returns `{"status": "ok"}`.

## Tests and Postman

```bash
uv run pytest -v
```

A Postman collection is in `docs/postman_collection.json`. Set its `api_key` variable to your key.

## Deploying

- Put Nginx or Caddy with HTTPS in front. The key travels in a header, so plain HTTP exposes it.
- Create `api/config.toml` on the server with a new key. Never copy the local one.
- Run from the project root: the model paths in the config are relative to the working directory.
- Keep the scikit-learn and numpy versions in `api/requirements.txt`. The saved model only loads reliably with the versions it was trained with.
- Check the install with `python scripts/verify_joblib.py`.
