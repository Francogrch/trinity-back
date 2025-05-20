from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from src.models.users.logica import get_usuario_by_id

def rol_requerido(roles_permitidos):
    """
    Decorador genérico para restringir acceso a rutas según roles permitidos (por id_rol).
    Ahora consulta los roles del usuario autenticado en la base de datos.
    
    Args:
        roles_permitidos (list): Lista de ids de roles (int) que pueden acceder al endpoint.
    
    Uso:
        @jwt_required()
        @rol_requerido([Rol.ADMINISTRADOR, Rol.EMPLEADO])
        def endpoint():
            ...
    
    El decorador obtiene el id_rol actual del usuario autenticado desde los claims del JWT.
    Si el id_rol no está en la lista de roles permitidos, retorna un error 403.
    Si el id_rol es válido, permite la ejecución normal del endpoint.
    
    Es importante usar @jwt_required() antes de este decorador para asegurar que el JWT esté validado.
    """
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            usuario = get_usuario_by_id(user_id)
            if not usuario:
                return jsonify({'mensaje': 'Usuario no encontrado'}), 404
            ids_roles_usuario = [rol.id for rol in usuario.roles]
            if not any(r in roles_permitidos for r in ids_roles_usuario):
                return jsonify({'mensaje': 'Acceso denegado: rol insuficiente'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorador
