from src.models import email
from src.models.reservas.logica import cambiar_estado_reserva,get_reservas_por_propiedad_filtrada, get_schema_email_reserva
from src.models.database import db
from src.models.propiedades.propiedad import Propiedad, PropiedadSchema, PropiedadProtegidaSchema, CodigoAccesoSchema
from src.models.reservas.reserva import Reserva 
from datetime import datetime
from flask import url_for

import re
from sqlalchemy import or_

def parse_datetime_string(dt_str: str) -> datetime:
    """
    Parsea una cadena de fecha y hora con el formato
    'Thu May 22 2025 22:08:41 GMT-0300 (Argentina Standard Time)'
    a un objeto datetime.

    Args:
        dt_str (str): La cadena de fecha y hora a parsear.

    Returns:
        datetime: El objeto datetime resultante.

    Raises:
        ValueError: Si la cadena no coincide con el formato esperado.
    """
    # Expresión regular para extraer las partes que nos interesan
    # Ignoramos explícitamente la parte "(Argentina Standard Time)" ya que strptime no la maneja bien con %Z.
    # El patrón capturará 'Thu May 22 2025 22:08:41 GMT-0300'
    match = re.match(r"^(.*?)\s*GMT([+-]\d{4})\s*\(.*?\)$", dt_str)

    if not match:
        # Intento alternativo si no hay "(Argentina Standard Time)"
        match = re.match(r"^(.*?)\s*GMT([+-]\d{4})$", dt_str)
        if not match:
            raise ValueError(f"Formato de fecha no reconocido: {dt_str}")

    date_time_part = match.group(1).strip() # 'Thu May 22 2025 22:08:41 '
    offset_part = match.group(2)            # '-0300'

    # Concatenamos la parte de fecha/hora con el offset para strptime
    # Asegúrate de que no haya espacios extra entre la hora y el offset
    # Si la cadena original ya incluye un espacio antes de GMT, deberías ajustar la regex.
    # Por el ejemplo, parece que sí lo incluye.
    full_datetime_string_for_strptime = f"{date_time_part} {offset_part}"

    # Formato para strptime:
    # %a: Abreviatura del día de la semana (Thu)
    # %b: Abreviatura del mes (May)
    # %d: Día del mes (22)
    # %Y: Año (2025)
    # %H: Hora (22)
    # %M: Minuto (08)
    # %S: Segundo (41)
    # %z: Desplazamiento UTC en formato +HHMM o -HHMM (-0300)
    format_string = "%a %b %d %Y %H:%M:%S %z"

    return datetime.strptime(full_datetime_string_for_strptime, format_string)

def has_reservas_activas(propiedad_id):
    return db.session.query(Reserva).\
    join(Propiedad).\
    filter(
            Propiedad.id == propiedad_id,
            Reserva.id_estado.in_([1,2])
    ).first() is not None

def check_estado_eliminada(propiedad_id):
    propiedad = get_propiedad_id(propiedad_id)
    if not propiedad or (propiedad.delete_at is not None and propiedad.delete_at < datetime.now()):
        return
    if has_reservas_activas(propiedad_id):
        return
    propiedad.delete_at = datetime.now()
    db.session.commit()

def get_propiedades_usuario(usuario):
    if usuario.get_roles()['is_encargado']:
        return Propiedad.query.filter_by(
                delete_at=None, id_encargado=usuario.id).all()
    return Propiedad.query.filter_by(delete_at=None).all()

def get_propiedades():
    return Propiedad.query.filter_by(delete_at=None).all()

def update_encargado(id_propiedad,id_encargado):
    propiedad = get_propiedad_id(id_propiedad)
    if not propiedad:
        return None
    propiedad.id_encargado = id_encargado
    db.session.commit()
    return propiedad 

# Deprecated
def get_propiedades_eliminadas():
    propiedades = Propiedad.query.filter(Propiedad.delete_at.isnot(None),Propiedad.delete_at >= datetime.now()).all()
    return propiedades

