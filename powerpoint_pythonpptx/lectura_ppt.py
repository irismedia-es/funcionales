from pptx import Presentation
import os

def cargar_presentacion(ruta_archivo):
    """
    Carga una presentación existente desde una ruta.
    
    Args:
        ruta_archivo (str): Ruta absoluta al archivo .pptx.
        
    Returns:
        Presentation: Objeto cargado o None si hay error.
    """
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo no existe: {ruta_archivo}")
        return None
    
    try:
        prs = Presentation(ruta_archivo)
        print(f"Presentación cargada desde: {ruta_archivo}")
        return prs
    except Exception as e:
        print(f"Error al cargar la presentación: {e}")
        return None

def listar_layouts(prs):
    """
    Imprime los nombres de los layouts disponibles en el Slide Master.
    Útil para saber cuál elegir.
    """
    print("--- Layouts Disponibles ---")
    for i, layout in enumerate(prs.slide_layouts):
        print(f"Índice {i}: {layout.name}")
    print("-------------------------")

def obtener_layout_por_nombre(prs, nombre_layout):
    """
    Busca y devuelve un layout por su nombre (parcial o exacto).
    
    Args:
        prs (Presentation): La presentación cargada.
        nombre_layout (str): Nombre a buscar (ej: 'Blank').
        
    Returns:
        SlideLayout: El layout encontrado o el layout 0 por defecto.
    """
    for layout in prs.slide_layouts:
        if nombre_layout.lower() in layout.name.lower():
            print(f"Layout encontrado: {layout.name}")
            return layout
            
    print(f"Advertencia: Layout '{nombre_layout}' no encontrado. Usando el índice 0.")
    return prs.slide_layouts[0]
