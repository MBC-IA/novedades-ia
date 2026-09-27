# Tablón de novedades de IA

Una web muy sencilla que muestra las novedades de inteligencia artificial del día.
Sirve como ejemplo para aprender a trabajar con GitHub en equipo.

## Qué hay en este repositorio

| Archivo | Para qué sirve |
|---|---|
| `novedades.md` | **El contenido del tablón.** Es un texto normal: aquí se añaden las noticias. |
| `index.html` | La página web. Lee `novedades.md` y lo muestra como tablón. |
| `estilos.css` | Colores y tipografía de la web. |
| `scripts/novedades_rss.py` | El "bot": lee noticias de fuentes RSS y las añade a `novedades.md`. |
| `.github/workflows/novedades-rss.yml` | La automatización (GitHub Action) que ejecuta el bot y propone sus cambios. |

## Cómo añadir una noticia

Cada día es un título `##` con la fecha y cada noticia es un punto de lista:

```markdown
## 2026-09-25

- **Titular de la noticia**: resumen en una o dos frases. [Fuente](https://ejemplo.com)
```

Hay dos maneras de hacerlo:

1. **Edición directa**: abre `novedades.md`, pulsa el lápiz ✏️, escribe y guarda con *Commit changes*.
   Rápido, pero el cambio se publica sin que nadie lo revise.
2. **Con revisión (recomendado)**: al guardar, elige *Create a new branch… and start a pull request*.
   Otra persona revisa el cambio y, cuando lo aprueba, se fusiona (*merge*) con `main`.

## Cómo se publica

La web se publica con **GitHub Pages** desde la rama `main`.
Todo lo que llega a `main` aparece en la web en uno o dos minutos; lo que está en otras ramas, no.

## El bot de novedades

En la pestaña **Actions → Bot de novedades (RSS) → Run workflow** se puede lanzar el bot a mano.
El bot nunca publica directamente: abre un Pull Request para que una persona lo revise.
Para que se ejecute solo cada mañana, hay que activar el bloque `schedule` del archivo del workflow.
