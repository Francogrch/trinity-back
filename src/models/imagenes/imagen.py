from src.models.database import db
from src.models.marshmallow import ma
from marshmallow import EXCLUDE, validate

class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False, comment='URL de la imagen almacenada')

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"<Imagen {self.id}>"

class ImagenSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    url = ma.String(required=True, validate=validate.URL(error="Debe ser una URL válida."))

