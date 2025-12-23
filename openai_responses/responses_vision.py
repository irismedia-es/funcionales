"""
openai_vision_snippets.py

Objetivo: snippets cortos, modulares y copiables para analizar UNA imagen con la
Responses API (visión). Cambias prompt/model/detail y listo.

Requisitos:
  pip install openai
  export OPENAI_API_KEY="..."
"""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from typing import Literal, Optional

from openai import OpenAI

Detail = Literal["low", "high", "auto"]


# -----------------------------
# 1) Cliente (reutilizable)
# -----------------------------
def get_client() -> OpenAI:
    """
    Devuelve un cliente listo para usar.
    - Lee OPENAI_API_KEY del entorno (recomendado).
    - Si en tu empresa usáis proxy/base_url/headers, centralízalo aquí.
    """
    return OpenAI()


# -----------------------------
# 2) Utilidades de imagen (local -> data URL)
# -----------------------------
def image_file_to_data_url(path: str | Path) -> str:
    """
    Convierte una imagen local a "data:<mime>;base64,<...>".
    Esto permite enviar la imagen embebida sin tener que subirla a ningún sitio.
    """
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"Imagen no encontrada: {p}")

    mime, _ = mimetypes.guess_type(str(p))
    if mime is None:
        # Fallback razonable; idealmente usa extensión correcta (.jpg/.png/.webp)
        mime = "image/jpeg"

    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


# -----------------------------
# 3) Snippet base: analizar imagen (lo que más copiarás)
# -----------------------------
def analyze_image(
    *,
    image: str,  # URL pública o data URL (lo más cómodo: usa image_file_to_data_url)
    prompt: str,
    model: str = "gpt-4.1-mini",
    detail: Detail = "auto",
    client: Optional[OpenAI] = None,
) -> str:
    """
    Snippet minimalista:
    - image: URL pública o data URL
    - prompt: instrucción (lo normal es que solo cambies esto)
    - detail: low/high/auto
    Devuelve: texto final del modelo.
    """
    client = client or get_client()

    resp = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": image, "detail": detail},
                ],
            }
        ],
    )
    return (resp.output_text or "").strip()


# -----------------------------
# 4) Snippets “listos para copiar” (prompts cortos)
#    (En empresa normalmente copias una de estas y ajustas 1-2 líneas)
# -----------------------------
def describe_scene(image: str, *, client: Optional[OpenAI] = None) -> str:
    return analyze_image(
        image=image,
        client=client,
        prompt="Describe la escena en 5 bullets. Incluye objetos, contexto y acción.",
        detail="auto",
    )


def extract_text_ocrish(image: str, *, client: Optional[OpenAI] = None) -> str:
    # Nota: si necesitas OCR “estricto” con bounding boxes, ya es otro flujo.
    return analyze_image(
        image=image,
        client=client,
        prompt="Extrae TODO el texto legible (tal cual). Si hay tablas, respétalas en Markdown.",
        detail="high",
    )


def brand_safety_quickcheck(image: str, *, client: Optional[OpenAI] = None) -> str:
    return analyze_image(
        image=image,
        client=client,
        prompt=(
            "Analiza riesgos básicos de brand safety en esta creatividad.\n"
            "- Contenido sensible (violencia, sexo, drogas, odio)\n"
            "- Claims o mensajes potencialmente problemáticos\n"
            "- Elementos que puedan infringir marca (logos ajenos, copyright evidente)\n"
            "Devuelve una tabla: Riesgo | Evidencia visual | Severidad (Baja/Media/Alta) | Acción sugerida."
        ),
        detail="high",
    )


# -----------------------------
# 5) Ejemplos de uso (copiar/pegar)
# -----------------------------
if __name__ == "__main__":
    client = get_client()

    # A) Imagen LOCAL (lo más habitual en equipos)
    img = image_file_to_data_url("./ejemplos/creatividad.jpg")
    print(describe_scene(img, client=client))

    # B) Imagen por URL
    # img_url = "https://tu-dominio.com/imagen.jpg"
    # print(extract_text_ocrish(img_url, client=client))

    # C) Snippet ultra-directo (el que más se recicla)
    # Cambia SOLO prompt/detail/model:
    # result = analyze_image(
    #     image=img,
    #     prompt="¿Qué producto aparece? Resume en 2 líneas.",
    #     detail="auto",
    #     model="gpt-4.1-mini",
    #     client=client,
    # )
    # print(result)
