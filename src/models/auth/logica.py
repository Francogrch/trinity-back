from flask_jwt_extended import create_access_token
from datetime import timedelta  # Para definir la duración del token
from src.extensions.jwt import BLOCKLIST  # Lista negra de tokens revocados

def login(usuario):
    additional_claims = {
        'id': usuario.id,
        'tipo_identificacion': usuario.tipo_identificacion.nombre if usuario.tipo_identificacion else None,
        'numero_identificacion': usuario.numero_identificacion
    }
    # Crea un token JWT con identidad del usuario y claims personalizados
    return create_access_token(
        identity=str(usuario.id),  # ID del usuario como identidad principal
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=2)  # Token válido por 2 horas
    )

def block_token(jti):
    BLOCKLIST.add(jti)  # Agrega el jti a la lista negra en memoria
