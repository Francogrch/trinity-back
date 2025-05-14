from src.models.database import db
from src.models.parametricas.parametricas import Provincia, Ciudad, PropiedadTipo, PoliticaReserva


def get_provincias():
    provincias = Provincia.query.all()
    return provincias

def get_ciudades_by_provincia_id(id):
    try:
        provincia = Provincia.query.get(id)
        return provincia.ciudades
    except:
        return None

def get_tipos_propiedad():
    tipos = PropiedadTipo.query.all()
    return tipos

def create_tipos_propiedad(tipo):
    try:
        tipo_propiedad = PropiedadTipo(tipo)
        db.session.add(tipo_propiedad)
        db.session.commit()
        return tipo_propiedad
    except:
        db.session.rollback()
        return None

def get_pol_reserva():
    pol_reserva = PoliticaReserva.query.all()
    return pol_reserva

def create_pol_reserva(label, porcentaje):
    try:
        nuevo = PoliticaReserva(label, porcentaje)
        db.session.add(nuevo)
        db.session.commit()
        return nuevo
    except:
        db.session.rollback()
        return None
