"""
Módulo de Utilidades para Peticiones HTTP
=========================================

Este módulo proporciona una envoltura robusta alrededor de la librería `requests`
para manejar peticiones HTTP de manera segura, con reintentos automáticos,
gestión de errores y logging detallado.

Ideal para ser importado en otros scripts que requieran interactuar con APIs externas.
"""

import requests
import logging
import time
from typing import Dict, Any, Optional

# Configuración básica de logging para ver qué está pasando
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def realizar_peticion_segura(
    metodo: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    intentos_maximos: int = 3,
    espera_inicial: int = 2
) -> Optional[requests.Response]:
    """
    Realiza una petición HTTP manejando posibles errores de conexión y timeouts.
    
    Args:
        metodo (str): El método HTTP a usar ('GET', 'POST', 'PUT', 'DELETE', etc.).
        url (str): La URL endpoint de la API.
        headers (dict, opcional): Diccionario de cabeceras HTTP.
        params (dict, opcional): Parámetros para la URL (query strings).
        data (dict, opcional): Datos para enviar en el cuerpo (form-encoded).
        json_data (dict, opcional): Datos para enviar en el cuerpo como JSON.
        intentos_maximos (int): Número máximo de reintentos en caso de fallo.
        espera_inicial (int): Segundos a esperar antes del primer reintento. El tiempo se duplica en cada fallo (backoff exponencial).
        
    Returns:
        response (requests.Response): Objeto de respuesta si la petición fue exitosa.
        None: Si la petición falló después de todos los intentos.
    """
    
    intentos = 0
    espera = espera_inicial
    
    # Aseguramos que el método esté en mayúsculas
    metodo = metodo.upper()
    
    while intentos < intentos_maximos:
        try:
            logger.info(f"Iniciando petición {metodo} a: {url} (Intento {intentos + 1}/{intentos_maximos})")
            
            # Ejecutamos la petición usando requests.request que cubre todos los métodos
            response = requests.request(
                method=metodo,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                timeout=30  # Timeout de 30 segundos para evitar bloqueos infinitos
            )
            
            # verificamos el código de estado
            # raise_for_status() lanzará una excepción si el código es 4xx o 5xx
            response.raise_for_status()
            
            logger.info(f"Petición exitosa. Código de estado: {response.status_code}")
            return response
            
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout al conectar con {url}. Reintentando en {espera} segundos...")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Error de conexión con {url}. Reintentando en {espera} segundos...")
        except requests.exceptions.HTTPError as err:
            logger.error(f"Error HTTP: {err}")
            # Si es un error 404 (Not Found) o 400 (Bad Request), a veces no queremos reintentar
            # pero para este ejemplo genérico, simplemente logueamos y decidimos si continuar.
            # Un 503 (Service Unavailable) o 500 (Server Error) son buenos candidatos para reintentar.
            if response.status_code in [400, 401, 403, 404]:
                 logger.error("Error de cliente, no se reintentará.")
                 return None
            
        except requests.exceptions.RequestException as err:
            logger.error(f"Error inesperado: {err}")
            
        # Lógica de reintento (Backoff exponencial)
        intentos += 1
        time.sleep(espera)
        espera *= 2 # Duplicamos el tiempo de espera para el siguiente intento
        
    logger.error(f"Fallo al realizar la petición a {url} después de {intentos_maximos} intentos.")
    return None

if __name__ == "__main__":
    # Bloque de prueba simple
    print("Probando script de utilidades...")
    
    # URL de prueba (una API que devuelve la IP actual)
    url_prueba = "https://httpbin.org/get"
    
    respuesta = realizar_peticion_segura("GET", url_prueba)
    
    if respuesta:
        print("Datos recibidos:")
        print(respuesta.json())
