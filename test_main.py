from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

def test_valid_prime_number():
    response = client.get("/api/classify-number", params={"number": "7"})
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 7
    assert data["is_prime"] is True
    assert "odd" in data["properties"]

def test_valid_perfect_number():
    response = client.get("/api/classify-number", params={"number": "28"})
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 28
    assert data["is_perfect"] is True
    assert "even" in data["properties"]

def test_valid_armstrong_number():
    response = client.get("/api/classify-number", params={"number": "153"})
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 153
    assert "armstrong" in data["properties"]

def test_even_number():
    response = client.get("/api/classify-number", params={"number": "10"})
    assert response.status_code == 200
    data = response.json()
    assert "even" in data["properties"]

def test_odd_number():
    response = client.get("/api/classify-number", params={"number": "9"})
    assert response.status_code == 200
    data = response.json()
    assert "odd" in data["properties"]

def test_invalid_number():
    response = client.get("/api/classify-number", params={"number": "abc"})
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is True
    assert data["message"] == "Invalid input. Please provide an integer."

def test_decimal_number():
    response = client.get("/api/classify-number", params={"number": "3.5"})
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is True
    assert data["message"] == "Decimals are not supported."
