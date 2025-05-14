from src.models.database import db
from src.models.propiedades.propiedad import Propiedad


def get_propiedades():
    propiedades = Propiedad.query.all()
    return propiedades


def create_propiedad(
    nombre, descripcion, entre_calles, calle, numero,
    piso, depto, id_ciudad, huespedes, ambientes,
    banios, cocheras, id_pol_reserva, precioNoche, id_tipo
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
            id_ciudad=id_ciudad,
            huespedes=huespedes,
            ambientes=ambientes,
            banios=banios,
            cocheras=cocheras,
            id_pol_reserva=id_pol_reserva,
            precioNoche=precioNoche,
            id_tipo=id_tipo
        )
        db.session.add(nueva)
        db.session.commit()
        return nueva
    except:
        db.session.rollback()
        return None
