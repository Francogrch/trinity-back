from src.models.database import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    rol = db.Column(db.String(50))

    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

