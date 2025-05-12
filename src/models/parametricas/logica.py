from src.models.database import db
from src.models.parametricas.parametricas import Provincia, Ciudad, PropiedadTipos


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
    tipos = PropiedadTipos.query.all()
    return tipos

def create_tipos_propiedad(tipo):
    try:
        tipo_propiedad = PropiedadTipos(tipo)
        db.session.add(tipo_propiedad)
        db.session.commit()
        return tipo_propiedad
    except:
        db.session.rollback()
        return None
