from src.models import propiedades

from flask import request, Blueprint
from marshmallow import ValidationError

propiedad_blueprint = Blueprint(
    'propiedades', __name__, url_prefix="/propiedades")


@propiedad_blueprint.get('/')
def get_propiedades():
    props = propiedades.get_propiedades()
    return propiedades.get_schema_propiedad().dump(props, many=True)


@propiedad_blueprint.get('/id/<int:prop_id>')
def get_propiedad_id(prop_id):
    propiedad = propiedades.get_propiedad_id(prop_id)
    return (propiedades.get_schema_propiedad().dump(propiedad), 201)


@propiedad_blueprint.post('/')
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
