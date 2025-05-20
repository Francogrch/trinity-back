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

# Función para verificar si el usuario autenticado puede crear un usuario con ciertos roles
# id_rol_actuales: lista de ids de roles del usuario autenticado
# id_roles_nuevos: lista de ids de roles a asignar al nuevo usuario
# Devuelve (True, None) si está permitido, (False, mensaje) si no
def verificar_permiso_creacion_usuario(id_rol_actuales, id_roles_nuevos):
    """
    Lógica para validar permisos de creación de usuarios según los roles actuales del creador.
    id_rol_actuales: lista de ids de roles del usuario autenticado
    id_roles_nuevos: lista de ids de roles a asignar al nuevo usuario
    """
    # Solo el rol ADMINISTRADOR puede crear empleados (EMPLEADO)
    if Rol.EMPLEADO.value in id_roles_nuevos:
        if Rol.ADMINISTRADOR.value not in id_rol_actuales:
            return False, 'Solo un Administrador puede crear usuarios Empleados'
    # Solo Administrador o Empleado pueden crear usuarios Inquilinos
    if Rol.INQUILINO.value in id_roles_nuevos:
        if not any(r in id_rol_actuales for r in [Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value]):
            return False, 'Solo Administrador o Empleado pueden crear usuarios Inquilinos'
    return True, None

# Endpoint: Obtener todos los usuarios (solo para admin y empleados)
@user_blueprint.get('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden acceder
# Devuelve la lista de usuarios serializada
def get_usuarios():
    usuarios = users.get_usuarios()  # Obtiene todos los usuarios de la base
    return users.get_schema_usuario().dumps(usuarios, many=True)  # Serializa y retorna

# Endpoint: Crear un nuevo usuario (solo admin y empleados)
@user_blueprint.post('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden crear usuarios
# Recibe los datos por JSON, valida permisos y crea el usuario
def create_usuario():
    from flask_jwt_extended import get_jwt_identity  # Importa función para obtener el usuario autenticado
    user_id = get_jwt_identity()  # Obtiene el id del usuario autenticado
    usuario_actual = users.get_usuario_by_id(user_id)  # Busca el usuario en la base
    id_rol_actuales = [rol.id for rol in usuario_actual.roles]  # Lista de ids de roles del usuario autenticado
    # Extrae el cuerpo de la solicitud HTTP en formato JSON y lo convierte en un diccionario de Python.
    data = request.get_json()  # Obtiene los datos del nuevo usuario
    permitido, mensaje = verificar_permiso_creacion_usuario(id_rol_actuales, data['roles_ids'])  # Valida permisos
    if not permitido:
        return jsonify({'mensaje': mensaje}), 403  # Si no tiene permiso, retorna error
    try:
        usuario = users.create_usuario(
            nombre=data['nombre'],
            apellido=data.get('apellido'),
            correo=data['correo'],
            roles_ids=data['roles_ids'],
            password=data.get('password'),
            id_tipo_identificacion=data.get('id_tipo_identificacion'),
            numero_identificacion=data.get('numero_identificacion'),
            id_pais=data.get('id_pais'),
            fecha_nacimiento=data.get('fecha_nacimiento')
        )  # Crea el usuario
        return (users.get_schema_usuario().dumps(usuario), 201)  # Retorna el usuario serializado
    except ValidationError as err:
        return (err.messages, 422)  # Si hay error de validación, retorna error
    except Exception as e:
        return ({"error": str(e)}, 400)  # Otro error

# Endpoint: Obtener usuario por id (solo admin y empleados)
@user_blueprint.get('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def get_usuario_by_id(user_id):
    usuario = users.get_usuario_by_id(user_id)  # Busca el usuario por id
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Si no existe, error
    return users.get_schema_usuario().dumps(usuario)  # Retorna usuario serializado

# Endpoint: Obtener el usuario autenticado (perfil propio)
@user_blueprint.get('/me')
@jwt_required()
def get_usuario_actual():
    from flask_jwt_extended import get_jwt_identity  # Importa función para obtener el usuario autenticado
    user_id = get_jwt_identity()  # Obtiene el id del usuario autenticado
    usuario = users.get_usuario_by_id(user_id)  # Busca el usuario en la base
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404  # Si no existe, error
    usuario_schema = users.get_schema_usuario()  # Obtiene el schema
    data = usuario_schema.dump(usuario)  # Serializa el usuario
    from src.models.users.logica import get_permisos_usuario  # Importa función de permisos
    data["permisos"] = get_permisos_usuario(usuario)  # Agrega los permisos calculados
    return data  # Retorna el usuario con permisos

# Endpoint: Obtener usuarios por rol (solo admin y empleados)
@user_blueprint.get('/por-rol/<int:rol_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def get_usuarios_por_rol(rol_id):
    usuarios = users.get_usuarios_by_rol(rol_id)  # Busca usuarios por rol
    return users.get_schema_usuario().dumps(usuarios, many=True)  # Serializa y retorna

# Endpoint: Eliminar usuario por id (solo admin)
@user_blueprint.delete('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value])
def delete_usuario_by_id(user_id):
    try:
        usuario = users.delete_usuario_by_id(user_id)  # Elimina el usuario
        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Si no existe, error
        return jsonify({'mensaje': 'Usuario eliminado correctamente'})  # Éxito
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Otro error

# Endpoint: Actualizar usuario por id (solo admin y empleados)
@user_blueprint.put('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def update_usuario(user_id):
    data = request.get_json()  # Obtiene los datos a actualizar
    try:
        usuario = users.update_usuario(user_id, data)  # Actualiza el usuario
        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Si no existe, error
        return users.get_schema_usuario().dumps(usuario)  # Retorna usuario actualizado
    except ValidationError as err:
        return (err.messages, 422)  # Error de validación
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Otro error
