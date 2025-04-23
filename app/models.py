from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    rol = db.Column(db.String(50))

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

def insert_default_data():
    if not Usuario.query.first():
        db.session.add_all([
            Usuario(nombre="Admin", rol="administrador"),
            Usuario(nombre="Juan", rol="inquilino")
        ])
        db.session.commit()

