from src.models.database import db
from src.models.marshmallow import ma

from marshmallow import validate, EXCLUDE
from datetime import datetime


class Propiedad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    entre_calles = db.Column(db.String, nullable=False)
    calle = db.Column(db.String, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    piso = db.Column(db.String)
    depto = db.Column(db.String)
    huespedes = db.Column(db.Integer, nullable=False)
    ambientes = db.Column(db.Integer, nullable=False)
    banios = db.Column(db.Integer, nullable=False)
    cocheras = db.Column(db.Integer, nullable=False)
    precioNoche = db.Column(db.Float, nullable=False)
    codigoAcceso = db.Column(db.String, nullable=False, default="0000")
    is_habilitada = db.Column(db.Boolean,nullable=False, default=True)
    #Relación con Porcentaje del primer pago
    id_pol_reserva = db.Column(db.Integer, db.ForeignKey("politicas_reserva.id"))
    pol_reserva = db.relationship("PoliticaReserva")
    #Relación con Tipos de propiedad
    id_tipo = db.Column(db.Integer, db.ForeignKey("propiedad_tipos.id"))
    tipo = db.relationship("PropiedadTipo")
    #Relación con Ciudad
    id_ciudad = db.Column(db.Integer, db.ForeignKey("ciudades.id"))
    ciudad = db.relationship("Ciudad")
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def __init__(
        self, nombre, descripcion, entre_calles, calle,
        numero, piso, depto, huespedes, ambientes, banios,
        cocheras, precioNoche, codigoAcceso, is_habilitada,
        id_pol_reserva, id_tipo, id_ciudad
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.entre_calles = entre_calles
        self.calle = calle
        self.numero = numero
        self.piso = piso
        self.depto = depto
        self.huespedes = huespedes
        self.ambientes = ambientes
        self.banios = banios
        self.cocheras = cocheras
        self.precioNoche = precioNoche
        self.codigoAcceso = codigoAcceso
        self.is_habilitada = is_habilitada
        self.id_pol_reserva = id_pol_reserva
        self.id_tipo = id_tipo
        self.id_ciudad = id_ciudad

    def __repr__(self):
        return f"<Propiedad {self.nombre}>"

class PropiedadSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)
    descripcion = ma.String(required=True)
    entre_calles = ma.String(required=True)
    calle = ma.String(required=True)
    numero = ma.Integer(required=True)
    piso = ma.String()
    depto = ma.String()
    huespedes = ma.Integer(required=True)
    ambientes = ma.Integer(required=True)
    banios = ma.Integer(required=True)
    cocheras = ma.Integer(required=True)
    precioNoche = ma.Float(required=True)
    codigoAcceso = ma.String(required=True, validate=validate.Regexp(r'[0-9][0-9][0-9][0-9]'))
    is_habilitada = ma.Boolean(required=True)
    id_pol_reserva = ma.Integer(required=True)
    id_tipo = ma.Integer(required=True)
    id_ciudad = ma.Integer(required=True)
    
    ciudad = ma.Function(lambda obj: obj.ciudad.nombre)
    id_provincia = ma.Function(lambda obj: obj.ciudad.provincia.id)
    provincia = ma.Function(lambda obj: obj.ciudad.provincia.nombre)
    tipo = ma.Function(lambda obj: obj.tipo.tipo)
