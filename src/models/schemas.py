from src.models.marshmallow import ma

class RolSchema(ma.Schema):
    id = ma.Integer()
    nombre = ma.String()

class PaisSchema(ma.Schema):
    id = ma.Integer()
    nombre = ma.String()
