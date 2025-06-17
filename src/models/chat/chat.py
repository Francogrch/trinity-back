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
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    id_user = db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    
    def __init__(self, id_chat, text, id_user):
        self.id_chat = id_chat
        self.text = text
        self.id_user = id_user

class MensajeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = EXCLUDE
    
    id = ma.Integer(dump_only=True)
    id_chat = ma.Integer(required=True)
    text = ma.String(required=True)
    created_at = ma.DateTime(allow_none=True, dump_only=True)
    id_user = ma.Integer(required=True)

class ChatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = EXCLUDE  
    id = ma.Integer(dump_only=True)
    created_at = ma.DateTime(allow_none=True, dump_only=True)
    updated_at = ma.DateTime(allow_none=True, dump_only=True)
    mensajes = ma.Nested(MensajeSchema, many=True, dump_only=True)