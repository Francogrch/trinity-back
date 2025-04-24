from src.models import users

def run():
    user1 = users.create_usuario(
        nombre="Juan",
        rol="Nadie"
    )
    user2 = users.create_usuario(
        nombre="Raul",
        rol="Empleado"
    )
    user3 = users.create_usuario(
        nombre="Roberto",
        rol="Cliente"
    )
