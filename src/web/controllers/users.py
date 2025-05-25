from logging import exception
import os
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from marshmallow import ValidationError

#Usa get_jwt_identity() si solo necesitas el identificador principal del usuario autenticado.
#Usa get_jwt() si necesitas acceder a otros datos o claims personalizados dentro del JWT.
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from src.models.imagenes import get_filename, upload_image, delete_image
from src.web.authorization.roles import rol_requerido
from src.models.users.logica import get_permisos_usuario
from src.models import users
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

# Endpoint: Obtener todos los empleados (solo para admin)
@user_blueprint.get('/empleados')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo rol Administrador puede acceder
# Devuelve la lista de empleados serializada
def get_empleados():
    usuarios = users.get_empleados()  # Obtiene todos los usuarios de la base
    return users.get_schema_empleado().dump(usuarios, many=True)  # Serializa y retorna

# Endpoint: Crear un nuevo usuario (solo admin y empleados)
@user_blueprint.post('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden crear usuarios
# Recibe los datos por JSON, valida permisos y crea el usuario
def create_usuario():
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
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value, Rol.INQUILINO.value])
def get_usuario_by_id(user_id):
    usuario = users.get_usuario_by_id(user_id)  # Busca el usuario por id
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Si no existe, error
    usuario_schema = users.get_schema_usuario()  # Obtiene el schema
    data = usuario_schema.dump(usuario)  # Serializa el usuario
    data["permisos"] = get_permisos_usuario(usuario)  # Agrega los permisos calculados
    return data  # Retorna usuario serializado con permisos

# Endpoint: Obtener el usuario autenticado (perfil propio)
@user_blueprint.get('/me')
@jwt_required()
def get_usuario_actual():
    user_id = get_jwt_identity()  # Obtiene el id del usuario autenticado
    usuario = users.get_usuario_by_id(user_id)  # Busca el usuario en la base
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404  # Si no existe, error
    usuario_schema = users.get_schema_usuario()  # Obtiene el schema
    data = usuario_schema.dump(usuario)  # Serializa el usuario
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

@user_blueprint.post('/imagenPerfil')
#@jwt_required()
def upload_imagen():
    id_usuario = request.args.get('id_usuario')
    image = upload_image('usuario',request,id_usuario=id_usuario)
    if image[1] == 201:
       users.set_imagen_usuario(id_usuario, str(image[0]['id']))
    return image

@user_blueprint.get('/imagenPerfil/<int:user_id>')
def get_imagen(user_id):
    user = users.get_usuario_by_id(user_id)
    if not user.id_imagen:
        return {"error": "El usuario no tiene una imagen asociada"}, 404
    imagen_id = str(user.id_imagen)

    base_upload_directory = os.path.abspath(
        os.path.join(current_app.root_path, "..", "..", "imagenes", "usuario")
    )

    filename = get_filename(imagen_id)

    return send_from_directory(
        directory=base_upload_directory,
        path=filename,
        as_attachment=False
    )

@user_blueprint.delete('/imagenPerfil')
#@jwt_required() 
def delete_imagen():
    id_usuario = request.args.get('id_usuario')
    user = users.get_usuario_by_id(id_usuario)
    if not user.id_imagen:
        return {"error": "El usuario no tiene una imagen asociada"}, 404
    id_imagen = str(user.id_imagen)

    success, message = delete_image(id_imagen, 'usuario')
    users.set_imagen_usuario(id_usuario,None) 

    if success:
        return jsonify({"message": message if message else f"Imagen con ID {id_imagen} eliminada exitosamente"}), 200
    else:
        return jsonify({"message": message}), 500

@user_blueprint.get('/encargados')
# @jwt_required()
# @rol_requerido([Rol.ADMINISTRADOR.value])  # Solo rol Administrador puede acceder
def get_encargados():
    usuarios = users.get_encargados()  # Obtiene todos los usuarios de la base
    return users.get_schema_empleado().dump(usuarios, many=True)  # Serializa y retorna


