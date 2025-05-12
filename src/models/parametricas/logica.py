from src.models.database import db
from src.models.parametricas.parametricas import Provincia, Ciudad


def get_provincias():
    provincias = Provincia.query.all()
    return provincias

def get_ciudades_by_provincia_id(id):
    try:
        provincia = Provincia.query.get(id)
        return provincia.ciudades
    except:
        return None
