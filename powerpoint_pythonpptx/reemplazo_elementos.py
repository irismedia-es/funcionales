def reemplazar_texto_en_forma(shape, texto_nuevo):
    """
    Reemplaza el texto de una forma preservando, si es posible, el formato básico.
    
    Args:
        shape: Objeto shape de pptx que contiene texto.
        texto_nuevo (str): El nuevo texto a insertar.
        
    Returns:
        bool: True si se realizó el reemplazo, False si la forma no tiene texto.
    """
    if not shape.has_text_frame:
        return False
    
    text_frame = shape.text_frame
    
    # Estrategia simple: reemplazar texto en el primer run del primer párrafo 
    # y borrar el resto para mantener el estilo del inicio.
    if len(text_frame.paragraphs) > 0:
        p = text_frame.paragraphs[0]
        if len(p.runs) > 0:
            p.runs[0].text = texto_nuevo
            # Limpiar runs extra en el primer párrafo
            for i in range(len(p.runs) - 1, 0, -1):
                p.runs[i].text = ""
        else:
            p.text = texto_nuevo
            
        # Limpiar párrafos extra
        for i in range(len(text_frame.paragraphs) - 1, 0, -1):
            # No hay método directo para borrar párrafos fácilmente en todas las versiones,
            # así que vaciamos el texto.
            text_frame.paragraphs[i].text = ""
            
    else:
        text_frame.text = texto_nuevo
        
    return True

def reemplazar_texto_en_diapositiva(slide, texto_buscar, texto_reemplazar):
    """
    Busca una cadena específica en toda la diapositiva y la reemplaza.
    Nota: Esto es una búsqueda simple y puede romper formatos si el texto buscado
    está dividido en múltiples 'runs'.
    
    Args:
        slide: Objeto diapositiva.
        texto_buscar (str): Texto a encontrar.
        texto_reemplazar (str): Texto nuevo.
        
    Returns:
        int: Número de reemplazos realizados.
    """
    reemplazos = 0
    for shape in slide.shapes:
        if shape.has_text_frame:
            # Iterar por párrafos y runs para ser más granular
            for paragraph in shape.text_frame.paragraphs:
                # Un enfoque simple es chequear el texto completo del párrafo
                if texto_buscar in paragraph.text:
                    # Reemplazo directo en el texto del párrafo (puede perder formato de runs individuales)
                    paragraph.text = paragraph.text.replace(texto_buscar, texto_reemplazar)
                    reemplazos += 1
    return reemplazos
