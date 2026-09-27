"""Lee titulares de IA de varias fuentes RSS y los añade a novedades.md bajo la fecha de hoy.

Solo usa la biblioteca estándar de Python. Si no hay titulares nuevos, no modifica nada.
"""

import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FUENTES = [
    ("Google Noticias", "https://news.google.com/rss/search?q=%22inteligencia+artificial%22+when:1d&hl=es&gl=ES&ceid=ES:es"),
    ("TechCrunch", "https://techcrunch.com/category/artificial-intelligence/feed/"),
]
MAX_POR_FUENTE = 3
ANTIGUEDAD_MAXIMA = timedelta(hours=36)
ARCHIVO = Path(__file__).resolve().parent.parent / "novedades.md"


def leer_fuente(nombre, url):
    peticion = urllib.request.Request(url, headers={"User-Agent": "novedades-ia-bot/1.0"})
    with urllib.request.urlopen(peticion, timeout=20) as respuesta:
        raiz = ET.fromstring(respuesta.read())

    limite = datetime.now(timezone.utc) - ANTIGUEDAD_MAXIMA
    titulares = []
    for item in raiz.iter("item"):
        titulo = (item.findtext("title") or "").strip()
        enlace = (item.findtext("link") or "").strip()
        if not titulo or not enlace:
            continue
        try:
            if parsedate_to_datetime(item.findtext("pubDate")) < limite:
                continue
        except (TypeError, ValueError):
            pass
        medio = (item.findtext("source") or nombre).strip()
        titulo = titulo.removesuffix(f" - {medio}")  # Google Noticias repite el medio al final del titular
        titulares.append((titulo, enlace, medio))
        if len(titulares) == MAX_POR_FUENTE:
            break
    return titulares


def limpiar(texto):
    # Evita que caracteres de Markdown rompan el formato de la lista
    return re.sub(r"[*_\[\]`]", "", texto)


def main():
    contenido = ARCHIVO.read_text(encoding="utf-8")
    ya_publicados = set(re.findall(r"\]\((https?://[^)]+)\)", contenido))

    lineas = []
    for nombre, url in FUENTES:
        try:
            titulares = leer_fuente(nombre, url)
        except Exception as error:  # una fuente caída no debe parar al resto
            print(f"Aviso: no se pudo leer {nombre}: {error}")
            continue
        for titulo, enlace, medio in titulares:
            if enlace in ya_publicados:
                continue
            lineas.append(f"- **{limpiar(titulo)}** · {limpiar(medio)}. [Leer noticia]({enlace})")

    if not lineas:
        print("No hay titulares nuevos.")
        return

    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cabecera = f"## {hoy}"
    bloque = "\n".join(lineas)

    if cabecera in contenido:
        # Añade las noticias justo debajo del título del día
        contenido = contenido.replace(f"{cabecera}\n\n", f"{cabecera}\n\n{bloque}\n", 1)
    else:
        # Crea el día nuevo encima del más reciente
        posicion = contenido.find("\n## ")
        nuevo = f"\n{cabecera}\n\n{bloque}\n"
        contenido = contenido + nuevo if posicion == -1 else contenido[:posicion] + nuevo + contenido[posicion:]

    ARCHIVO.write_text(contenido, encoding="utf-8")
    print(f"Añadidos {len(lineas)} titulares a {ARCHIVO.name}.")


if __name__ == "__main__":
    main()
