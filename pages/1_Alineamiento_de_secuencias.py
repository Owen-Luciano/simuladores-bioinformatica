import streamlit as plt
import streamlit as st

# =====================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES
# =====================================================
st.set_page_config(page_title="🧬 Simulador ADN", layout="centered")

# CSS personalizado optimizado para estudiantes de secundaria (Estilo Bio-Tech moderno)
st.markdown("""
<style>
/* Fondo general con degradado sutil */
.main {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #f8fafc;
}

/* Títulos con tipografía moderna y colores llamativos */
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

/* Botones estilo "Videojuego/Moderno" */
div.stButton > button {
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%) !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 0.6rem 2rem !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 16px !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
}

/* Inputs de texto limpios y redondeados */
input {
    background-color: #1e293b !important;
    border: 2px solid #475569 !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
    font-size: 16px !important;
}
input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important;
}

/* Tarjetas informativas personalizadas */
.bio-card {
    background-color: rgba(30, 41, 59, 0.7);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(167, 139, 250, 0.3);
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* =====================================================
MODIFICAR EL TAMAÑO DE LAS PESTAÑAS (TABS)
===================================================== */
button[data-baseweb="tab"] {
    font-size: 18px !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
}

div[data-baseweb="tab-panel"] {
    font-size: 16px !important;
}

/* Separadores */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
    margin: 2rem 0;
}

</style>
""", unsafe_allow_html=True)

