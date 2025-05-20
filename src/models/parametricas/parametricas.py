from src.models.database import db
from src.models.marshmallow import ma

from marshmallow import EXCLUDE


class Provincia(db.Model):
    __tablename__ = "provincias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    ciudades = db.relationship("Ciudad", back_populates="provincia")

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre


class Ciudad(db.Model):
    __tablename__ = "ciudades"
    id = db.Column(db.Integer, primary_key=True)
    id_provincia = db.Column(db.Integer, db.ForeignKey("provincias.id"))
    nombre = db.Column(db.String, nullable=False)
    provincia = db.relationship("Provincia", back_populates="ciudades")

    def __init__(self, provincia, nombre):
        self.provincia = provincia
        self.nombre = nombre

    def __repr__(self):
        return f"<{self.provincia}, {self.nombre}>"


class PropiedadTipo(db.Model):
    __tablename__ = "propiedad_tipos"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo

    def __repr__(self):
        return self.tipo


class PoliticaReserva(db.Model):
    __tablename__ = "politicas_reserva"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, unique=True, nullable=False)
    porcentaje = db.Column(db.Float, unique=True, nullable=False)

    def __init__(self, label, porcentaje):
        self.label = label
        self.porcentaje = porcentaje

    def __repr__(self):
        return self.porcentaje


class TipoIdentificacion(db.Model):
    __tablename__ = "tipo_identificacion"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre


class Pais(db.Model):
    __tablename__ = "paises"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre


class ProvinciaSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True, dump_only=True)


class CiudadSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    id_provincia = ma.Integer(required=True, dump_only=True)
    nombre = ma.String(required=True, dump_only=True)


class PropiedadTipoSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    tipo = ma.String(required=True)


class PoliticaReservaSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    label = ma.String(required=True)
    porcentaje = ma.Float(required=True)


class TipoIdentificacionSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)


class PaisSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)


class RolSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    label = ma.String(required=True)
