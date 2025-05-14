from src.models.database import db
from datetime import datetime


class Propiedad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    entre_calles = db.Column(db.String, nullable=False)
    calle = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    piso = db.Column(db.String, nullable=False)
    depto = db.Column(db.String, nullable=False)
    huespedes = db.Column(db.Integer, nullable=False)
    ambientes = db.Column(db.Integer, nullable=False)
    banios = db.Column(db.Integer, nullable=False)
    cocheras = db.Column(db.Integer, nullable=False)
    precioNoche = db.Column(db.Float, nullable=False)
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
        numero, piso, depto, id_ciudad,
        huespedes, ambientes, banios,
        cocheras, id_pol_reserva, precioNoche, id_tipo
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.entre_calles = entre_calles
        self.calle = calle
        self.numero = numero
        self.piso = piso
        self.depto = depto
        self.id_ciudad = id_ciudad
        self.huespedes = huespedes
        self.ambientes = ambientes
        self.banios = banios
        self.cocheras = cocheras
        self.id_pol_reserva = id_pol_reserva
        self.precioNoche = precioNoche
        self.id_tipo = id_tipo

    def __repr__(self):
        return f"<Propiedad {self.nombre}>"
