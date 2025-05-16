from src.models.database import db

from src.models.users.user import Usuario, UsuarioSchema


def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios

    
def create_usuario(nombre, correo, rol, password):
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

def get_schema_usuario():
    return UsuarioSchema()
