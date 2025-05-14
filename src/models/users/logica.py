from src.models.database import db

from src.models.users.user import Usuario, UsuarioSchema


def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios


def create_usuario(nombre, rol):
    try:
        nuevo = Usuario(nombre, rol)
        db.session.add(nuevo)
        db.session.commit()
        return nuevo
    except:
        db.session.rollback()
        raise()

def get_schema_usuario():
    return UsuarioSchema()
