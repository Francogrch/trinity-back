from flask import request, jsonify, Blueprint
from src.models import propiedades

propiedad_blueprint = Blueprint(
    'propiedades', __name__, url_prefix="/propiedades")


@propiedad_blueprint.get('/')
def get_propiedades():
    props = propiedades.get_propiedades()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'descripcion': p.descripcion,
        'entre_calles': p.entre_calles,
        'calle': p.calle,
        'numero': p.numero,
        'piso': p.piso,
        'depto': p.depto,
        'id_ciudad': p.id_ciudad,
        'huespedes': p.huespedes,
        'ambientes': p.ambientes,
        'banios': p.banios,
        'cocheras': p.cocheras,
        'id_pol_reserva': p.id_pol_reserva,
        'precioNoche': p.precioNoche,
        'created_at': p.created_at.isoformat(),
        'updated_at': p.updated_at.isoformat()
    } for p in props])


@propiedad_blueprint.post('/')
def create_propiedad():
    data = request.get_json()
    nueva = propiedades.create_propiedad(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        entre_calles=data['entre_calles'],
        calle=data['calle'],
        numero=data['numero'],
        piso=data['piso'],
        depto=data['depto'],
        id_ciudad=data['id_ciudad'],
        huespedes=data['huespedes'],
        ambientes=data['ambientes'],
        banios=data['banios'],
        cocheras=data['cocheras'],
        id_pol_reserva=data['id_pol_reserva'],
        precioNoche=data['precioNoche']
    )
    if nueva:
        return jsonify({'mensaje': 'Propiedad creada'}), 201
    else:
        return jsonify({'error': 'Error al crear la propiedad'}), 400
