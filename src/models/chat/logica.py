from src.models.database import db
from src.models.chat.chat import Chat, Mensaje, ChatSchema, MensajeSchema



def create_chat():
    chat = Chat()
    db.session.add(chat)
    db.session.commit()
    return chat

def create_mensaje(chat_id, texto, id_user):
    mensaje = Mensaje(id_chat=chat_id, text=texto, id_user=id_user)
    db.session.add(mensaje)
    db.session.commit()
    return mensaje

def get_chat_schema():
    return ChatSchema()

def get_mensaje_schema():
    return MensajeSchema()