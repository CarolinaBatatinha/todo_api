import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.core.security import create_access_token
from app.core.config import settings

client = TestClient(app)

@pytest.fixture
def test_user():
    return {"email": "test@example.com", "password": "testpass"}

@pytest.fixture
def test_token(test_user):
    return create_access_token(data={"sub": test_user["email"]})

def test_create_todo(test_token):
    test_data = {
        "title": "Test To-do",
        "description": "Lista de tarefas"
    }
    
    response = client.post(
        "/todos/",
        json=test_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["title"] == test_data["title"]
    