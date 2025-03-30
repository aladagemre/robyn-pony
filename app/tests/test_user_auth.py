import pytest
import json
import requests
import threading
from app.app import app
from app.db.database import db  # Import your database

def run_test_server():
    app.start(port=8001)

@pytest.fixture(scope="session", autouse=True)
def server():
    # Start the server in a thread instead of a process
    server_thread = threading.Thread(target=run_test_server, daemon=True)
    server_thread.start()
    
    # Give it a moment to start
    import time
    time.sleep(1)
    
    return "http://localhost:8001"

@pytest.fixture(autouse=True)
def clean_db():
    # Clean up before each test
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    yield
    # Clean up after each test
    db.drop_all_tables(with_all_data=True)

@pytest.fixture
def test_user_data():
    return {
        "name": "Emre",
        "email": "emre@example.com",
        "password": "123456"
    }

@pytest.fixture
def create_test_user(server, test_user_data):
    response = requests.post(
        f"{server}/signup",
        json=test_user_data,
        headers={"Content-Type": "application/json"}
    )
    return response.json()["token"]

def test_user_signup(server, test_user_data):
    response = requests.post(
        f"{server}/signup",
        json=test_user_data,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)

def test_duplicate_signup(server, test_user_data, create_test_user):
    response = requests.post(
        f"{server}/signup",
        json=test_user_data,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 409
    data = response.json()
    assert "error" in data
    assert data["error"] == "Email already exists"

def test_user_login(server, test_user_data, create_test_user):
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = requests.post(
        f"{server}/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)

def test_me_endpoint(server, test_user_data, create_test_user):
    token = create_test_user  # Using the fixture
    
    response = requests.get(
        f"{server}/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user_data["name"]
    assert data["email"] == test_user_data["email"]

def test_login_invalid_credentials(server, test_user_data, create_test_user):
    login_data = {
        "email": test_user_data["email"],
        "password": "wrong_password"
    }
    response = requests.post(
        f"{server}/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"] == "Invalid credentials"

def test_me_endpoint_invalid_token(server):
    response = requests.get(
        f"{server}/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 403
    data = response.json()
    assert "error" in data
    assert data["error"] == "Invalid token"

def test_me_endpoint_missing_token(server):
    response = requests.get(f"{server}/me")
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"] == "Token missing" 