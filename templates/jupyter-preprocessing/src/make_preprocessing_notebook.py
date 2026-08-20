"""Create a small Jupyter notebook for flatten, normalize, and sigmoid lessons."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def markdown_cell(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code_cell(code: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.splitlines(True),
    }


def build_notebook() -> dict:
    cells = [
        markdown_cell(
            "# Flatten, Normalize, and Sigmoid\n\n"
            "A compact teaching notebook for image preprocessing exercises."
        ),
        code_cell(
            "import numpy as np\n\n"
            "# Demo image tensors: (m, num_px, num_px, channels)\n"
            "m_train, m_test, num_px = 5, 2, 2\n"
            "train_set_x_orig = np.arange(m_train * num_px * num_px * 3).reshape(m_train, num_px, num_px, 3)\n"
            "test_set_x_orig = np.arange(m_test * num_px * num_px * 3).reshape(m_test, num_px, num_px, 3)\n"
            "train_set_x_orig.shape, test_set_x_orig.shape\n"
        ),
        markdown_cell("## Flatten\n\nConvert each image into a column vector."),
        code_cell(
            "train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T\n"
            "test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T\n"
            "print(train_set_x_flatten.shape)\n"
            "print(test_set_x_flatten.shape)\n"
        ),
        markdown_cell("## Normalize\n\nScale pixel values to the `[0, 1]` range."),
        code_cell(
            "train_set_x = train_set_x_flatten / 255.0\n"
            "test_set_x = test_set_x_flatten / 255.0\n"
            "print(train_set_x.min(), train_set_x.max())\n"
            "print(test_set_x.min(), test_set_x.max())\n"
        ),
        markdown_cell("## Sigmoid\n\nImplement the activation function used in logistic regression."),
        code_cell(
            "def sigmoid(z):\n"
            "    return 1 / (1 + np.exp(-z))\n\n"
            "print(sigmoid(np.array([0, 2])))\n"
        ),
        markdown_cell("## Checks"),
        code_cell(
            "assert train_set_x_flatten.shape == (num_px * num_px * 3, m_train)\n"
            "assert test_set_x_flatten.shape == (num_px * num_px * 3, m_test)\n"
            "assert 0 <= train_set_x.min() <= train_set_x.max() <= 1\n"
            "assert np.isclose(sigmoid(0), 0.5)\n"
            "print('All checks passed.')\n"
        ),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a preprocessing notebook.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("flatten_normalize_sigmoid.ipynb"),
        help="Notebook path to write.",
    )
    args = parser.parse_args()
    args.output.write_text(json.dumps(build_notebook(), indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
