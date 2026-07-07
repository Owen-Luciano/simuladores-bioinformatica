import streamlit as st
from graphviz import Digraph
import pandas as pd

# -------------------------------------------------------
# LÓGICA DEL ALGORITMO (Funciones)
# -------------------------------------------------------
def generar_kmers(secuencia, k):
    return [secuencia[i:i+k] for i in range(len(secuencia) - k + 1)]

def obtener_conexiones(kmers):
    conexiones = []
    for kmer in kmers:
        prefijo = kmer[:-1]
        sufijo = kmer[1:]
        conexiones.append({
            "k-mer": kmer,
            "Prefijo": prefijo,
            "Sufijo": sufijo
        })
    return conexiones

def dibujar_grafo(conexiones):
    dot = Digraph()
    dot.attr(rankdir='LR', bgcolor='transparent')  # Fondo transparente para acoplarse al tema
    
    # Estilo de nodos futurista/bio-tech para secundaria
    dot.attr('node', shape='circle', style='filled', 
             color='#a78bfa', fillcolor='#1e1b4b', 
             fontcolor='#38bdf8', fontname='Arial Bold', penwidth='2')
    
    # Estilo de las flechas (aristas)
    dot.attr('edge', color='#38bdf8', fontcolor='#f8fafc', 
             fontname='Arial Italic', fontsize='10', arrowsize='0.8')

    for c in conexiones:
        prefijo = c["Prefijo"]
        sufijo = c["Sufijo"]
        kmer = c["k-mer"]
        dot.node(prefijo)
        dot.node(sufijo)
        dot.edge(prefijo, sufijo, label=f" {kmer} ")

    return dot

# -------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES (CSS)
# -------------------------------------------------------
st.set_page_config(
    page_title="Simulador De Bruijn",
    page_icon="🧬",
    layout="wide"
)

