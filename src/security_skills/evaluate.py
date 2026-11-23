"""Score labeled fixture predictions. This does not itself run or evaluate an LLM."""

from __future__ import annotations

from typing import Any

from .models import ValidationError, require_list, require_mapping


def score(labels: Any, predictions: Any) -> dict[str, float | int]:
    truth = require_list(labels, "labels")
    found = require_list(predictions, "predictions")
    for collection in (truth, found):
        if not all(isinstance(item, str) for item in collection):
            raise ValidationError("labels and predictions must contain strings")
        if len(collection) != len(set(collection)):
            raise ValidationError("labels and predictions must not contain duplicates")
    expected, actual = set(truth), set(found)
    tp, fp, fn = len(expected & actual), len(actual - expected), len(expected - actual)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision,
            "recall": recall, "f1": f1}


def score_document(document: Any) -> dict[str, float | int]:
    obj = require_mapping(document, "evaluation")
    return score(obj.get("expected"), obj.get("predicted"))
