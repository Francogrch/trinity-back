from flask import Blueprint, request, jsonify, current_app  # Para manejar rutas, peticiones y respuestas JSON
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from marshmallow import ValidationError

from datetime import timedelta  # Para definir la duración del token

from src.models import users
from src.extensions.jwt import BLOCKLIST  # Lista negra de tokens revocados
from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol

# Crea un blueprint para agrupar las rutas de autenticación
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.post('/login')
def login():
    """
    Ruta para iniciar sesión.
    Recibe JSON con 'correo' y 'password', verifica las credenciales y devuelve un token JWT si son válidas.
    """
    data = request.get_json()  # Extrae el JSON enviado en el body de la solicitud
    usuario = users.get_usuario_by_correo(data['correo'])  # Busca el usuario por su correo

    if usuario and usuario.check_password(data['password']):  # Si el usuario existe y la contraseña es correcta
        # Claims personalizados: id, tipo y número de identificación
        additional_claims = {
            'id': usuario.id,
            'tipo_identificacion': usuario.tipo_identificacion.nombre if usuario.tipo_identificacion else None,
            'numero_identificacion': usuario.numero_identificacion
        }
        # Crea un token JWT con identidad del usuario y claims personalizados
        access_token = create_access_token(
            identity=str(usuario.id),  # ID del usuario como identidad principal
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=2)  # Token válido por 2 horas
        )
        return jsonify({'token': access_token})  # Devuelve el token al cliente

    # Si el usuario no existe o la contraseña es incorrecta, devuelve error 401
    return jsonify({'mensaje': 'Credenciales inválidas'}), 401


@auth_blueprint.post('/logout')
@jwt_required()
def logout():
    """
    Ruta protegida para cerrar sesión.
    Revoca el token actual agregándolo a la blocklist (lista negra).
    """
    jti = get_jwt()["jti"]  # Obtiene el identificador único del token actual (JWT ID)
    BLOCKLIST.add(jti)  # Agrega el jti a la lista negra en memoria
    return jsonify(msg="Sesión cerrada correctamente"), 200  # Confirma que el logout fue exitoso


@auth_blueprint.post('/forgot-password/reset')
@jwt_required()
def reset_password():
    usuario = users.get_usuario_by_id(get_jwt_identity())
    claims = get_jwt()
    if not usuario or claims.get('purpose') != 'RESET_PASSWORD':
        return {'error': 'Token incorrecto'}, 422
    data = request.get_json()  # Extrae el JSON enviado en el body de la solicitud
    try:
        data_password = users.get_schema_password().load(data)
        users.change_password(usuario, data_password['password'])
    except ValidationError as err:
        return (err.messages, 422)
    except Exception as e:
        print(e)
        return ({"error": "No se pudo editar la contraseña."}, 400)
    BLOCKLIST.add(claims['jti'])  # Agrega el jti a la lista negra en memoria
    return {}, 200  # Confirma que el logout fue exitoso


@auth_blueprint.post('/forgot-password')
def generate_temporary_link():
    data = request.get_json()  # Extrae el JSON enviado en el body de la solicitud
    usuario = users.get_usuario_by_correo(data['correo'])  # Busca el usuario por su correo
    if not usuario:
        return {}, 200
    expires = timedelta(minutes=2)
    additional_claims = {"purpose": "RESET_PASSWORD"}
    access_token = create_access_token(identity=str(usuario.id), expires_delta=expires, additional_claims=additional_claims)
    # send mail
    return {'token': access_token}, 200  # Devuelve el token al cliente
