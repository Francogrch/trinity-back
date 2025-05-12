from src.models import users, propiedades, parametricas


def run():
    # Tipos de propiedades
    dpto = parametricas.create_tipos_propiedad("Departamento")
    cabana = parametricas.create_tipos_propiedad("Cabaña")

    # Usuarios de ejemplo
    user1 = users.create_usuario(nombre="Juan", rol="Nadie")
    user2 = users.create_usuario(nombre="Raul", rol="Empleado")
    user3 = users.create_usuario(nombre="Roberto", rol="Cliente")

    # Propiedades de ejemplo
    prop1 = propiedades.create_propiedad(
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

    prop2 = propiedades.create_propiedad(
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

    prop3 = propiedades.create_propiedad(
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
