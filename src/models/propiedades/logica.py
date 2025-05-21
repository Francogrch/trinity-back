from src.models.database import db
from src.models.propiedades.propiedad import Propiedad, PropiedadSchema, CodigoAccesoSchema
from src.models.reservas.reserva import Reserva 
from datetime import datetime


def get_propiedades():
    propiedades = Propiedad.query.filter_by(delete_at=None).all()
    return propiedades


def get_propiedades_eliminadas():
    propiedades = Propiedad.query.filter(Propiedad.delete_at.isnot(None)).all()
    return propiedades


def get_propiedad_id(id):
    return Propiedad.query.get(id)


def eliminar_prop(prop_id):
    propiedad = get_propiedad_id(prop_id)
    if not propiedad:
        return None

    propiedad.delete_at = datetime.now()
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
    id_pol_reserva, id_tipo, id_ciudad, piso=None, depto=None,requiere_documentacion=False
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
            requiere_documentacion=requiere_documentacion
        )
        db.session.add(nueva)
        db.session.commit()
        return nueva
    except Exception as e:
        db.session.rollback()
        raise ()

#! Acomodar id_estado
def get_propiedades_search(checkin:datetime, checkout:datetime,huespedes):
    reservas_solapadas = Reserva.query.filter(
        Reserva.id_estado.is_(None),
        Reserva.fecha_inicio <= checkout,
        Reserva.fecha_fin >= checkin
    ).all()

    propiedades_reservadas_ids = [r.id_propiedad for r in reservas_solapadas]

    query = Propiedad.query.filter(
        Propiedad.delete_at.is_(None),
        Propiedad.is_habilitada == True,
        Propiedad.huespedes >= huespedes
    )

    if propiedades_reservadas_ids:
        query = query.filter(~Propiedad.id.in_(propiedades_reservadas_ids))

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
    id_pol_reserva, id_tipo, id_ciudad, requiere_documentacion, piso=None, depto=None
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


def get_schema_codigo_acceso():
    return CodigoAccesoSchema()
