import requests

def obtener_headers_auth(token_acceso):
    """
    Genera los encabezados de autenticación necesarios para las llamadas a Microsoft Graph API.

    Args:
        token_acceso (str): El token de acceso de Microsoft Graph (Bearer token).

    Returns:
        dict: Diccionario con los encabezados HTTP, incluyendo 'Authorization'.
    """
    return {
        "Authorization": f"Bearer {token_acceso}",
        "Content-Type": "application/json"
    }

if __name__ == "__main__":
    # Ejemplo de uso
    mi_token = "TU_TOKEN_DE_ACCESO_AQUI"
    headers = obtener_headers_auth(mi_token)
    print("Headers generados:", headers)