def get_propiedades_eliminadas_usuario(usuario):
    if usuario.get_roles()['is_encargado']:
        return Propiedad.query.filter(
                Propiedad.id_encargado == usuario.id,
                Propiedad.delete_at.isnot(None),
                Propiedad.delete_at >= datetime.now()
                ).all()
    return Propiedad.query.filter(
            Propiedad.delete_at.isnot(None),
            Propiedad.delete_at >= datetime.now()
            ).all()


def get_propiedad_usuario(propiedad_id, usuario):
    filtro_propiedades_accesibles = or_(
        Propiedad.delete_at == None,  # delete_at is NULL
        Propiedad.delete_at > datetime.now()     # delete_at es futura
    )
    roles = usuario.get_roles()
    if roles['is_admin']:
        return Propiedad.query.filter(
                filtro_propiedades_accesibles,
                Propiedad.id == propiedad_id
                ).one()
    if roles['is_encargado']:
        return Propiedad.query.filter(
                filtro_propiedades_accesibles,
                Propiedad.id_encargado == usuario.id,
                Propiedad.id == propiedad_id
                ).one()
    return None


def get_propiedad_id(id):
    return Propiedad.query.get(id)

def cambiar_nombre_eliminada(prop_id):
    propiedad = get_propiedad_id(prop_id)
    if not propiedad:
        return None
    # Cambiar el nombre de la propiedad eliminada
    propiedad.nombre = f"{propiedad.nombre} (Eliminada el dia {propiedad.delete_at.strftime('%d/%m/%Y')})"
    return propiedad 

def eliminar_prop_hasta_fecha(prop_id):
    propiedad = get_propiedad_id(prop_id)
    if not propiedad:
        return None
    propiedad.is_habilitada = False
    reservas_propiedad= Reserva.query.filter_by(id_propiedad=prop_id).filter(Reserva.id_estado == 1).all()

    if reservas_propiedad:
        fecha_max = max(reservas_propiedad, key=lambda reserva: reserva.fecha_fin)
        propiedad.delete_at = fecha_max.fecha_fin 
    else: 
        propiedad.delete_at = datetime.now()
    cambiar_nombre_eliminada(prop_id)
    try:
        db.session.commit()
        return propiedad
    except Exception:
        db.session.rollback()
        raise

def eliminar_prop_con_reservas(prop_id,usuario):
    propiedad = get_propiedad_id(prop_id)
    
    if not propiedad:
        return None
    propiedad.is_habilitada = False
    # Eliminar todas las reservas asociadas a la propiedad
    reservas_propiedad = get_reservas_por_propiedad_filtrada(prop_id,id_estado=1)
    for reserva in reservas_propiedad:
        res = cambiar_estado_reserva(reserva.id, 3) 
        if res:
            # Generar datos necesarios para el email
            data_email = get_schema_email_reserva().dump(res)
            reserva_url = f"http://localhost:4200/detalle-reserva/{res.id}"
            logo_url = url_for('static', filename='img/laTrinidadAzulChico.png', _external=True)
            # Enviar correos en segundo plano sin bloquear la respuesta HTTP
            email.run_async_with_context(email.send_reserva_cancelada, data_email, reserva_url, logo_url, usuario.get_roles()['is_inquilino'])
    propiedad.delete_at = datetime.now()
    cambiar_nombre_eliminada(prop_id)
    try:
        db.session.commit()
        return propiedad
    except Exception:
        db.session.rollback()
        raise

def create_propiedad(
    nombre, descripcion, entre_calles, calle, numero,
    huespedes, ambientes, banios, cocheras,
    precioNoche, codigoAcceso, is_habilitada,
    id_pol_reserva, id_tipo, id_ciudad, id_encargado,
    piso=None, depto=None,requiere_documentacion=False
):
    try:
        nueva = Propiedad(
            nombre=nombre,
            descripcion=descripcion,
            entre_calles=entre_calles,
            calle=calle,
            numero=numero,
            piso=piso,
            depto=depto,
            huespedes=huespedes,
            ambientes=ambientes,
            banios=banios,
            cocheras=cocheras,
            precioNoche=precioNoche,
            codigoAcceso=codigoAcceso,
            is_habilitada=is_habilitada,
            id_pol_reserva=id_pol_reserva,
            id_tipo=id_tipo,
            id_ciudad=id_ciudad,
            id_encargado = id_encargado,
            requiere_documentacion=requiere_documentacion
        )
        db.session.add(nueva)
        db.session.commit()
        return nueva
    except Exception as e:
        db.session.rollback()
        raise ()
