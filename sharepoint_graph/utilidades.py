import base64
import requests
from .autenticacion import obtener_headers_auth

def codificar_url_compartida(url_compartida):
    """
    Codifica una URL de SharePoint para usarla con la API de 'shares' de Microsoft Graph.
    La codificación requiere base64 URL-safe, sin relleno y con prefijo 'u!'.
    
    Args:
        url_compartida (str): La URL completa de SharePoint (sharing link).

    Returns:
        str: El ID codificado ('sharing token') listo para usar en la API.
    """
    # 1. Codificar en base64
    b64_encoded = base64.urlsafe_b64encode(url_compartida.encode('utf-8')).decode('utf-8')
    # 2. Eliminar el padding '=' al final
    b64_encoded = b64_encoded.rstrip('=')
    # 3. Añadir el prefijo 'u!' y devolver
    return f"u!{b64_encoded}"

def resolver_url_a_drive_item(url_compartida, token_acceso):
    """
    Resuelve una URL pública/compartida de SharePoint a un objeto driveItem de Graph API.
    Esto permite obtener el ID del archivo, el ID del drive, y otros metadatos.

    Args:
        url_compartida (str): La URL de SharePoint.
        token_acceso (str): Token de acceso válido.

    Returns:
        dict: El objeto JSON de la respuesta de Graph (driveItem) o None si falla.
    """
    sharing_token = codificar_url_compartida(url_compartida)
    # Endpoint: /shares/{sharingToken}/driveItem
    endpoint = f"https://graph.microsoft.com/v1.0/shares/{sharing_token}/driveItem"
    
    headers = obtener_headers_auth(token_acceso)
    
    try:
        respuesta = requests.get(endpoint, headers=headers)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error al resolver la URL compartida: {e}")
        print(respuesta.text)
        return None

if __name__ == "__main__":
    # Ejemplo de uso
    url_ejemplo = "https://tu-organizacion.sharepoint.com/:x:/s/sitio/EjemPl0..."
    token = "TU_TOKEN_AQUI"
    
    # Nota: Esto fallará sin un token real
    # item = resolver_url_a_drive_item(url_ejemplo, token)
    # if item:
    #     print(f"ID del archivo: {item.get('id')}")
    #     print(f"Nombre: {item.get('name')}")
