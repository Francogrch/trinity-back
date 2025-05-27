"""
Decorador genérico para restringir acceso a rutas según roles permitidos (por id_rol).

Este decorador se utiliza para proteger endpoints de Flask según los roles del usuario autenticado.

Funcionamiento:
- Consulta el usuario autenticado a partir del JWT (usando get_jwt_identity).
- Busca los roles asociados a ese usuario en la base de datos.
- Verifica si alguno de los roles del usuario está en la lista de roles permitidos (roles_permitidos).
- Si el usuario no existe o no tiene un rol permitido, retorna un error 403 (o 404 si no existe el usuario).
- Si tiene permiso, permite la ejecución normal del endpoint.

Parámetros:
    roles_permitidos (list): Lista de ids de roles (int) que pueden acceder al endpoint.

Uso recomendado:
    @jwt_required()
    @rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
    def endpoint():
        ...

Notas:
- Es importante usar @jwt_required() antes de este decorador para asegurar que el JWT esté validado.
- El decorador es compatible con usuarios con múltiples roles.
"""

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from src.models.users.logica import get_usuario_by_id

def rol_requerido(roles_permitidos):
    """
    Decorador para restringir acceso a rutas según roles permitidos (por id de rol).

    Este decorador protege endpoints de Flask verificando que el usuario autenticado tenga al menos uno de los roles requeridos.

    Args:
        roles_permitidos (list[int]): Lista de ids de roles (int) que pueden acceder al endpoint.

    Uso recomendado:
        @jwt_required()
        @rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
        def endpoint():
            ...

    Funcionamiento:
    - Obtiene el id del usuario autenticado desde el JWT.
    - Consulta los roles del usuario en la base de datos.
    - Si el usuario no existe, retorna 404.
    - Si el usuario no tiene ninguno de los roles permitidos, retorna 403.
    - Si tiene permiso, permite la ejecución normal del endpoint.

    Notas:
    - Es importante usar @jwt_required() antes de este decorador para asegurar que el JWT esté validado.
    - Compatible con usuarios con múltiples roles.
    """
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Obtiene el id del usuario autenticado desde el JWT
            user_id = get_jwt_identity()
            # Busca el usuario en la base de datos
            usuario = get_usuario_by_id(user_id)
            if not usuario:
                # Si el usuario no existe, retorna 404
                return jsonify({'mensaje': 'Usuario no encontrado'}), 404
            # Obtiene la lista de ids de roles del usuario
            ids_roles_usuario = [rol.id for rol in usuario.roles]
            # Verifica si el usuario tiene al menos uno de los roles permitidos
            if not any(r in roles_permitidos for r in ids_roles_usuario):
                # Si no tiene ninguno de los roles requeridos, retorna 403
                return jsonify({'mensaje': 'Acceso denegado: rol insuficiente'}), 403
            # Si tiene permiso, permite la ejecución normal del endpoint
            return f(*args, **kwargs)
        return wrapper
    return decorador
