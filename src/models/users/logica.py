import sqlalchemy
from src.models.imagenes.logica import set_id_usuario
from src.models.database import db
from src.models.users.user import Usuario, usuario_rol, UsuarioSchema, UsuarioResumidoSchema, EmpleadoSchema, Rol,Tarjeta, PasswordSchema
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
    filter(Usuario.delete_at == None).\
    all()
    return empleados

def get_encargados():
    empleados = db.session.query(Usuario).\
    join(Usuario.roles).\
    filter(Rol.id == EnumRol.EMPLEADO.value).\
    filter(Usuario.delete_at == None).\
    all()
    return empleados

def get_inquilinos():
    inquilinos = db.session.query(Usuario).\
    join(Usuario.roles).\
    filter(Rol.id == EnumRol.INQUILINO.value).\
    all()
    return inquilinos

def get_inquilinos_activos():
    inquilinos = db.session.query(Usuario).\
    join(Usuario.roles).\
    filter(Rol.id == EnumRol.INQUILINO.value).\
    filter(Usuario.is_bloqueado == False).\
    all()
    return inquilinos

def get_administradores():
    administradores = db.session.query(Usuario).\
    join(Usuario.roles).\
    filter(Rol.id == EnumRol.ADMINISTRADOR.value).\
    filter(Usuario.delete_at == None).\
    all()
    return administradores

def get_correos_administradores():
    administradores = get_administradores()
    correos = [admin.correo for admin in administradores]
    return correos

# no se usa
def create_usuario(nombre, correo, roles_ids, password, is_bloqueado=False, id_tipo_identificacion=None, numero_identificacion=None, apellido=None, fecha_nacimiento=None, id_pais=None):
    """Crea un nuevo usuario con los datos recibidos y múltiples roles."""
    try:
        # Asegura que roles_ids sea una lista de enteros
        if not isinstance(roles_ids, list):
            raise ValueError("roles_ids debe ser una lista de IDs de roles")
        roles = Rol.query.filter(Rol.id.in_(roles_ids)).all()
        if not roles or len(roles) != len(roles_ids):
            raise ValueError("Uno o más roles no existen")
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
            id_pais=id_pais,
            is_bloqueado=is_bloqueado
        )
        db.session.add(nuevo)
        db.session.commit()
        # Refresca la instancia para que los roles y relaciones estén actualizados
        db.session.refresh(nuevo)
        return nuevo
    except Exception as e:
        db.session.rollback()
        raise e
    
def create_tarjeta(numero,nombre_titular,fecha_vencimiento,cvv,usuario_id):
    """Crea una nueva tarjeta asociada a un usuario."""
    nuevo = Tarjeta(
        numero=numero,
        nombre_titular=nombre_titular,
        fecha_vencimiento=fecha_vencimiento,
        cvv=cvv,
        usuario_id=usuario_id
    )
    return nuevo
 
    
def create_new_usuario(nombre, correo, roles_ids, password, id_tipo_identificacion=None, numero_identificacion=None, apellido=None, fecha_nacimiento=None, id_pais=None):
    """Crea un nuevo usuario con los datos recibidos y múltiples roles."""
    
    roles = Rol.query.filter(Rol.id.in_(roles_ids)).all()
    # roles = roles_ids
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
    #db.session.add(nuevo)
    #db.session.commit()
    return nuevo

def cambiar_estado_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    usuario.is_bloqueado = not usuario.is_bloqueado
    db.session.commit()
    return usuario
