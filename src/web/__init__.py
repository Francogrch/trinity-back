from flask import Flask
from flask_cors import CORS
from src.models import database, seed
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.users import user_blueprint
from src.web.controllers.propiedades import propiedad_blueprint
from src.extensions import jwt  # Importa la instancia desde extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object('src.web.config.Config')

    jwt.init_app(app)  # Inicializa JWT
    CORS(app)

    with app.app_context():
        database.init_db(app)

    @app.get("/")
    def home():
        return "<h1>Holas</h1>"

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(propiedad_blueprint)

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()
        seed.run()

    return app
