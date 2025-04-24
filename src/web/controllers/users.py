from flask import request, jsonify
from src.models import users

from flask import Blueprint

user_blueprint = Blueprint('users', __name__, url_prefix="/usuarios")

@user_blueprint.get('/')
def get_usuarios():
    usuarios = users.get_usuarios()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'rol': u.rol} for u in usuarios])

@user_blueprint.post('/')
def create_usuario():
    data = request.get_json()
    nuevo = users.create_usuario(nombre=data['nombre'], rol=data['rol'])
    return jsonify({'mensaje': 'Usuario creado'}), 201