def get_nombre(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    return usuario.nombre
def get_rol(user_id):
    usuario = Usuario.query.get(user_id)
    usuario = get_schema_usuario().dump(usuario)
    if not usuario:
        return None
    if not usuario["roles_ids"]:
        return None
    return usuario["roles_ids"][0]

def is_usuario_bloqueado(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    return usuario.is_bloqueado
    
def existe_identificacion(numero_identificacion, id_tipo_identificacion,id_usuario):
    return Usuario.query.filter_by(
        id_tipo_identificacion=id_tipo_identificacion,
        numero_identificacion=numero_identificacion,
    ).filter(Usuario.id != id_usuario).first()
    
# lo agrego para que no se rompa las cosas viejas
def existe_identificacion_viejo(numero_identificacion, id_tipo_identificacion):
    return Usuario.query.filter_by(
        id_tipo_identificacion=id_tipo_identificacion,
        numero_identificacion=numero_identificacion,
    ).first()

def get_cantidad_admins():
    return db.session.query(Usuario)\
            .join(usuario_rol)\
            .filter(usuario_rol.c.rol_id == 1, Usuario.delete_at == None)\
            .count()

def get_usuario_by_nombre(nombre):
    return Usuario.query.filter_by(nombre=nombre).first()

def get_usuario_by_correo(correo):
    return Usuario.query.filter_by(correo=correo, delete_at=None).first()

def get_usuario_by_id(user_id):
    return Usuario.query.get(user_id)

def get_usuario_activo_by_id(user_id):
    return Usuario.query.filter_by(id=user_id, delete_at=None).first()

# así no se pueden controlar la cantidad de admin. Uso el de abajo
def delete_usuario_by_id(user_id):
    usuario = Usuario.query.filter_by(id=user_id, delete_at=None).first()
    if not usuario:
        return None
    usuario.delete_at = date.today()
    #db.session.delete(usuario)
    db.session.commit()
    return usuario

def delete_usuario(usuario):
    usuario.delete_at = date.today()
    #db.session.delete(usuario)
    db.session.commit()
    return usuario

def cambiar_id_encargado(user_id,new_id_encargado):
    from src.models.propiedades.logica import get_propiedades_usuario
    propiedades = get_propiedades_usuario(get_usuario_by_id(user_id))
    
    if propiedades:
        for propiedad in propiedades:
            propiedad.id_encargado = new_id_encargado
        try:
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
   

def update_usuario(user_id, data):
    usuario = Usuario.query.get(user_id)
    if usuario.delete_at:
        raise ValueError("No se puede actualizar un usuario eliminado")
    # Conversión robusta de fecha_nacimiento a date si es string
    if data['fecha_nacimiento'] and isinstance(data['fecha_nacimiento'], str):
        try:
            data['fecha_nacimiento'] = datetime.strptime(data['fecha_nacimiento'], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("El formato de fecha_nacimiento debe ser YYYY-MM-DD")
    if not usuario:
        return None
    for campo in ['nombre', 'correo', 'id_tipo_identificacion', 'numero_identificacion', 'apellido', 'fecha_nacimiento', 'id_pais']:
        if campo in data:
            setattr(usuario, campo, data[campo])
            
    return usuario

def update_me(user_id, data):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    if data['correo'] != usuario.correo and correo_exists(data['correo']):
        raise ValueError("El correo ya está en uso")
    # Conversión robusta de fecha_nacimiento a date si es string
    if data['fecha_nacimiento'] and isinstance(data['fecha_nacimiento'], str):
        try:
            data['fecha_nacimiento'] = datetime.strptime(data['fecha_nacimiento'], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("El formato de fecha_nacimiento debe ser YYYY-MM-DD")
    for campo in ['nombre', 'correo', 'id_tipo_identificacion', 'numero_identificacion', 'apellido', 'fecha_nacimiento']:
        if campo in data:
            setattr(usuario, campo, data[campo])
    usuario.id_pais = data['pais']
    usuario.id_tipo_identificacion = data['tipo_identificacion']
    if (usuario.get_roles()["is_inquilino"] and data['tarjetas'][0] and data['id_imagenes'][0]):
        if data['tarjetas'][0]:
            update_tarjeta(usuario.id, data)
        if data['id_imagenes'][0]:
            set_id_usuario(data['id_imagenes'][0],usuario.id)
            set_id_usuario(data['id_imagenes'][1],usuario.id)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return usuario

def correo_exists(correo):
    return Usuario.query.filter_by(correo=correo).first() is not None

def update_delete_at(user_id,data):
    usuario = get_usuario_by_id(user_id)
    if not usuario:
        return None
    if data['correo'] != usuario.correo and correo_exists(data['correo']):
        raise ValueError("El correo ya está en uso")
    if existe_identificacion(data['numero_identificacion'], data['tipo_identificacion'], user_id):
        raise ValueError("El número de identificación ya está en uso")
    try:
        usuario.delete_at = None
        if data['fecha_nacimiento'] and isinstance(data['fecha_nacimiento'], str):
            try:
                data['fecha_nacimiento'] = datetime.strptime(data['fecha_nacimiento'], "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de fecha_nacimiento debe ser YYYY-MM-DD")
        if not usuario:
            return None
        for campo in ['nombre', 'correo', 'numero_identificacion', 'apellido', 'fecha_nacimiento']:
            if campo in data:
                setattr(usuario, campo, data[campo])
        usuario.id_tipo_identificacion=data.get('tipo_identificacion')
        usuario.id_pais=data.get('pais')
        if data.get('roles'):
            usuario.roles = [Rol.query.filter_by(id=str(data['roles'])).first()]
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        raise ValueError("Hay datos que ya estan registrados, por favor verifique los datos ingresados")
    except Exception as e:
        db.session.rollback()
        raise e
    return usuario

def update_imagen(user_id, id_imagen):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    usuario.imagenes_doc = id_imagen
    db.session.commit()
    return usuario

def change_password(usuario, password):
    usuario.set_password(password)
    db.session.commit()
    return usuario

def update_tarjeta(user_id, data):
    from src.models.users.user import Tarjeta
    tarjeta = Tarjeta.query.filter_by(usuario_id=user_id).first()
    if not tarjeta:
        return None
    for campo in ['numero', 'nombre_titular', 'fecha_vencimiento', 'cvv']:
        if campo in data['tarjetas'][0]:
            setattr(tarjeta, campo, data['tarjetas'][0][campo])
    return tarjeta

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

def get_roles_by_ids(roles_ids):
    from src.models.users.user import Rol
    return Rol.query.filter(Rol.id.in_(roles_ids)).all()

def empleado_exists(correo):
    empleado = db.session.query(Usuario).\
    join(Usuario.roles).\
    filter(Usuario.correo == correo).\
    filter(Rol.id != EnumRol.INQUILINO.value).\
    first()
    return empleado


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
    
def tiene_reservas_en_curso(usuario):
    from src.models.reservas.logica import get_reservas_por_usuario
    reservas = get_reservas_por_usuario(usuario)
    for reserva in reservas:
        # Testear bien este if
        print(f"Reserva: {reserva.id}, Fecha Inicio: {reserva.fecha_inicio}, Fecha Fin: {reserva.fecha_fin}, Estado: {reserva.id_estado}")
        if reserva.fecha_inicio.date() <= date.today() <= reserva.fecha_fin.date() and reserva.id_estado not in [3,4]:
            return True
    return False

def eliminar_inquilino(user_id):
    from src.models.reservas.logica import cancelar_reservas_not_commit
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return None
    if usuario.get_roles()["is_admin"] or usuario.get_roles()["is_encargado"]:
        raise ValueError("No se puede eliminar un usuario con rol de administrador o encargado.")
    if usuario.delete_at:
        raise ValueError("El usuario ya está eliminado")
    if tiene_reservas_en_curso(usuario):
        usuario.is_bloqueado = True
        cancelar_reservas_not_commit(user_id)
        db.session.commit()
        raise ValueError("El usuario tiene reservas en curso, no se puede eliminar. Fue bloqueado. Se cancelaron reservas futuras.")
    try:
        usuario.delete_at = date.today()
        cancelar_reservas_not_commit(user_id)
        # Hay que testear que el correo pueda ser null, hay que modificar el esquema
        usuario.correo = f"{usuario.correo}{date.today().strftime('%Y%m%d')}"
        usuario.nombre = f"{usuario.nombre} (eliminado)"
        usuario.apellido = f"{usuario.apellido} (eliminado)"
        usuario.numero_identificacion = None
        usuario.is_bloqueado = True
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        raise ValueError("Error de integración: No se puede eliminar el usuario porque tiene datos relacionados.")
    except Exception as e:
        db.session.rollback()
        raise e
    return usuario



def get_schema_usuario():
    return UsuarioSchema()

def get_schema_empleado():
    return EmpleadoSchema()

def get_schema_usuario_resumido():
    return UsuarioResumidoSchema()

def get_schema_password():
    return PasswordSchema()
