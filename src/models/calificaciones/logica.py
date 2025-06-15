from src.models.calificaciones.calificacion import CalificacionPropiedad
from src.models.calificaciones.calificacion import CalificacionInquilino
from src.models.calificaciones.calificacion import CalificacionPropiedadSchema
from src.models.calificaciones.calificacion import CalificacionInquilinoSchema
from src.models.database import db
from datetime import datetime
from flask import url_for


def create_calificacion_propiedad(data):
    calificacion = CalificacionPropiedad(**data)
    db.session.add(calificacion)
    db.session.commit()
    return calificacion


def create_calificacion_inquilino(data):
    calificacion = CalificacionInquilino(**data)
    db.session.add(calificacion)
    db.session.commit()
    return calificacion


def get_schema_calificacion_propiedad():
    return CalificacionPropiedadSchema()


def get_schema_calificacion_inquilino():
    return CalificacionInquilinoSchema()
