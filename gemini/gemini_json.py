"""
Gemini API (Google GenAI SDK) - Ejemplo de Salida Estructurada (JSON)
---------------------------------------------------------------------
Demuestra cómo obtener respuestas JSON validas usando Pydantic y `response_schema`.

Requisitos:
    pip install google-genai pydantic
"""

from pydantic import BaseModel, Field
from typing import List
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

MODELO = "gemini-2.0-flash-exp"

# --- Definición de Esquemas con Pydantic ---

class Ingrediente(BaseModel):
    nombre: str
    cantidad: str
    calorias_aprox: int

class Receta(BaseModel):
    nombre_plato: str = Field(description="Nombre del plato")
    pais_origen: str
    ingredientes: List[Ingrediente]
    pasos: List[str]
    tiempo_preparacion_min: int

def generar_json_estructurado():
    print(f"\n--- Generando JSON Estructurado ({MODELO}) ---")
    
    prompt = "Dame una receta tradicional japonesa que no sea Sushi."
    
    try:
        # Pasamos la clase Pydantic directamente a 'response_schema'
        # y especificamos el MIME type json.
        response = client.models.generate_content(
            model=MODELO,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Receta 
            )
        )
        
        print("Respuesta Texto (JSON raw):")
        print(response.text)
        
        # El SDK nuevo a veces tiene propiedad '.parsed' si se usa schema,
        # o podemos parsearlo nosotros.
        # En la versión beta, response.parsed devuelve una instancia del modelo Pydantic si es posible.
        
        if hasattr(response, 'parsed') and response.parsed:
            print("\n--- Objeto Parseado (Pydantic) ---")
            receta: Receta = response.parsed
            print(f"Plato: {receta.nombre_plato}")
            print(f"Origen: {receta.pais_origen}")
            print(f"Ingredientes: {len(receta.ingredientes)}")
            for ing in receta.ingredientes:
                print(f" - {ing.nombre}: {ing.cantidad}")
        else:
            # Fallback manual
            import json
            data = json.loads(response.text)
            print("\n(Parseado manualmente con json.loads)")
            print(data)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if client:
        generar_json_estructurado()
