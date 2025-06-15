from src.models.database import db
from src.models.marshmallow import ma
from marshmallow import EXCLUDE
from datetime import datetime


class CalificacionPropiedad(db.Model):
    __tablename__ = "calificacion_propiedad"
    id = db.Column(db.Integer, primary_key=True)
    personal = db.Column(db.Float, nullable=False)
    instalaciones_servicios = db.Column(db.Float, nullable=False)
    limpieza = db.Column(db.Float, nullable=False)
    confort = db.Column(db.Float, nullable=False)
    precio_calidad = db.Column(db.Float, nullable=False)
    ubicacion = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def __init__(self, personal,
                 instalaciones_servicios, limpieza,
                 confort, precio_calidad, ubicacion):
        self.personal = personal
        self.instalaciones_servicios = instalaciones_servicios
        self.limpieza = limpieza
        self.confort = confort
        self.precio_calidad = precio_calidad
        self.ubicacion = ubicacion


    def __repr__(self):
        return f"<Calificación {self.id}>"


class CalificacionPropiedadSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    personal = ma.Float(required=True)
    instalaciones_servicios = ma.Float(required=True)
    limpieza = ma.Float(required=True)
    confort = ma.Float(required=True)
    precio_calidad = ma.Float(required=True)
    ubicacion = ma.Float(required=True)
    created_at = ma.DateTime(allow_none=True, dump_only=True)


class CalificacionInquilino(db.Model):
    __tablename__ = "calificacion_inquilino"
    id = db.Column(db.Integer, primary_key=True)
    calificacion = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def __init__(self, calificacion):
        self.calificacion = calificacion


    def __repr__(self):
        return f"<Calificación {self.id}>"


class CalificacionInquilinoSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    calificacion = ma.Float(required=True)
    created_at = ma.DateTime(allow_none=True, dump_only=True)
