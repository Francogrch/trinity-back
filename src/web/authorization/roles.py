from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps

def rol_requerido(roles_permitidos):
    """
    Decorador genérico para restringir acceso a rutas según roles permitidos (por id_rol).
    
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
            claims = get_jwt()
            id_rol_actual = claims.get('id_rol')
            if id_rol_actual not in roles_permitidos:
                return jsonify({'mensaje': 'Acceso denegado: rol insuficiente'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorador
