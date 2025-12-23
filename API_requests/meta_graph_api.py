"""
Ejemplo de Conexión a Meta Graph API (Facebook/Instagram)
=========================================================

Este script muestra cómo estructurar peticiones a la API Graph de Meta.
La API de Meta se basa en nodos (objetos), aristas (conexiones) y campos.

Documentación oficial: https://developers.facebook.com/docs/graph-api

Requisitos previos:
- Tener un Access Token (User Token o Page Token).
- Conocer el ID de la página o cuenta publicitaria.
"""

from utils_requests import realizar_peticion_segura # Importamos nuestra utilidad
import json

class MetaGraphConnector:
    """Clase para encapsular la lógica de conexión con Meta."""
    
    BASE_URL = "https://graph.facebook.com/v19.0" # Comprueba siempre la versión más reciente
    
    def __init__(self, access_token: str):
        """
        Inicializa el conector.
        
        Args:
            access_token (str): Token de acceso válido obtenido desde Meta Developers.
        """
        self.access_token = access_token
    
    def obtener_info_pagina(self, page_id: str):
        """
        Obtiene información básica de una página de Facebook.
        """
        endpoint = f"{self.BASE_URL}/{page_id}"
        
        # Parámetros que queremos recibir (fields)
        parametros = {
            "access_token": self.access_token,
            "fields": "id,name,username,followers_count,verification_status"
        }
        
        print(f"Consultando información para la página: {page_id}")
        
        respuesta = realizar_peticion_segura(
            metodo="GET",
            url=endpoint,
            params=parametros
        )
        
        if respuesta:
            data = respuesta.json()
            return data
        else:
            print("No se pudo obtener la información de la página.")
            return None

    def obtener_posts_pagina(self, page_id: str, limite: int = 5):
        """
        Obtiene los últimos posts publicados en la página.
        """
        endpoint = f"{self.BASE_URL}/{page_id}/posts"
        
        parametros = {
            "access_token": self.access_token,
            "fields": "id,message,created_time,type,permalink_url",
            "limit": limite
        }
        
        print(f"Consultando últimos {limite} posts para la página: {page_id}")
        
        respuesta = realizar_peticion_segura("GET", endpoint, params=parametros)
        
        if respuesta:
            data = respuesta.json()
            # La lista de posts suele venir dentro de 'data'
            return data.get('data', [])
        else:
            return []

if __name__ == "__main__":
    # --- ZONA DE CONFIGURACIÓN ---
    # PARA PROBAR ESTO NECESITAS UN TOKEN REAL
    # Puedes obtener uno temporal en: https://developers.facebook.com/tools/explorer/
    
    MI_TOKEN = "TU_ACCESS_TOKEN_AQUI"
    PAGE_ID_EJEMPLO = "me" # "me" funciona si el token es de usuario, o pon el ID numérico
    
    # -----------------------------
    
    api = MetaGraphConnector(MI_TOKEN)
    
    # 1. Probar obtener info
    info = api.obtener_info_pagina(PAGE_ID_EJEMPLO)
    if info:
        print("\nInformación de la Página:")
        print(json.dumps(info, indent=4))
    
    # 2. Probar obtener posts
    if info: 
        # Si obtuvimos info, usamos el ID real (aunque 'me' también sirve a veces)
        posts = api.obtener_posts_pagina(info.get('id', 'me'))
        if posts:
            print(f"\nSe encontraron {len(posts)} posts:")
            for post in posts:
                print(f"- [{post.get('created_time')}] {post.get('message', 'Sin texto')[:50]}...")
