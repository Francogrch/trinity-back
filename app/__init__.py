from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    # Importar modelos y rutas
    from app import models 

    with app.app_context():
        db.create_all()  # Crea tablas si no existen
        models.insert_default_data()  # Opcional: carga datos por defecto
    
    # Importar y registrar el blueprint de rutas
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)
    
    return app

