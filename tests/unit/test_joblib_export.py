import subprocess
import sys
from pathlib import Path

from scripts.verify_joblib import load_model

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "models/best_model/model.joblib"


def test_joblib_loads_in_fresh_process():
    code = f"import joblib; joblib.load(r'{MODEL}')"
    result = subprocess.run([sys.executable, "-c", code])
    assert result.returncode == 0


def test_inference_matches_expected_labels():
    model = load_model(str(MODEL))
    texts = [
        "Great game . Love it",
        "Broke after a week . The controller stopped working",
    ]
    scores = model.decision_function(texts)
    assert scores[0] > 0.0
    assert scores[1] < 0.0
    assert list(model.predict(texts)) == [1, 0]


def test_model_takes_raw_text():
    model = load_model(str(MODEL))
    assert len(model.predict(["x . y"])) == 1
