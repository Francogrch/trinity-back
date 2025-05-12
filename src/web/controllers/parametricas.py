from flask import request, jsonify, Blueprint
from src.models import parametricas

parametricas_blueprint = Blueprint(
    'parametricas', __name__, url_prefix="/parametricas")


@parametricas_blueprint.get('/provincias')
def get_provincias():
    provincias = parametricas.get_provincias()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre
    } for p in provincias])


@parametricas_blueprint.get('/ciudades')
def get_ciudades_by_provincia():
    ciudades = parametricas.get_ciudades_by_provincia_id(request.args.get('id', type=int))
    if ciudades:
        return jsonify([{
        'id': c.id,
        'nombre': c.nombre
        } for c in ciudades])
    else:
        return jsonify({'error': 'No hay ciudades'}), 400

