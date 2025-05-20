"""
Clases polimórficas para permisos de roles de usuario.
Cada clase representa los permisos asociados a un rol específico.
El método get_permisos() devuelve un diccionario con los permisos habilitados (True/False) para ese rol.
Se utiliza para centralizar y exponer la lógica de permisos en el backend.

Uso:
Para obtener los permisos de un usuario según su(s) rol(es):

    # Ejemplo: obtener permisos para un usuario con rol 'Administrador'
    permisos = PERMISOS_CLASSES['Administrador']().get_permisos()
    # permisos es un diccionario con los permisos habilitados para ese rol

Si un usuario tiene múltiples roles, puedes combinar los permisos:

    roles_usuario = ['Administrador', 'Inquilino']
    permisos_finales = {}
    for rol in roles_usuario:
        clase_permiso = PERMISOS_CLASSES.get(rol)
        if clase_permiso:
            permisos_rol = clase_permiso().get_permisos()
            # Combina los permisos (True si al menos un rol lo permite)
            for k, v in permisos_rol.items():
                permisos_finales[k] = permisos_finales.get(k, False) or v

    # permisos_finales tendrá todos los permisos habilitados por cualquiera de los roles
"""

class PermisosRol:
    def get_permisos(self):
        # Devuelve los permisos base (todos en False) para un usuario sin rol específico.
        return {
            "ver_panel_admin": False,          # Acceso al panel de administración
            "gestionar_usuarios": False,       # Permiso para crear, editar o eliminar usuarios
            "ver_panel_empleado": False,       # Acceso al panel de empleados
            "gestionar_propiedades": False,    # Permiso para gestionar propiedades
            "reservar": False,                 # Permiso para realizar reservas
            "ver_panel_inquilino": False       # Acceso al panel de inquilinos
        }

class PermisosAdministrador(PermisosRol):
    def get_permisos(self):
        # Permisos habilitados para el rol Administrador
        p = super().get_permisos()
        p.update({
            "ver_panel_admin": True,
            "gestionar_usuarios": True,
            "ver_panel_empleado": True,
            "reservar": True,
            "ver_panel_inquilino": True
        })
        return p

class PermisosEncargado(PermisosRol):
    def get_permisos(self):
        # Permisos habilitados para el rol Encargado/Empleado
        p = super().get_permisos()
        p.update({
            "ver_panel_empleado": True,
            "gestionar_propiedades": True
        })
        return p

class PermisosInquilino(PermisosRol):
    def get_permisos(self):
        # Permisos habilitados para el rol Inquilino
        p = super().get_permisos()
        p.update({
            "reservar": True,
            "ver_panel_inquilino": True
        })
        return p

# Diccionario para mapear el nombre del rol a su clase de permisos correspondiente
PERMISOS_CLASSES = {
    "Administrador": PermisosAdministrador,
    "Encargado": PermisosEncargado,
    "Inquilino": PermisosInquilino
}
