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


@parametricas_blueprint.get('/tipos')
def get_tipos_propiedad():
    tipos = parametricas.get_tipos_propiedad()
    if tipos:
        return jsonify([{
        'id': t.id,
        'tipo': t.tipo
        } for t in tipos])
    else:
        return jsonify({'error': 'No hay tipos de propiedad definidos'}), 400


@parametricas_blueprint.post('/tipos')
def create_tipos_propiedad():
    data = request.get_json()
    tipo = parametricas.create_tipos_propiedad(tipo=data['tipo'])
    if tipo:
        return jsonify({'mensaje': 'Tipo creado'}), 201
    else:
        return jsonify({'error': 'Error al crear el tipo'}), 400


@parametricas_blueprint.get('/politicas')
def get_pol_reserva():
    pol_reserva = parametricas.get_pol_reserva()
    return jsonify([{
        'id': p.id,
        'label': p.label,
        'porcentaje': p.porcentaje
    } for p in pol_reserva])
