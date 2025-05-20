from src.models.marshmallow import ma
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import validate, post_load
from src.models.database import db

# Tabla de asociación para muchos-a-muchos entre usuarios y roles
usuario_rol = db.Table(
    'usuario_rol',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True)
)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tipo_identificacion = db.Column(db.String(50), nullable=True)  # Nuevo campo
    numero_identificacion = db.Column(db.String(50), nullable=True)  # Nuevo campo
    apellido = db.Column(db.String(100), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    id_pais = db.Column(db.Integer, db.ForeignKey('paises.id'), nullable=True)
    pais = db.relationship('Pais', backref='usuarios')
    roles = db.relationship('Rol', secondary=usuario_rol, backref=db.backref('usuarios', lazy='dynamic'))

    def __init__(self, nombre, correo, roles=None, password=None, tipo_identificacion=None, numero_identificacion=None, apellido=None, fecha_nacimiento=None, id_pais=None):
        self.nombre = nombre
        self.correo = correo
        if roles:
            self.roles = roles
        if password:
            self.set_password(password)
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.id_pais = id_pais

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Rol {self.nombre}>"

class RolSchema(ma.Schema):
    id = ma.Integer()
    nombre = ma.String()

class UsuarioSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    nombre = ma.String(required=True)
    correo = ma.String(required=True)
    tipo_identificacion = ma.String()
    numero_identificacion = ma.String()
    apellido = ma.String()
    fecha_nacimiento = ma.Date()
    id_pais = ma.Integer()
    pais = ma.Nested('PaisSchema', dump_only=True)
    roles = ma.Nested(RolSchema, many=True, dump_only=True)
    # Puedes agregar más campos si es necesario
