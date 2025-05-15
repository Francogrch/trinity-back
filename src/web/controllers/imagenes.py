from src.models.imagenes.imagen import ImagenSchema, Imagen
from flask import Blueprint, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from src.models import imagenes

imagen_blueprint = Blueprint('imagenes', __name__, url_prefix="/imagenes")


@imagen_blueprint.post('/')
def upload_image():
    if 'image' not in request.files:
        return {'error': 'No hay imagen'}, 400

    file = request.files['image']
    if file.filename == '':
        return {'error': 'No se selecciono un archivo'}, 400

    if file and imagenes.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # Guardar la URL en la base de datos
        imagen = imagenes.create_imagen(url=f"/imagenes/uploads/{filename}")
        return imagenes.get_schema_imagen().dump(imagen), 201

    return {'error': 'Tipo invalido de archivo'}, 400


@imagen_blueprint.get('/')
def get_imagenes():
    imgs = imagenes.get_imagenes()
    return imagenes.get_schema_imagen().dump(imgs, many=True)


@imagen_blueprint.get('/<filename>')
def get_uploaded_file(filename):
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(upload_folder, filename)


@imagen_blueprint.get('/id/<int:imagen_id>')
def get_uploaded_file_by_id(imagen_id):
    imagen = imagenes.get_imagen_id(imagen_id)
    if not imagen:
        return {'error': 'Imagen no encontrada'}, 404

    filename = os.path.basename(imagen.url)
    base_dir = os.path.abspath(os.path.join(current_app.root_path, '..', '..'))
    upload_folder = os.path.join(base_dir, current_app.config['UPLOAD_FOLDER'])
    upload_folder = os.path.abspath(upload_folder)

    return send_from_directory(upload_folder, filename)
