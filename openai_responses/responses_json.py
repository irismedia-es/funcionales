import os
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI

# =================================================================================================
# PLANTILLA DE GENERACIÓN DE JSON ESTRUCTURADO CON OPENAI (NUEVA API RESPONSES)
# =================================================================================================
#
# OBJETIVO:
# Esta plantilla demuestra el uso de la nueva API `client.responses` para obtener 
# salidas estructuradas validada con Pydantic.
#
# CAMBIOS IMPORTANTES RESPECTO A CHAT COMPLETIONS:
# 1. Método: Se usa `client.responses.parse` en lugar de `client.chat.completions.parse`.
# 2. Parámetros: Se usa `input` para el prompt y `text_format` para el modelo Pydantic.
# 3. Respuesta: La estructura del objeto de respuesta es jerárquica (Output -> Content).
#
# REQUISITOS:
# 1. `pip install openai pydantic`
# 2. API KEY configurada.
# =================================================================================================

# 1. CONFIGURACIÓN DEL CLIENTE
# -------------------------------------------------------------------------------------------------
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 2. DEFINICIÓN DE MODELOS DE DATOS (PYDANTIC)
# -------------------------------------------------------------------------------------------------
# Definimos la estructura exacta que queremos recibir.

class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskItem(BaseModel):
    id: int = Field(..., description="Identificador único.")
    title: str = Field(..., description="Título de la tarea.")
    description: str = Field(..., description="Descripción detallada.")
    priority: PriorityLevel = Field(..., description="Prioridad.")
    estimated_hours: float = Field(..., description="Horas estimadas.")
    assignee: Optional[str] = Field(None, description="Responsable asignado.")
    
    # Método helper para imprimir bonito
    def to_string(self):
        return f"[{self.priority.value.upper()}] {self.title} ({self.estimated_hours}h) - {self.assignee or 'N/A'}"

class ProjectPlan(BaseModel):
    """
    Modelo Raíz que pasaremos a 'text_format'.
    """
    project_name: str = Field(..., description="Nombre del proyecto.")
    summary: str = Field(..., description="Resumen ejecutivo.")
    tasks: List[TaskItem] = Field(..., description="Lista de tareas detectadas.")
    is_feasible: bool = Field(..., description="Viabilidad del proyecto.")

# 3. FUNCIÓN DE EXTRACCIÓN (NUEVA API)
# -------------------------------------------------------------------------------------------------
def extract_with_responses_api(user_input: str) -> Optional[ProjectPlan]:
    """
    Utiliza client.responses.parse para obtener datos estructurados.
    """
    
    print(f"Enviando input a OpenAI Responses API...\nInput: {user_input[:50]}...")
    
    # LLAMADA A LA NUEVA API
    rsp = client.responses.parse(
        model="gpt-4o-2024-08-06", # Asegurarse de usar un modelo compatible
        input=user_input,          # Texto de entrada directo
        text_format=ProjectPlan    # Esquema Pydantic esperado
    )

    # PROCESAMIENTO DE LA RESPUESTA
    # La respuesta puede contener múltiples salidas, iteramos para encontrar la correcta.
    # Estructura típica: Response -> Output (message) -> Content (output_text) -> Parsed Data
    
    for output in rsp.output:
        # Verificamos que sea de tipo mensaje
        if output.type != "message":
            continue

        for item in output.content:
            # Verificamos que sea texto de salida y que haya sido parseado correctamente
            if item.type == "output_text" and item.parsed:
                return item.parsed # Retorna la instancia de ProjectPlan

    return None

# 4. EJEMPLO DE USO
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Prompt que incluye instrucciones implícitas y datos
    raw_prompt = """
    Instrucciones: Analiza el siguiente texto y extrae un plan de proyecto.
    
    Texto: Hola equipo, para el lanzamiento de la web (Proyecto Alpha) necesitamos varias cosas para el viernes.
    Primero, Ana debe diseñar los banners (high priority, 4h). 
    Segundo, Juan tiene que hacer el frontend (medium, 10h).
    Y por último revisar textos (low, 1h), cualquiera puede hacerlo.
    Creo que es viable si nos ponemos las pilas.
    """

    try:
        plan = extract_with_responses_api(raw_prompt)

        if plan:
            print("\n" + "="*50)
            print(f"PLAN GENERADO: {plan.project_name}")
            print("="*50)
            print(f"Resumen: {plan.summary}")
            print(f"Viable:  {'SÍ' if plan.is_feasible else 'NO'}")
            print("-" * 50)
            for task in plan.tasks:
                print(task.to_string())
        else:
            print("No se pudo extraer un plan válido de la respuesta.")

    except Exception as e:
        print(f"\nERROR: {e}")
        print("Nota: Asegúrate de tener la versión más reciente del SDK de OpenAI que soporte 'client.responses'.")