# Video Games Reviews: Sentiment Classification

## Overview

This project classifies Amazon product reviews as negative or positive, so that complaints can be found without reading every review.

- **Data:** Amazon Reviews 2023, category Video Games, reviews written up to 31 December 2019.
- **Input:** review title and review text. **Label:** rating 1 and 2 are negative, 4 and 5 are positive, 3 is dropped.
- **Metric:** macro-F1, the mean of the F1 score of the negative class and of the positive class.
The whole work is in one notebook, `notebook.ipynb`: it downloads and cleans the data, explores it, compares a baseline with classical and transformer models, scores the final model on the test set, interprets it, and saves and reloads it.

## Method

**Data split.** By time, not at random, so the model is always tested on reviews newer than the ones it learned from, as in real use.

| Set | Share | Reviews | Period | Use |
|---|---|---|---|---|
| Train | oldest 70% | 1,946,795 | up to 2017-10-20 | fit models |
| Validation | next 15% | 417,170 | to 2018-12-31 | compare models, choose settings |
| Test | newest 15% | 417,171 | to 2019-12-31 | scored once, at the end |

**Model.** The title and the text are joined and turned into TF-IDF features (word 1-2 grams, 1.5 million features). A linear classifier (SGD, modified Huber loss) is trained on them, and errors on negative reviews count twice as much as errors on positive ones.

**Why this model.**
- Complaints are the minority (about 20% of the reviews), so the double weight raises the share of negative reviews found from 87.2% (baseline) to 93.0% on validation.
- 33 models were compared on validation only. Three linear models tied within the noise (0.0009), so the fastest one was chosen: it fits in 20 seconds, against 617 seconds for the LinearSVC that scored 0.9499.
- The frozen transformer encoder (MiniLM embeddings) was clearly worse (0.8898) and was not extended.

## Result

| | Validation macro-F1 | Test macro-F1 |
|---|---|---|
| Baseline: TF-IDF and logistic regression | 0.9393 | 0.9397 |
| **Final: TF-IDF and SGD classifier, negative class weight x2** | **0.9501** | **0.9492** |

On validation the final model has negative recall 0.930 and negative precision 0.912. On the test set it finds 93.4% of the negative reviews, and 90.0% of the reviews it calls negative are negative. The notebook explains why the transformer lost, and lists the limits and next steps.

## Project Structure

```
notebook.ipynb         main notebook, run from top to bottom
data/                  downloaded and prepared data, and cached embeddings (created by the notebook)
models/best_model/     final model: model.joblib, model.pkl and model_info.json
models/                the best classical model of the search (created by the notebook)
pyproject.toml         dependencies for uv
requirements.txt       dependencies for pip
```

## How to Run

Python 3.11 or newer is required, and an internet connection for the first run.

| Requirement | Needed |
|---|---|
| Memory | 16 GB or more (about 15 GB at the heaviest step). The notebook warns below 16 GB. |
| Free disk space | about 11 GB (data and embeddings 4.3 GB, packages 6 GB, models 0.1 GB) |
| Downloads | the data (about 2.7 GB), the encoder (about 90 MB) and the packages (on Linux `torch` is the large CUDA build, which runs on the CPU) |
| GPU | not needed, everything runs on the CPU |
| Time | several hours on the first run (about 2 for the transformer embeddings); reruns use the cache and are much faster |

**With uv** (installs the locked dependencies, and the required Python if it is missing):

```bash
pip install uv
uv sync
uv run jupyter lab
```

**With pip:**

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt jupyterlab ipykernel
jupyter lab
```

Open `notebook.ipynb` and run all cells, or run `jupyter nbconvert --to notebook --execute --inplace notebook.ipynb` (with `uv run` in front for uv).

## Using the Saved Model

```python
import joblib
model = joblib.load('models/best_model/model.joblib')   # or pickle.load on model.pkl
model.predict(['Great game . Love it'])                 # 1 is positive, 0 is negative
```

The input is the title and the text joined with `" . "`. A title that is only a star rating, such as "Five Stars", is left empty (Section 12.3 has a helper). `model_info.json` holds the settings, scores and library versions. `python scripts/verify_joblib.py` checks that the file reloads and predicts.

## Backend Service

A FastAPI service in `api/` serves the saved model with a `POST /predict` endpoint protected by an `x-api-key` header. Setup, endpoints and deployment are in [`api/README.md`](api/README.md).
