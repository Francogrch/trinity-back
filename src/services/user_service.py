"""
Servicio de usuarios: lógica de negocio y operaciones sobre usuarios.
"""
from src.models.users.user import Usuario
from src.models.database import db

def obtener_todos_los_usuarios():
    """Devuelve la lista de todos los usuarios."""
    return Usuario.query.all()

def crear_usuario(nombre, correo, rol, password):
    """Crea un nuevo usuario con los datos recibidos."""
    try:
        nuevo = Usuario(nombre, correo, rol, password)
        db.session.add(nuevo)
        db.session.commit()
        return nuevo
    except Exception as e:
        db.session.rollback()
        return None

def get_usuario_by_nombre(nombre):
    return Usuario.query.filter_by(nombre=nombre).first()

def get_usuario_by_correo(correo):
    return Usuario.query.filter_by(correo=correo).first()
