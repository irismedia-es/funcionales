"""
Gemini API (Google GenAI SDK) - Ejemplo de Visión (Multimodal)
--------------------------------------------------------------
Demuestra cómo analizar imágenes y archivos usando `google-genai`.
Utiliza `client.files.upload` para subir archivos multimedia para el análisis.

Requisitos:
    pip install google-genai
"""

import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

MODELO = "gemini-2.0-flash-exp"

def analizar_imagen_local_upload(ruta_archivo):
    """
    Sube un archivo local a la API de File de Gemini y luego lo usa en el prompt.
    Este es el método recomendado para archivos grandes o persistencia temporal.
    """
    print(f"\n--- Analizando Imagen (Vía Upload): {ruta_archivo} ---")
    
    if not os.path.exists(ruta_archivo):
        print("Error: Archivo no encontrado.")
        return

    try:
        # 1. Subir el archivo
        print("Subiendo archivo...")
        archivo_subido = client.files.upload(file=ruta_archivo)
        print(f"Archivo subido: {archivo_subido.name} ({archivo_subido.uri})")
        
        # Esperar a que se procese si es necesario (generalmente rápido para imágenes)
        # while archivo_subido.state.name == "PROCESSING":
        #    time.sleep(1)
        #    archivo_subido = client.files.get(name=archivo_subido.name)

        # 2. Generar contenido usando el descriptor del archivo
        prompt = "Describe detalladamente esta imagen en español."
        
        response = client.models.generate_content(
            model=MODELO,
            contents=[prompt, archivo_subido] # [Texto, Archivo]
        )
        
        print(f"\nGemini: {response.text}")
        
        # (Opcional) Borrar el archivo si ya no se necesita
        # client.files.delete(name=archivo_subido.name)

    except Exception as e:
        print(f"Error: {e}")

def analizar_imagen_bytes(ruta_archivo):
    """
    Opcional: Envío directo de bytes (types.Part.from_bytes) si se prefiere no usar Upload API.
    A veces es más rápido para imágenes pequeñas efímeras.
    """
    print(f"\n--- Analizando Imagen (Bytes Directos) ---")
    try:
        with open(ruta_archivo, "rb") as f:
            image_bytes = f.read()
            
        response = client.models.generate_content(
            model=MODELO,
            contents=[
                types.Part.from_text(text="¿Qué ves en esta imagen?"),
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg") 
            ]
        )
        print(f"Gemini: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if client:
        # Crear imagen dummy para test
        ruta_test = "prueba_vision.jpg"
        if not os.path.exists(ruta_test):
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='green')
            img.save(ruta_test)
        
        analizar_imagen_local_upload(ruta_test)
        # analizar_imagen_bytes(ruta_test)
