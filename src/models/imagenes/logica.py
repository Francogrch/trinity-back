# Aca hay que hacer refactoring de src.web.controllers.imagenes.py
from .imagen import ImagenSchema,Imagen
from src.models.database import db

_schema_imagen = ImagenSchema()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_schema_imagen():
    return _schema_imagen

def get_imagenes():
    return Imagen.query.all()

def get_imagen_id(id):
    return Imagen.query.get(id)

def create_imagen(url):
    imagen = Imagen(url=url)
    db.session.add(imagen)
    db.session.commit()
    return imagen

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


