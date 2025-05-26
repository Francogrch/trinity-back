class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alquileres.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super-secret-key'  # Agrega la clave secreta para JWT y sesiones

    # Configuraciones para Flask-JWT-Extended
    JWT_SECRET_KEY = SECRET_KEY  # Usar la misma clave para JWT
    JWT_ACCESS_TOKEN_EXPIRES = 7200  # Tiempo de expiración en segundos (2 horas)
    JWT_BLACKLIST_ENABLED = True  # Activar la blacklist para revocar tokens
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']  # Revocar tokens de acceso (no refresh)

    # Configuraciones de Flask-Mail
    """ Esto es para testear local con aiosmtpd
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    """
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'alquiloando1@gmail.com'
    MAIL_PASSWORD = 'uioermbleomvetkj' # APP Password para integrar con flask, password real=?J3:m~Jk2}w6Z&H
    MAIL_SUPPRESS_SEND = True # Esto bloquea el envio del msg.
    #MAIL_SUPPRESS_SEND = False # Descomentar esto para que mande realmente el email.
    MAIL_DEFAULT_SENDER = ('Alquiloando SA', 'alquiloando1@gmail.com')
