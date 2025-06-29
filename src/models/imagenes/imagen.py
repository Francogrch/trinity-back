from src.models.database import db
from src.models.marshmallow import ma
from marshmallow import EXCLUDE, validate

class Imagen(db.Model):
    
    __tablename__ = "imagen"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=True)

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'), nullable=True)
    id_reserva = db.Column(db.Integer, db.ForeignKey('reserva.id'), nullable=True)
    usuario = db.relationship('Usuario', foreign_keys=[id_usuario], back_populates='imagen') # O el nombre que uses
    propiedad = db.relationship('Propiedad', foreign_keys=[id_propiedad], back_populates='imagenes')
    reserva = db.relationship('Reserva', foreign_keys=[id_reserva], back_populates='documentacion')
    def __init__(self, url=None,id_usuario=None, id_propiedad=None,id_reserva=None):
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.id_propiedad = id_propiedad
        self.url = url

    def __repr__(self):
        return f"{self.id}"

class ImagenSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    url = ma.String(required=True, validate=validate.URL(error="Debe ser una URL válida."))

