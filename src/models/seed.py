from src.services import user_service
from src.services import propiedad_service

def run():
    user1 = user_service.crear_usuario(nombre="Juan", correo="juan@mail.com", rol="Administrador", password="1234")
    user2 = user_service.crear_usuario(nombre="Raul", correo="raul@mail.com", rol="Empleado", password="1234")
    user3 = user_service.crear_usuario(nombre="Roberto", correo="roberto@mail.com", rol="Inquilino", password="1234")
    print("Usuarios de ejemplo creados")

    # Propiedades de ejemplo
    prop1 = propiedad_service.crear_propiedad(
        nombre="Casa de Playa",
        descripcion="Hermosa casa frente al mar",
        entre_calles="Calle A y Calle B",
        calle="Calle del Mar",
        numero="123",
        piso="1",
        depto="A",
        id_ciudad=1,
        huespedes=6,
        ambientes=4,
        banios=2,
        cocheras=1,
        id_pol_reserva=1,
        precioNoche=150.0
    )

    prop2 = propiedad_service.crear_propiedad(
        nombre="Departamento Céntrico",
        descripcion="Cómodo departamento en el centro",
        entre_calles="Av. Principal y Calle 9",
        calle="Calle Central",
        numero="456",
        piso="2",
        depto="B",
        id_ciudad=2,
        huespedes=3,
        ambientes=2,
        banios=1,
        cocheras=0,
        id_pol_reserva=1,
        precioNoche=75.0
    )

    prop3 = propiedad_service.crear_propiedad(
        nombre="Cabaña en el bosque",
        descripcion="Acogedora cabaña rodeada de naturaleza",
        entre_calles="Camino viejo y Ruta 5",
        calle="Sendero Verde",
        numero="789",
        piso="PB",
        depto="Único",
        id_ciudad=3,
        huespedes=4,
        ambientes=3,
        banios=1,
        cocheras=2,
        id_pol_reserva=2,
        precioNoche=120.0
    )
    print("Propiedades de ejemplo creadas")