# Inyección de CSS blindado universal (Claro/Oscuro)
st.markdown("""
<style>
/* Forzar fondo general claro y degradado */
.stApp, .main {
    background: linear-gradient(180deg, #fdf6ff 0%, #f2f7ff 100%) !important;
}

/* Forzar color de textos generales y de control */
p, li, span, label, .stMarkdown, .stDataFrame, .stRadio { 
    color: #333333 !important; 
}

/* Títulos y Subtítulos con contraste fijo */
h1 {
    color: #4b2e83 !important; 
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    text-align: center;
    text-shadow: 0px 2px 6px rgba(123, 44, 191, 0.1) !important;
    margin-bottom: 20px !important;
}
h2, h3, h4 {
    color: #7b2cbf !important; 
    font-family: 'Inter', sans-serif;
    font-weight: 700;
}

/* Botones Modernos estilo laboratorio */
div.stButton > button {
    background: linear-gradient(90deg, #7b2cbf 0%, #6366f1 100%) !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 0.6rem 2rem !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 16px !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    transition: all 0.3s ease;
    width: 100%;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
}

/* Cajas de texto e Inputs con fondos legibles */
input {
    background-color: #ffffff !important;
    border: 2px solid #e3d5f5 !important;
    border-radius: 12px !important;
    color: #333333 !important;
}
input:focus {
    border-color: #7b2cbf !important;
}

/* Contenedores y Tarjetas adaptables e inmunes al modo oscuro */
.bio-card {
    background-color: rgba(123, 44, 191, 0.06) !important;
    padding: 22px;
    border-radius: 16px;
    border-left: 6px solid #7b2cbf !important;
    margin-bottom: 20px;
    color: #333333 !important;
}

/* Ajustes de legibilidad para elementos específicos de Streamlit */
.stCaption, figcaption, small, .stWidgetLabel {
    color: #555555 !important;
}
.streamlit-expanderHeader {
    color: #333333 !important;
}

/* MODIFICAR EL TAMAÑO DE LAS PESTAÑAS (TABS) */
button[data-baseweb="tab"] {
    font-size: 20px !important; 
    font-weight: 700 !important; 
    padding: 12px 24px !important; 
    color: #6b7280 !important;
}
button[aria-selected="true"] {
    color: #7b2cbf !important;
}
div[data-baseweb="tab-panel"] {
    font-size: 16px !important;
    padding-top: 20px;
}

/* Separadores Neón Sutiles */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #a78bfa, transparent) !important;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.markdown("<h1>🧬 Secuenciación de ADN: Simulador de Grafos De Bruijn</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='bio-card' style='text-align: center;'>
    ¡Bienvenido al rompecabezas molecular! Las máquinas de secuenciación rompen el ADN en pedazos pequeños. 
    Tu misión aquí es descubrir cómo los científicos vuelven a unir esos pedazos usando matemáticas y grafos.
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# PANEL DE ENTRADA (Organizado en columnas limpias)
# -------------------------------------------------------
st.markdown("### 📥 Configura tus muestras biológicas")
col_in1, col_in2 = st.columns([2, 2])

with col_in1:
    secuencia = st.text_input("Cadena de ADN a fragmentar", "ATGCGAT")
with col_in2:
    k = st.slider("Tamaño del fragmento (Valor de k-mer)", 2, 8, 4)

if "construir" not in st.session_state:
    st.session_state.construir = False

if st.button("🚀 Romper ADN y Empezar Ensamblaje"):
    st.session_state.construir = True

# -------------------------------------------------------
# PROCESAMIENTO Y RENDERIZADO INTERACTIVO
# -------------------------------------------------------
if st.session_state.construir:
    secuencia = secuencia.upper().strip()

    # Validaciones amigables
    if len(secuencia) == 0:
        st.error("❌ ¡Espera! Necesitamos que escribas una secuencia de ADN para trabajar.")
        st.stop()
    if not set(secuencia).issubset({"A", "T", "C", "G"}):
        st.error("❌ Error de código genético: Recuerda usar únicamente las letras válidas (A, T, C, G).")
        st.stop()
    if k >= len(secuencia):
        st.error(f"❌ El tamaño del k-mer ({k}) no puede ser mayor o igual que el largo de tu ADN ({len(secuencia)}). Baja el valor en la barra deslizadora.")
        st.stop()

    st.toast("🧬 Datos listos para secuenciación", icon="🔬")

    # Cálculos algorítmicos base
    kmers = generar_kmers(secuencia, k)
    conexiones = obtener_conexiones(kmers)

    if len(kmers) < 2:
        st.warning("⚠️ La secuencia genera muy pocos fragmentos. Pon una palabra más larga o achica el valor de 'k'.")
        st.stop()

    # =====================================================
    # DISTRIBUCIÓN POR TABS GRANDES (UI REORGANIZADA)
    # =====================================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Guía y Teoría", 
        "🧩 Paso 1: k-mers obtenidos", 
        "🕸️ Paso 2: El Grafo Molecular", 
        "🏆 Reto: Quiz de Laboratorio"
    ])

    # 📥 PESTAÑA 1: TEORÍA DE MANERA EXPANSIBLE
    with tab1:
        st.subheader("🧠 ¿Cómo funciona este mapa de De Bruijn?")
        st.markdown("""
        Imagínate que trituramos muchas copias de un texto y ahora hay que reconstruirlo viendo qué letras se solapan. 
        En biología hacemos exactamente eso mediante estos pasos:
        """)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("""
            * **Paso 1: Cortar en K-mers:** Cortamos la cadena en trozos pequeños de tamaño igual a **$k$**.
            * **Paso 2: Prefijos y Sufijos:** A cada trozo le sacamos su 'inicio' (prefijo) y su 'final' (sufijo), recortando solo $k-1$ letras.
            """)
        with col_t2:
            st.markdown("""
            * **Paso 3: Unir los puntos:** Si el final de un fragmento encaja con el inicio de otro, ¡los conectamos con una flecha!
            * **Paso 4: Reconstrucción:** Caminamos siguiendo las flechas para leer el ADN corrido.
            """)
            
        st.info(f"💡 **Ejemplo en vivo:** Con tus datos, el primer fragmento es **{kmers[0]}**. Su prefijo (inicio) es **{kmers[0][:-1]}** y su sufijo (final) es **{kmers[0][1:]}** (Largo de $k-1 = {k-1}$ letras).")

    # 🔬 PESTAÑA 2: FRAGMENTOS (K-MERS)
    with tab2:
        st.subheader("🧬 Lista de K-mers (Tus fragmentos de ADN)")
        st.write("Aquí están todos los pedacitos en los que se dividió tu secuencia:")
        
        col_list, col_df = st.columns([1, 2])
        with col_list:
            for i, kmer in enumerate(kmers, start=1):
                st.markdown(f"**{i}.** `{kmer}`")
        with col_df:
            # Vista interactiva limpia de la tabla de datos
            tabla = pd.DataFrame({
                "Identificador": [f"Fragmento {i+1}" for i in range(len(kmers))],
                "Código K-mer": kmers
            })
            st.dataframe(tabla, hide_index=True, use_container_width=True)

    # 🕸️ PESTAÑA 3: MAPA / GRAFO Y RECONSTRUCCIÓN
    with tab3:
        st.subheader("🕸️ Red de Conexiones e Historial de Ensamblaje")
        
        # Dashboard de estadísticas rápidas estilo videojuegos
        st.markdown("#### 📊 Métricas del proceso")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Largo ADN original", f"{len(secuencia)} bases")
        m2.metric("Tamaño k", f"{k}")
        m3.metric("Total K-mers", f"{len(kmers)}")
        m4.metric("Conexiones encontradas", f"{len(conexiones)}")
        
        st.divider()
        
        col_g1, col_g2 = st.columns([2, 3])
        with col_g1:
            st.markdown("#### 🔗 Relación de Cruces")
            for c in conexiones:
                st.markdown(f"• `{c['Prefijo']}` $\\rightarrow$ `{c['Sufijo']}` *(vía {c['k-mer']})*")
        
        with col_g2:
            st.markdown("#### 🗺️ Grafo Visual de De Bruijn")
            st.caption("Los nodos representan los extremos y las
