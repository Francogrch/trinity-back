from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps

def rol_requerido(roles_permitidos):
    """
    Decorador genérico para restringir acceso a rutas según roles permitidos.
    
    Args:
        roles_permitidos (list): Lista de roles (str) que pueden acceder al endpoint.
    
    Uso:
        @jwt_required()
        @rol_requerido(['Administrador', 'Empleado'])
        def endpoint():
            ...
    
    El decorador obtiene el rol actual del usuario autenticado desde los claims del JWT.
    Si el rol no está en la lista de roles permitidos, retorna un error 403.
    Si el rol es válido, permite la ejecución normal del endpoint.
    
    Es importante usar @jwt_required() antes de este decorador para asegurar que el JWT esté validado.
    """
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            rol_actual = claims.get('rol')
            if rol_actual not in roles_permitidos:
                return jsonify({'mensaje': 'Acceso denegado: rol insuficiente'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorador
