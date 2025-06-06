from src.models.database import db
from src.models.reservas.reserva import Reserva, ReservaSchema
from src.models.propiedades.propiedad import Propiedad


def get_reservas_por_propiedad(id_propiedad):
    reservas = Reserva.query.filter_by(id_propiedad=id_propiedad).all()
    return reservas


def get_reservas_por_usuario(usuario):
    roles = usuario.get_roles()
    if roles['is_inquilino']:
        return Reserva.query.filter_by(id_inquilino=usuario.id).all()
    if roles['is_encargado']:
        reservas = db.session.query(Reserva).\
        join(Propiedad).\
        filter(Propiedad.id_encargado == usuario.id).\
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
        filter(Propiedad.id_encargado == usuario.id,
               Reserva.id == reserva_id).\
        one_or_none()
    if roles['is_inquilino']:
        return db.session.query(Reserva).\
        filter(Reserva.id_inquilino == usuario.id,
               Reserva.id == reserva_id).\
        one_or_none()
    return None


def create_reserva(data):
    nueva_reserva = Reserva(**data)
    db.session.add(nueva_reserva)
    db.session.commit()
    return nueva_reserva


def cancel_reserva(reserva_id, usuario):
    roles = usuario.get_roles()
    reserva = get_reserva(reserva_id, usuario)
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
    Reserva.id_propiedad == id_propiedad,
    Reserva.fecha_inicio <= end_date,
    Reserva.fecha_fin >= start_date
    ).first() is not None


def get_schema_reserva():
    return ReservaSchema()
