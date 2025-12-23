"""
Plantillas Generales de Conexión a APIs
=======================================

Este archivo contiene ejemplos de código (snippets) para los métodos de autenticación
más comunes. Puedes copiar y adaptar estas funciones para nuevas integraciones.

Tipos cubiertos:
1. Autenticación Básica (Usuario/Contraseña)
2. Bearer Token (JWT / OAuth2 estándar)
3. API Key en Cabeceras (Headers)
4. API Key en Parámetros (Query Params)
"""

from utils_requests import realizar_peticion_segura
import base64

# --- 1. Autenticación Básica ---
def template_auth_basic(url, usuario, password):
    """
    Ejemplo de Auth Básica.
    Requests lo maneja nativamente con el parámetro `auth`.
    """
    from requests.auth import HTTPBasicAuth
    
    print(f"Conectando a {url} con Auth Básica...")
    
    # Opción A: Usando el objeto auth de requests (Recomendado)
    # respuesta = requests.get(url, auth=HTTPBasicAuth(usuario, password))
    
    # Opción B: Construyendo el header manualmente (Para entenderlo)
    credenciales = f"{usuario}:{password}"
    token_b64 = base64.b64encode(credenciales.encode()).decode()
    headers = {
        "Authorization": f"Basic {token_b64}"
    }
    
    respuesta = realizar_peticion_segura("GET", url, headers=headers)
    return respuesta

# --- 2. Bearer Token (OAuth2) ---
def template_auth_bearer(url, token):
    """
    Estándar para la mayoría de APIs modernas (Stripe, GitHub, etc).
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"Conectando a {url} con Bearer Token...")
    
    respuesta = realizar_peticion_segura("GET", url, headers=headers)
    return respuesta

# --- 3. API Key en Headers ---
def template_apikey_header(url, api_key, key_name="X-API-KEY"):
    """
    Común en servicios SaaS. El nombre del header varía (x-api-key, api-key, etc).
    """
    headers = {
        key_name: api_key
    }
    
    print(f"Conectando a {url} con API Key en Headers...")
    
    respuesta = realizar_peticion_segura("GET", url, headers=headers)
    return respuesta

# --- 4. API Key en Query Params ---
def template_apikey_params(url, api_key, param_name="key"):
    """
    Visto en Google Maps API, Giphy, etc.
    """
    params = {
        param_name: api_key
    }
    
    print(f"Conectando a {url} con API Key en Parametros...")
    
    respuesta = realizar_peticion_segura("GET", url, params=params)
    return respuesta

if __name__ == "__main__":
    print("Este módulo es una librería de plantillas. Importa las funciones que necesites.")
