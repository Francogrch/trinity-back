import requests

def test_get_propiedades(base_url, auth_headers_admin, auth_headers_encargado, auth_headers_inquilino):
    response = requests.get(f"{base_url}/propiedades/", headers=auth_headers_admin)
    assert response.status_code == 200
    assert len(response.json()) == 15
    response = requests.get(f"{base_url}/propiedades/", headers=auth_headers_encargado)
    assert response.status_code == 200
    assert len(response.json()) == 1
    response = requests.get(f"{base_url}/propiedades/", headers=auth_headers_inquilino)
    assert response.status_code == 403
    response = requests.get(f"{base_url}/propiedades/")
    assert response.status_code == 401

def test_post_propiedades(base_url, auth_headers_admin):
    payload = { "ambientes":4,
        "banios":2,
        "calle":"Calle del Mar",
        "cocheras":1,
        "codigoAcceso":"abc",
        "depto":"A",
        "descripcion":"Hermosa casa frente al mar",
        "entre_calles":"Calle A y Calle B",
        "huespedes":6,
        "id_ciudad":1,
        "id_encargado":5,
        "id_pol_reserva":1,
        "id_tipo":1,
        "is_habilitada":False,
        "nombre":"casa",
        "numero":123,
        "piso":"1",
        "precioNoche":150.0,
        "requiere_documentacion":False}
    response = requests.post(f"{base_url}/propiedades/", json=payload)
    assert response.status_code == 401
    response = requests.post(f"{base_url}/propiedades/", headers=auth_headers_admin, json=payload)
    assert response.status_code == 422
    payload['codigoAcceso'] = "1234"
    response = requests.post(f"{base_url}/propiedades/", headers=auth_headers_admin, json=payload)
    assert response.status_code == 201
    response = requests.post(f"{base_url}/propiedades/", headers=auth_headers_admin, json=payload)
    assert response.status_code == 400
