import os
from src.models.imagenes.logica import delete_image, get_filename, get_schema_imagen, upload_image
from src.models import propiedades
from src.models import users
from flask import current_app, request, Blueprint, send_from_directory
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # Importa funciones para manejo de JWT (autenticación y claims)
from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol

propiedad_blueprint = Blueprint(
    'propiedades', __name__, url_prefix="/propiedades")


@propiedad_blueprint.get('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden acceder
def get_propiedades():
    usuario = users.get_usuario_by_id(get_jwt_identity())
    props = propiedades.get_propiedades_usuario(usuario)
    return propiedades.get_schema_propiedad().dump(props, many=True)


@propiedad_blueprint.get('/eliminadas')
@jwt_required()
def get_propiedades_eliminadas():
    props = propiedades.get_propiedades_eliminadas()
    return propiedades.get_schema_propiedad().dump(props, many=True)


@propiedad_blueprint.get('/id/<int:prop_id>')
#@jwt_required()
def get_propiedad_id_route(prop_id):
    propiedad = propiedades.get_propiedad_id(prop_id)
    return (propiedades.get_schema_propiedad().dump(propiedad), 201)


@propiedad_blueprint.post('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden crear propiedades
def create_propiedad():
    data = request.get_json()
    if "id_encargado" not in data or data['id_encargado'] == None:
        data['id_encargado'] = get_jwt_identity()
    try:
        data_propiedad = propiedades.get_schema_propiedad().load(data)
        propiedad = propiedades.create_propiedad(**data_propiedad)
        return (propiedades.get_schema_propiedad().dump(propiedad), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Propiedad repetida?"}, 400)


@propiedad_blueprint.patch('/cambiarEstado/<int:prop_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def cambiar_estado_propiedad(prop_id):
    try:
        propiedad = propiedades.toggle_estado(prop_id)
    except:
        return {'error': 'Error al actualizar la propiedad'}, 500

    if not propiedad:
        return {'error': 'Propiedad no encontrada'}, 404

    return propiedades.get_schema_propiedad().dump(propiedad), 200


# Esta logica es de testeo
@propiedad_blueprint.patch('/eliminar/<int:prop_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def eliminar_propiedad(prop_id):
    try:
        propiedad = propiedades.eliminar_prop_hasta_fecha(prop_id)
    except:
        return {'error': 'Error al actualizar la propiedad'}, 500

    if not propiedad:
        return {'error': 'Propiedad no encontrada'}, 404

    return propiedades.get_schema_propiedad().dump(propiedad), 200

@propiedad_blueprint.patch('/eliminarConReservas/<int:prop_id>')
#@jwt_required()
#@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def eliminar_propiedad_reservas(prop_id):
    try:
        propiedad = propiedades.eliminar_prop_con_reservas(prop_id)
    except:
        return {'error': 'Error al actualizar la propiedad'}, 500

    if not propiedad:
        return {'error': 'Propiedad no encontrada'}, 404

    return propiedades.get_schema_propiedad().dump(propiedad), 200


@propiedad_blueprint.patch('/editar')
def update_propiedad():
    data = request.get_json()
    prop_id = data['id']
    try:
        data_propiedad = propiedades.get_schema_propiedad().load(data)
        propiedad = propiedades.update_propiedad(prop_id, **data_propiedad)
        return (propiedades.get_schema_propiedad().dump(propiedad), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Propiedad repetida?"}, 400)


@propiedad_blueprint.patch('/editarCodigo')
def update_codigo_acceso():
    data = request.get_json()
    try:
        data_propiedad = propiedades.get_schema_codigo_acceso().load(data)
        propiedad = propiedades.update_codigo_acceso(**data_propiedad)
        if propiedad:
            return (propiedades.get_schema_propiedad().dump(propiedad), 201)
        return {'error': 'Propiedad no encontrada'}, 404
    except ValidationError as err:
        return (err.messages, 422)
    except:
        return ({"error": "Propiedad repetida?"}, 400)
    

@propiedad_blueprint.get('/search')
#@jwt_required()
def get_propiedades_search():
    id = request.args.get('id', default=None, type=int)
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    huespedes = request.args.get('huespedes', type=int)
    
    if id:
        props = propiedades.get_propiedades_search_id(id,checkin, checkout,huespedes)
    else:
        props = propiedades.get_propiedades_search(checkin, checkout,huespedes)

    if not props or len(props) == 0:
        return {'error': 'No se encontraron propiedades'}, 204

    return propiedades.get_schema_propiedad().dump(props, many=True)


@propiedad_blueprint.get('/imagen/<int:imagen_id>')
def get_imagen(imagen_id):
    # Ruta absoluta a la carpeta de imágenes de usuarios
    base_upload_directory = os.path.abspath(
        os.path.join(current_app.root_path, "..", "..", "imagenes", "propiedad")
    )

    filename = get_filename(imagen_id)

    return send_from_directory(
        directory=base_upload_directory,
        path=filename,
        as_attachment=False
    )

@propiedad_blueprint.get('/imagenes')
def get_imagenes_id():
    id_propiedad = request.args.get('id_propiedad')
    if not id_propiedad:
        return {'error': 'ID de propiedad es requerido.'}, 400
    
    try:
        id_propiedad = int(id_propiedad)
    except ValueError:
        return {'error': 'ID de propiedad inválido.'}, 400

    propiedad = propiedades.get_propiedad_id(id_propiedad)
    if not propiedad:
        return {'error': 'Propiedad no encontrada.'}, 404

    imagenes_de_propiedad = propiedad.imagenes
    return [imagen.id for imagen in imagenes_de_propiedad], 200



@propiedad_blueprint.post('/imagen')
#@jwt_required()
def upload_imagen():
    id_propiedad = request.args.get('id_propiedad')
    image = upload_image('propiedad',request,id_propiedad=id_propiedad)
    return image

@propiedad_blueprint.delete('/deleteImagen')
#@jwt_required() 
def delete_imagen():
    id_imagen = request.args.get('id_imagen')

    success, message = delete_image(id_imagen, 'propiedad')

    if success:
        return {"message": message if message else f"Imagen con ID {id_imagen} eliminada exitosamente"}, 200
    else:
        return {"message": message}, 500

@propiedad_blueprint.patch('/setEncargado')
def update_encargado():
    id_propiedad = request.args.get('id_propiedad')
    id_encargado = request.args.get('id_encargado')
    try:
        propiedad = propiedades.update_encargado(id_propiedad,id_encargado)
        if propiedad:
            return (propiedades.get_schema_propiedad().dump(propiedad), 201)
        return {'error': 'Propiedad no encontrada'}, 404
    except ValidationError as err:
        return (err.messages, 422)
 

@propiedad_blueprint.get('/imagenPerfil/<int:id_propiedad>')
def get_imagen_perfil(id_propiedad):
    propiedad = propiedades.get_propiedad_id(id_propiedad)

    if not propiedad:
        return {'error': 'Propiedad no encontrada.'}, 404
    
    imagen = propiedad.imagenes[0] if propiedad.imagenes else None
    if not imagen:
        return {'error': 'No hay imagenes para esta propiedad.'}, 404

    return get_imagen(imagen.id)

