from flask_jwt_extended import JWTManager, get_jwt

jwt = JWTManager()


# Lista negra en memoria (usá Redis o una tabla real si querés persistencia)
BLOCKLIST = set()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Esta función verifica si un token está en la lista de bloqueo.
    Retorna True si el token debe considerarse inválido (revocado).
    """
    jti = jwt_payload.get("jti")
    # Acá podrías consultar una base de datos o lista negra en memoria
    return jti in BLOCKLIST


@jwt.unauthorized_loader
def unauthorized_response(callback):
    print("DEBUG: Token requerido - no se envió o está mal el header")
    return {"msg": "Token requerido"}, 401


@jwt.invalid_token_loader
def invalid_token_response(error):
    print(f"DEBUG: Token inválido - {error}")
    return {"msg": "Token inválido"}, 422

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    if jwt_payload.get('purpose') == 'RESET_PASSWORD':
        return {'msg': 'USED'}, 401
    return {'msg': 'LOGGED_OUT'}, 401

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return {'msg': 'EXPIRED'}, 401
