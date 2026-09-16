# Models for Deployment Exercise

This folder provides a small model artifact for learning how to put model inference behind a command-line interface or an HTTP endpoint. The example estimates whether a mobile-money transaction should be sent for review.

> **Classroom use only:** The coefficients and standardization values are illustrative. This model was not trained or validated for real fraud or financial decisions.

## Folder contents

- `model.json` stores model metadata, feature order, preprocessing values, coefficients, labels, and the decision threshold in a portable format.
- `predict.py` loads the artifact, validates an input record, applies the same standardization to each feature, and returns a JSON prediction.

The example uses only the Python standard library, so no package installation is required.

## Input schema

| Feature | Type | Valid values | Meaning |
|---|---|---|---|
| `amount_kes` | number | 0 or greater | Transaction amount in Kenyan shillings |
| `hour_of_day` | integer | 0 through 23 | Hour when the transaction was requested |
| `failed_attempts_24h` | integer | 0 or greater | Failed attempts associated with the account in the previous 24 hours |

## Run a prediction

From the repository root:

```bash
python models-for-deployment-exercise/predict.py \
  --amount-kes 15000 \
  --hour-of-day 2 \
  --failed-attempts-24h 3
```

The command prints a deployment-friendly response:

```json
{
  "label": "review",
  "review_probability": 0.997991,
  "model_version": "1.0.0"
}
```

## Use it in an API

Import `predict` in the route or controller that handles a request, then return its result as JSON:

```python
from predict import predict

response = predict(
    amount_kes=request_data["amount_kes"],
    hour_of_day=request_data["hour_of_day"],
    failed_attempts_24h=request_data["failed_attempts_24h"],
)
```

For the exercise, students can wrap this function with Flask, FastAPI, Django, or another framework; add health and prediction endpoints; and test valid and invalid requests.