def chekin_check(checkin:datetime, checkout:datetime):
    """
    Verifica si las fechas de check-in y check-out son válidas.
    El check-in debe ser anterior al check-out.
    """
    checkin = parse_datetime_string(checkin)
    checkout = parse_datetime_string(checkout)
    return checkin < checkout

def get_propiedades_search(checkin:datetime, checkout:datetime,huespedes):
    checkin = parse_datetime_string(checkin)
    checkout = parse_datetime_string(checkout)
    reservas_solapadas = Reserva.query.filter(
        Reserva.id_estado == "1",
        Reserva.fecha_inicio <= checkout,
        Reserva.fecha_fin >= checkin
    ).all()
    
    propiedades_disponibles_ids = [r.id_propiedad for r in reservas_solapadas]
    
    query = Propiedad.query.filter(
        Propiedad.delete_at.is_(None),
        Propiedad.is_habilitada == True,
        Propiedad.huespedes >= huespedes
    )

    if propiedades_disponibles_ids:
        query = query.filter(~Propiedad.id.in_(propiedades_disponibles_ids))

    disponibles = query.all()
    return disponibles
    

def get_propiedades_search_id(id,checkin, checkout,huespedes):
    todas_las_propiedades_disponibles = get_propiedades_search(checkin, checkout, huespedes)
    propiedades_filtradas_por_ciudad = [
        prop for prop in todas_las_propiedades_disponibles
        if prop.id_ciudad == id
    ]
    return propiedades_filtradas_por_ciudad



def toggle_estado(prop_id):
    propiedad = get_propiedad_id(prop_id)
    if not propiedad:
        return None

    propiedad.is_habilitada = not propiedad.is_habilitada
    try:
        db.session.commit()
        return propiedad
    except Exception:
        db.session.rollback()
        raise


def update_propiedad(
    prop_id, nombre, descripcion, entre_calles, calle, numero,
    huespedes, ambientes, banios, cocheras,
    precioNoche, codigoAcceso, is_habilitada,
    id_pol_reserva, id_tipo, id_ciudad, id_encargado,
    requiere_documentacion, piso=None, depto=None
):
    try:
        propiedad = get_propiedad_id(prop_id)

        propiedad.nombre=nombre
        propiedad.descripcion=descripcion
        propiedad.entre_calles=entre_calles
        propiedad.calle=calle
        propiedad.numero=numero
        propiedad.piso=piso
        propiedad.depto=depto
        propiedad.huespedes=huespedes
        propiedad.ambientes=ambientes
        propiedad.banios=banios
        propiedad.cocheras=cocheras
        propiedad.precioNoche=precioNoche
        propiedad.codigoAcceso=codigoAcceso
        propiedad.is_habilitada=is_habilitada
        propiedad.id_pol_reserva=id_pol_reserva
        propiedad.id_tipo=id_tipo
        propiedad.id_ciudad=id_ciudad
        propiedad.id_encargado=id_encargado
        propiedad.requiere_documentacion=requiere_documentacion
        db.session.commit()
        return propiedad
    except Exception as e:
        db.session.rollback()
        raise ()


def update_codigo_acceso(id, codigoAcceso):
    propiedad = get_propiedad_id(id)
    if not propiedad:
        return None

    propiedad.codigoAcceso = codigoAcceso
    try:
        db.session.commit()
        return propiedad
    except Exception:
        db.session.rollback()
        raise


def get_schema_propiedad():
    return PropiedadSchema()


def get_schema_propiedad_protegida():
    return PropiedadProtegidaSchema()


def get_schema_codigo_acceso():
    return CodigoAccesoSchema()
