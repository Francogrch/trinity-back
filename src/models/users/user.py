from src.models.database import db
from src.models.marshmallow import ma

from marshmallow import validate, post_load


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    id_rol = db.Column(db.Integer, db.ForeignKey("rol.id"))
    rol = db.relationship("Rol")

    def __init__(self, nombre, id_rol):
        self.nombre = nombre
        self.id_rol = id_rol

    def __repr__(self):
        return f"<Usuario {self.nombre}>"


class UsuarioSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)
    id_rol = ma.Integer(required=True)
