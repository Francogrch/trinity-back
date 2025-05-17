from flask import request
from src.models import users

from flask import Blueprint
from marshmallow import ValidationError

user_blueprint = Blueprint('users', __name__, url_prefix="/usuarios")


@user_blueprint.get('/')
def get_usuarios():
    usuarios = users.get_usuarios()
    return users.get_schema_usuario().dumps(usuarios, many=True)


@user_blueprint.post('/')
def create_usuario():
    data = request.get_json()
    try:
        data_usuario = users.get_schema_usuario().load(data)    # Valida JSON del request
        # Valida que sea unico en DB
        usuario = users.create_usuario(**data_usuario)
        return (users.get_schema_usuario().dumps(usuario), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Usuario repetido?"}, 400)
