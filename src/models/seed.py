from src.models import users, propiedades, parametricas
from src.models.users.user import Tarjeta
from datetime import date


def run():
    # Roles
    administrador = parametricas.create_rol("Administrador")
    encargado = parametricas.create_rol("Encargado")
    inquilino = parametricas.create_rol("Inquilino")

    # Tipos de identificación
    dni = parametricas.create_tipo_identificacion("DNI")
    pasaporte = parametricas.create_tipo_identificacion("Pasaporte")
    cedula = parametricas.create_tipo_identificacion("Cédula")

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

    # Paises de ejemplo
    pais_arg = parametricas.create_pais("Argentina")
    pais_uru = parametricas.create_pais("Uruguay")
    pais_chi = parametricas.create_pais("Chile")

    # Usuarios de ejemplo con múltiples roles y tipo de identificación
    user1 = users.create_usuario(
        nombre="Juan",
        apellido="Pérez",
        correo="juan@mail.com",
        roles_ids=[administrador.id, inquilino.id],
        password="1234",
        id_tipo_identificacion=dni.id,
        numero_identificacion="12345678",
        id_pais=pais_arg.id,
        fecha_nacimiento="1990-01-01"
    )
    user2 = users.create_usuario(
        nombre="Raul",
        apellido="Gómez",
        correo="raul@mail.com",
        roles_ids=[encargado.id, inquilino.id],
        password="1234",
        id_tipo_identificacion=pasaporte.id,
        numero_identificacion="A1234567",
        id_pais=pais_uru.id,
        fecha_nacimiento="1985-05-10"
    )
    user3 = users.create_usuario(
        nombre="Roberto",
        apellido="López",
        correo="roberto@mail.com",
        roles_ids=[inquilino.id],
        password="1234",
        id_tipo_identificacion=cedula.id,
        numero_identificacion="87654321",
        id_pais=pais_chi.id,
        fecha_nacimiento="2000-12-31"
    )
    print("Usuarios y tipos de identificación de ejemplo creados")

    # Usuarios adicionales empleados
    user4 = users.create_usuario(
        nombre="Emilia",
        apellido="Martínez",
        correo="emilia@mail.com",
        roles_ids=[encargado.id],
        password="1234",
        id_tipo_identificacion=dni.id,
        numero_identificacion="23456789",
        id_pais=pais_arg.id,
        fecha_nacimiento="1992-03-15"
    )
    user5 = users.create_usuario(
        nombre="Sofía",
        apellido="Fernández",
        correo="sofia@mail.com",
        roles_ids=[encargado.id],
        password="1234",
        id_tipo_identificacion=cedula.id,
        numero_identificacion="34567890",
        id_pais=pais_uru.id,
        fecha_nacimiento="1988-07-22"
    )
    # Usuarios adicionales inquilinos
    user6 = users.create_usuario(
        nombre="Lucía",
        apellido="García",
        correo="lucia@mail.com",
        roles_ids=[inquilino.id],
        password="1234",
        id_tipo_identificacion=pasaporte.id,
        numero_identificacion="B9876543",
        id_pais=pais_chi.id,
        fecha_nacimiento="1995-11-30"
    )
    user7 = users.create_usuario(
        nombre="Martín",
        apellido="Suárez",
        correo="martin@mail.com",
        roles_ids=[inquilino.id],
        password="1234",
        id_tipo_identificacion=dni.id,
        numero_identificacion="45678901",
        id_pais=pais_arg.id,
        fecha_nacimiento="1998-04-18"
    )
    print("Usuarios empleados e inquilinos adicionales creados")

    # Paramétricas de tarjetas
    from src.models.users.user import MarcaTarjeta, TipoTarjeta
    from src.models.database import db
    visa = MarcaTarjeta(nombre="Visa")
    mastercard = MarcaTarjeta(nombre="Mastercard")
    amex = MarcaTarjeta(nombre="Amex")
    credito = TipoTarjeta(nombre="crédito")
    debito = TipoTarjeta(nombre="débito")
    db.session.add_all([visa, mastercard, amex, credito, debito])
    db.session.commit()

    # Tarjetas de ejemplo solo para usuarios inquilinos
    tarjeta1 = Tarjeta(
        numero="4111111111111111",
        nombre_titular="Juan Pérez",
        fecha_inicio=date(2022, 1, 1),
        fecha_vencimiento=date(2026, 1, 1),
        cvv="123",
        usuario_id=user1.id,
        anverso_url="/static/tarjetas/juan_anverso.png",
        reverso_url="/static/tarjetas/juan_reverso.png",
        id_marca=visa.id,
        id_tipo=credito.id
    )
    tarjeta2 = Tarjeta(
        numero="5500000000000004",
        nombre_titular="Juan Pérez",
        fecha_inicio=date(2023, 5, 1),
        fecha_vencimiento=date(2027, 5, 1),
        cvv="456",
        usuario_id=user1.id,
        anverso_url="/static/tarjetas/juan2_anverso.png",
        reverso_url="/static/tarjetas/juan2_reverso.png",
        id_marca=mastercard.id,
        id_tipo=debito.id
    )
    tarjeta3 = Tarjeta(
        numero="4000000000000002",
        nombre_titular="Raul Gómez",
        fecha_inicio=date(2021, 6, 1),
        fecha_vencimiento=date(2025, 6, 1),
        cvv="789",
        usuario_id=user2.id,
        anverso_url="/static/tarjetas/raul_anverso.png",
        reverso_url="/static/tarjetas/raul_reverso.png",
        id_marca=visa.id,
        id_tipo=debito.id
    )
    tarjeta4 = Tarjeta(
        numero="340000000000009",
        nombre_titular="Roberto López",
        fecha_inicio=date(2022, 9, 1),
        fecha_vencimiento=date(2026, 9, 1),
        cvv="321",
        usuario_id=user3.id,
        anverso_url="/static/tarjetas/roberto_anverso.png",
        reverso_url="/static/tarjetas/roberto_reverso.png",
        id_marca=amex.id,
        id_tipo=credito.id
    )
    db.session.add_all([tarjeta1, tarjeta2, tarjeta3, tarjeta4])
    db.session.commit()
    print("Tarjetas de ejemplo creadas y asociadas a usuarios inquilinos")

    # Tarjetas para los nuevos inquilinos
    tarjeta5 = Tarjeta(
        numero="6011000000000004",
        nombre_titular="Lucía García",
        fecha_inicio=date(2023, 2, 1),
        fecha_vencimiento=date(2027, 2, 1),
        cvv="654",
        usuario_id=user6.id,
        anverso_url="/static/tarjetas/lucia_anverso.png",
        reverso_url="/static/tarjetas/lucia_reverso.png",
        id_marca=visa.id,
        id_tipo=credito.id
    )
    tarjeta6 = Tarjeta(
        numero="3530111333300000",
        nombre_titular="Martín Suárez",
        fecha_inicio=date(2024, 1, 1),
        fecha_vencimiento=date(2028, 1, 1),
        cvv="852",
        usuario_id=user7.id,
        anverso_url="/static/tarjetas/martin_anverso.png",
        reverso_url="/static/tarjetas/martin_reverso.png",
        id_marca=mastercard.id,
        id_tipo=debito.id
    )
    db.session.add_all([tarjeta5, tarjeta6])
    db.session.commit()
    print("Tarjetas de ejemplo creadas y asociadas a nuevos usuarios inquilinos")

    # Relacionar tarjetas solo con usuarios que sean inquilinos
    user1.tarjetas.extend([tarjeta1, tarjeta2])
    user2.tarjetas.append(tarjeta3)
    user3.tarjetas.append(tarjeta4)
    user6.tarjetas.append(tarjeta5)
    user7.tarjetas.append(tarjeta6)
    db.session.add_all([user1, user2, user3, user6, user7, user4, user5])
    db.session.commit()
    print("Tarjetas asociadas a usuarios inquilinos en la relación uno-a-muchos.")

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
        id_ciudad=1,
        requiere_documentacion=True
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
        requiere_documentacion=True
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
        requiere_documentacion=True
    )
    print("Propiedades de ejemplo creadas")
