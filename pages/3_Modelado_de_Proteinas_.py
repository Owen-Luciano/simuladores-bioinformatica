"""
🧬 SIMULADOR 3: MODELADO ESTRUCTURAL DE PROTEÍNAS
--------------------------------------------------------------
Guía didáctica e interactiva para estudiantes de secundaria.
Usa BioPython para analizar la estructura de una proteína real
(descargada del Protein Data Bank) y 3Dmol.js para visualizarla
en 3D, girarla y explorarla desde el navegador.

Cómo ejecutarlo:
    1. Instala las librerías necesarias (una sola vez):
       pip install streamlit biopython py3Dmol matplotlib
    2. Ejecuta en la terminal:
       streamlit run simulador_proteinas.py

Nota: se necesita conexión a internet para descargar las
estructuras desde el Protein Data Bank (rcsb.org).
"""

import os
import streamlit as st
import py3Dmol
import matplotlib.pyplot as plt
from Bio.PDB import PDBList, PDBParser
from Bio.PDB.Polypeptide import is_aa
from Bio.SeqUtils import seq1

# ============================================================
# CONFIGURACIÓN Y ESTILO GENERAL
# ============================================================
st.set_page_config(page_title="Simulador de Proteínas", page_icon="🧬", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #fdf6ff 0%, #f2f7ff 100%); }
    h1, h2, h3 { color: #4b2e83; }
    .stButton>button {
        background-color: #7b2cbf;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1.3em;
        font-weight: bold;
        border: none;
    }
    .tarjeta {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 1.1em;
        border: 1px solid #e3d5f5;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("🧬 Simulador de Modelado Estructural de Proteínas")
st.caption("Explora cómo lucen las proteínas en 3D y descubre su lenguaje oculto: los aminoácidos.")

st.info(
    "**¿Qué vamos a hacer?**\n\n"
    "Las proteínas no son solo una lista de letras: se doblan en el espacio hasta formar "
    "figuras 3D muy precisas, y esa forma define su función. Aquí vas a cargar una proteína real, "
    "verla girar en 3D y analizar de qué aminoácidos está hecha."
)

# ============================================================
# GUÍA TEÓRICA (NIVELES DE ESTRUCTURA)
# ============================================================
# ============================================================
# BOTÓN DE AYUDA GUIADA
# ============================================================
if "mostrar_ayuda" not in st.session_state:
    st.session_state.mostrar_ayuda = False

if st.button("Ayuda guiada: ¿cómo uso este simulador?"):
    st.session_state.mostrar_ayuda = not st.session_state.mostrar_ayuda 

if st.session_state.mostrar_ayuda:
    st.markdown(
        """
        <div class='tarjeta'>
        <b>Sigue estos pasos:</b><br><br>
        1️⃣ Elige una proteína conocida del listado (o escribe tu propio código PDB).<br>
        2️⃣ Selecciona el estilo de dibujo (cinta, varillas o esferas) y el esquema de color.<br>
        3️⃣ Presiona <b>"Cargar y analizar proteína"</b> y espera a que se descargue.<br>
        4️⃣ Observa los datos generales: número de cadenas y aminoácidos totales.<br>
        5️⃣ Revisa el gráfico de composición de aminoácidos.<br>
        6️⃣ Explora el modelo 3D: arrastra con el mouse para rotar y usa la rueda para el zoom.<br>
        7️⃣ Baja hasta el final y responde el quiz para autoevaluarte. ✅
        </div>
        """,
        unsafe_allow_html=True
    )

with st.expander("📘 Los 4 niveles de estructura de una proteína (haz clic para ver)"):
    st.markdown("""
    | Nivel | ¿Qué es? |
    |---|---|
    |  **Primaria** | La secuencia de aminoácidos, uno detrás de otro, como cuentas de un collar. |
    |  **Secundaria** | Pliegues locales: hélices (α) y láminas (β) que forman patrones repetidos. |
    |  **Terciaria** | El doblado completo de toda la cadena en una forma 3D única. |
    |  **Cuaternaria** | Cuando varias cadenas (subunidades) se unen para formar la proteína final. |
    """)
    st.caption("💡 En este simulador vas a observar sobre todo la estructura terciaria (y cuaternaria si hay varias cadenas).")

# ============================================================
# PASO 1: ELEGIR LA PROTEÍNA
# ============================================================
st.markdown("### 1️⃣ Elige una proteína para explorar")

proteinas_ejemplo = {
    "Hemoglobina (transporta oxígeno en la sangre)": "1HHO",
    "Insulina (regula el azúcar en la sangre)": "4INS",
    "Lisozima (destruye bacterias, está en la saliva y lágrimas)": "1LYZ",
    "Mioglobina (almacena oxígeno en los músculos)": "1MBN"
}

eleccion = st.selectbox("Proteínas conocidas:", list(proteinas_ejemplo.keys()))
pdb_id = proteinas_ejemplo[eleccion]

st.markdown("### 2️⃣ Elige cómo quieres visualizarla")
col1, col2 = st.columns(2)
with col1:
    estilo = st.selectbox("Estilo de dibujo", ["cartoon (cinta)", "stick (varillas)", "sphere (esferas)"])
with col2:
    color = st.selectbox("Colores", ["spectrum (arcoíris)", "chain (por cadena)", "residue_type (por tipo de aminoácido)"])

cargar = st.button("🔬 Cargar y analizar proteína")

# ============================================================
# FUNCIONES
# ============================================================
@st.cache_data(show_spinner=False)
def descargar_estructura(codigo_pdb):
    """Descarga el archivo PDB de la proteína desde el Protein Data Bank."""
    pdbl = PDBList(verbose=False)
    ruta = pdbl.retrieve_pdb_file(codigo_pdb, pdir="pdb_temp", file_format="pdb")
    return ruta


def analizar_estructura(ruta_archivo, codigo_pdb):
    """
    Usa BioPython para leer la estructura y extraer:
    - número de cadenas
    - número de residuos (aminoácidos)
    - composición de aminoácidos (para el gráfico)
    """
    parser = PDBParser(QUIET=True)
    estructura = parser.get_structure(codigo_pdb, ruta_archivo)

    cadenas = list(estructura.get_chains())
    composicion = {}
    total_residuos = 0

    for cadena in cadenas:
        for residuo in cadena:
            if is_aa(residuo, standard=True):
                total_residuos += 1
                letra = seq1(residuo.get_resname())
                composicion[letra] = composicion.get(letra, 0) + 1

    return len(cadenas), total_residuos, composicion


def dibujar_composicion(composicion):
    """Genera un gráfico de barras simple con la frecuencia de cada aminoácido."""
    letras = sorted(composicion.keys())
    valores = [composicion[l] for l in letras]

    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(letras, valores, color="#9d4edd")
    ax.set_xlabel("Aminoácido (código de 1 letra)")
    ax.set_ylabel("Cantidad")
    ax.set_title("Composición de aminoácidos")
    return fig


def mostrar_3d(ruta_archivo, estilo, color):
    """Construye la visualización 3D interactiva con 3Dmol.js y la incrusta en Streamlit."""
    with open(ruta_archivo, "r") as f:
        contenido_pdb = f.read()

    vista = py3Dmol.view(width=650, height=450)
    vista.addModel(contenido_pdb, "pdb")

    esquema_color = {
        "spectrum (arcoíris)": "spectrum",
        "chain (por cadena)": "chain",
        "residue_type (por tipo de aminoácido)": "amino"
    }[color]

    if estilo.startswith("cartoon"):
        vista.setStyle({"cartoon": {"color": esquema_color}})
    elif estilo.startswith("stick"):
        vista.setStyle({"stick": {"colorscheme": esquema_color}})
    else:
        vista.setStyle({"sphere": {"colorscheme": esquema_color}})

    vista.zoomTo()
    vista.spin(True)
    return vista._make_html()


# ============================================================
# LÓGICA PRINCIPAL
# ============================================================
if cargar:
    if not pdb_id or len(pdb_id) < 4:
        st.error("⚠️ Escribe un código PDB válido (4 caracteres, ejemplo: 1LYZ).")
    else:
        with st.spinner(f"Descargando y analizando la proteína {pdb_id}..."):
            try:
                ruta = descargar_estructura(pdb_id)
                num_cadenas, num_residuos, composicion = analizar_estructura(ruta, pdb_id)
            except Exception:
                st.error(
                    "❌ No se pudo descargar o leer esa proteína. "
                    "Revisa que el código PDB exista en rcsb.org e inténtalo de nuevo."
                )
                st.stop()

        st.success(f"✅ Proteína **{pdb_id}** cargada correctamente.")

        # --- Estadísticas rápidas ---
        st.markdown("### 📊 Datos generales de la proteína")
        c1, c2 = st.columns(2)
        c1.metric("Cadenas (subunidades)", num_cadenas)
        c2.metric("Aminoácidos totales", num_residuos)

        if num_cadenas > 1:
            st.info("🔗 Esta proteína tiene **más de una cadena**: eso es estructura **cuaternaria**.")
        else:
            st.info("🧩 Esta proteína tiene **una sola cadena**: observa su plegado, es estructura **terciaria**.")

        # --- Gráfico de composición ---
        st.markdown("### 🧬 Composición de aminoácidos")
        st.pyplot(dibujar_composicion(composicion))
        st.caption("🔍 Fíjate cuáles aminoácidos son más frecuentes: no todas las proteínas usan los 20 en la misma proporción.")

        # --- Visualización 3D ---
        st.markdown("### Visualización 3D interactiva")
        st.caption("Arrastra con el mouse para rotar, usa la rueda para hacer zoom.")
        html_3d = mostrar_3d(ruta, estilo, color)
        st.components.v1.html(html_3d, height=470, scrolling=False)

        with st.expander("🧠 ¿Qué debo observar en el modelo 3D?"):
            st.markdown("""
            - Las **zonas en forma de espiral** son hélices alfa (estructura secundaria).
            - Las **zonas planas tipo cinta o flecha** son láminas beta (estructura secundaria).
            - La **forma general doblada** de toda la cadena es la estructura terciaria.
            - Si ves **varios colores separados por cadena**, esa proteína tiene estructura cuaternaria.
            """)

# ============================================================
# AUTOEVALUACIÓN (QUIZ FINAL)
# ============================================================
st.markdown("---")
st.markdown("## 🧪 Autoevaluación rápida")
st.caption("Responde estas preguntas para comprobar qué aprendiste.")

preguntas = {
    "¿Qué es la estructura primaria de una proteína?": {
        "opciones": [
            "La secuencia de aminoácidos en orden",
            "La forma final en 3D de toda la proteína",
            "La unión de varias cadenas distintas"
        ],
        "correcta": 0
    },
    "¿Qué representa una hélice alfa o una lámina beta?": {
        "opciones": [
            "Estructura primaria",
            "Estructura secundaria",
            "Estructura cuaternaria"
        ],
        "correcta": 1
    },
    "Si una proteína tiene varias cadenas unidas, ¿qué nivel de estructura tiene?": {
        "opciones": [
            "Primaria",
            "Secundaria",
            "Cuaternaria"
        ],
        "correcta": 2
    },
    "¿Para qué sirve visualizar una proteína en 3D?": {
        "opciones": [
            "Solo para que se vea bonita",
            "Para entender su forma y cómo esa forma explica su función",
            "Para contar cuántas letras tiene su nombre"
        ],
        "correcta": 1
    }
}

aciertos = 0
for pregunta, datos in preguntas.items():
    st.markdown(f"**{pregunta}**")
    respuesta = st.radio(" ", datos["opciones"], key=pregunta, label_visibility="collapsed")
    if datos["opciones"].index(respuesta) == datos["correcta"]:
        aciertos += 1

if st.button("✅ Revisar mis respuestas"):
    st.write(f"Obtuviste **{aciertos} de {len(preguntas)}** respuestas correctas.")
    if aciertos == len(preguntas):
        st.balloons()
        st.success("¡Perfecto! Entendiste muy bien los niveles de estructura de las proteínas.")
    elif aciertos > 0:
        st.info("Buen intento. Repasa la guía teórica de arriba para reforzar lo que falta.")
    else:
        st.warning("Vuelve a leer la sección de 'Los 4 niveles de estructura' y vuelve a intentarlo.")
# ============================================================
# CRÉDITOS
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 1em; color: #6b6b6b; font-size: 0.9em;'>
        🧬 Creado por <b>Owen Ranyelis Luciano Valdez</b> y <b>Ruth Margarita Canela Herrera</b><br>
        Proyecto realizado para la asignatura de <b>Bioinformática</b>
    </div>
    """,
    unsafe_allow_html=True
)