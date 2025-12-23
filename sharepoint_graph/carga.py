import os
import requests
from .autenticacion import obtener_headers_auth

def subir_archivo(drive_id, parent_id, ruta_archivo_local, token_acceso):
    """
    Sube un archivo local a una carpeta específica de SharePoint.
    Esta función usa el método simple (PUT) adecuado para archivos menores a 4MB.
    Para archivos más grandes, se debería usar una sesión de carga (Upload Session).

    Args:
        drive_id (str): ID del Drive destino.
        parent_id (str): ID de la carpeta padre donde se subirá el archivo (usar 'root' para la raíz).
        ruta_archivo_local (str): Ruta absoluta del archivo a subir.
        token_acceso (str): Token de acceso.

    Returns:
        dict: Respuesta JSON de Graph API con los metadatos del archivo creado, o None si falla.
    """
    if not os.path.exists(ruta_archivo_local):
        print(f"El archivo local no existe: {ruta_archivo_local}")
        return None

    nombre_archivo = os.path.basename(ruta_archivo_local)
    
    # Endpoint: /drives/{drive-id}/items/{parent-id}:/{filename}:/content
    endpoint = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_id}:/{nombre_archivo}:/content"
    
    headers = obtener_headers_auth(token_acceso)
    # Para subida, el Content-Type debe ser el del archivo o genérico
    headers['Content-Type'] = 'application/octet-stream'

    try:
        with open(ruta_archivo_local, 'rb') as f:
            contenido = f.read()
            
        respuesta = requests.put(endpoint, headers=headers, data=contenido)
        respuesta.raise_for_status()
        
        print(f"Archivo subido exitosamente: {nombre_archivo}")
        return respuesta.json()

    except requests.exceptions.RequestException as e:
        print(f"Error al subir el archivo: {e}")
        try:
            print(respuesta.text)
        except:
            pass
        return None
