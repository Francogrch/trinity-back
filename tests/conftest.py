import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope='session', autouse=True)
def reset_db_before_and_after_tests():
    # Llamamos a resetdb() antes de cualquier test
    requests.get(f"{BASE_URL}/resetdb")
    yield  # Esto marca el punto donde pytest continuará con los tests
    # Llamamos a resetdb() después de que todos los tests hayan corrido
    requests.get(f"{BASE_URL}/resetdb")

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def jwt_admin():
    # Simula un login para obtener el JWT o usa uno fijo de testing
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "correo": "juan@mail.com",
        "password": "Grupo12!"
    })
    return response.json().get("token")

@pytest.fixture(scope="session")
def jwt_encargado():
    # Simula un login para obtener el JWT o usa uno fijo de testing
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "correo": "sofia@mail.com",
        "password": "Grupo12!"
    })
    return response.json().get("token")

@pytest.fixture(scope="session")
def jwt_inquilino():
    # Simula un login para obtener el JWT o usa uno fijo de testing
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "correo": "roberto@mail.com",
        "password": "Grupo12!"
    })
    return response.json().get("token")

@pytest.fixture
def auth_headers_admin(jwt_admin):
    return {"Authorization": f"Bearer {jwt_admin}"}

@pytest.fixture
def auth_headers_encargado(jwt_encargado):
    return {"Authorization": f"Bearer {jwt_encargado}"}

@pytest.fixture
def auth_headers_inquilino(jwt_inquilino):
    return {"Authorization": f"Bearer {jwt_inquilino}"}
