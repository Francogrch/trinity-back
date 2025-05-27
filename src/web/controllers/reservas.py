from flask import request, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity  # Importa funciones para manejo de JWT (autenticación y claims)

from src.models import reservas
from src.models import users
from src.models import email

from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol

reserva_blueprint = Blueprint('reservas', __name__, url_prefix="/reservas")


@reserva_blueprint.get('/')
@jwt_required()
def get_reservas_usuario():
    usuario = users.get_usuario_by_id(get_jwt_identity())
    try:
        res = reservas.get_reservas_por_usuario(usuario)
        return reservas.get_schema_reserva().dump(res, many=True), 200
    except:
        return {'error': 'Error al obtener las reservas'}, 500


@reserva_blueprint.get('/<int:reserva_id>')
@jwt_required()
def get_reserva(reserva_id):
    usuario = users.get_usuario_by_id(get_jwt_identity())
    try:
        res = reservas.get_reserva(reserva_id, usuario)
    except:
        return {'error': 'Error al obtener las reservas'}, 500
    if not res:
        return {'error': 'Reserva no encontrada'}, 404
    return reservas.get_schema_reserva().dump(res), 200


@reserva_blueprint.get('/propiedad/<int:propiedad_id>')
@jwt_required()
def get_reservas_propiedad(propiedad_id):
    try:
        res = reservas.get_reservas_por_propiedad(propiedad_id)
        return reservas.get_schema_reserva().dump(res, many=True), 200
    except:
        return {'error': 'Error al obtener las reservas'}, 500


@reserva_blueprint.post('/')
@jwt_required()
def create_reserva():
    data = request.get_json()
    if "id_inquilino" not in data or data['id_inquilino'] == None:
        data['id_inquilino'] = get_jwt_identity()
    else:
        data['id_usuario_carga'] = get_jwt_identity()
    try:
        data_reserva = reservas.get_schema_reserva().load(data)
        if reservas.hay_reservas_solapadas(
                data_reserva['id_propiedad'], data_reserva['fecha_inicio'], data_reserva['fecha_fin']
                ):
            return {'error': 'Propiedad no disponible'}, 400
        reserva = reservas.create_reserva(data_reserva)
        # Notificaciones por email
        email.send_reserva_creada_inquilino(reserva)
        email.send_reserva_creada_encargado(reserva)
        return reservas.get_schema_reserva().dump(reserva), 201
    except ValidationError as err:
        return err.messages, 422
    except:
        return {'error': 'Error al crear la reserva'}, 400


@reserva_blueprint.patch('/cancelar/<int:reserva_id>')
@jwt_required()
def cancel_reserva(reserva_id):
    usuario = users.get_usuario_by_id(get_jwt_identity())
    try:
        res = reservas.cancel_reserva(reserva_id, usuario)
    except:
        return {'error': 'Error al obtener las reservas'}, 500
    if not res:
        return {'error': 'Reserva no encontrada'}, 404
    email.send_reserva_cancelada(res, usuario)
    return reservas.get_schema_reserva().dump(res), 200


@reserva_blueprint.patch('/cambiarEstado/<int:reserva_id>')
@jwt_required()
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
