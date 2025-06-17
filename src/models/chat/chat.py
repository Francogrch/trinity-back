from src.models.database import db
from src.models.marshmallow import ma
from marshmallow import EXCLUDE, validate
from datetime import datetime


class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)
    mensajes = db.relationship(
        'Mensaje', backref='chat', lazy=True, cascade="all, delete-orphan")

    def __init__(self):
        pass

    def __repr__(self):
        return f"<Chat {self.id}>"

class Mensaje(db.Model):
    __tablename__ = "mensaje"
    id = db.Column(db.Integer, primary_key=True)
    id_chat = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    id_user = db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    
    def __init__(self, id_chat, text, id_user):
        self.id_chat = id_chat
        self.mensaje = text
        self.id_user = id_user

class MensajeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = EXCLUDE
    
    mensaje = ma.String(required=True)
    fecha = ma.DateTime(allow_none=True, dump_only=True)
    nombre = ma.Method("get_nombre", dump_only=True)  # Assuming get_nombre is a function to fetch user name
    rol = ma.Method("get_rol", dump_only=True)  # Assuming get_rol is a function to fetch user role

    def get_nombre(self, obj):
       from src.models.users.logica import get_nombre
       user = get_nombre(obj.id_user)
       return user
    def get_rol(self, obj):
         from src.models.users.logica import get_rol
         rol = get_rol(obj.id_user)
         return rol

class ChatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = EXCLUDE  
    mensajes = ma.Nested(MensajeSchema, many=True, dump_only=True)