# Header principal interactivo
st.markdown("<h1>🧬 Laboratorio de ADN: Simulador Needleman-Wunsch</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='bio-card' style='text-align: center;'>
    ¡Bienvenido al simulador biológico! Aquí podrás convertirte en un bioinformático y descubrir 
    cómo las computadoras comparan el código genético de diferentes seres vivos paso a paso.
</div>
""", unsafe_allow_html=True)

# =====================================================
# ENTRADA DE DATOS (Agrupados estéticamente)
# =====================================================
st.markdown("### 📥 Ingresa tus secuencias de ADN")
col_input1, col_input2 = st.columns(2)

with col_input1:
    secuencia1 = st.text_input("Primera Secuencia", value="", placeholder="Ej. ATCGATT")
with col_input2:
    secuencia2 = st.text_input("Segunda Secuencia", value="", placeholder="Ej. ATGGAA")

# Botón principal estilizado
if st.button("🚀 ¡Iniciar Alineamiento Genético!"):
    st.session_state.ejecutado = True

if "ejecutado" in st.session_state:
    
    # Validaciones básicas
    secuencia1 = secuencia1.upper().strip()
    secuencia2 = secuencia2.upper().strip()
    nucleotidos = {"A", "T", "C", "G"}

    if secuencia1 == "" or secuencia2 == "":
        st.error("❌ ¡Ups! Debes rellenar ambas secuencias para poder compararlas.")
        st.stop()

    if not set(secuencia1).issubset(nucleotidos) or not set(secuencia2).issubset(nucleotidos):
        st.error("❌ Código erróneo: El ADN solo contiene las bases A, T, C y G.")
        st.stop()

    st.toast("🧬 ¡Secuencias procesadas con éxito!", icon="✅")

    # =====================================================
    # ORGANIZACIÓN POR PESTAÑAS (Mejora drásticamente la UX)
    # =====================================================
    tab1, tab2, tab3 = st.tabs(["📊 Matriz e Instrucciones", "🎯 Resultado Final", "🧪 Zona de Juego (Quiz)"])

    # Cálculos algorítmicos detrás de escena
    MATCH, MISMATCH, GAP = 1, -1, -1
    filas, columnas = len(secuencia1) + 1, len(secuencia2) + 1
    matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas): matriz[i][0] = i * GAP
    for j in range(columnas): matriz[0][j] = j * GAP

    for i in range(1, filas):
        for j in range(1, columnas):
            score = MATCH if secuencia1[i - 1] == secuencia2[j - 1] else MISMATCH
            matriz[i][j] = max(matriz[i - 1][j - 1] + score, matriz[i - 1][j] + GAP, matriz[i][j - 1] + GAP)

    # --- PESTAÑA 1: MATRIZ Y AYUDA ---
    with tab1:
        # Reemplazado botón de ayuda por un Expander nativo elegante
        with st.expander("🧠 ¿No sabes qué hacer? Abre la Guía Rápida"):
            st.markdown("""
            ### 🔬 Tu misión en el laboratorio:
            1. Observa la tabla de abajo: muestra cómo el algoritmo le da puntos a las coincidencias.
            2. Analiza los colores de las celdas para guiarte.
            
            ### 📊 Código de colores del juego:
            - 🟩 **MATCH** (+1 punto) → ¡Los nucleótidos son idénticos!
            - 🟥 **MISMATCH** (-1 punto) → Hubo una mutación (letras diferentes).
            - 🟦 **GAP** (-1 punto) → Espacio vacío, falta o sobra una letra en la evolución.
            """)

        st.subheader("Matriz de Puntuación Resultante")
        st.caption("Mira cómo se cruzaron tus secuencias en la cuadrícula:")
        
        col_labels = ["-"] + list(secuencia2)
        row_labels = ["-"] + list(secuencia1)

        # Renderizado visual optimizado de la matriz
        header_cols = st.columns(len(col_labels) + 1)
        header_cols[0].write("")
        for j in range(len(col_labels)):
            header_cols[j + 1].markdown(f"<div style='text-align:center;font-weight:bold;color:#38bdf8;'>{col_labels[j]}</div>", unsafe_allow_html=True)

        for i in range(filas):
            cols = st.columns(len(col_labels) + 1)
            cols[0].markdown(f"<div style='font-weight:bold;color:#a78bfa;'>{row_labels[i]}</div>", unsafe_allow_html=True)
            for j in range(columnas):
                value = matriz[i][j]
                if i == 0 or j == 0:
                    cols[j + 1].markdown(f"<div style='text-align:center;background-color:#1e3a8a;border-radius:6px;padding:2px;font-size:14px;'>🟦 {value}</div>", unsafe_allow_html=True)
                else:
                    if value > 0:
                        cols[j + 1].markdown(f"<div style='text-align:center;background-color:#065f46;border-radius:6px;padding:2px;font-size:14px;'>🟩 {value}</div>", unsafe_allow_html=True)
                    elif value < 0:
                        cols[j + 1].markdown(f"<div style='text-align:center;background-color:#991b1b;border-radius:6px;padding:2px;font-size:14px;'>🟥 {value}</div>", unsafe_allow_html=True)
                    else:
                        cols[j + 1].markdown(f"<div style='text-align:center;background-color:#334155;border-radius:6px;padding:2px;font-size:14px;'>⬜ {value}</div>", unsafe_allow_html=True)

    # Traceback algorítmico
    i, j = len(secuencia1), len(secuencia2)
    alineamiento1, alineamiento2, matches = [], [], []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and matriz[i][j] == matriz[i-1][j-1] + (1 if secuencia1[i-1] == secuencia2[j-1] else -1):
            alineamiento1.insert(0, secuencia1[i-1])
            alineamiento2.insert(0, secuencia2[j-1])
            matches.insert(0, secuencia1[i-1] == secuencia2[j-1])
            i, j = i - 1, j - 1
        elif i > 0 and matriz[i][j] == matriz[i-1][j] - 1:
            alineamiento1.insert(0, secuencia1[i-1])
            alineamiento2.insert(0, "-")
            matches.insert(0, False)
            i -= 1
        else:
            alineamiento1.insert(0, "-")
            alineamiento2.insert(0, secuencia2[j-1])
            matches.insert(0, False)
            j -= 1

    total = len(alineamiento1)
    matches_count = sum(1 for a, b in zip(alineamiento1, alineamiento2) if a == b)
    gaps_count = sum(1 for a, b in zip(alineamiento1, alineamiento2) if a == "-" or b == "-")
    mismatches_count = total - matches_count - gaps_count

    # --- PESTAÑA 2: RESULTADOS Y ESTADÍSTICAS ---
    with tab2:
        st.subheader("📊 Estadísticas de tu Comparación")
        
        # Uso de st.metric para dar aspecto de Dashboard profesional
        m1, m2, m3 = st.columns(3)
        m1.metric("🧬 Coincidencias", f"{matches_count}", f"{round(matches_count/total*100, 1)}%", delta_color="normal")
        m2.metric("⚠️ Mutaciones", f"{mismatches_count}", f"-{round(mismatches_count/total*100, 1)}%", delta_color="inverse")
        m3.metric("⚪ Gaps (Espacios)", f"{gaps_count}", f"{round(gaps_count/total*100, 1)}%", delta_color="off")

        st.subheader("🔍 Alineamiento Visual")
        linea1 = " ".join(alineamiento1)
        linea2 = " ".join(alineamiento2)
        linea3 = " ".join(["|" if m else " " for m in matches])
        
        st.code(f"{linea1}\n{linea3}\n{linea2}", language="text")

        # Explicación simplificada usando contenedores nativos
        st.info("💡 **Interpretación Biológica:** Los trozos con muchas líneas verticales `|` indican que ambas especies provienen de un ancestro común muy cercano. Los espacios `-` son adaptaciones evolutivas.")

    # --- PESTAÑA 3: MINI QUIZ INTERACTIVO ---
    with tab3:
        st.subheader("🧪 ¡Ponte a prueba!")
        st.write("Demuestra lo aprendido respondiendo este rápido cuestionario:")

        q1 = st.radio("1. ¿Qué representa un MATCH en el alineamiento?", 
                      ["A. Una penalización por diferencia", "B. Una coincidencia exacta entre nucleótidos", "C. Un espacio insertado (gap)"], index=0)
        
        q2 = st.radio("2. ¿Qué significan evolutivamente los Gaps?", 
                      ["A. Mutaciones por pérdida o inserción de ADN", "B. Que el código falló", "C. Duplicación perfecta"], index=0)
        
        q3 = st.radio("3. ¿Para qué sirve el camino inverso (Traceback)?", 
                      ["A. Para borrar los datos", "B. Para encontrar el mapa final de alineamiento óptimo", "C. Para cambiar las letras del ADN"], index=0)

        if st.button("🎯 Validar mis Respuestas"):
            score = 0
            if q1.startswith("B"): score += 1
            if q2.startswith("A"): score += 1
            if q3.startswith("B"): score += 1

            if score == 3:
                st.balloons()
                st.success("🎉 ¡Increíble! Puntuación 3/3. ¡Eres todo un bioinformático!")
            elif score == 2:
                st.warning(f"👍 ¡Muy bien! Sacaste {score}/3. Revisa los detalles en la pestaña 1 para obtener la puntuación perfecta.")
            else:
                st.error(f"📚 Obtuviste {score}/3. ¡No te rindas! Te recomendamos volver a leer la pestaña de ayuda.")

# =====================================================
# CRÉDITOS (Al pie de página de manera discreta)
# =====================================================
st.markdown("<hr>", unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div style='text-align: center; font-size: 13px; opacity: 0.7;'>
        <b>Simulador de Alineamiento Global (Needleman-Wunsch)</b><br>
        Desarrollado con fines educativos por <b>Owen Ranyelis Luciano Valdez</b> y <b>Ruth Margarita Canela Herrera</b>.<br>
        🐍 Python + 🚀 Streamlit | © 2026
    </div>
    """, unsafe_allow_html=True)
