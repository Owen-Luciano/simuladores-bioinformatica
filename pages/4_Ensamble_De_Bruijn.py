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

st.markdown("""
<style>
/* Fondo general con degradado biológico moderno */
.main {
    background: linear-gradient(135deg, #090d16 0%, #111827 100%);
    color: #f8fafc;
}

/* Títulos y Subtítulos dinámicos */
h1 {
    color: #38bdf8 !important;
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    text-align: center;
    text-shadow: 0px 4px 12px rgba(56, 189, 248, 0.2);
}
h2, h3 {
    color: #a78bfa !important;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
}

/* Botones Modernos estilo laboratorio */
div.stButton > button {
    background: linear-gradient(90deg, #0284c7 0%, #6366f1 100%) !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 0.6rem 2rem !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 16px !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    transition: all 0.3s ease;
    width: 100%;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
}

/* Cajas de texto e Inputs */
input {
    background-color: #1f2937 !important;
    border: 2px solid #374151 !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
}
input:focus {
    border-color: #38bdf8 !important;
}

/* Contenedores visuales estéticos */
.bio-card {
    background-color: rgba(31, 41, 55, 0.6);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(56, 189, 248, 0.2);
    margin-bottom: 20px;
    backdrop-filter: blur(8px);
}

/* =====================================================
MODIFICAR EL TAMAÑO DE LAS PESTAÑAS (TABS) - ¡TUS FAVORITAS!
===================================================== */
button[data-baseweb="tab"] {
    font-size: 20px !important; 
    font-weight: 700 !important; 
    padding: 12px 24px !important; 
    color: #9ca3af !important;
}
button[aria-selected="true"] {
    color: #38bdf8 !important;
}
div[data-baseweb="tab-panel"] {
    font-size: 16px !important;
    padding-top: 20px;
}

/* Separadores Neón */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #a78bfa, transparent);
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
            *   **Paso 1: Cortar en K-mers:** Cortamos la cadena en trozos pequeños de tamaño igual a **$k$**.
            *   **Paso 2: Prefijos y Sufijos:** A cada trozo le sacamos su 'inicio' (prefijo) y su 'final' (sufijo), recortando solo $k-1$ letras.
            """)
        with col_t2:
            st.markdown("""
            *   **Paso 3: Unir los puntos:** Si el final de un fragmento encaja con el inicio de otro, ¡los conectamos con una flecha!
            *   **Paso 4: Reconstrucción:** Caminamos siguiendo las flechas para leer el ADN corrido.
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
            st.caption("Los nodos representan los extremos y las flechas con letras son tus k-mers. ¡Sigue las flechas para armarlo!")
            grafo = dibujar_grafo(conexiones)
            st.graphviz_chart(grafo, use_container_width=True)

        st.divider()
        st.markdown("### 🗺️ El camino de reconstrucción paso a paso")
        
        # Animación visual simulada del armado paso a paso
        reconstruccion = kmers[0]
        st.markdown(f"🟩 **Punto de Partida:** Empezamos leyendo el primer bloque: `{reconstruccion}`")
        
        for i in range(1, len(kmers)):
            reconstruccion += kmers[i][-1]
            st.markdown(f"➡️ **Paso {i}:** Enganchamos la letra **{kmers[i][-1]}** del fragmento `{kmers[i]}` $\\rightarrow$ Historial actual: `{reconstruccion}`")
        
        # Comparación final clara
        st.markdown("#### 🎯 Comparación de Control de Calidad")
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Secuencia de Entrada:**\n`{secuencia}`")
        with c2:
            if secuencia == reconstruccion:
                st.success(f"**Secuencia Armada:**\n`{reconstruccion}`")
                st.balloons()
            else:
                st.error(f"**Secuencia Armada:**\n`{reconstruccion}`\n*(¡Hubo un problema de ambigüedad en el mapa!)*")

    # 🏆 PESTAÑA 4: EVALUACIÓN TRADUCIDA A TRIVIA INTERACTIVA
    with tab4:
        st.subheader("🧪 ¡Desafío de Laboratorio!")
        st.write("Demuestra tus superpoderes en bioinformática respondiendo estos desafíos basados en tus datos cargados:")

        kmer1, kmer2, kmer3 = kmers[0], kmers[1], kmers[-1]
        se_conectan = kmer1[1:] == kmer3[:-1]

        # Preguntas adaptadas
        res1 = st.text_input(f"1. Mirando el fragmento `{kmer1}`, ¿cuál es su PREFIJO (letras iniciales)?")
        res2 = st.text_input(f"2. Mirando el fragmento `{kmer2}`, ¿cuál es su SUFIJO (letras finales)?")
        
        res3 = st.radio(f"3. Basado en las reglas, ¿pueden conectarse directamente `{kmer1}` con `{kmer3}`?", ["Sí", "No"], index=0)
        
        res4 = st.number_input(f"4. Si configuraste tu slider con k = {k}, ¿cuántas letras mide CADA prefijo o sufijo?", min_value=1, max_value=20, step=1)

        if st.button("🎯 Entregar Informe de Respuestas"):
            puntos = 0
            st.markdown("### 📋 Corrección de tu informe:")
            
            if res1.upper().strip() == kmer1[:-1]:
                st.success("✔ **Pregunta 1:** ¡Correcto! Quitaste la última letra a la perfección.")
                puntos += 1
            else:
                st.error(f"✘ **Pregunta 1:** Incorrecto. El prefijo de `{kmer1}` es `{kmer1[:-1]}`.")

            if res2.upper().strip() == kmer2[1:]:
                st.success("✔ **Pregunta 2:** ¡Espectacular! Te quedaste solo con el bloque final.")
                puntos += 1
            else:
                st.error(f"✘ **Pregunta 2:** Incorrecto. El sufijo de `{kmer2}` es `{kmer2[1:]}`.")

            resp_correcta_3 = "Sí" if se_conectan else "No"
            if res3 == resp_correcta_3:
                st.success("✔ **Pregunta 3:** ¡Excelente deducción lógica!")
                puntos += 1
            else:
                st.error(f"✘ **Pregunta 3:** Fallaste. La respuesta es `{resp_correcta_3}` porque sus extremos " + ("sí" if se_conectan else "no") + " son idénticos.")

            if res4 == k - 1:
                st.success(f"✔ **Pregunta 4:** ¡Exacto! Siempre es la fórmula matemática de $k - 1$ (en este caso, {k-1}).")
                puntos += 1
            else:
                st.error(f"✘ **Pregunta 4:** Incorrecto. Recuerda que la longitud siempre es $k - 1$, o sea, {k-1}.")

            st.markdown(f"## 🏆 Tu nota de laboratorio: {puntos}/4")
            if puntos == 4:
                st.success("🥇 ¡Perfecto! Eres oficialmente un experto genetista computacional.")
            elif puntos >= 2:
                st.warning("🥈 ¡Buen intento! Tienes las nociones básicas bien claras.")
            else:
                st.error("📚 Te sugerimos releer la pestaña de 'Guía y Teoría' para aclarar las dudas.")

# -------------------------------------------------------
# PIE DE PÁGINA (CRÉDITOS DISCRETOS)
# -------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 13px; opacity: 0.7;'>
    <b>Simulador de Ensamblaje Genómico (Grafos de De Bruijn)</b><br>
    Asignatura: Bioinformática | Licenciatura en Biología Orientada a la Educación Secundaria.<br>
    Creado por <b>Owen Ranyelis Luciano Valdez</b> y <b>Ruth Margarita Canela Herrera</b> | © 2026
</div>
""", unsafe_allow_html=True)