# Video Games Reviews: Sentiment Classification

## Overview

This project classifies Amazon product reviews as negative or positive, so that complaints can be found without reading every review.

- **Data:** Amazon Reviews 2023, category Video Games, reviews written up to 31 December 2019.
- **Input:** review title and review text.
- **Label:** rating 1 and 2 are negative, rating 4 and 5 are positive, rating 3 is dropped.
- **Metric:** macro-F1, the mean of the F1 score of the negative class and the F1 score of the positive class.
- **Split:** by time into train, validation and test sets. The test set is used only once, at the end.

The whole work is in one notebook, `notebook.ipynb`. It downloads the data, audits and cleans it, explores it, compares a baseline with several models, saves the final model in `models/`, and reloads it to check it.

## Project Structure

```
notebook.ipynb     main notebook, run from top to bottom
data/              downloaded and prepared data (created by the notebook)
models/            saved model (created by the notebook)
pyproject.toml     dependencies for uv
requirements.txt   dependencies for pip
```

## How to Run

Python 3.11 or newer is required. The first run downloads about 2.7 GB of data, so it needs disk space and an internet connection.

### Option 1: uv

Install uv first if it is not available (see the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)):

```bash
# Linux and macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# or with pip
pip install uv
```

Check the installation with `uv --version`, then set up the project. `uv sync` creates `.venv` and installs the locked dependencies, and uv downloads the required Python version if it is missing.

```bash
uv sync
uv run jupyter lab
```

Open `notebook.ipynb` and run all cells. To run it without opening Jupyter:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

### Option 2: Python and requirements.txt

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install jupyterlab ipykernel
jupyter lab
```

Open `notebook.ipynb` and run all cells. To run it without opening Jupyter:

```bash
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```
