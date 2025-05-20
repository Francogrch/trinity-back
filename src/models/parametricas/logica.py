from src.models.database import db
from src.models.parametricas.parametricas import Provincia, Ciudad, PropiedadTipo, PoliticaReserva
from src.models.parametricas.parametricas import ProvinciaSchema, CiudadSchema, PropiedadTipoSchema, PoliticaReservaSchema
from src.models.users.user import Rol, RolSchema


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


def get_roles():
    roles = Rol.query.all()
    return roles


def create_rol(nombre):
    try:
        rol = Rol()
        rol.nombre = nombre
        db.session.add(rol)
        db.session.commit()
        return rol
    except:
        db.session.rollback()
        raise


def create_tipos_propiedad(tipo):
    try:
        tipo_propiedad = PropiedadTipo(tipo)
        db.session.add(tipo_propiedad)
        db.session.commit()
        return tipo_propiedad
    except:
        db.session.rollback()
        raise ()


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


def get_schema_provincia():
    return ProvinciaSchema()


def get_schema_ciudad():
    return CiudadSchema()


def get_schema_tipo_propiedad():
    return PropiedadTipoSchema()


def get_schema_pol_reserva():
    return PoliticaReservaSchema()


def get_schema_rol():
    return RolSchema()


def get_tipos_identificacion():
    from src.models.parametricas.parametricas import TipoIdentificacion
    return TipoIdentificacion.query.all()


def get_schema_tipo_identificacion():
    from src.models.parametricas.parametricas import TipoIdentificacionSchema
    return TipoIdentificacionSchema()


def create_tipo_identificacion(nombre):
    from src.models.parametricas.parametricas import TipoIdentificacion
    try:
        tipo = TipoIdentificacion(nombre)
        db.session.add(tipo)
        db.session.commit()
        return tipo
    except:
        db.session.rollback()
        raise
