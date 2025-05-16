from src.models.database import db
from src.models.marshmallow import ma

from marshmallow import validate, post_load

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    rol = db.Column(db.String(50))

    def __init__(self, nombre, correo, rol, password=None):
        self.nombre = nombre
        self.correo = correo
        # Asegura que el rol sea un valor válido del enum
        if isinstance(rol, Rol):
            self.rol = rol.value
        elif rol in [r.value for r in Rol]:
            self.rol = rol
        else:
            raise ValueError(f"Rol inválido: {rol}")
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

class UsuarioSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)
    rol = ma.String(required=True, validate=validate.OneOf(["Cliente", "Encargado", "Administrador"]))
