def insert_default_data():
    if not Usuario.query.first():
        db.session.add_all([
            Usuario(nombre="Admin", rol="administrador"),
            Usuario(nombre="Juan", rol="inquilino")
        ])
        db.session.commit()

