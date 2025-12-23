import os
import requests
from .autenticacion import obtener_headers_auth
from .utilidades import resolver_url_a_drive_item

def descargar_archivo_por_id(drive_id, item_id, ruta_destino, token_acceso):
    """
    Descarga un archivo de SharePoint usando su Drive ID e Item ID.

    Args:
        drive_id (str): ID de la unidad (Drive) donde está el archivo.
        item_id (str): ID del archivo (Item).
        ruta_destino (str): Ruta local completa donde se guardará el archivo.
        token_acceso (str): Token de acceso.
    
    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario.
    """
    # Endpoint: /drives/{drive-id}/items/{item-id}/content
    endpoint = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content"
    headers = obtener_headers_auth(token_acceso)

    try:
        # Nota: requests sigue las redirecciones (302) automáticamente, que es lo habitual en Graph para descargas
        with requests.get(endpoint, headers=headers, stream=True) as respuesta:
            respuesta.raise_for_status()
            
            # Crear directorios si no existen
            os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
            
            with open(ruta_destino, 'wb') as f:
                for chunk in respuesta.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Archivo descargado exitosamente en: {ruta_destino}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        return False

def descargar_desde_url(url_compartida, ruta_destino, token_acceso):
    """
    Descarga un archivo directamente desde una URL pública/compartida de SharePoint.
    Primero resuelve el item y luego lo descarga.

    Args:
        url_compartida (str): URL de SharePoint.
        ruta_destino (str): Ruta local de guardado.
        token_acceso (str): Token de acceso.

    Returns:
        bool: True si éxito, False si error.
    """
    item = resolver_url_a_drive_item(url_compartida, token_acceso)
    
    if not item:
        print("No se pudo resolver el item desde la URL.")
        return False
    
    # Extraer IDs necesarios del objeto item
    # 'parentReference' suele contener el driveId
    parent_ref = item.get('parentReference', {})
    drive_id = parent_ref.get('driveId')
    item_id = item.get('id')
    
    if not drive_id or not item_id:
        # Intento alternativo: a veces el item tiene '@microsoft.graph.downloadUrl' directamente
        download_url = item.get('@microsoft.graph.downloadUrl')
        if download_url:
            print("Usando URL de descarga directa...")
            try:
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
                    with open(ruta_destino, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                return True
            except Exception as e:
                print(f"Fallo en descarga directa: {e}")
                return False
        
        print("No se encontraron driveId o itemId válidos en la respuesta.")
        return False
        
    print(f"Item resuelto. Drive ID: {drive_id}, Item ID: {item_id}")
    return descargar_archivo_por_id(drive_id, item_id, ruta_destino, token_acceso)
