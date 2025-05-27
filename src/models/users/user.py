from src.models.marshmallow import ma
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import validate, post_load, EXCLUDE
from src.models.database import db
from src.models.schemas import RolSchema, PaisSchema
from src.models.parametricas.parametricas import Pais
from src.models.parametricas.parametricas import TipoIdentificacionSchema
from src.enums.roles import Rol as rol_enum
from src.models.imagenes.imagen import ImagenSchema,Imagen

# Tabla de asociación para muchos-a-muchos entre usuarios y roles
usuario_rol = db.Table(
    'usuario_rol',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True)
)


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    id_tipo_identificacion = db.Column(db.Integer, db.ForeignKey('tipo_identificacion.id'), nullable=True)
    tipo_identificacion = db.relationship('TipoIdentificacion')
    numero_identificacion = db.Column(db.String(50), nullable=True)  # Nuevo campo
    apellido = db.Column(db.String(100), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    id_pais = db.Column(db.Integer, db.ForeignKey('paises.id'), nullable=True)
    pais = db.relationship("Pais", backref="usuario")
    roles = db.relationship('Rol', secondary=usuario_rol, backref=db.backref('usuario', lazy='dynamic'))
    tarjetas = db.relationship('Tarjeta', backref='usuario', lazy=True)
    propiedades = db.relationship("Propiedad", back_populates="encargado")
    id_imagen = db.Column(db.Integer, db.ForeignKey('imagen.id'), nullable=True)
    imagen = db.relationship('Imagen', back_populates='usuario', uselist=False, lazy=True,foreign_keys='[Imagen.id_usuario]')
    imagenes_doc = db.relationship('Imagen', back_populates='usuario', lazy=True, foreign_keys='[Imagen.id_usuario]')

    def __init__(self, nombre, correo, roles=None, password=None, id_tipo_identificacion=None, tipo_identificacion=None, numero_identificacion=None, apellido=None, fecha_nacimiento=None, id_pais=None, id_imagen=None):
        self.nombre = nombre
        self.correo = correo
        if roles:
            self.roles = roles
        if password:
            self.set_password(password)
        self.id_tipo_identificacion = id_tipo_identificacion
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.id_pais = id_pais
        self.id_imagen = id_imagen

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_roles(self):
        ids_roles_usuario = [rol.id for rol in self.roles]
        return {
                "is_admin": any(r == rol_enum.ADMINISTRADOR.value for r in ids_roles_usuario),
                "is_encargado": any(r == rol_enum.EMPLEADO.value for r in ids_roles_usuario),
                "is_inquilino": any(r == rol_enum.INQUILINO.value for r in ids_roles_usuario)
                }

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Rol {self.nombre}>"

class Tarjeta(db.Model):
    __tablename__ = "tarjeta"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), nullable=False)
    nombre_titular = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.String, nullable=True)  # Cambiado a String
    fecha_vencimiento = db.Column(db.String, nullable=False)  # Cambiado a String
    cvv = db.Column(db.String(10), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_marca = db.Column(db.Integer, db.ForeignKey('marca_tarjeta.id'), nullable=True)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipo_tarjeta.id'), nullable=True)
    marca = db.relationship('MarcaTarjeta', foreign_keys=[id_marca])
    tipo = db.relationship('TipoTarjeta', foreign_keys=[id_tipo])

    def __init__(self, numero, nombre_titular, fecha_inicio, fecha_vencimiento, cvv, usuario_id, id_marca=None, id_tipo=None):
        self.numero = numero
        self.nombre_titular = nombre_titular
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.cvv = cvv
        self.usuario_id = usuario_id
        self.id_marca = id_marca
        self.id_tipo = id_tipo

    def __repr__(self):
        return f"<Tarjeta {self.numero[-4:]} - {self.nombre_titular}>"

# --- Paramétricas para tarjeta ---
class MarcaTarjeta(db.Model):
    __tablename__ = 'marca_tarjeta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    def __repr__(self):
        return f"<MarcaTarjeta {self.nombre}>"

class TipoTarjeta(db.Model):
    __tablename__ = 'tipo_tarjeta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    def __repr__(self):
        return f"<TipoTarjeta {self.nombre}>"

class RolSchema(ma.Schema):
    id = ma.Integer()
    nombre = ma.String()

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ["imagen"]

    # IDs explícitos para facilitar consumo en frontend
    id_pais = ma.Integer(attribute="id_pais")
    id_tipo_identificacion = ma.Integer(attribute="id_tipo_identificacion")
    roles_ids = ma.Method("get_roles_ids")

    pais = ma.Nested(PaisSchema, only=("id", "nombre"))
    roles = ma.Nested(RolSchema, many=True, only=("id", "nombre"))
    tipo_identificacion = ma.Nested(TipoIdentificacionSchema, only=("id", "nombre"))
    tarjetas = ma.Nested(lambda: TarjetaSchema(), many=True)
    imagenes_doc = ma.Nested(ImagenSchema(only=('id',), many=True, dump_only=('id',)))

    id_imagenes = ma.Method("get_image_ids", dump_only=True)

    def get_roles_ids(self, obj):
        return [rol.id for rol in obj.roles] if obj.roles else []

    def get_image_ids(self, obj):
        if obj.imagenes_doc:
            return [img.id for img in obj.imagenes_doc]
        return []


class EmpleadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    nombre = ma.String(dump_only=True)
    correo = ma.String(dump_only=True)

# --- TarjetaSchema al final para evitar ciclos ---
class MarcaTarjetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MarcaTarjeta
        load_instance = True

class TipoTarjetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoTarjeta
        load_instance = True

class TarjetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tarjeta
        include_fk = True
        load_instance = True
    fecha_inicio = ma.String(allow_none=True)  # Cambiado a String
    fecha_vencimiento = ma.String(required=True)  # Cambiado a String
    marca = ma.Nested(MarcaTarjetaSchema, allow_none=True)
    tipo = ma.Nested(TipoTarjetaSchema, allow_none=True)
