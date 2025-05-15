class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alquileres.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super-secret-key'  # Agrega la clave secreta para JWT y sesiones

    # Configuraciones para Flask-JWT-Extended
    JWT_SECRET_KEY = SECRET_KEY  # Usar la misma clave para JWT
    JWT_ACCESS_TOKEN_EXPIRES = 7200  # Tiempo de expiración en segundos (2 horas)
    JWT_BLACKLIST_ENABLED = True  # Activar la blacklist para revocar tokens
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']  # Revocar tokens de acceso (no refresh)
