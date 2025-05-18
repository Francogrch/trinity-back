from src.models import propiedades
from flask import request, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # Importa funciones para manejo de JWT (autenticación y claims)
from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol

propiedad_blueprint = Blueprint(
    'propiedades', __name__, url_prefix="/propiedades")


@propiedad_blueprint.get('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden acceder
def get_propiedades():
    props = propiedades.get_propiedades()
    return propiedades.get_schema_propiedad().dump(props, many=True)


@propiedad_blueprint.get('/eliminadas')
def get_propiedades_eliminadas():
    props = propiedades.get_propiedades_eliminadas()
    return propiedades.get_schema_propiedad().dump(props, many=True)


@propiedad_blueprint.get('/id/<int:prop_id>')
def get_propiedad_id_route(prop_id):
    propiedad = propiedades.get_propiedad_id(prop_id)
    return (propiedades.get_schema_propiedad().dump(propiedad), 201)


@propiedad_blueprint.post('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden crear propiedades
def create_propiedad():
    data = request.get_json()
    try:
        data_propiedad = propiedades.get_schema_propiedad().load(data)
        propiedad = propiedades.create_propiedad(**data_propiedad)
        return (propiedades.get_schema_propiedad().dump(propiedad), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Propiedad repetida?"}, 400)


@propiedad_blueprint.patch('/cambiarEstado/<int:prop_id>')
def cambiar_estado_propiedad(prop_id):
    try:
        propiedad = propiedades.toggle_estado(prop_id)
    except:
        return {'error': 'Error al actualizar la propiedad'}, 500

    if not propiedad:
        return {'error': 'Propiedad no encontrada'}, 404

    return propiedades.get_schema_propiedad().dump(propiedad), 200


# Esta logica es de testeo
@propiedad_blueprint.patch('/eliminar/<int:prop_id>')
def eliminar_propiedad(prop_id):
    try:
        propiedad = propiedades.eliminar_prop(prop_id)
    except:
        return {'error': 'Error al actualizar la propiedad'}, 500

    if not propiedad:
        return {'error': 'Propiedad no encontrada'}, 404

    return propiedades.get_schema_propiedad().dump(propiedad), 200
