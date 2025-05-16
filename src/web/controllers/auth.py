from flask import Blueprint, request, jsonify, current_app  # Para manejar rutas, peticiones y respuestas JSON
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt  # Funciones necesarias para manejo de JWT
)
from datetime import timedelta  # Para definir la duración del token
from src.models.users.logica import get_usuario_by_correo  # Lógica de acceso a datos del usuario
from src.extensions.jwt import BLOCKLIST  # Lista negra de tokens revocados

# Crea un blueprint para agrupar las rutas de autenticación
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.post('/login')
def login():
    """
    Ruta para iniciar sesión.
    Recibe JSON con 'correo' y 'password', verifica las credenciales y devuelve un token JWT si son válidas.
    """
    data = request.get_json()  # Extrae el JSON enviado en el body de la solicitud
    usuario = get_usuario_by_correo(data['correo'])  # Busca el usuario por su correo

    if usuario and usuario.check_password(data['password']):  # Si el usuario existe y la contraseña es correcta
        # Define los claims adicionales (datos extras que querés guardar en el token)
        additional_claims = {
            'correo': usuario.correo,
            'rol': usuario.rol
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
