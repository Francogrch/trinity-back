from src.models.database import db
from src.models.users.user import Usuario, UsuarioSchema, EmpleadoSchema, Rol
from src.models.parametricas.parametricas import TipoIdentificacion
from datetime import date, datetime
from src.models.users.permisos import PermisosRol, PERMISOS_CLASSES
from src.enums.roles import Rol as EnumRol

def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios

def get_empleados():
    empleados = db.session.query(Usuario).\
    join(Usuario.roles).\
    filter(Rol.id != EnumRol.INQUILINO.value).\
    all()
    return empleados
    
def create_usuario(nombre, correo, roles_ids, password, id_tipo_identificacion=None, numero_identificacion=None, apellido=None, fecha_nacimiento=None, id_pais=None):
    """Crea un nuevo usuario con los datos recibidos y múltiples roles."""
    try:
        roles = Rol.query.filter(Rol.id.in_(roles_ids)).all()
        # Conversión robusta de fecha_nacimiento a date si es string
        if fecha_nacimiento and isinstance(fecha_nacimiento, str):
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de fecha_nacimiento debe ser YYYY-MM-DD")
        tipo_identificacion_obj = None
        if id_tipo_identificacion:
            tipo_identificacion_obj = TipoIdentificacion.query.get(id_tipo_identificacion)
        nuevo = Usuario(
            nombre=nombre,
            correo=correo,
            roles=roles,
            password=password,
            id_tipo_identificacion=id_tipo_identificacion,
            tipo_identificacion=tipo_identificacion_obj,
            numero_identificacion=numero_identificacion,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            id_pais=id_pais
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo
    except Exception as e:
        db.session.rollback()
        raise e


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
    for campo in ['nombre', 'correo', 'id_tipo_identificacion', 'numero_identificacion', 'apellido', 'fecha_nacimiento', 'id_pais']:
        if campo in data:
            setattr(usuario, campo, data[campo])
    if 'id_tipo_identificacion' in data:
        from src.models.parametricas.parametricas import TipoIdentificacion
        usuario.tipo_identificacion = TipoIdentificacion.query.get(data['id_tipo_identificacion'])
    if 'roles_ids' in data:
        roles = Rol.query.filter(Rol.id.in_(data['roles_ids'])).all()
        usuario.roles = roles
    if 'password' in data and data['password']:
        usuario.set_password(data['password'])
    db.session.commit()
    return usuario

def set_imagen_usuario(user_id, id_imagen):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    usuario.id_imagen = id_imagen
    db.session.commit()
    return usuario

def get_usuarios_by_rol(rol_id):
    usuarios = Usuario.query.join(Usuario.roles).filter_by(id=rol_id).all()
    for usuario in usuarios:
        _ = usuario.roles
    return usuarios

def get_permisos_usuario(usuario, modo='combinado', rol_exclusivo=None):
    """
    Devuelve un diccionario de permisos del usuario, donde las claves son los nombres de los permisos y los valores son booleanos.

    El comportamiento varía según el modo seleccionado:
    - **'combinado'** (por defecto): combina los permisos de todos los roles del usuario. Un permiso se considera otorgado si al menos uno de los roles lo permite.
    - **'exclusivo'**: devuelve únicamente los permisos correspondientes a un solo rol. Este puede ser:
        - el especificado mediante `rol_exclusivo` (debe ser una instancia de `EnumRol`), o
        - el de mayor precedencia del usuario, si no se indica uno explícitamente.

    Args:
        usuario: Objeto `Usuario` con la relación `roles` previamente cargada.
        modo (str, opcional): Modo de evaluación de permisos. Puede ser `'combinado'` o `'exclusivo'`. Valor por defecto: `'combinado'`.
        rol_exclusivo (EnumRol, opcional): Rol específico a considerar cuando se usa el modo `'exclusivo'`.

    Returns:
        dict: Diccionario donde cada clave es un nombre de permiso y cada valor es `True` o `False`.

    Ejemplos:
        # Combina los permisos de todos los roles del usuario
        permisos = get_permisos_usuario(usuario)

        # Permisos del rol de mayor precedencia del usuario
        permisos = get_permisos_usuario(usuario, modo='exclusivo')

        # Permisos solo del rol 'ADMINISTRADOR'
        permisos = get_permisos_usuario(usuario, modo='exclusivo', rol_exclusivo=EnumRol.ADMINISTRADOR)
    """
    if modo == 'exclusivo':
        # Se requiere que rol_exclusivo sea None o EnumRol
        if rol_exclusivo:
            if not hasattr(rol_exclusivo, 'value'):
                raise ValueError('rol_exclusivo debe ser un EnumRol (por ejemplo, EnumRol.ADMINISTRADOR)')
            rol_nombre = rol_exclusivo.value
            clase_permiso = PERMISOS_CLASSES.get(rol_nombre, PermisosRol)
            return clase_permiso().get_permisos()
        elif usuario.roles:
            # Determinar el rol de mayor precedencia
            jerarquia = [EnumRol.ADMINISTRADOR.value, EnumRol.ENCARGADO.value, EnumRol.INQUILINO.value]
            roles_usuario = [rol.nombre for rol in usuario.roles]
            for rol_j in jerarquia:
                if rol_j in roles_usuario:
                    clase_permiso = PERMISOS_CLASSES.get(rol_j, PermisosRol)
                    return clase_permiso().get_permisos()
            # Si no hay coincidencia, usar el primer rol
            clase_permiso = PERMISOS_CLASSES.get(usuario.roles[0].nombre, PermisosRol)
            return clase_permiso().get_permisos()
        else:
            return PermisosRol().get_permisos()
    else:  # modo combinado
        permisos = PermisosRol().get_permisos()
        for rol in usuario.roles:
            clase_permiso = PERMISOS_CLASSES.get(rol.nombre, PermisosRol)
            rol_permisos = clase_permiso().get_permisos()
            for permiso, valor in rol_permisos.items():
                permisos[permiso] = permisos[permiso] or valor
        return permisos

def get_schema_usuario():
    return UsuarioSchema()

def get_schema_empleado():
    return EmpleadoSchema()
