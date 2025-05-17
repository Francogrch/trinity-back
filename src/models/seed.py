from src.models import users, propiedades, parametricas, reservas
from datetime import datetime


def run():
    # Roles
    administrador = parametricas.create_rol("Administrador")
    encargado = parametricas.create_rol("Encargado")
    inquilino = parametricas.create_rol("Inquilino")

    # Tipos de propiedades
    dpto = parametricas.create_tipos_propiedad("Departamento")
    cabana = parametricas.create_tipos_propiedad("Cabaña")

    # Porcentajes del primer pago
    cero = parametricas.create_pol_reserva(
        "Seña del 0% del valor de la estadía", 0)
    veinte = parametricas.create_pol_reserva(
        "Seña del 20% del valor de la estadía", 0.2)
    cien = parametricas.create_pol_reserva(
        "Seña del 100% del valor de la estadía", 1)

    # Usuarios de ejemplo
    user1 = users.create_usuario(nombre="Juan", id_rol=1)
    user2 = users.create_usuario(nombre="Raul", id_rol=2)
    user3 = users.create_usuario(nombre="Roberto", id_rol=3)

    # Propiedades de ejemplo
    prop1 = propiedades.create_propiedad(
        nombre="Casa de Playa",
        descripcion="Hermosa casa frente al mar",
        entre_calles="Calle A y Calle B",
        calle="Calle del Mar",
        numero="123",
        piso="1",
        depto="A",
        huespedes=6,
        ambientes=4,
        banios=2,
        cocheras=1,
        precioNoche=150.0,
        codigoAcceso="1234",
        is_habilitada=True,
        id_pol_reserva=1,
        id_tipo=dpto.id,
        id_ciudad=1
    )

    prop2 = propiedades.create_propiedad(
        nombre="Departamento Céntrico",
        descripcion="Cómodo departamento en el centro",
        entre_calles="Av. Principal y Calle 9",
        calle="Calle Central",
        numero="456",
        piso="2",
        depto="B",
        huespedes=3,
        ambientes=2,
        banios=1,
        cocheras=0,
        precioNoche=75.0,
        codigoAcceso="1234",
        is_habilitada=True,
        id_pol_reserva=1,
        id_tipo=dpto.id,
        id_ciudad=2,
    )

    prop3 = propiedades.create_propiedad(
        nombre="Cabaña en el bosque",
        descripcion="Acogedora cabaña rodeada de naturaleza",
        entre_calles="Camino viejo y Ruta 5",
        calle="Sendero Verde",
        numero="789",
        piso="PB",
        depto="Único",
        huespedes=4,
        ambientes=3,
        banios=1,
        cocheras=2,
        precioNoche=120.0,
        codigoAcceso="1234",
        is_habilitada=True,
        id_pol_reserva=2,
        id_tipo=cabana.id,
        id_ciudad=3,
    )

    # Crear reservas de ejemplo
    #
    #
    #
    # Crear reservas de ejemplo
    reserva1 = reservas.create_reserva({
        "id_propiedad": prop1.id,
        "id_inquilino": user3.id,
        "id_usuario_carga": user2.id,
        "cantidad_personas": 4,
        "monto_pagado": 150.0,
        "monto_total": 600.0,
        "id_chat": None,
        "id_estado": 1,  # Estado "Pendiente"
        "fecha_inicio": datetime(2025, 12, 10),
        "fecha_fin": datetime(2025, 12, 14)
    })

    reserva2 = reservas.create_reserva({
        "id_propiedad": prop2.id,
        "id_inquilino": user3.id,
        "id_usuario_carga": user1.id,
        "cantidad_personas": 2,
        "monto_pagado": 75.0,
        "monto_total": 150.0,
        "id_chat": None,
        "id_estado": 1,
        "fecha_inicio": datetime(2025, 11, 1),
        "fecha_fin": datetime(2025, 11, 3)
    })

    reserva3 = reservas.create_reserva({
        "id_propiedad": prop3.id,
        "id_inquilino": user3.id,
        "id_usuario_carga": user2.id,
        "cantidad_personas": 3,
        "monto_pagado": 120.0,
        "monto_total": 360.0,
        "id_chat": None,
        "id_estado": 1,
        "fecha_inicio": datetime(2025, 10, 20),
        "fecha_fin": datetime(2025, 10, 23)
    })
