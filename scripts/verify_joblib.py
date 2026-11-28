"""Check that the exported joblib reloads and runs inference.

Usage: python scripts/verify_joblib.py [path/to/model.joblib]
"""

import sys

import joblib

DEFAULT_PATH = "models/best_model/model.joblib"
SAMPLES = [
    "Great game . Love it",
    "Broke after a week . The controller stopped working",
]


def load_model(path: str = DEFAULT_PATH):
    return joblib.load(path)


if __name__ == "__main__":
    model = load_model(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH)
    for text, score in zip(SAMPLES, model.decision_function(SAMPLES)):
        print(f"{'positive' if score > 0 else 'negative'}  score {score:+.3f}  {text}")
