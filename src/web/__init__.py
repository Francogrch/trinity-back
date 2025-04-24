from flask import Flask

from src.models import database, seed
from src.web.controllers.users import user_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.web.config.Config')

    with app.app_context():
        database.init_db(app)
    
    @app.get("/")
    def home():
        return "<h1>Holas</h1>"

    # Importar y registrar el blueprint de rutas
    app.register_blueprint(user_blueprint)

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()
        seed.run()
    
    return app

