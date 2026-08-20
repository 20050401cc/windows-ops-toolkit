import json
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from make_preprocessing_notebook import build_notebook


def test_notebook_has_required_cells():
    notebook = build_notebook()
    text = json.dumps(notebook)
    assert notebook["nbformat"] == 4
    assert "reshape(train_set_x_orig.shape[0], -1).T" in text
    assert "/ 255.0" in text
    assert "def sigmoid" in text
    assert "All checks passed." in text
