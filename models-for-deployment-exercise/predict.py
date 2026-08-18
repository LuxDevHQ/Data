"""Run inference with the classroom transaction-risk model."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


MODEL_PATH = Path(__file__).with_name("model.json")


def load_model(path: Path = MODEL_PATH) -> dict[str, Any]:
    """Load and return the portable JSON model artifact."""
    with path.open(encoding="utf-8") as model_file:
        return json.load(model_file)


def predict(
    amount_kes: float,
    hour_of_day: int,
    failed_attempts_24h: int,
    model: dict[str, Any] | None = None,
) -> dict[str, float | str]:
    """Return the risk label and probability for one transaction."""
    if amount_kes < 0:
        raise ValueError("amount_kes must be zero or greater")
    if not 0 <= hour_of_day <= 23:
        raise ValueError("hour_of_day must be between 0 and 23")
    if failed_attempts_24h < 0:
        raise ValueError("failed_attempts_24h must be zero or greater")

    artifact = model or load_model()
    values = [amount_kes, hour_of_day, failed_attempts_24h]
    means = artifact["standardization"]["mean"]
    scales = artifact["standardization"]["scale"]
    standardized = [
        (value - mean) / scale
        for value, mean, scale in zip(values, means, scales, strict=True)
    ]
    logit = artifact["intercept"] + sum(
        coefficient * value
        for coefficient, value in zip(
            artifact["coefficients"], standardized, strict=True
        )
    )
    probability = 1.0 / (1.0 + math.exp(-logit))
    label_key = (
        "positive" if probability >= artifact["decision_threshold"] else "negative"
    )

    return {
        "label": artifact["labels"][label_key],
        "review_probability": round(probability, 6),
        "model_version": artifact["model_version"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amount-kes", type=float, required=True)
    parser.add_argument("--hour-of-day", type=int, required=True)
    parser.add_argument("--failed-attempts-24h", type=int, required=True)
    args = parser.parse_args()
    result = predict(args.amount_kes, args.hour_of_day, args.failed_attempts_24h)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
