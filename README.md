# Proyecto Funcionales

Este repositorio contiene una colección de scripts y utilidades en Python diseñados para la automatización de tareas y la interacción con diversas APIs y formatos de archivo. El proyecto está organizado en módulos específicos según la tecnología o servicio utilizado.

## Estructura de Archivos

A continuación se detalla la estructura del proyecto y la descripción de cada módulo y archivo.

### 📂 `excel_openpyxl`
Scripts para la manipulación y automatización de archivos Excel utilizando la librería `openpyxl`.

- **`leer_workbook.py`**: Script para abrir, leer y analizar la estructura de libros de Excel existentes.
- **`extraer_campos.py`**: Ejemplos de cómo extraer datos de celdas específicas o relativas a cabeceras conocidas.
- **`escribir_excel.py`**: Demostración de cómo escribir datos, añadir nuevas hojas y modificar celdas en archivos Excel.
- **`funciones.py`**: Implementación de fórmulas y funciones de Excel (como SUMA, PROMEDIO) automatizadas desde Python.
- **`calificaciones.xlsx`**: Archivo de muestra utilizado para pruebas de lectura y escritura.

---

### 📂 `gemini`
Ejemplos de interacción con la API de Google Gemini para generación de texto, análisis de imágenes y uso de herramientas.

- **`gemini_chat.py`**: Implementación básica de un chat interactivo con el modelo Gemini.
- **`gemini_json.py`**: Ejemplo de configuración para obtener respuestas estructuradas en formato JSON.
- **`gemini_tools.py`**: Demostración de Function Calling (uso de herramientas) con Gemini para tareas externas.
- **`gemini_vision.py`**: Uso de las capacidades multimodales de Gemini para analizar y describir imágenes.

---

### 📂 `openai_responses`
Colección de scripts para trabajar con la API de OpenAI (GPT), enfocados en diferentes modalidades de respuesta.

- **`responses.py`**: Ejemplos básicos de solicitud y respuesta de texto con modelos GPT.
- **`responses_json.py`**: Plantilla detallada para la generación y validación de respuestas en formato JSON estructurado.
- **`responses_tool.py`**: Implementación de llamadas a funciones (Function Calling) para integrar capacidades de cómputo o búsqueda.
- **`responses_vision.py`**: Ejemplos de análisis de imágenes utilizando el modelo GPT-4o con capacidades de visión.

---

### 📂 `powerpoint_pythonpptx`
Utilidades para la creación, lectura y modificación programática de presentaciones PowerPoint (.pptx).

- **`generacion_ppt.py`**: Script para crear una nueva presentación desde cero.
- **`lectura_ppt.py`**: Funciones para abrir y leer el contenido de diapositivas existentes.
- **`analisis_diapositiva.py`**: Herramientas para inspeccionar elementos (formas, textos, imágenes) dentro de una diapositiva.
- **`reemplazo_elementos.py`**: Automatización del reemplazo de textos o imágenes en plantillas predefinidas.
- **`creacion_graficos.py`**: Generación automática de gráficos nativos de PowerPoint basados en datos.
- **`modificacion_graficos.py`**: Actualización de datos en gráficos ya existentes en una presentación.
- **`test_completo.py`**: Script de integración que prueba múltiples funcionalidades en flujo.
- **`temp_prueba.pptx` / `resultado_final.pptx`**: Archivos de salida generados durante las pruebas.

### 📂 `sharepoint_graph`
Conjunto de módulos para interactuar con archivos en SharePoint mediante la API de Microsoft Graph.

- **`autenticacion.py`**: Gestión de cabeceras y tokens de acceso para autenticación.
- **`utilidades.py`**: Herramientas para resolver URLs compartidas (Sharing Links) a identificadores de Graph.
- **`descarga.py`**: Funciones para descargar archivos utilizando IDs directos o enlaces públicos.
- **`carga.py`**: Scripts para subir archivos locales a carpetas específicas de SharePoint.
- **`exploracion.py`**: Utilidades para listar contenido de carpetas y recorrer estructuras de directorios recursivamente.

---

## Requisitos

Cada módulo puede requerir dependencias específicas. Asegúrese de tener instaladas las librerías necesarias (como `openpyxl`, `python-pptx`, `google-generativeai`, `openai`) en su entorno virtual.
