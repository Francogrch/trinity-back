from app import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    rol = db.Column(db.String(50))

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

def insert_default_data():
    if not Usuario.query.first():
        db.session.add_all([
            Usuario(nombre="Admin", rol="administrador"),
            Usuario(nombre="Juan", rol="inquilino")
        ])
        db.session.commit()


class Propiedad(db.Model):
    __tablename__ = 'propiedad'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    descripcion = db.Column(db.String)
    ubicacion = db.Column(db.String)
    huespedes = db.Column(db.Integer)
    ambientes = db.Column(db.Integer)
    banios = db.Column(db.Integer)
    cocheras = db.Column(db.Integer)
    precio_noche = db.Column(db.Float)
    creado = db.Column(db.DateTime) 
    actualizado = db.Column(db.DateTime) 

    pol_cancel_id = db.Column(db.Integer,db.ForeignKey('politica_cancelacion.id')) 
    pol_reserva_id = db.Column(db.Integer,db.ForeignKey('politica_reserva.id')) 
    calificacion_id = db.Column(db.Integer,db.ForeignKey('calificacion_prop.id')) 

    # Relaciones para SQLAlchemy
    # Esto se escribe en las relaciones de uno a muchos
    # Backref para acceder desde la otra tabla, lazy para que no lo cargue hasta la query
    calificaciones = db.relationship('CalificacionProp', backref='propiedad',lazy=True,foreign_keys='CalificacionProp.propiedad_id')
    reservas = db.relationship('Reserva', backref='propiedad', lazy=True)
    imagenes = db.relationship('ImagenPropiedad', backref='propiedad', lazy=True)

class PoliticaReserva(db.Model):
    __tablename__ = 'politica_reserva'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String)
    propiedades = db.relationship('Propiedad', backref='politica_reserva', lazy=True, foreign_keys='Propiedad.pol_reserva_id')

class PoliticaCancelacion(db.Model):
    __tablename__ = 'politica_cancelacion'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String)
    propiedades = db.relationship('Propiedad', backref='politica_cancelacion', lazy=True, foreign_keys='Propiedad.pol_cancel_id')

class ImagenPropiedad(db.Model):
    __tablename__ = 'imagen_propiedad'
    id = db.Column(db.Integer,primary_key=True)
    propiedad_id = db.Column(db.Integer,db.ForeignKey('propiedad.id')) 
    url = db.Column(db.String)

class Reserva(db.Model):
    __tablename__ = 'reserva'
    id = db.Column(db.Integer,primary_key=True)
    propiedad_id = db.Column(db.Integer,db.ForeignKey('propiedad.id')) 
    inquilino_id = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    chat_id = db.Column(db.Integer) # FK de chat
    estado = db.Column(db.String)
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    creado = db.Column(db.DateTime)
    actualizado = db.Column(db.DateTime)

class CalificacionProp(db.Model):
    __tablename__ = 'calificacion_prop'
    id = db.Column(db.Integer,primary_key=True)
    propiedad_id = db.Column(db.Integer,db.ForeignKey('propiedad.id'))
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    puntaje = db.Column(db.Integer)
    comentario = db.Column(db.String)
    creado = db.Column(db.DateTime)
