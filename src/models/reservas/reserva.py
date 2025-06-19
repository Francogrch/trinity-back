from src.models.database import db
from src.models.marshmallow import ma
from marshmallow import EXCLUDE, validates_schema, ValidationError
from datetime import datetime, timedelta
from src.models.chat.logica import create_chat

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True)
    id_propiedad = db.Column(db.Integer, db.ForeignKey("propiedad.id"))
    id_inquilino = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    id_usuario_carga = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=True)
    cantidad_personas = db.Column(db.Integer, nullable=False)
    monto_pagado = db.Column(db.Float)
    monto_total = db.Column(db.Float, nullable=False)
    # Falta tabla chat y tabla estado
    id_chat = db.Column(db.Integer, db.ForeignKey("chat.id"))
    id_estado = db.Column(db.Integer,db.ForeignKey("estado.id"))
    id_calificacion_propiedad = db.Column(db.Integer,db.ForeignKey("calificacion_propiedad.id"))
    id_calificacion_inquilino = db.Column(db.Integer,db.ForeignKey("calificacion_inquilino.id"))
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    propiedad = db.relationship(
        "Propiedad", backref="reservas", foreign_keys=[id_propiedad])
    inquilino = db.relationship("Usuario", foreign_keys=[id_inquilino])
    usuario_carga = db.relationship("Usuario", foreign_keys=[id_usuario_carga])

    estado = db.relationship("Estado", foreign_keys=[id_estado])

    calificacion_propiedad = db.relationship("CalificacionPropiedad")
    calificacion_inquilino = db.relationship("CalificacionInquilino")

    def __init__(self, id_propiedad, id_inquilino, cantidad_personas, monto_total,
                 fecha_inicio, fecha_fin, monto_pagado=None, 
                 id_chat=None, id_estado=None, id_usuario_carga=None):
        self.id_propiedad = id_propiedad
        self.id_inquilino = id_inquilino
        self.id_usuario_carga = id_usuario_carga
        self.cantidad_personas = cantidad_personas
        self.monto_total = monto_total
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.monto_pagado = monto_pagado
        if id_chat is None:
            chat_new = create_chat()
            self.id_chat = chat_new.id
        else:
            self.id_chat = id_chat
        self.id_estado = id_estado

    def __repr__(self):
        return f"<Reserva id={self.id} propiedad={self.id_propiedad} inquilino={self.id_inquilino}>"

    def calificar_propiedad(self, calificacion):
        self.calificacion_propiedad = calificacion
        db.session.commit()

    def calificar_inquilino(self, calificacion):
        self.calificacion_inquilino = calificacion
        db.session.commit()

    def is_calificable(self):
        hoy = datetime.today()
        dos_semanas_despues = self.fecha_fin + timedelta(days=15)
        if self.id_estado == 4 and self.fecha_fin <= hoy <= dos_semanas_despues:
            return True
        return False


class ReservaSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    id_propiedad = ma.Integer(required=True)
    id_inquilino = ma.Integer(required=True)
    id_usuario_carga = ma.Integer(allow_none=True)
    cantidad_personas = ma.Integer(required=True)
    monto_pagado = ma.Float(allow_none=True)
    monto_total = ma.Float(required=True)
    id_chat = ma.Integer(allow_none=True)
    id_estado = ma.Integer(allow_none=True)
    fecha_inicio = ma.DateTime(required=True)
    fecha_fin = ma.DateTime(required=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)

    estado = ma.Function(lambda obj: obj.estado.label)

    @validates_schema
    def validar_fechas(self, data, **kwargs):
        if data['fecha_inicio'] >= data['fecha_fin']:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.", field_name='fecha_inicio')


class EmailReservaSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    monto_pagado = ma.Float(allow_none=True)
    inquilino_nombre = ma.Function(lambda obj: obj.inquilino.nombre)
    encargado_nombre = ma.Function(lambda obj: obj.propiedad.encargado.nombre)
    propiedad_nombre = ma.Function(lambda obj: obj.propiedad.nombre)
    fecha_inicio = ma.Function(lambda obj: obj.fecha_inicio)
    fecha_fin = ma.Function(lambda obj: obj.fecha_fin)
    correo_inquilino = ma.Function(lambda obj: obj.inquilino.correo)
    correo_encargado = ma.Function(lambda obj: obj.propiedad.encargado.correo)
