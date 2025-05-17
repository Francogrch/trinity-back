from src.models.database import db
from src.models.propiedades.propiedad import Propiedad, PropiedadSchema
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
    id_pol_reserva, id_tipo, id_ciudad, piso=None, depto=None
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
        )
        db.session.add(nueva)
        db.session.commit()
        return nueva
    except Exception as e:
        db.session.rollback()
        raise ()


def get_schema_propiedad():
    return PropiedadSchema()


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
