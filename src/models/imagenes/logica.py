# Aca hay que hacer refactoring de src.web.controllers.imagenes.py
from .imagen import ImagenSchema,Imagen
from src.models.database import db
from flask import Blueprint, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from src.web.authorization.roles import rol_requerido
from src.enums.roles import Rol
from flask import Flask


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_schema_imagen():
    return ImagenSchema()

def get_imagenes():
    return Imagen.query.all()

def get_imagen_id(id):
    return Imagen.query.get(id)

def create_imagen(url=None,id_usuario=None, id_propiedad=None):
    imagen = Imagen(url=url,id_usuario=id_usuario, id_propiedad=id_propiedad)
    db.session.add(imagen)
    db.session.commit()
    return imagen

def set_url(imagen,url):
    imagen.url = url
    db.session.commit()
    return imagen

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image(tipo_imagen,request,id_usuario=None, id_propiedad=None):
    upload_folder = current_app.config.get('UPLOAD_FOLDER', f"imagenes/{tipo_imagen}")

    if 'image' not in request.files:
        return {'error': 'No hay imagen'}, 400

    file = request.files['image']
    if file.filename == '':
        return {'error': 'No se selecciono un archivo'}, 400

    if file and allowed_file(file.filename):
        if id_usuario:
            imagen = create_imagen(id_usuario=id_usuario)
        if id_propiedad:
            imagen = create_imagen(id_propiedad=id_propiedad)

        print(f"Imagen creada: {imagen.id}")

        original_filename_secure = secure_filename(file.filename)

        file_extension = os.path.splitext(original_filename_secure)[1]
       
        new_filename = f"{imagen.id}{file_extension}"
        filepath = os.path.join(upload_folder, new_filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        file.save(filepath)

        image_url = f"/imagenes/{tipo_imagen}/{new_filename}"
        imagen = set_url(imagen,image_url)
        db.session.commit()

        return get_schema_imagen().dump(imagen), 201

    return {'error': 'Tipo invalido de archivo'}, 400


def delete_image(imagen_id,tipo_imagen):
    image_to_delete = Imagen.query.get(imagen_id)

    if not image_to_delete:
        return False, "Imagen no encontrada en la base de datos."

    file_to_delete_name = os.path.basename(image_to_delete.url)
        
    upload_folder_base = os.path.abspath(
            os.path.join(current_app.root_path, "..", "..", "imagenes", f"{tipo_imagen}") # Asumo 'usuario' como tipo aquí
        )
    file_path = os.path.join(upload_folder_base, file_to_delete_name)

    try:
        # Eliminar el registro de la base de datos
        db.session.delete(image_to_delete)
        db.session.commit()
        # Eliminar el archivo físico del sistema de archivos
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo eliminado: {file_path}")
        else:
            print(f"Advertencia: El archivo {file_path} no existe en el disco, pero se eliminó de la DB.")

    except:
        return False, "Error al eliminar la imagen de la base de datos o del sistema de archivos."

    return True, None # Éxito
    

def get_filename(imagen_id):
    imagen = get_imagen_id(imagen_id)
    if not imagen:
        return None
    return os.path.basename(imagen.url)