from flask import Flask
from flask_cors import CORS
from flask_mail import Mail, Message

from src.models import database, marshmallow, email, seed, seed_ciudades
from src.models.email import mail

from src.web.controllers.auth import auth_blueprint
from src.web.controllers.users import user_blueprint
from src.web.controllers.propiedades import propiedad_blueprint
from src.web.controllers.parametricas import parametricas_blueprint
from src.web.controllers.imagenes import imagen_blueprint 
from src.web.controllers.reservas import reserva_blueprint
from src.extensions import jwt  # Importa la instancia desde extensions


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
        msg = Message("Correo de prueba", recipients=["mcingolani28@gmail.com"])
        msg.html = "<h1>Este es un test usando aiosmtpd</h1>"
        mail.send(msg)
        return "<h1>Holas</h1>"
    # Carpeta de subidas
    app.config['UPLOAD_FOLDER'] = 'uploads'

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(propiedad_blueprint)
    app.register_blueprint(parametricas_blueprint)
    app.register_blueprint(imagen_blueprint)
    app.register_blueprint(reserva_blueprint)

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()
        seed_ciudades.run()
        seed.run()

    return app
