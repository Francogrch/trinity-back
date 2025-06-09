from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail, Message

from src.models import database, marshmallow, email, seed, seed_ciudades

from src.web.utils.reset_tools import resetdb

from src.web.controllers.auth import auth_blueprint
from src.web.controllers.users import user_blueprint
from src.web.controllers.propiedades import propiedad_blueprint
from src.web.controllers.parametricas import parametricas_blueprint
from src.web.controllers.imagenes import imagen_blueprint 
from src.web.controllers.reservas import reserva_blueprint
from src.extensions import jwt  # Importa la instancia desde extensions
import os


def initialize_upload_folders(app: Flask):
    app.config['UPLOAD_BASE_FOLDER'] = 'imagenes'
    app.config['UPLOAD_FOLDER_PROPIEDADES'] = os.path.join(app.config['UPLOAD_BASE_FOLDER'], 'propiedad')
    app.config['UPLOAD_FOLDER_USUARIOS'] = os.path.join(app.config['UPLOAD_BASE_FOLDER'], 'usuario')

    app_root_path = os.path.abspath(os.path.dirname(__file__))

    propiedades_upload_path = os.path.join(app_root_path, app.config['UPLOAD_FOLDER_PROPIEDADES'])
    usuarios_upload_path = os.path.join(app_root_path, app.config['UPLOAD_FOLDER_USUARIOS'])

    os.makedirs(propiedades_upload_path, exist_ok=True)
    os.makedirs(usuarios_upload_path, exist_ok=True)


def create_app():
    app = Flask(__name__)
    app.config.from_object('src.web.config.Config')

    jwt.init_app(app)  # Inicializa JWT

    # Config CORS
    CORS(app)

    with app.app_context():
        database.init_db(app)
        marshmallow.init_ma(app)
        email.init_mail(app)

    @app.get("/")
    def home():
        return "<h1>Hola</h1>"

    #Esto es horrible, pero es lo que hay
    @app.get("/resetdb")
    def reset_endpoint():
        resetdb()
        return {}, 200

    # Carpeta de subidas

    #initialize_upload_folders(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(propiedad_blueprint)
    app.register_blueprint(parametricas_blueprint)
    app.register_blueprint(imagen_blueprint)
    app.register_blueprint(reserva_blueprint)

    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%d/%m/%Y'):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

    # Registrar el comando de Flask CLI
    @app.cli.command(name="resetdb")
    def resetdb_command():
        resetdb()

    return app
