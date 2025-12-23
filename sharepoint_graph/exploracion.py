import requests
from .autenticacion import obtener_headers_auth

def listar_contenido_carpeta(drive_id, folder_id, token_acceso):
    """
    Obtiene una lista de los items inmediatos (hijos) dentro de una carpeta.

    Args:
        drive_id (str): ID del Drive.
        folder_id (str): ID de la carpeta (o 'root' para la raíz).
        token_acceso (str): Token de acceso.

    Returns:
        list: Lista de diccionarios, donde cada diccionario es un item (archivo o carpeta).
    """
    # Endpoint: /drives/{drive-id}/items/{item-id}/children
    endpoint = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}/children"
    headers = obtener_headers_auth(token_acceso)
    
    items_encontrados = []
    
    while endpoint:
        try:
            respuesta = requests.get(endpoint, headers=headers)
            respuesta.raise_for_status()
            data = respuesta.json()
            
            items = data.get('value', [])
            items_encontrados.extend(items)
            
            # Paginación: Graph API devuelve '@odata.nextLink' si hay más resultados
            endpoint = data.get('@odata.nextLink')
            
        except requests.exceptions.RequestException as e:
            print(f"Error al listar contenido de carpeta: {e}")
            break
            
    return items_encontrados

def explorar_carpeta_recursiva(drive_id, folder_id, token_acceso, nivel=0):
    """
    Generador que recorre recursivamente una estructura de carpetas.
    
    Args:
        drive_id (str): ID del Drive.
        folder_id (str): ID de la carpeta inicial.
        token_acceso (str): Token de acceso.
        nivel (int): Nivel de profundidad actual (para indentación visual si se desea).
    
    Yields:
        tuple: (item, nivel) Por cada archivo o carpeta encontrado.
    """
    items = listar_contenido_carpeta(drive_id, folder_id, token_acceso)
    
    for item in items:
        # Devolvemos el item actual
        yield item, nivel
        
        # Si tiene la propiedad 'folder', es una carpeta y debemos entrar
        if 'folder' in item:
            nuevo_folder_id = item.get('id')
            # Llamada recursiva (yield from)
            yield from explorar_carpeta_recursiva(drive_id, nuevo_folder_id, token_acceso, nivel + 1)

if __name__ == "__main__":
    # Ejemplo de uso (simulado, requiere token real)
    pass
