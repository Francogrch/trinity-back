from src.models.database import db


class Provincia(db.Model):
    __tablename__ = "provincias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    ciudades = db.relationship("Ciudad", back_populates="provincia")

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre

class Ciudad(db.Model):
    __tablename__ = "ciudades"
    id = db.Column(db.Integer, primary_key=True)
    id_provincia = db.Column(db.Integer, db.ForeignKey("provincias.id"))
    nombre = db.Column(db.String, nullable=False)
    provincia = db.relationship("Provincia", back_populates="ciudades")

    def __init__(self, provincia, nombre):
        self.provincia = provincia
        self.nombre = nombre

    def __repr__(self):
        return f"<{self.provincia}, {self.nombre}>"


class PropiedadTipo(db.Model):
    __tablename__ = "propiedad_tipos"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo

    def __repr__(self):
        return self.tipo

