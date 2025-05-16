from flask import Blueprint, request, jsonify  # Importa Blueprint para rutas, request para datos y jsonify para respuestas JSON
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # Importa funciones para manejo de JWT (autenticación y claims)
from src.services import user_service  # Importa el servicio que maneja la lógica de usuarios
from src.enums.roles import Rol  # Importa el enum Rol para validaciones de roles

# Crea un blueprint para las rutas relacionadas a usuarios, con prefijo /usuarios
user_blueprint = Blueprint('users', __name__, url_prefix="/usuarios")

def rol_requerido(roles_permitidos):
    """
    Decorador para restringir acceso a rutas según roles permitidos.
    Uso: @rol_requerido(['Administrador', 'Empleado'])
    """
    def decorador(f):
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            rol_actual = claims.get('rol')
            if rol_actual not in roles_permitidos:
                return jsonify({'mensaje': 'Acceso denegado: rol insuficiente'}), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorador

def verificar_permiso_creacion_usuario(rol_actual, rol_nuevo):
    """
    Lógica para validar permisos de creación de usuarios según rol del creador.
    Retorna (True, None) si está permitido, o (False, mensaje) si no.
    """
    if rol_nuevo == Rol.EMPLEADO.value:  # Si se quiere crear un usuario con rol Empleado
        if rol_actual != Rol.ADMINISTRADOR.value:  # Solo un Administrador puede hacerlo
            return False, 'Solo un Administrador puede crear usuarios Empleados'
    elif rol_nuevo == Rol.INQUILINO.value:  # Si se quiere crear un usuario con rol Inquilino
        if rol_actual not in [Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value]:  # Solo Admin o Empleado pueden hacerlo
            return False, 'Solo Administrador o Empleado pueden crear usuarios Inquilinos'
    else:
        return False, 'Rol destino no permitido'  # Si el rol nuevo no es válido, no se permite
    return True, None  # Si todo está ok, permite la creación

@user_blueprint.get('/')
@jwt_required()  # Requiere token válido para acceder a esta ruta
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden acceder
def get_usuarios():
    usuarios = user_service.obtener_todos_los_usuarios()  # Llama al servicio para obtener todos los usuarios
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'rol': u.rol} for u in usuarios])

@user_blueprint.post('/')
@jwt_required()  # Requiere token válido para acceder a esta ruta
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden crear usuarios
def create_usuario():
    claims = get_jwt()
    current_user_rol = claims.get('rol')
    data = request.get_json()
    permitido, mensaje = verificar_permiso_creacion_usuario(current_user_rol, data['rol'])
    if not permitido:
        return jsonify({'mensaje': mensaje}), 403
    nuevo = user_service.crear_usuario(
        nombre=data['nombre'],
        correo=data['correo'],
        rol=data['rol'],
        password=data['password']
    )
    if nuevo:
        return jsonify({'mensaje': 'Usuario creado'}), 201
    else:
        return jsonify({'mensaje': 'Error al crear usuario'}), 400
