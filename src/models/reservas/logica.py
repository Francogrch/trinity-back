from src.models.database import db
from src.models.reservas.reserva import Reserva, ReservaSchema


def get_reservas_por_propiedad(id_propiedad):
    reservas = Reserva.query.filter_by(id_propiedad=id_propiedad).all()
    return reservas


def get_reservas_por_usuario(usuario):
    roles = usuario.get_roles()
    if roles['is_inquilino']:
        return Reserva.query.filter_by(id_inquilino=usuario.id).all()
    if roles['is_encargado']:
        return Reserva.query.all()
    if roles['is_admin']:
        return Reserva.query.all()
    return []


def get_reserva(reserva_id, usuario):
    roles = usuario.get_roles()
    reserva = Reserva.query.get(reserva_id)
    if roles['is_admin']:
        return reserva
    if roles['is_encargado']:
        return reserva  # Hay que corregir esto
    if roles['is_inquilino'] and reserva and reserva.id_inquilino == usuario.id:
        return reserva
    return None


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
