from src.models.database import db  # Importa la base de datos SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # Para manejo seguro de passwords
from src.enums.roles import Rol  # Importa el enum de roles

class Usuario(db.Model):  # Define el modelo de usuario
    id = db.Column(db.Integer, primary_key=True)  # ID único autoincremental
    nombre = db.Column(db.String(100))  # Nombre del usuario
    correo = db.Column(db.String(120), unique=True, nullable=False)  # Correo único y obligatorio
    rol = db.Column(db.String(50))  # Guarda el rol como string (valor del enum)
    password_hash = db.Column(db.String(128))  # Hash de la contraseña

    def __init__(self, nombre, correo, rol, password=None):
        self.nombre = nombre
        self.correo = correo
        # Asegura que el rol sea un valor válido del enum
        if isinstance(rol, Rol):
            self.rol = rol.value
        elif rol in [r.value for r in Rol]:
            self.rol = rol
        else:
            raise ValueError(f"Rol inválido: {rol}")
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.nombre} ({self.rol})>"
