from flask import Blueprint, request, jsonify  # Importa Blueprint para rutas, request para datos y jsonify para respuestas JSON
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # Importa funciones para manejo de JWT (autenticación y claims)
from src.services import user_service  # Importa el servicio que maneja la lógica de usuarios

# Crea un blueprint para las rutas relacionadas a usuarios, con prefijo /usuarios
user_blueprint = Blueprint('users', __name__, url_prefix="/usuarios")

def rol_requerido(roles_permitidos):
    """
    Decorador para restringir acceso a rutas según roles permitidos.
    Uso: @rol_requerido(['Administrador', 'Empleado'])
    """
    def decorador(f):
        # Aplica el decorador jwt_required para que la ruta requiera token válido
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()  # Obtiene los claims (datos) del token JWT
            rol_actual = claims.get('rol')  # Extrae el rol del usuario desde el token
            if rol_actual not in roles_permitidos:  # Verifica si el rol tiene permiso
                return jsonify({'mensaje': 'Acceso denegado: rol insuficiente'}), 403  # Si no, responde con error 403 Forbidden
            return f(*args, **kwargs)  # Si está permitido, ejecuta la función original
        wrapper.__name__ = f.__name__  # Evita problemas con el nombre de la función decorada
        return wrapper  # Devuelve el wrapper decorado
    return decorador  # Devuelve el decorador parametrizado con roles permitidos

def verificar_permiso_creacion_usuario(rol_actual, rol_nuevo):
    """
    Lógica para validar permisos de creación de usuarios según rol del creador.
    Retorna (True, None) si está permitido, o (False, mensaje) si no.
    """
    if rol_nuevo == 'Empleado':  # Si se quiere crear un usuario con rol Empleado
        if rol_actual != 'Administrador':  # Solo un Administrador puede hacerlo
            return False, 'Solo un Administrador puede crear usuarios Empleados'
    elif rol_nuevo == 'Inquilino':  # Si se quiere crear un usuario con rol Inquilino
        if rol_actual not in ['Administrador', 'Empleado']:  # Solo Admin o Empleado pueden hacerlo
            return False, 'Solo Administrador o Empleado pueden crear usuarios Inquilinos'
    else:
        return False, 'Rol destino no permitido'  # Si el rol nuevo no es válido, no se permite
    return True, None  # Si todo está ok, permite la creación

@user_blueprint.get('/')
@jwt_required()  # Requiere token válido para acceder a esta ruta
@rol_requerido(['Administrador', 'Empleado'])  # Solo roles Administrador y Empleado pueden acceder
def get_usuarios():
    usuarios = user_service.obtener_todos_los_usuarios()  # Llama al servicio para obtener todos los usuarios
    # Devuelve la lista de usuarios como JSON con id, nombre y rol
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'rol': u.rol} for u in usuarios])

@user_blueprint.post('/')
@jwt_required()  # Requiere token válido para acceder a esta ruta
@rol_requerido(['Administrador', 'Empleado'])  # Solo roles Administrador y Empleado pueden crear usuarios
def create_usuario():
    claims = get_jwt()  # Obtiene claims del token actual
    current_user_rol = claims.get('rol')  # Obtiene el rol del usuario autenticado
    data = request.get_json()  # Extrae los datos JSON enviados en la petición
    # Verifica permisos para crear el nuevo usuario según su rol y el rol del actual
    permitido, mensaje = verificar_permiso_creacion_usuario(current_user_rol, data['rol'])
    if not permitido:  # Si no tiene permiso
        return jsonify({'mensaje': mensaje}), 403  # Responde con error 403 Forbidden y mensaje
    # Llama al servicio para crear el usuario con los datos recibidos
    nuevo = user_service.crear_usuario(
        nombre=data['nombre'],
        correo=data['correo'],
        rol=data['rol'],
        password=data['password']
    )
    if nuevo:  # Si se creó correctamente
        return jsonify({'mensaje': 'Usuario creado'}), 201  # Responde con éxito y código 201 Created
    else:
        return jsonify({'mensaje': 'Error al crear usuario'}), 400  # Si hubo error, responde con 400 Bad Request
