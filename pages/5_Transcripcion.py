"""
PÁGINA STREAMLIT: SIMULADOR DE TRANSCRIPCIÓN Y TRADUCCIÓN DEL ADN
--------------------------------------------------------------
Este simulador NO fue programado en Python: fue desarrollado en
HTML y JavaScript tradicional (los estilos ya vienen incluidos
dentro del propio HTML, no hay un archivo .css separado). Esta
página no reescribe ese trabajo, solo lo LEE y lo INCRUSTA dentro
de Streamlit, para que funcione como una página más del sitio.

Requisito: los 2 archivos originales deben estar juntos, sin
modificar, dentro de la subcarpeta "transcripcion_assets" al lado
de este script:

pages/
├── 4_Transcripcion.py         <- este archivo
└── transcripcion_assets/
    ├── index.html
    └── script.js
"""

from pathlib import Path
import streamlit as st

st.markdown("### 🧬 Simulador de Transcripción y Traducción del ADN")

st.info(
    "🧭 **Ayuda guiada:** escribe (o elige) una secuencia de ADN, presiona 'Iniciar' y avanza "
    "paso a paso por la transcripción y la traducción. Al final puedes ir a la pestaña "
    "'Autoevaluación' para poner a prueba lo aprendido con mutaciones aleatorias."
)

# ------------------------------------------------------------
# Localizar los 2 archivos originales (deben estar sin modificar)
# ------------------------------------------------------------
carpeta_assets = Path(__file__).parent / "transcripcion_assets"

ruta_html = carpeta_assets / "index.html"
ruta_js = carpeta_assets / "script.js"

archivos_faltantes = [p.name for p in (ruta_html, ruta_js) if not p.exists()]

if archivos_faltantes:
    st.error(
        "⚠️ No se encontraron estos archivos dentro de "
        f"`pages/transcripcion_assets/`: {', '.join(archivos_faltantes)}. "
        "Verifica que index.html y script.js estén en esa carpeta."
    )
else:
    html_original = ruta_html.read_text(encoding="utf-8")
    js_original = ruta_js.read_text(encoding="utf-8")

    # Este archivo no usa style.css separado (los estilos ya están dentro
    # del propio <style> del HTML), así que solo se reemplaza la línea
    # <script src="script.js"></script> por el contenido real del script.
    html_integrado = html_original.replace(
        '<script src="script.js"></script>',
        f"<script>{js_original}</script>"
    )

    # Alto suficiente para mostrar los 5 pasos + pestañas + quiz sin cortar.
    st.components.v1.html(html_integrado, height=1500, scrolling=True)
