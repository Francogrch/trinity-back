from src.models import parametricas

from flask import request, Blueprint
from marshmallow import ValidationError

parametricas_blueprint = Blueprint(
    'parametricas', __name__, url_prefix="/parametricas")


@parametricas_blueprint.get('/provincias')
def get_provincias():
    provincias = parametricas.get_provincias()
    return parametricas.get_schema_provincia().dump(provincias, many=True)


@parametricas_blueprint.get('/ciudades')
def get_ciudades_by_provincia():
    ciudades = parametricas.get_ciudades_by_provincia_id(
        request.args.get('id', type=int))
    return parametricas.get_schema_ciudad().dump(ciudades, many=True)


@parametricas_blueprint.get('/tipos')
def get_tipos_propiedad():
    tipos = parametricas.get_tipos_propiedad()
    return parametricas.get_schema_tipo_propiedad().dump(tipos, many=True)


@parametricas_blueprint.post('/tipos')
def create_tipos_propiedad():
    data = request.get_json()
    try:
        data_tipo = parametricas.get_schema_tipo_propiedad().load(data)
        tipo = parametricas.create_tipos_propiedad(**data_tipo)
        return (parametricas.get_schema_tipo_propiedad().dump(tipo), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Tipo repetido?"}, 400)


@parametricas_blueprint.get('/politicas')
def get_pol_reserva():
    pol_reserva = parametricas.get_pol_reserva()
    return parametricas.get_schema_pol_reserva().dump(pol_reserva, many=True)


@parametricas_blueprint.get('/roles')
def get_roles():
    return parametricas.get_schema_rol().dump(parametricas.get_roles(), many=True)
