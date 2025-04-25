
from app import db
from datetime import datetime


def insert_default_data():
    # Inserta datos por defecto aquí, por ejemplo:
    if not Usuario.query.first():  # Si no hay usuarios
        usuario = Usuario(nombre="Admin", email="admin@trinity.com")
        db.session.add(usuario)
        db.session.commit()


class Tarjeta(db.Model):
    __tablename__ = 'tarjeta'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String)


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    rol = db.Column(db.String)
    tarjeta_id = db.Column(db.Integer, db.ForeignKey('tarjeta.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tarjeta = db.relationship('Tarjeta', backref='usuarios')


class PoliticaCancelacion(db.Model):
    __tablename__ = 'politica_cancelacion'
    id = db.Column(db.Integer, primary_key=True)


class PoliticaReserva(db.Model):
    __tablename__ = 'politica_reserva'
    id = db.Column(db.Integer, primary_key=True)


class Propiedad(db.Model):
    __tablename__ = 'propiedad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    ubicacion = db.Column(db.String)
    huespedes = db.Column(db.Integer)
    ambientes = db.Column(db.Integer)
    banios = db.Column(db.Integer)
    cocheras = db.Column(db.Integer)
    pol_cancel_id = db.Column(
        db.Integer, db.ForeignKey('politica_cancelacion.id'))
    pol_reserva_id = db.Column(
        db.Integer, db.ForeignKey('politica_reserva.id'))
    precio_noche = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Reserva(db.Model):
    __tablename__ = 'reserva'
    id = db.Column(db.Integer, primary_key=True)
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedad.id'))
    inquilino_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    estado = db.Column(db.String)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CalificacionUser(db.Model):
    __tablename__ = 'calificacion_user'
    id = db.Column(db.Integer, primary_key=True)
    evaluado_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    evaluador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    puntaje = db.Column(db.Integer)
    comentario = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CalificacionProp(db.Model):
    __tablename__ = 'calificacion_prop'
    id = db.Column(db.Integer, primary_key=True)
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedad.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    puntaje = db.Column(db.Integer)
    comentario = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    mensaje_id = db.Column(db.Integer)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    hora = db.Column(db.DateTime)
    texto = db.Column(db.Text)


class ImagenPropiedad(db.Model):
    __tablename__ = 'imagen_propiedad'
    id = db.Column(db.Integer, primary_key=True)
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedad.id'))
    url = db.Column(db.Text)
