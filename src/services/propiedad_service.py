"""
Servicio de propiedades: lógica de negocio y operaciones sobre propiedades.
"""
from src.models.propiedades.propiedad import Propiedad
from src.models.database import db

def obtener_todas_las_propiedades():
    """Devuelve la lista de todas las propiedades."""
    return Propiedad.query.all()

def crear_propiedad(nombre, descripcion, entre_calles, calle, numero, piso, depto, id_ciudad, huespedes, ambientes, banios, cocheras, id_pol_reserva, precioNoche):
    """Crea una nueva propiedad con los datos recibidos."""
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
            precioNoche=precioNoche
        )
        db.session.add(nueva)
        db.session.commit()
        return nueva
    except Exception as e:
        db.session.rollback()
        return None
# Puedes agregar aquí más funciones de negocio relacionadas a propiedades
