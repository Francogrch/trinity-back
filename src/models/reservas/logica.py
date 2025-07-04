from src.models.database import db
from src.models.reservas.reserva import Reserva, ReservaSchema, EmailReservaSchema
from src.models.propiedades.propiedad import Propiedad
from src.models.chat.logica import get_chat_schema
from src.models.chat.chat import Chat

from sqlalchemy import or_

def get_reservas_por_propiedad(id_propiedad):
    reservas = Reserva.query.filter_by(id_propiedad=id_propiedad).all()
    return reservas

def get_reservas_por_propiedad_filtrada(id_propiedad,id_estado):
    reservas = Reserva.query.filter_by(id_propiedad=id_propiedad, id_estado=id_estado).all()
    return reservas

def get_reservas_por_usuario(usuario):
    roles = usuario.get_roles()
    if roles['is_inquilino']:
        return Reserva.query.filter_by(id_inquilino=usuario.id).all()
    if roles['is_encargado']:
        reservas = db.session.query(Reserva).\
            join(Propiedad).\
            filter(
                or_(
                    Propiedad.id_encargado == usuario.id,
                    Reserva.id_usuario_carga == usuario.id
                )
            ).\
            all()
        return reservas
    if roles['is_admin']:
        return Reserva.query.all()
    return []


def get_reserva(reserva_id, usuario):
    roles = usuario.get_roles()
    if roles['is_admin']:
        return Reserva.query.get(reserva_id)
    if roles['is_encargado']:
        return db.session.query(Reserva).\
        join(Propiedad).\
        filter(
                or_(
                    Propiedad.id_encargado == usuario.id,
                    Reserva.id_usuario_carga == usuario.id
                    ),
               Reserva.id == reserva_id).\
        one()
    if roles['is_inquilino']:
        return db.session.query(Reserva).\
        filter(Reserva.id_inquilino == usuario.id,
               Reserva.id == reserva_id).\
        one()
    return None

def get_reserva_id(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return None
    return reserva

def create_reserva(data):
    nueva_reserva = Reserva(**data)
    db.session.add(nueva_reserva)
    db.session.commit()
    return nueva_reserva


def cancel_reserva(reserva_id, usuario):
    roles = usuario.get_roles()
    try:
        reserva = get_reserva(reserva_id, usuario)
    except:
        reserva = None
    if not reserva or reserva.id_estado == 3 or reserva.id_estado == 4:
        # Si no existe o está finalizada o cancelada devuelve 404
        return None
    reserva.id_estado = 3 # Cambia a estado "Cancelada"
    db.session.commit()
    return reserva


def cambiar_estado_reserva(id_reserva, nuevo_id_estado):
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        return None
    reserva.id_estado = nuevo_id_estado
    db.session.commit()
    return reserva


def hay_reservas_solapadas(id_propiedad, start_date, end_date):
    return Reserva.query.filter(
    Reserva.id_estado != 3,  # Excluye reservas canceladas
    Reserva.id_propiedad == id_propiedad,
    Reserva.fecha_inicio <= end_date,
    Reserva.fecha_fin >= start_date
    ).first() is not None

def cancelar_reservas_not_commit(user_id):
    from datetime import date
    reservas = Reserva.query.filter_by(id_inquilino=user_id).filter(Reserva.id_estado.in_((1, 2))).all()
    for reserva in reservas:
        if not (reserva.fecha_inicio.date() <= date.today() <= reserva.fecha_fin.date() and reserva.id_estado not in [3,4]):
            reserva.id_estado = 3  # Cambia a estado "Cancelada"
    return reservas

def get_chat_id_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return None
    return reserva.id_chat

def get_chat_reserva(chat_id):
    chat = Chat.query.get(chat_id)
    if not chat:
        return None
    return chat

def get_schema_reserva():
    return ReservaSchema()


def get_schema_email_reserva():
    return EmailReservaSchema()
