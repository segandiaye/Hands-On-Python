# Description

This project brings together examples to get started with the FastAPI REST API.

```bash
TODO : This example has not yet finished so the code and architecture is not clean
```

# Testing example

```bash
curl -X POST http://127.0.0.1:8000/newcaliforniareg \
  -H "Content-Type: application/json" \
  -d '{
    "train_ratio": 0.8,
    "alpha": 1.0,
    "name": "ridge_model_test"
}'
```