import requests

def test_reservas_inquilino(base_url, auth_headers_inquilino):
    payload = {
        "cantidad_personas": 4,
        "estado": "Finalizada",
        "fecha_inicio": "2026-12-14T00:00:00",
        "fecha_fin": "2026-12-10T00:00:00",
        "id_chat": None,
        "id_estado": 4,
        "id_propiedad": 1,
        "monto_pagado": 150.0,
        "monto_total": 600.0,
    }
    # GET reservas del inquilino
    response = requests.get(f"{base_url}/reservas/", headers=auth_headers_inquilino)
    assert response.status_code == 200
    assert len(response.json()) == 2
    # GET reserva por id
    response = requests.get(f"{base_url}/reservas/1", headers=auth_headers_inquilino)
    assert response.status_code == 403
    response = requests.get(f"{base_url}/reservas/2", headers=auth_headers_inquilino)
    assert response.status_code == 200
    # POST crear reserva
    response = requests.post(f"{base_url}/reservas/", headers=auth_headers_inquilino, json=payload)
    assert response.status_code == 422
    payload['fecha_inicio'] = "2026-12-10T00:00:00"
    payload['fecha_fin'] = "2026-12-14T00:00:00"
    response = requests.post(f"{base_url}/reservas/", headers=auth_headers_inquilino, json=payload)
    assert response.status_code == 201
    response = requests.post(f"{base_url}/reservas/", headers=auth_headers_inquilino, json=payload)
    assert response.status_code == 400
    # PATCH cancelar reserva
    response = requests.patch(f"{base_url}/reservas/cancelar/2", headers=auth_headers_inquilino)
    assert response.status_code == 200
    response = requests.patch(f"{base_url}/reservas/cancelar/2", headers=auth_headers_inquilino)
    assert response.status_code == 404
