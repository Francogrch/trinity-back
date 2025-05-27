from flask_jwt_extended import jwt_required
from src.models import parametricas
from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol

from flask import request, Blueprint
from marshmallow import ValidationError

parametricas_blueprint = Blueprint(
    'parametricas', __name__, url_prefix="/parametricas")

from src.models.parametricas.logica import get_paises, create_pais, get_schema_pais

@parametricas_blueprint.get('/provincias')
def get_provincias():
    provincias = parametricas.get_provincias()
    return parametricas.get_schema_provincia().dump(provincias, many=True)


@parametricas_blueprint.get('/ciudades')
def get_ciudades_by_provincia():
    ciudades = parametricas.get_ciudades_by_provincia_id(
        request.args.get('id', type=int))
    return parametricas.get_schema_ciudad().dump(ciudades, many=True)


@parametricas_blueprint.get('/ciudadesConPropiedades')
def get_ciudades_con_propiedades():
    ciudades = parametricas.get_ciudades_con_propiedades()
    if not ciudades:
        return {"error": "No se encontraron ciudades con propiedades."}, 404
    return parametricas.get_schema_ciudad().dump(ciudades, many=True)


@parametricas_blueprint.get('/tipos')
def get_tipos_propiedad():
    tipos = parametricas.get_tipos_propiedad()
    return parametricas.get_schema_tipo_propiedad().dump(tipos, many=True)

# Sin uso

@parametricas_blueprint.post('/tipos')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
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


@parametricas_blueprint.get('/tipos-identificacion')
def get_tipos_identificacion():
    from src.models.parametricas.logica import get_tipos_identificacion, get_schema_tipo_identificacion
    tipos = get_tipos_identificacion()
    return get_schema_tipo_identificacion().dump(tipos, many=True)

@parametricas_blueprint.get('/paises')
def get_paises_route():
    paises = get_paises()
    return get_schema_pais().dump(paises, many=True)

@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
@parametricas_blueprint.post('/paises')
def create_pais_route():
    data = request.get_json()
    try:
        pais = create_pais(data['nombre'])
        return get_schema_pais().dump(pais), 201
    except Exception as e:
        return {"error": str(e)}, 400

@parametricas_blueprint.get('/marcas-tarjeta')
def get_marcas_tarjeta():
    from src.models.users.user import MarcaTarjeta, MarcaTarjetaSchema
    marcas = MarcaTarjeta.query.all()
    return MarcaTarjetaSchema(many=True).dump(marcas)

@parametricas_blueprint.get('/tipos-tarjeta')
def get_tipos_tarjeta():
    from src.models.users.user import TipoTarjeta, TipoTarjetaSchema
    tipos = TipoTarjeta.query.all()
    return TipoTarjetaSchema(many=True).dump(tipos)