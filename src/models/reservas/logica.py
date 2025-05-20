from src.models.database import db
from src.models.reservas.reserva import Reserva, ReservaSchema


def get_reservas_por_propiedad(id_propiedad):
    reservas = Reserva.query.filter_by(id_propiedad=id_propiedad).all()
    return reservas


def create_reserva(data):
    nueva_reserva = Reserva(
        id_propiedad=data["id_propiedad"],
        id_inquilino=data["id_inquilino"],
        id_usuario_carga=data["id_usuario_carga"],
        cantidad_personas=data["cantidad_personas"],
        monto_total=data["monto_total"],
        fecha_inicio=data["fecha_inicio"],
        fecha_fin=data["fecha_fin"],
        monto_pagado=data.get("monto_pagado"),
        id_chat=data.get("id_chat"),
        id_estado=data.get("id_estado")
    )
    db.session.add(nueva_reserva)
    db.session.commit()
    return nueva_reserva


def cambiar_estado_reserva(id_reserva, nuevo_id_estado):
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        return None
    reserva.id_estado = nuevo_id_estado
    db.session.commit()
    return reserva


def get_schema_reserva():
    return ReservaSchema()
