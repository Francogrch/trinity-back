from src.models.marshmallow import ma
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import validate, post_load
from src.models.database import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey("rol.id"))
    rol = db.relationship("Rol")
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, nombre, correo, id_rol, password=None):
        self.nombre = nombre
        self.correo = correo
        self.id_rol = id_rol
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

class RolSchema(ma.Schema):
    id = ma.Integer()
    nombre = ma.Method("get_nombre")

    def get_nombre(self, obj):
        # Devuelve label si existe, si no, intenta nombre
        return getattr(obj, "label", None) or getattr(obj, "nombre", None)

class UsuarioSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)
    id_rol = ma.Integer(required=True)
    correo = ma.String(required=True)
    rol = ma.Nested(RolSchema, dump_only=True)  # Incluye el objeto rol serializado solo al hacer dump
    # Puedes agregar más campos si es necesario
