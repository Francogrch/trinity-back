from src.models.database import db
from src.models.users.user import Usuario, UsuarioSchema, Rol


def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios

    
def create_usuario(nombre, correo, roles_ids, password, tipo_identificacion=None, numero_identificacion=None):
    """Crea un nuevo usuario con los datos recibidos y múltiples roles."""
    try:
        roles = Rol.query.filter(Rol.id.in_(roles_ids)).all()
        nuevo = Usuario(
            nombre=nombre,
            correo=correo,
            roles=roles,
            password=password,
            tipo_identificacion=tipo_identificacion,
            numero_identificacion=numero_identificacion
        )
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
    for campo in ['nombre', 'correo', 'tipo_identificacion', 'numero_identificacion']:
        if campo in data:
            setattr(usuario, campo, data[campo])
    if 'roles_ids' in data:
        roles = Rol.query.filter(Rol.id.in_(data['roles_ids'])).all()
        usuario.roles = roles
    if 'password' in data and data['password']:
        usuario.set_password(data['password'])
    db.session.commit()
    return usuario

def get_usuarios_by_rol(rol_id):
    usuarios = Usuario.query.join(Usuario.roles).filter_by(id=rol_id).all()
    for usuario in usuarios:
        _ = usuario.roles
    return usuarios

def get_schema_usuario():
    return UsuarioSchema()
