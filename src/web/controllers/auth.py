from flask import Blueprint, request, jsonify, url_for  # Para manejar rutas, peticiones y respuestas JSON
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from marshmallow import ValidationError

from datetime import timedelta  # Para definir la duración del token

from src.models import users
from src.models import email
from src.extensions.jwt import BLOCKLIST  # Lista negra de tokens revocados
from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol
from src.models import auth

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

        access_token = auth.login(usuario)
        return jsonify({'token': access_token, 'rol': usuario.roles[0].id})  # Devuelve el token al cliente

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


@auth_blueprint.post('/check-password')
@jwt_required()
def check_password():
    usuario = users.get_usuario_by_id(get_jwt_identity())
    password = request.get_json().get('password')
    if usuario and password and usuario.check_password(password):  # Si el usuario existe y la contraseña es correcta
        return {}, 200
    return {'error': 'Contraseña incorrecta'}, 401


@auth_blueprint.post('/forgot-password/reset')
@jwt_required()
def reset_password():
    usuario = users.get_usuario_by_id(get_jwt_identity())
    claims = get_jwt()
    if not usuario:
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
    if claims.get('purpose') != "LOGIN":
        BLOCKLIST.add(claims['jti'])  # Agrega el jti a la lista negra en memoria si el jwt no es de sesion
    return {}, 200  # Confirma que el logout fue exitoso


@auth_blueprint.post('/forgot-password')
def generate_temporary_link():
    data = request.get_json()  # Extrae el JSON enviado en el body de la solicitud
    usuario = users.get_usuario_by_correo(data['correo'])  # Busca el usuario por su correo
    if not usuario:
        return {}, 200
    expires = timedelta(hours=24)
    additional_claims = {"purpose": "RESET_PASSWORD"}
    access_token = create_access_token(identity=str(usuario.id), expires_delta=expires, additional_claims=additional_claims)
    # Generar datos necesarios para el email
    reset_password_url = f"http://localhost:4200/usuarios/reset-password?token={access_token}"
    logo_url = url_for('static', filename='img/laTrinidadAzulChico.png', _external=True)
    # Enviar correos en segundo plano sin bloquear la respuesta HTTP
    email.run_async_with_context(email.send_reset_password, logo_url, reset_password_url, usuario.correo)
    return {}, 200
