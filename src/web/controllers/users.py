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

def verificar_permiso_creacion_usuario(id_rol_actuales, id_roles_nuevos):
    """
    Lógica para validar permisos de creación de usuarios según los roles actuales del creador.
    id_rol_actuales: lista de ids de roles del usuario autenticado
    id_roles_nuevos: lista de ids de roles a asignar al nuevo usuario
    """
    # Ejemplo: solo el rol ADMINISTRADOR puede crear empleados (EMPLEADO)
    if Rol.EMPLEADO.value in id_roles_nuevos:
        if Rol.ADMINISTRADOR.value not in id_rol_actuales:
            return False, 'Solo un Administrador puede crear usuarios Empleados'
    if Rol.INQUILINO.value in id_roles_nuevos:
        if not any(r in id_rol_actuales for r in [Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value]):
            return False, 'Solo Administrador o Empleado pueden crear usuarios Inquilinos'
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
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    usuario_actual = users.get_usuario_by_id(user_id)
    id_rol_actuales = [rol.id for rol in usuario_actual.roles]
    data = request.get_json()
    permitido, mensaje = verificar_permiso_creacion_usuario(id_rol_actuales, data['roles_ids'])
    if not permitido:
        return jsonify({'mensaje': mensaje}), 403
    try:
        usuario = users.create_usuario(
            nombre=data['nombre'],
            apellido=data.get('apellido'),
            correo=data['correo'],
            roles_ids=data['roles_ids'],
            password=data.get('password'),
            tipo_identificacion=data.get('tipo_identificacion'),
            numero_identificacion=data.get('numero_identificacion'),
            id_pais=data.get('id_pais'),
            fecha_nacimiento=data.get('fecha_nacimiento')
        )
        return (users.get_schema_usuario().dumps(usuario), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except Exception as e:
        return ({"error": str(e)}, 400)

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
