# Video Games Reviews: Sentiment Classification

## Overview

This project classifies Amazon product reviews as negative or positive, so that complaints can be found without reading every review.

- **Data:** Amazon Reviews 2023, category Video Games, reviews written up to 31 December 2019.
- **Input:** review title and review text. **Label:** rating 1 and 2 are negative, 4 and 5 are positive, 3 is dropped.
- **Metric:** macro-F1, the mean of the F1 score of the negative class and of the positive class.
- **Split:** by time. The oldest 70% of the reviews train, the next 15% validate, the newest 15% test. The test set is scored once.

The whole work is in one notebook, `notebook.ipynb`: it downloads and cleans the data, explores it, compares a baseline with classical and transformer models, scores the final model on the test set, interprets it, and saves and reloads it.

## Result

| | Validation macro-F1 | Test macro-F1 |
|---|---|---|
| Baseline: TF-IDF and logistic regression | 0.9393 | 0.9397 |
| **Final: TF-IDF and SGD classifier, negative class weight x2** | **0.9501** | **0.9492** |

The final model finds 93.4% of the negative reviews on the test set, and 90.0% of the reviews it calls negative are negative. A frozen transformer encoder (MiniLM embeddings) scored 0.8898 on validation and was not competitive. The notebook explains why, and lists the limits and next steps.

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
| Memory | 16 GB or more (about 15 GB are in use at the heaviest step, developed with 32 GB). The notebook warns below 16 GB. |
| Free disk space | about 11 GB: data and cached embeddings 4.3 GB, packages 6 GB, models 0.1 GB |
| Downloads | the data (about 2.7 GB), the encoder (about 90 MB) and the Python packages. On Linux the `torch` wheel is the CUDA build, which is large and runs on the CPU. |
| GPU | not needed, everything runs on the CPU |
| Time | several hours on the first run, about 2 of them for the transformer embeddings. The data and the embeddings are cached, so a rerun is much faster. |

**With uv** (installs the locked dependencies, and the required Python if it is missing):

```bash
pip install uv        # or see https://docs.astral.sh/uv/getting-started/installation/
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

Open `notebook.ipynb` and run all cells. To run it without opening Jupyter, use `jupyter nbconvert --to notebook --execute --inplace notebook.ipynb` (with `uv run` in front for uv).

## Using the Saved Model

```python
import joblib
model = joblib.load('models/best_model/model.joblib')   # or pickle.load on model.pkl
model.predict(['Great game . Love it'])                 # 1 is positive, 0 is negative
```

The input is the title and the text joined with `" . "`. A title that is only a star rating, such as "Five Stars", is left empty, as in the notebook (Section 12.3 has a helper). `model_info.json` holds the settings, the scores and the library versions that the file needs.
