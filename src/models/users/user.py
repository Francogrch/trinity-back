from src.models.database import db
from src.models.marshmallow import ma

from marshmallow import validate, post_load

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    rol = db.Column(db.String(50))

    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

class UsuarioSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)
    rol = ma.String(required=True, validate=validate.OneOf(["Cliente", "Encargado", "Administrador"]))
