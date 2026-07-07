"""
🌳 PÁGINA STREAMLIT: SIMULADOR DE FILOGENIA (UPGMA)
--------------------------------------------------------------
Este simulador NO fue programado en Python: fue desarrollado en
HTML, CSS y JavaScript tradicional. Esta página no reescribe ese
trabajo, solo lo LEE y lo INCRUSTA dentro de Streamlit, para que
funcione como una página más del sitio integrado.

Requisito: los 3 archivos originales deben estar juntos, sin
modificar, dentro de la subcarpeta "filogenia_assets" al lado de
este script:

pages/
├── 3_🌳_Filogenia.py        <- este archivo
└── filogenia_assets/
    ├── index.html
    ├── style.css
    └── script.js
"""

from pathlib import Path
import streamlit as st

st.markdown("### 🌳 Simulador de Filogenia (UPGMA)")

st.info(
    "🧭 **Ayuda guiada:** escribe el nombre de 4 especies, completa la matriz de "
    "distancias (o presiona 'Cargar Ejemplo'), y presiona 'Construir Árbol' para "
    "ver cómo el algoritmo UPGMA agrupa las especies paso a paso."
)

# ------------------------------------------------------------
# Localizar los 3 archivos originales (deben estar sin modificar)
# ------------------------------------------------------------
carpeta_assets = Path(__file__).parent / "filogenia_assets"

ruta_html = carpeta_assets / "index.html"
ruta_css = carpeta_assets / "style.css"
ruta_js = carpeta_assets / "script.js"

archivos_faltantes = [p.name for p in (ruta_html, ruta_css, ruta_js) if not p.exists()]

if archivos_faltantes:
    st.error(
        "⚠️ No se encontraron estos archivos dentro de "
        f"`pages/filogenia_assets/`: {', '.join(archivos_faltantes)}. "
        "Verifica que index.html, style.css y script.js estén en esa carpeta."
    )
else:
    html_original = ruta_html.read_text(encoding="utf-8")
    css_original = ruta_css.read_text(encoding="utf-8")
    js_original = ruta_js.read_text(encoding="utf-8")

    # Streamlit no puede cargar archivos externos (style.css / script.js) por
    # una ruta relativa dentro del recuadro incrustado, así que se insertan
    # directamente en el HTML, en el mismo lugar donde el archivo original
    # los referenciaba con <link> y <script src="...">.
    html_integrado = html_original.replace(
        '<link rel="stylesheet" href="style.css">',
        f"<style>{css_original}</style>"
    ).replace(
        '<script src="script.js"></script>',
        f"<script>{js_original}</script>"
    )

    # Alto suficiente para mostrar todo el simulador sin cortar contenido
    # (tabla + botones + explicación + árbol + quiz + ayuda + créditos).
    st.components.v1.html(html_integrado, height=1650, scrolling=True)
