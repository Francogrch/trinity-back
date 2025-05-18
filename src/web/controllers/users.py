from flask import request
from src.models import users
from marshmallow import ValidationError
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol

# Crea un blueprint para las rutas relacionadas a usuarios, con prefijo /usuarios
user_blueprint = Blueprint('users', __name__, url_prefix="/usuarios")

def verificar_permiso_creacion_usuario(id_rol_actual, id_rol_nuevo):
    """
    Lógica para validar permisos de creación de usuarios según el id de rol del creador.
    Retorna (True, None) si está permitido, o (False, mensaje) si no.
    """
    # Ejemplo: solo el rol ADMINISTRADOR puede crear empleados (EMPLEADO)
    if id_rol_nuevo == Rol.EMPLEADO.value:
        if id_rol_actual != Rol.ADMINISTRADOR.value:
            return False, 'Solo un Administrador puede crear usuarios Empleados'
    elif id_rol_nuevo == Rol.INQUILINO.value:
        if id_rol_actual not in [Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value]:
            return False, 'Solo Administrador o Empleado pueden crear usuarios Inquilinos'
    else:
        return False, 'Rol destino no permitido'
    return True, None

@user_blueprint.get('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden acceder
def get_usuarios():
    usuarios = users.get_usuarios()
    return users.get_schema_usuario().dumps(usuarios, many=True)

@user_blueprint.post('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden crear usuarios
def create_usuario():
    claims = get_jwt()
    id_rol_actual = claims.get('id_rol')
    data = request.get_json()
    permitido, mensaje = verificar_permiso_creacion_usuario(id_rol_actual, data['id_rol'])
    if not permitido:
        return jsonify({'mensaje': mensaje}), 403
    try:
        data_usuario = users.get_schema_usuario().load(data)
        usuario = users.create_usuario(**data_usuario)
        return (users.get_schema_usuario().dumps(usuario), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Usuario repetido?"}, 400)

@user_blueprint.get('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def get_usuario_by_id(user_id):
    usuario = users.get_usuario_by_id(user_id)
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    return users.get_schema_usuario().dumps(usuario)

@user_blueprint.get('/me')
@jwt_required()
def get_usuario_actual():
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    usuario = users.get_usuario_by_id(user_id)
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    return users.get_schema_usuario().dumps(usuario)

@user_blueprint.get('/por-rol/<int:rol_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def get_usuarios_por_rol(rol_id):
    usuarios = users.get_usuarios_by_rol(rol_id)
    return users.get_schema_usuario().dumps(usuarios, many=True)

@user_blueprint.delete('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value])
def delete_usuario_by_id(user_id):
    try:
        usuario = users.delete_usuario_by_id(user_id)
        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        return jsonify({'mensaje': 'Usuario eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_blueprint.put('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def update_usuario(user_id):
    data = request.get_json()
    try:
        usuario = users.update_usuario(user_id, data)
        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        return users.get_schema_usuario().dumps(usuario)
    except ValidationError as err:
        return (err.messages, 422)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
