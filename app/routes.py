from flask import Blueprint, request, jsonify
from app import db
from app.models import (
    Usuario, Tarjeta, Reserva, Propiedad, PoliticaCancelacion,
    PoliticaReserva, CalificacionUser, CalificacionProp,
    Chat, Mensaje, ImagenPropiedad
)
from datetime import datetime

routes_bp = Blueprint('routes', __name__)

# --- USUARIOS ---


@routes_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


@routes_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    usuario = Usuario(**data)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado', 'id': usuario.id}), 201

# --- PROPIEDADES ---


@routes_bp.route('/propiedades', methods=['GET'])
def get_propiedades():
    propiedades = Propiedad.query.all()
    return jsonify([p.to_dict() for p in propiedades])


@routes_bp.route('/propiedades', methods=['POST'])
def create_propiedad():
    data = request.get_json()
    propiedad = Propiedad(**data)
    db.session.add(propiedad)
    db.session.commit()
    return jsonify({'mensaje': 'Propiedad creada', 'id': propiedad.id}), 201

# --- RESERVAS ---


@routes_bp.route('/reservas', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    return jsonify([r.to_dict() for r in reservas])


@routes_bp.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()
    reserva = Reserva(**data)
    db.session.add(reserva)
    db.session.commit()
    return jsonify({'mensaje': 'Reserva creada', 'id': reserva.id}), 201

# --- CALIFICACIONES USUARIO ---


@routes_bp.route('/calificaciones/usuario', methods=['GET'])
def get_calificaciones_usuario():
    calificaciones = CalificacionUser.query.all()
    return jsonify([c.to_dict() for c in calificaciones])


@routes_bp.route('/calificaciones/usuario', methods=['POST'])
def create_calificacion_usuario():
    data = request.get_json()
    calificacion = CalificacionUser(**data)
    db.session.add(calificacion)
    db.session.commit()
    return jsonify({'mensaje': 'Calificación creada', 'id': calificacion.id}), 201

# --- CALIFICACIONES PROPIEDAD ---


@routes_bp.route('/calificaciones/propiedad', methods=['GET'])
def get_calificaciones_prop():
    calificaciones = CalificacionProp.query.all()
    return jsonify([c.to_dict() for c in calificaciones])


@routes_bp.route('/calificaciones/propiedad', methods=['POST'])
def create_calificacion_prop():
    data = request.get_json()
    calificacion = CalificacionProp(**data)
    db.session.add(calificacion)
    db.session.commit()
    return jsonify({'mensaje': 'Calificación creada', 'id': calificacion.id}), 201

# --- CHATS ---


@routes_bp.route('/chats', methods=['GET'])
def get_chats():
    chats = Chat.query.all()
    return jsonify([c.to_dict() for c in chats])


@routes_bp.route('/chats', methods=['POST'])
def create_chat():
    data = request.get_json()
    chat = Chat(**data)
    db.session.add(chat)
    db.session.commit()
    return jsonify({'mensaje': 'Chat creado', 'id': chat.id}), 201

# --- MENSAJES ---


@routes_bp.route('/mensajes', methods=['GET'])
def get_mensajes():
    mensajes = Mensaje.query.all()
    return jsonify([m.to_dict() for m in mensajes])


@routes_bp.route('/mensajes', methods=['POST'])
def create_mensaje():
    data = request.get_json()
    mensaje = Mensaje(**data)
    db.session.add(mensaje)
    db.session.commit()
    return jsonify({'mensaje': 'Mensaje creado', 'id': mensaje.id}), 201

# --- IMAGENES PROPIEDAD ---


@routes_bp.route('/imagenes', methods=['GET'])
def get_imagenes():
    imagenes = ImagenPropiedad.query.all()
    return jsonify([i.to_dict() for i in imagenes])


@routes_bp.route('/imagenes', methods=['POST'])
def create_imagen():
    data = request.get_json()
    imagen = ImagenPropiedad(**data)
    db.session.add(imagen)
    db.session.commit()
    return jsonify({'mensaje': 'Imagen agregada', 'id': imagen.id}), 201
