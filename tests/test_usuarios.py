import requests

def test_get_usuarios_autenticado(base_url, auth_headers_admin):
    response = requests.get(f"{base_url}/usuarios/", headers=auth_headers_admin)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_usuarios_sin_autenticacion(base_url):
    response = requests.get(f"{base_url}/usuarios/")
    assert response.status_code == 401

def test_get_usuario_por_id(base_url, auth_headers_admin):
    # Suponiendo que el ID 1 existe
    response = requests.get(f"{base_url}/usuarios/1", headers=auth_headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert "nombre" in data
