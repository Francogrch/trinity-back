from flask import request, jsonify
from app import db
from app.models import Usuario
from app import create_app

from flask import current_app as app
from flask import Blueprint

routes_bp = Blueprint('routes', __name__)
@routes_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'rol': u.rol} for u in usuarios])

@routes_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    nuevo = Usuario(nombre=data['nombre'], rol=data['rol'])
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado'}), 201

