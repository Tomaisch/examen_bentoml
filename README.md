# Admission Prediction Service

Predicts a student's chance of admission based on academic profile data, using a Linear Regression model served with BentoML. The API is secured with JWT authentication.

## Development Setup (reproducing from scratch)

These steps are not required for evaluation (the Docker image already contains the trained model), but document how the project was built.

### 1. Install dependencies

```sh
uv sync
```

### 2. Download the raw data

```sh
wget -P data/raw/ https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv
```

### 3. Prepare the data

```sh
uv run python src/prepare_data.py
```

### 4. Train the model

```sh
uv run python src/train_model.py
```

### 5. Serve locally (without Docker)

```sh
uv run bentoml serve src.service:AdmissionPredictionService --port 3000
```

## Evaluation Setup (required)

### Prerequisites

- Docker
- Python 3.12+ with `pip`

### 1. Load the Docker image

```sh
docker load -i admission_prediction_service.tar
```

### 2. Run the service

```sh
docker run --rm -d -p 3000:3000 --name admission_service admission_prediction_service:latest
```

The API is now available at `http://localhost:3000`.

### 3. Install test dependencies

```sh
pip install -r requirements.txt
pip install pytest requests
```

### 4. Run the tests

```sh
pytest tests/ -v
```

### 5. Stop the service

```sh
docker stop admission_service
```

## API Usage

### Login

```sh
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"credentials": {"username": "user123", "password": "password123"}}'
```

Returns a JWT token, valid for 1 hour.

### Predict

```sh
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"input_data": {"GRE_Score": 320, "TOEFL_Score": 110, "University_Rating": 4, "SOP": 4.5, "LOR": 4.0, "CGPA": 9.0, "Research": 1}}'
```

Returns the predicted chance of admission (a value between 0 and 1).