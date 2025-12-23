"""
Gemini API (Google GenAI SDK) - Ejemplo de Function Calling (Herramientas)
--------------------------------------------------------------------------
Demuestra cómo usar herramientas (Tools) con la nueva librería `google-genai`.
El SDK soporta pasar funciones Python directamente y maneja la ejecución automática.

Requisitos:
    pip install google-genai
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

MODELO = "gemini-2.0-flash-exp"

# --- 1. Definir Funciones Python Puras ---

def obtener_clima(ciudad: str) -> str:
    """
    Devuelve el clima actual de una ciudad.
    
    Args:
        ciudad: Nombre de la ciudad (ej. Madrid).
    """
    print(f"\n[TOOL] Consultando clima para: {ciudad}...")
    # Simulación
    datos = {
        "madrid": "Soleado, 22°C",
        "barcelona": "Húmedo, 20°C",
        "bogota": "Llovizna, 14°C"
    }
    return datos.get(ciudad.lower(), "Datos no disponibles")

def calcular_descuento(precio: float, porcentaje: int) -> float:
    """
    Calcula el precio final con descuento.
    
    Args:
        precio: Precio original.
        porcentaje: Porcentaje de descuento (0-100).
    """
    print(f"\n[TOOL] Calculando descuento: {precio} - {porcentaje}%")
    return precio * (1 - porcentaje/100)

# --- 2. Ejecución con Automatic Function Calling ---

def ejemplo_tools_automatico():
    print(f"\n--- Ejemplo: Function Calling Automático ({MODELO}) ---")
    
    # Pasamos las funciones directamente en la lista 'tools' dentro de 'config'.
    # El SDK genera el esquema JSON automáticamente y maneja la llamada.
    
    prompt = "Hace buen tiempo en Madrid hoy? Y si compro algo de 100 euros con 20% de descuento cuanto pago?"
    print(f"Usuario: {prompt}")

    try:
        response = client.models.generate_content(
            model=MODELO,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[obtener_clima, calcular_descuento],
                # automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False) # Default es True si hay tools
                temperature=0 # Temperatura baja para llamadas precisas
            )
        )
        
        # El modelo debería haber llamado a las funciones internamente y generado una respuesta final.
        print(f"\nGemini: {response.text}")
        
        # Podemos inspeccionar las llamadas si quisiéramos (dependiendo de lo que devuelva el objeto response)
        # print(response.function_calls) # Puede estar vacío si la respuesta final ya integró el resultado
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if client:
        ejemplo_tools_automatico()
