from logging import exception
import os
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from marshmallow import ValidationError

#Usa get_jwt_identity() si solo necesitas el identificador principal del usuario autenticado.
#Usa get_jwt() si necesitas acceder a otros datos o claims personalizados dentro del JWT.
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from src.models.imagenes import get_filename, upload_image, delete_image, upload_image_usuario,set_id_usuario
from src.web.authorization.roles import rol_requerido
from src.models.users.logica import get_permisos_usuario, get_roles_by_ids
from src.models import users
from src.enums.roles import Rol

# Crea un blueprint para las rutas relacionadas a usuarios, con prefijo /usuarios
user_blueprint = Blueprint('users', __name__, url_prefix="/usuarios")

# Función para verificar si el usuario autenticado puede crear un usuario con ciertos roles
# id_rol_actuales: lista de ids de roles del usuario autenticado
# id_roles_nuevos: lista de ids de roles a asignar al nuevo usuario
# Devuelve (True, None) si está permitido, (False, mensaje) si no
def verificar_permiso_creacion_usuario(id_rol_actuales, id_roles_nuevos):
    """
    Lógica para validar permisos de creación de usuarios según los roles actuales del creador.
    id_rol_actuales: lista de ids de roles del usuario autenticado
    id_roles_nuevos: lista de ids de roles a asignar al nuevo usuario
    """
    # Solo el rol ADMINISTRADOR puede crear empleados (EMPLEADO)
    if Rol.EMPLEADO.value in id_roles_nuevos:
        if Rol.ADMINISTRADOR.value not in id_rol_actuales:
            return False, 'Solo un Administrador puede crear usuarios Empleados'
    # Solo Administrador o Empleado pueden crear usuarios Inquilinos
    if Rol.INQUILINO.value in id_roles_nuevos:
        if not any(r in id_rol_actuales for r in [Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value]):
            return False, 'Solo Administrador o Empleado pueden crear usuarios Inquilinos'
    return True, None

# Endpoint: Obtener todos los usuarios (solo para admin y empleados)
@user_blueprint.get('/')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo roles Administrador y Empleado pueden acceder
# Devuelve la lista de usuarios serializada
def get_usuarios():
    usuarios = users.get_usuarios()  # Obtiene todos los usuarios de la base
    return users.get_schema_usuario().dumps(usuarios, many=True)  # Serializa y retorna

# Endpoint: Obtener todos los empleados (solo para admin)
@user_blueprint.get('/empleados')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])  # Solo rol Administrador puede acceder
# Devuelve la lista de empleados serializada
def get_empleados():
    usuarios = users.get_empleados()  # Obtiene todos los usuarios de la base
    return users.get_schema_empleado().dump(usuarios, many=True)  # Serializa y retorna

