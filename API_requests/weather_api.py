"""
Ejemplo de Conexión a OpenWeatherMap API
========================================

Este script muestra cómo conectar a una API pública sencilla de clima.
Perfecto para probar conexiones sin una configuración OAuth compleja.

Documentación: https://openweathermap.org/api
"""

from utils_requests import realizar_peticion_segura
import os

def obtener_clima_actual(ciudad: str, api_key: str):
    """
    Obtiene el clima actual para una ciudad específica.
    """
    
    # Endpoint base de la API
    # NOTA: Usar unidades 'metric' para Celsius
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    parametros = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",
        "lang": "es" # Respuestas en español
    }
    
    print(f"Consultando clima para: {ciudad}...")
    
    respuesta = realizar_peticion_segura("GET", base_url, params=parametros)
    
    if respuesta:
        datos = respuesta.json()
        
        # Extracción segura de datos anidados
        temp = datos.get("main", {}).get("temp")
        descripcion = datos.get("weather", [{}])[0].get("description")
        humedad = datos.get("main", {}).get("humidity")
        
        print(f"--- Clima en {ciudad} ---")
        print(f"Temperatura: {temp}°C")
        print(f"Descripción: {descripcion}")
        print(f"Humedad: {humedad}%")
        
        return datos
    else:
        print(f"No se pudo obtener el clima para {ciudad}.")
        return None

if __name__ == "__main__":
    # --- ZONA DE CONFIGURACIÓN ---
    # Regístrate gratis en openweathermap.org para obtener una API Key
    API_KEY = "TU_API_KEY_AQUI" 
    CIUDAD_OBJETIVO = "Madrid"
    
    # -----------------------------
    
    # Solo ejecutamos si hay una key definida (o intentamos para mostrar el error 401)
    obtener_clima_actual(CIUDAD_OBJETIVO, API_KEY)
