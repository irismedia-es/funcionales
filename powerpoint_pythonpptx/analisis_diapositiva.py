from pptx.enum.shapes import MSO_SHAPE_TYPE

def obtener_tipo_forma(shape):
    """
    Devuelve una representación en string del tipo de forma.
    """
    if shape.shape_type == MSO_SHAPE_TYPE.TEXT_BOX:
        return "Caja de Texto"
    elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        return "Imagen"
    elif shape.shape_type == MSO_SHAPE_TYPE.TABLE:
        return "Tabla"
    elif shape.shape_type == MSO_SHAPE_TYPE.CHART:
        return "Gráfico"
    elif shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
        return "AutoForma"
    elif shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        return "Grupo"
    elif shape.shape_type == MSO_SHAPE_TYPE.PLACEHOLDER:
        return f"Placeholder ({shape.name})"
    else:
        return str(shape.shape_type)

def obtener_elementos_diapositiva(slide):
    """
    Analiza una diapositiva y devuelve una lista de sus elementos con propiedades clave.
    
    Args:
        slide (Slide): Objeto de diapositiva.
        
    Returns:
        list: Lista de diccionarios con info de cada elemento.
    """
    elementos = []
    for i, shape in enumerate(slide.shapes):
        info = {
            "indice": i,
            "id": shape.shape_id,
            "nombre": shape.name,
            "tipo": obtener_tipo_forma(shape),
            "izquierda": shape.left,
            "arriba": shape.top,
            "ancho": shape.width,
            "alto": shape.height,
            "texto": shape.text if hasattr(shape, "text") else None
        }
        elementos.append(info)
    return elementos

def imprimir_estructura_diapositiva(slide):
    """
    Imprime en consola la estructura detallada de una diapositiva.
    """
    print(f"\n--- Análisis de Diapositiva (ID: {slide.slide_id}) ---")
    elementos = obtener_elementos_diapositiva(slide)
    if not elementos:
        print("La diapositiva está vacía.")
    
    for elem in elementos:
        print(f"[{elem['indice']}] {elem['tipo']} - '{elem['nombre']}'")
        print(f"    Posición: ({elem['izquierda']}, {elem['arriba']})")
        if elem['texto']:
            # Mostrar solo los primeros 50 caracteres para no saturar
            texto_preview = (elem['texto'][:50] + '...') if len(elem['texto']) > 50 else elem['texto']
            print(f"    Texto: '{texto_preview}'")
    print("------------------------------------------------")
