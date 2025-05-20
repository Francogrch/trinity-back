from src.models import reservas

from flask import request, Blueprint
from marshmallow import ValidationError

reserva_blueprint = Blueprint('reservas', __name__, url_prefix="/reservas")


@reserva_blueprint.get('/<int:propiedad_id>')
def get_reservas_propiedad(propiedad_id):
    try:
        res = reservas.get_reservas_por_propiedad(propiedad_id)
        return reservas.get_schema_reserva().dump(res, many=True), 200
    except:
        return {'error': 'Error al obtener las reservas'}, 500


@reserva_blueprint.post('/')
def create_reserva():
    data = request.get_json()
    try:
        data_reserva = reservas.get_schema_reserva().load(data)
        reserva = reservas.create_reserva(**data_reserva)
        return reservas.get_schema_reserva().dump(reserva), 201
    except ValidationError as err:
        return err.messages, 422
    except:
        return {'error': 'Error al crear la reserva'}, 400


@reserva_blueprint.patch('/cambiarEstado/<int:reserva_id>')
def cambiar_estado_reserva(reserva_id):
    try:
        data = request.get_json()
        nuevo_estado = data.get("nuevo_id_estado")
        if nuevo_estado is None:
            return {'error': 'Falta el nuevo_id_estado en el body'}, 400
        reserva = reservas.cambiar_estado_reserva(reserva_id, nuevo_estado)
    except:
        return {'error': 'Error al cambiar el estado de la reserva'}, 500

    if not reserva:
        return {'error': 'Reserva no encontrada'}, 404

    return reservas.get_schema_reserva().dump(reserva), 200
