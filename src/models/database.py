from flask_sqlalchemy import SQLAlchemy  # Importa la extensión SQLAlchemy para manejar la base de datos

# Instancia global de SQLAlchemy para usar en los modelos
# Se inicializa con la app en init_db

db = SQLAlchemy()


def init_db(app):
    """
    Inicializa la base de datos con la app Flask.
    - Llama a db.init_app(app) para asociar la app con SQLAlchemy.
    - Crea todas las tablas según los modelos definidos.
    - Registra un handler para cerrar la sesión de la base de datos al finalizar cada request.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()


def reset_db():
    """
    Elimina todas las tablas y las vuelve a crear según los modelos actuales.
    Útil para desarrollo y testing. Debe ejecutarse dentro de un contexto de app.
    """
    from flask import current_app
    with current_app.app_context():
        db.drop_all()
        db.create_all()
        print("DB reseteada")
