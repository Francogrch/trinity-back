from src.models.database import db
from src.models.propiedades.propiedad import Propiedad, PropiedadSchema


def get_propiedades():
    propiedades = Propiedad.query.all()
    return propiedades


def create_propiedad(
    nombre, descripcion, entre_calles, calle, numero,
    piso, depto, huespedes, ambientes, banios, cocheras,
    precioNoche, codigoAcceso, is_habilitada, id_pol_reserva,
    id_tipo, id_ciudad
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
    except:
        db.session.rollback()
        raise()

def get_schema_propiedad():
    return PropiedadSchema()
