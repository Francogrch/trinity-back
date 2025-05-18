from src.models.database import db
from src.models.users.user import Usuario, UsuarioSchema


def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios

    
def create_usuario(nombre, correo, id_rol, password):
    """Crea un nuevo usuario con los datos recibidos."""
    try:
        nuevo = Usuario(nombre, correo, id_rol, password)
        db.session.add(nuevo)
        db.session.commit()
        return nuevo
    except Exception as e:
        db.session.rollback()
        raise ()


def get_usuario_by_nombre(nombre):
    return Usuario.query.filter_by(nombre=nombre).first()

def get_usuario_by_correo(correo):
    return Usuario.query.filter_by(correo=correo).first()

def get_usuario_by_id(user_id):
    return Usuario.query.get(user_id)

def delete_usuario_by_id(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    db.session.delete(usuario)
    db.session.commit()
    return usuario

def update_usuario(user_id, data):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    # Solo actualiza los campos permitidos
    for campo in ['nombre', 'correo', 'id_rol']:
        if campo in data:
            setattr(usuario, campo, data[campo])
    if 'password' in data and data['password']:
        usuario.set_password(data['password'])
    db.session.commit()
    return usuario

def get_usuarios_by_rol(rol_id):
    # Forzar carga de la relación rol para cada usuario
    usuarios = Usuario.query.filter_by(id_rol=rol_id).all()
    for usuario in usuarios:
        _ = usuario.rol  # Accede a la relación para asegurar que se cargue
    return usuarios

def get_schema_usuario():
    return UsuarioSchema()
