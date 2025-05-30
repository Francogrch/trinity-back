import os
import shutil

def copiar_y_limpiar_directorio(origen, destino):
    """
    Copia el contenido de una carpeta de origen a una de destino,
    limpiando previamente la carpeta de destino si existe.

    Args:
        origen (str): La ruta de la carpeta de origen.
        destino (str): La ruta de la carpeta de destino.
    """
    try:
        # 1. Verificar si la carpeta de destino existe y limpiarla
        if os.path.exists(destino):
            print(f"Limpiando la carpeta '{destino}'...")
            shutil.rmtree(destino)  # Elimina el directorio y todo su contenido
            print(f"Carpeta '{destino}' limpiada exitosamente.")
        else:
            print(f"La carpeta '{destino}' no existe. Se creará.")

        # 2. Crear la carpeta de destino si no existe (o después de limpiarla)
        os.makedirs(destino, exist_ok=True) # exist_ok=True evita un error si ya existe

        # 3. Copiar el contenido de la carpeta de origen a la de destino
        print(f"Copiando el contenido de '{origen}' a '{destino}'...")
        # shutil.copytree copia el directorio y su contenido.
        # Si el destino ya existiera (lo que ya manejamos con rmtree),
        # se necesitaría dirs_exist_ok=True, pero en este caso no es necesario
        # porque nos aseguramos de que el destino esté vacío o no exista.
        for item in os.listdir(origen):
            s = os.path.join(origen, item)
            d = os.path.join(destino, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d) # copy2 también copia metadatos

        print(f"¡Copia exitosa de '{origen}' a '{destino}'!")

    except FileNotFoundError:
        print(f"Error: La carpeta de origen '{origen}' no fue encontrada.")
    except PermissionError:
        print(f"Error de permisos: No se pudo acceder o escribir en alguna de las carpetas.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
def run():

    """
    Función principal para ejecutar el script.
    Define las rutas de origen y destino y llama a la función de copia.
    """
    carpeta_origen = "backup/imagenes/propiedad"
    carpeta_destino = "imagenes/propiedad"

    copiar_y_limpiar_directorio(carpeta_origen, carpeta_destino)

    carpeta_origen = "backup/imagenes/usuario"
    carpeta_destino = "imagenes/usuario"
    
    copiar_y_limpiar_directorio(carpeta_origen, carpeta_destino)

if __name__ == "__main__":
    carpeta_origen = "backup/imagenes/propiedad"
    carpeta_destino = "imagenes/propiedad"

    copiar_y_limpiar_directorio(carpeta_origen, carpeta_destino)