# Endpoint: Crear un nuevo usuario (solo admin y empleados)
@user_blueprint.post('/')
@jwt_required(optional=True)
def create_usuario():
    from flask_jwt_extended import get_jwt_identity
    # Intentar obtener el user_id si hay JWT, si no, será None
    user_id = None
    try:
        user_id = get_jwt_identity()
    except Exception:
        pass
    data = request.get_json()
    if not data or 'roles_ids' not in data:
        return jsonify({'error': 'El campo roles_ids es obligatorio en el cuerpo de la petición.'}), 400

    # --- CASO AUTOREGISTRO (sin JWT): solo inquilino ---
    if not user_id:
        # Aceptar también el caso donde roles_ids es [int], [str], o mezcla
        try:
            roles_ids_int = [int(r) for r in data['roles_ids']]
        except Exception:
            return jsonify({'mensaje': 'roles_ids debe ser una lista de enteros o strings numéricos.'}), 400
        # Permitir también que el frontend mande el valor como string ("3")
        if not (len(roles_ids_int) == 1 and roles_ids_int[0] == int(Rol.INQUILINO.value)):
            return jsonify({'mensaje': f'Solo se permite el auto-registro de inquilinos. roles_ids recibido: {data["roles_ids"]}'}), 403
        # Crear usuario inquilino y login automático
        try:
            usuario = users.create_usuario(
                nombre=data['nombre'],
                correo=data['correo'],
                roles_ids=data['roles_ids'],
                password=data['password'],
                id_tipo_identificacion=data.get('id_tipo_identificacion'),
                numero_identificacion=data.get('numero_identificacion'),
                apellido=data.get('apellido'),
                fecha_nacimiento=data.get('fecha_nacimiento'),
                id_pais=data.get('id_pais')
            )
            tarjetas_data = data.get('tarjetas')
            if tarjetas_data and isinstance(tarjetas_data, list):
                from src.models.users.user import Tarjeta
                from src.models.database import db
                for t in tarjetas_data:
                    tarjeta = Tarjeta(
                        numero=t['numero'],
                        nombre_titular=t['nombre_titular'],
                        fecha_inicio=t.get('fecha_inicio'),
                        fecha_vencimiento=t['fecha_vencimiento'],
                        cvv=t['cvv'],
                        usuario_id=usuario.id,
                        id_marca=t.get('id_marca'),
                        id_tipo=t.get('id_tipo')
                    )
                    db.session.add(tarjeta)
                db.session.commit()
            from flask_jwt_extended import create_access_token
            from datetime import timedelta
            access_token = create_access_token(identity=str(usuario.id), expires_delta=timedelta(days=1))
            return jsonify({
                'usuario': users.get_schema_usuario().dump(usuario),
                'access_token': access_token
            }), 201
        except ValidationError as err:
            return jsonify(err.messages), 422
        except Exception as e:
            return jsonify({"error": "Mail ya registrado"}), 400

    # --- CASO ADMINISTRADOR O EMPLEADO (con JWT) ---
    usuario_actual = users.get_usuario_by_id(user_id)
    id_rol_actuales = [int(r.id) for r in usuario_actual.roles]
    try:
        roles_ids_int = [int(r) for r in data['roles_ids']]
    except Exception:
        return jsonify({'mensaje': 'roles_ids debe ser una lista de enteros o strings numéricos.'}), 400
    
    # Solo admin puede crear empleados
    if any(r == int(Rol.EMPLEADO.value) for r in roles_ids_int):
        print(f"[DEBUG] Check admin for empleado: {int(Rol.ADMINISTRADOR.value)} in {id_rol_actuales}")
        if int(Rol.ADMINISTRADOR.value) not in id_rol_actuales:
            return jsonify({'mensaje': 'Solo un Administrador puede crear usuarios Empleados', 'debug': {'id_rol_actuales': id_rol_actuales, 'roles_ids_int': roles_ids_int}}), 403
    # Solo admin o empleado pueden crear inquilinos
    if any(r == int(Rol.INQUILINO.value) for r in roles_ids_int):
        print(f"[DEBUG] Check admin/empleado for inquilino: {[int(Rol.ADMINISTRADOR.value), int(Rol.EMPLEADO.value)]} in {id_rol_actuales}")
        if not any(r in id_rol_actuales for r in [int(Rol.ADMINISTRADOR.value), int(Rol.EMPLEADO.value)]):
            return jsonify({'mensaje': 'Solo Administrador o Empleado pueden crear usuarios Inquilinos', 'debug': {'id_rol_actuales': id_rol_actuales, 'roles_ids_int': roles_ids_int}}), 403
    # No permitir que empleados creen empleados
    if any(r == int(Rol.EMPLEADO.value) for r in roles_ids_int) and int(Rol.ADMINISTRADOR.value) not in id_rol_actuales:
        print(f"[DEBUG] Empleado intentando crear empleado: {id_rol_actuales}")
        return jsonify({'mensaje': 'Solo un Administrador puede crear usuarios Empleados', 'debug': {'id_rol_actuales': id_rol_actuales, 'roles_ids_int': roles_ids_int}}), 403
    try:
        usuario = users.create_usuario(
            nombre=data['nombre'],
            correo=data['correo'],
            roles_ids=roles_ids_int,  # Usar la lista normalizada a int
            password=data['password'],
            id_tipo_identificacion=data.get('id_tipo_identificacion'),
            numero_identificacion=data.get('numero_identificacion'),
            apellido=data.get('apellido'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            id_pais=data.get('id_pais')
        )
        tarjetas_data = data.get('tarjetas')
        if tarjetas_data and isinstance(tarjetas_data, list):
            from src.models.users.user import Tarjeta
            from src.models.database import db
            for t in tarjetas_data:
                tarjeta = Tarjeta(
                    numero=t['numero'],
                    nombre_titular=t['nombre_titular'],
                    fecha_inicio=t.get('fecha_inicio'),
                    fecha_vencimiento=t['fecha_vencimiento'],
                    cvv=t['cvv'],
                    usuario_id=usuario.id,
                    id_marca=t.get('id_marca'),
                    id_tipo=t.get('id_tipo')
                )
                db.session.add(tarjeta)
            db.session.commit()
        return (users.get_schema_usuario().dumps(usuario), 201)
    except ValidationError as err:
        return (err.messages, 422)
    except Exception as e:
        # Manejo de errores específicos de integridad
        error_msg = str(e)
        if 'UNIQUE constraint failed: usuario.correo' in error_msg:
            return jsonify({'error': 'El correo electrónico ya está registrado. Usa otro correo.'}), 400
        if 'UNIQUE constraint failed: usuario.id_tipo_identificacion, usuario.numero_identificacion' in error_msg or \
           'UNIQUE constraint failed: usuario.numero_identificacion' in error_msg:
            return jsonify({'error': 'Ya existe un usuario con ese tipo y número de identificación. Verifica los datos.'}), 400
        print(f"[ERROR] Error al crear usuario: {error_msg}")
        return ({"error": error_msg}, 400)

# Endpoint: Obtener usuario por id (solo admin y empleados)
@user_blueprint.get('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value, Rol.INQUILINO.value])
def get_usuario_by_id(user_id):
    usuario = users.get_usuario_by_id(user_id)  # Busca el usuario por id
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Si no existe, error
    usuario_schema = users.get_schema_usuario()  # Obtiene el schema
    data = usuario_schema.dump(usuario)  # Serializa el usuario
    data["permisos"] = get_permisos_usuario(usuario)  # Agrega los permisos calculados
    return data  # Retorna usuario serializado with permisos

# Endpoint: Obtener el usuario autenticado (perfil propio)
@user_blueprint.get('/me')
@jwt_required()
def get_usuario_actual():
    user_id = get_jwt_identity()  # Obtiene el id del usuario autenticado
    usuario = users.get_usuario_by_id(user_id)  # Busca el usuario en la base
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404  # Si no existe, error
    usuario_schema = users.get_schema_usuario()  # Obtiene el schema
    data = usuario_schema.dump(usuario)  # Serializa el usuario
    data["permisos"] = get_permisos_usuario(usuario)  # Agrega los permisos calculados
    return data  # Retorna el usuario con permisos

# Endpoint: Obtener usuarios por rol (solo admin y empleados)
@user_blueprint.get('/por-rol/<int:rol_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def get_usuarios_por_rol(rol_id):
    usuarios = users.get_usuarios_by_rol(rol_id)  # Busca usuarios por rol
    return users.get_schema_usuario().dumps(usuarios, many=True)  # Serializa y retorna

# Endpoint: Eliminar usuario por id (solo admin)
@user_blueprint.delete('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value])
def delete_usuario_by_id(user_id):
    try:
        usuario = users.delete_usuario_by_id(user_id)  # Elimina el usuario
        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Si no existe, error
        return jsonify({'mensaje': 'Usuario eliminado correctamente'})  # Éxito
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Otro error

# Endpoint: Actualizar usuario por id (solo admin y empleados)
@user_blueprint.put('/<int:user_id>')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value, Rol.EMPLEADO.value])
def update_usuario(user_id):
    data = request.get_json()  # Obtiene los datos a actualizar
    try:
        usuario = users.update_usuario(user_id, data)  # Actualiza el usuario
        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Si no existe, error
        return users.get_schema_usuario().dumps(usuario)  # Retorna usuario actualizado
    except ValidationError as err:
        return (err.messages, 422)  # Error de validación
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Otro error

@user_blueprint.get('/imagenPerfil/<int:user_id>')
@jwt_required()
def get_imagen(user_id):
    user = users.get_usuario_by_id(user_id)
    if not user.id_imagen:
        return {"error": "El usuario no tiene una imagen asociada"}, 404
    imagen_id = str(user.id_imagen)

    base_upload_directory = os.path.abspath(
        os.path.join(current_app.root_path, "..", "..", "imagenes", "usuario")
    )

    filename = get_filename(imagen_id)

    return send_from_directory(
        directory=base_upload_directory,
        path=filename,
        as_attachment=False
    )

# SIn uso
@user_blueprint.delete('/imagenPerfil')
@jwt_required() 
def delete_imagen():
    id_usuario = request.args.get('id_usuario')
    user = users.get_usuario_by_id(id_usuario)
    if not user.id_imagen:
        return {"error": "El usuario no tiene una imagen asociada"}, 404
    id_imagen = str(user.id_imagen)

    success, message = delete_image(id_imagen, 'usuario')
    users.set_imagen_usuario(id_usuario,None) 

    if success:
        return jsonify({"message": message if message else f"Imagen con ID {id_imagen} eliminada exitosamente"}), 200
    else:
        return jsonify({"message": message}), 500

@user_blueprint.get('/encargados')
@jwt_required()
@rol_requerido([Rol.ADMINISTRADOR.value])  # Solo rol Administrador puede acceder
def get_encargados():
    usuarios = users.get_encargados()  # Obtiene todos los usuarios de la base
    return users.get_schema_empleado().dump(usuarios, many=True)  # Serializa y retorna


# --- ENDPOINTS DE IMÁGENES Y DOCUMENTOS DE USUARIO ---

@user_blueprint.post('/imagenDocumento')
@jwt_required()
def upload_imagen():
    """
    Sube la imagen principal (documento o foto de perfil) de un usuario.
    - Método: POST
    - URL: /usuarios/imagenDocumento?id_usuario=<id>
    - Parámetros:
        - id_usuario (query string): ID del usuario al que se asocia la imagen.
    - Body: multipart/form-data con el archivo bajo la clave 'file'.
    - Respuesta: JSON con información de la imagen subida o error.
    """
    try:
        id_usuario = request.args.get('id_usuario')
        if not id_usuario:
            return jsonify({'error': 'El parámetro id_usuario es requerido.'}), 400
        image = upload_image('usuario', request, id_usuario=id_usuario)
        if isinstance(image, tuple) and len(image) == 2 and image[1] == 201:
            return image
        # Si image es un dict de error
        if isinstance(image, dict) and 'error' in image:
            return jsonify(image), 400
        # Si image es una tupla con error
        if isinstance(image, tuple) and len(image) == 2 and image[1] != 201:
            return jsonify(image[0]), image[1]
        return jsonify({'error': 'Error desconocido al subir la imagen.'}), 500
    except Exception as e:
        print(f"[ERROR] Excepción en upload_imagen: {e}")
        return jsonify({'error': f'Error interno al subir la imagen: {str(e)}'}), 500

@user_blueprint.get('/imagenesDoc')
@jwt_required()
def get_imagenes_id():
    """
    Obtiene los IDs de los documentos/imágenes adicionales asociados a un usuario.
    - Método: GET
    - URL: /usuarios/imagenesDoc?id_usuario=<id>
    - Parámetros:
        - id_usuario (query string): ID del usuario.
    - Respuesta: Lista de IDs de imágenes/documentos o error.
    """
    id_usuario = request.args.get('id_usuario')
    if not id_usuario:
        return {'error': 'ID de usuario es requerido.'}, 400
    
    try:
        id_usuario = int(id_usuario)
    except ValueError:
        return {'error': 'ID de usuairo inválido.'}, 400

    usuario = users.get_usuario_by_id(id_usuario)
    if not usuario:
        return {'error': 'Usuario no encontrada.'}, 404

    imagenes_de_usuario = usuario.imagenes_doc
    return [imagen.id for imagen in imagenes_de_usuario], 200

@user_blueprint.post('/imagenDoc')
#@jwt_required()
def upload_imagen_doc():
    """
    Sube un documento o imagen adicional asociado a un usuario (puede haber varios por usuario).
    - Método: POST
    - URL: /usuarios/imagenDoc?id_usuario=<id>
    - Parámetros:
        - id_usuario (query string): ID del usuario.
    - Body: multipart/form-data con el archivo bajo la clave 'file'.
    - Respuesta: JSON con información de la imagen/documento subido o error.
    """
    id_usuario = request.args.get('id_usuario')
    image = upload_image('usuario',request,id_usuario=id_usuario)
    return image


@user_blueprint.delete('/imagenDoc')
@jwt_required() 
def delete_imagen_doc():
    """
    Elimina un documento o imagen adicional de un usuario.
    - Método: DELETE
    - URL: /usuarios/imagenDoc?id_imagen=<id>
    - Parámetros:
        - id_imagen (query string): ID de la imagen/documento a eliminar.
    - Respuesta: Mensaje de éxito o error.
    """
    id_imagen = request.args.get('id_imagen')
    print(f"[DEBUG] Eliminar imagen con ID: {id_imagen}")
    if not id_imagen:
        return jsonify({'error': 'El parámetro id_imagen es requerido.'}), 400
    try:
        success, message = delete_image(id_imagen, 'usuario')
        if success:
            return jsonify({"message": message if message else f"Imagen con ID {id_imagen} eliminada exitosamente"}), 200
        else:
            return jsonify({"error": message if message else f"No se pudo eliminar la imagen con ID {id_imagen}"}), 500
    except Exception as e:
        print(f"[ERROR] Excepción al eliminar imagen: {e}")
        return jsonify({"error": f"Error al eliminar la imagen: {str(e)}"}), 500

@user_blueprint.get('/imagenDoc/<int:imagen_id>')
def get_imagen_doc(imagen_id):
    """
    Devuelve la imagen/documento de usuario por su ID.
    - Método: GET
    - URL: /usuarios/imagenDoc/<imagen_id>
    - Respuesta: Archivo de imagen o error.
    """
    base_upload_directory = os.path.abspath(
        os.path.join(current_app.root_path, "..", "..", "imagenes", "usuario")
    )
    filename = get_filename(str(imagen_id))
    return send_from_directory(
        directory=base_upload_directory,
        path=filename,
        as_attachment=False
    )


@user_blueprint.post('/registrar')
def registrar():
    """
    nombre: string;
    correo: string;
    password_hash?: string;
    tipo_identificacion?: TipoIdentificacion;
    numero_identificacion?: string;
    apellido?: string;
    fecha_nacimiento?: string | Date;
    pais?: Pais;
    roles: Rol[];
    tarjetas?: Tarjeta[];
    permisos?: PermisosUsuario;
    imagenes_id?: number[];
    
    class Tarjeta {
    id: number;
    numero: number;
    nombre_titular: string;
    fecha_vencimiento: string;
    cvv: number;
    
    
    """
    data = request.get_json()  # Obtiene los datos del nuevo usuario
    imagenes = data['imagenes_id']
    usuario = users.create_new_usuario(
            nombre=data['nombre'],
            apellido=data.get('apellido'),
            correo=data['correo'],
            roles_ids=data['id_rol'],
            password=data.get('password'),
            id_tipo_identificacion=data.get('id_tipo_identificacion'),
            numero_identificacion=data.get('numero_identificacion'),
            id_pais=data.get('id_pais'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            tarjeta=data.get('tarjeta', None)
        )  # Crea el usuario
    # Tarjetas[0] -> numero, nombre_titular, fecha_vencimiento, cvv

    for id_imagen in imagenes:
        set_id_usuario(id_imagen,usuario.id)
    # Vincular tarjeta  a usuario si se proporciona
    return users.get_schema_usuario().dump(usuario)


# Subir una imagen sin id_usuario
@user_blueprint.post('/imagen')
#@jwt_required()
def upload_imagen_user():
    image = upload_image_usuario(request)
    return image