import streamlit as st

st.set_page_config(page_title="Simuladores de Bioinformática", page_icon="🧬", layout="centered")

st.title("🧬 Suite de Simuladores Bioinformáticos Educativos")
st.caption("Proyecto de la asignatura de Bioinformática")

st.markdown("""
Bienvenido/a. Este sitio reúne **simuladores interactivos** pensados para
estudiantes de secundaria, cada uno explicando un algoritmo real de
bioinformática de forma visual y guiada.

Usa el menú de la izquierda para navegar entre ellos:

1.  **Alineamiento de secuencias** — Needleman-Wunsch
2.  **Filogenia** — UPGMA
3.  **Modelado estructural de proteínas** — BioPython + 3Dmol.js
4.  **Ensamble de fragmentos** — Grafos de De Bruijn
5.  **Transcripción y traducción del ADN**

""")

st.info("💡 Cada simulador incluye su propio botón de ayuda guiada y un quiz de autoevaluación al final.")

st.markdown("---")
st.caption("Creado por Owen Ranyelis Luciano Valdez y Ruth Margarita Canela Herrera")
