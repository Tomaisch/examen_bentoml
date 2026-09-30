import jwt
import requests
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:3000"

VALID_CREDENTIALS = {"username": "user123", "password": "password123"}
INVALID_USERNAME = {"username": "user12345", "password": "password123"}
INVALID_PASSWORD = {"username": "user123", "password": "password12345"}
INVALID_TOKEN = 12345

VALID_INPUT = {
    "GRE_Score": 321,
    "TOEFL_Score": 108,
    "University_Rating": 4,
    "SOP": 3.5,
    "LOR": 4.0,
    "CGPA": 8.22,
    "Research": 1,
}
INVALID_INPUT = {
    "TOEFL_Score": 108,
    "University_Rating": 4,
    "SOP": 3.5,
    "LOR": 4.0,
    "CGPA": 8.22,
    "Research": 1,
}

JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

def get_token():
    response = requests.post(f"{BASE_URL}/login", json={"credentials": VALID_CREDENTIALS})
    return response.json()["token"]

def create_expired_token():
    expired_time = datetime.now(timezone.utc) - timedelta(hours=1)
    payload = {"sub": "user123", "exp": expired_time}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def test_login_valid_credentials():
    response = requests.post(f"{BASE_URL}/login", json={"credentials": VALID_CREDENTIALS})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_invalid_username():
    response = requests.post(f"{BASE_URL}/login", json={"credentials": INVALID_USERNAME})
    assert response.status_code == 401

def test_login_invalid_password():
    response = requests.post(f"{BASE_URL}/login", json={"credentials": INVALID_PASSWORD})
    assert response.status_code == 401

def test_predict_without_token():
    response = requests.post(f"{BASE_URL}/predict", json={"input_data": VALID_INPUT})
    assert response.status_code == 401

def test_predict_with_invalid_token():
    headers = {"authorization": f"Bearer {INVALID_TOKEN}"}
    response = requests.post(f"{BASE_URL}/predict", json={"input_data": VALID_INPUT}, headers=headers)
    assert response.status_code == 401

def test_predict_with_valid_token():
    token = get_token()
    headers = {"authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/predict", json={"input_data": VALID_INPUT}, headers=headers)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_with_invalid_input():
    token = get_token()
    headers = {"authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/predict", json={"input_data": INVALID_INPUT}, headers=headers)
    assert response.status_code != 200

def test_predict_with_expired_token():
    token = create_expired_token()
    headers = {"authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/predict", json={"input_data": VALID_INPUT}, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Token has expired"