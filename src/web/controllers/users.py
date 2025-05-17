from flask import request
from src.models import users
from marshmallow import ValidationError
from flask import Blueprint, request, jsonify  # Importa Blueprint para rutas, request para datos y jsonify para respuestas JSON
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # Importa funciones para manejo de JWT (autenticación y claims)
from src.enums.roles import Rol  # Importa el enum Rol para validaciones de roles
from functools import wraps
from src.web.authorization.roles import rol_requerido

# Crea un blueprint para las rutas relacionadas a usuarios, con prefijo /usuarios
user_blueprint = Blueprint('users', __name__, url_prefix="/usuarios")

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
    usuarios = users.get_usuarios()
    return users.get_schema_usuario().dumps(usuarios, many=True)

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
    
    try:
        data_usuario = users.get_schema_usuario().load(data)    # Valida JSON del request
        usuario = users.create_usuario(**data_usuario)          # Valida que sea unico en DB
        return (users.get_schema_usuario().dumps(usuario), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Usuario repetido?"}, 400)
