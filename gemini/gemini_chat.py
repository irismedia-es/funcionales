"""
Gemini API (Google GenAI SDK) - Ejemplo de Chat y Texto Básico
--------------------------------------------------------------
Este script utiliza la nueva librería `google-genai` (v1.0+).
Demuestra cómo:
1. Inicializar el cliente `genai.Client`.
2. Generar contenido simple.
3. Gestionar un chat manteniendo el historial manualmente (o usando helpers si disponibles).

Requisitos:
    pip install google-genai python-dotenv
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# --- 1. Configuración del Cliente ---
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY no encontrada.")
else:
    # El cliente lee automáticamente GOOGLE_API_KEY si está en el entorno,
    # pero podemos pasarla explícitamente.
    client = genai.Client(api_key=api_key)

# Modelo a usar (según ejemplos recientes: gemini-2.0-flash o variantes preview)
MODELO = "gemini-2.0-flash-exp" 

def ejemplo_generacion_simple():
    """
    Generación de texto simple sin contexto.
    """
    print(f"\n--- Ejemplo 1: Generación Simple ({MODELO}) ---")
    prompt = "Explica en una frase qué es la Inteligencia Artificial Generativa."
    
    try:
        response = client.models.generate_content(
            model=MODELO,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=500
            )
        )
        print(f"Gemini: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

def ejemplo_chat_manual():
    """
    Simulación de Chat manteniendo el historial de mensajes 'contents'.
    En el nuevo SDK, pasamos una lista de mensajes previos.
    """
    print(f"\n--- Ejemplo 2: Chat Interactivo ({MODELO}) ---")
    
    # Historial inicial
    chat_history = []
    
    print("Escribe 'salir' para terminar.")
    
    while True:
        user_input = input("\nTú: ")
        if user_input.lower() in ["salir", "exit"]:
            break
        
        # 1. Agregar mensaje del usuario al historial
        # El SDK acepta strings directos que convierte a types.UserContent,
        # o objetos types.Content explícitos.
        chat_history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)]
            )
        )
        
        try:
            # 2. Enviar todo el historial al modelo
            response = client.models.generate_content(
                model=MODELO,
                contents=chat_history,
                config=types.GenerateContentConfig(
                    system_instruction="Eres un asistente útil y respondes siempre en español."
                )
            )
            
            print(f"Gemini: {response.text}")
            
            # 3. Agregar respuesta del modelo al historial para mantener el contexto
            chat_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=response.text)]
                )
            )
            
        except Exception as e:
            print(f"Error en el chat: {e}")

if __name__ == "__main__":
    if "client" in locals():
        ejemplo_generacion_simple()
        # Descomentar para probar chat
        # ejemplo_chat_manual()
