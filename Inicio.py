import streamlit as st

# =====================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES
# =====================================================
st.set_page_config(
    page_title="Bioinformática Educativa",
    page_icon="💻",
    layout="wide"
)

# Inyección de CSS blindado universal para la página de inicio
st.markdown("""
<style>
/* Forzar fondo general claro y degradado premium */
.stApp, .main {
    background: linear-gradient(180deg, #fdf6ff 0%, #f2f7ff 100%) !important;
}

/* Forzar color de textos generales y listas */
p, li, span, label, .stMarkdown { 
    color: #333333 !important; 
}

/* Título Principal de la Suite */
.main-title {
    color: #4b2e83 !important; 
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    text-align: center;
    font-size: 42px !important;
    text-shadow: 0px 2px 8px rgba(123, 44, 191, 0.15) !important;
    margin-bottom: 5px !important;
    margin-top: -20px !important;
}

/* Subtítulo del proyecto */
.sub-title {
    color: #6366f1 !important;
    font-family: 'Inter', sans-serif;
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 25px;
}

/* Tarjeta de bienvenida de ancho completo */
.welcome-card {
    background-color: rgba(123, 44, 191, 0.05) !important;
    padding: 25px;
    border-radius: 16px;
    border-left: 6px solid #7b2cbf !important;
    margin-bottom: 30px;
    font-size: 16px;
    line-height: 1.6;
    color: #333333 !important;
    box-shadow: 0 4px 12px rgba(123, 44, 191, 0.03);
}

/* Encabezados de secciones secundarias */
.section-title {
    color: #7b2cbf !important; 
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    margin-bottom: 20px;
}

/* Tarjetas Dinámicas para cada Simulador (Dashboard Grid) */
.dashboard-card {
    background-color: #ffffff !important;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e3d5f5 !important;
    border-bottom: 4px solid #6366f1 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.3s ease-index;
    height: 190px;
    margin-bottom: 20px;
}
.dashboard-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15) !important;
    border-bottom: 4px solid #7b2cbf !important;
}

.card-icon {
    font-size: 28px;
    margin-bottom: 10px;
}

.card-title {
    color: #4b2e83 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin-bottom: 8px !important;
}

.card-desc {
    color: #555555 !important;
    font-size: 14px !important;
    line-height: 1.4;
}

/* Separadores sutiles */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #a78bfa, transparent) !important;
    margin: 2.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# RENDERIZADO DEL ENCABEZADO Y HERO SECTION
# =====================================================
st.markdown("<div class='main-title'>🧬 Suite de Simuladores Bioinformáticos Educativos</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Proyecto de Innovación para la Enseñanza de las Ciencias Naturales</div>", unsafe_allow_html=True)

# Estructura de dos columnas para integrar la imagen de fondo de laboratorio
col_hero1, col_hero2 = st.columns([5, 4], gap="large")

with col_hero1:
    st.markdown("""
    <div class='welcome-card'>
        <b>¡Bienvenido/a al laboratorio digital de genética computacional!</b><br><br>
        Esta plataforma reúne una colección de <b>simuladores interactivos</b> diseñados especialmente 
        para que estudiantes de secundaria exploren los algoritmos reales que utilizan los científicos 
        para descifrar los secretos de la vida. A través de interfaces visuales, guías paso a paso 
        y retos interactivos, transformamos las matemáticas moleculares en un entorno de aprendizaje dinámico.
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Indicación:** Usa el menú desplegable o la barra lateral izquierda de la pantalla para seleccionar y ejecutar el simulador que deseas explorar el día de hoy.")

with col_hero2:
    # Ruta local de la imagen de portada configurada correctamente para leer desde GitHub
    st.image(
        "imagenes/portada.png", 
        caption="Análisis genómico y modelado computacional",
        use_container_width=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================
# SECCIÓN DE CUADRÍCULA (DASHBOARD GRID DE SIMULADORES)
# =====================================================
st.markdown("<h3 class='section-title'>🔬 Explora nuestros módulos disponibles</h3>", unsafe_allow_html=True)

# Configuración de filas y columnas para las tarjetas dinámicas
fila1_c1, fila1_c2, fila1_c3 = st.columns(3)

with fila1_c1:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>🧬</div>
        <div class='card-title'>Alineamiento Global</div>
        <div class='card-desc'>Compara cadenas de ADN usando el algoritmo de <b>Needleman-Wunsch</b>. Descubre mutaciones, coincidencias evolutivas y calcula matrices paso a paso.</div>
    </div>
    """, unsafe_allow_html=True)

with fila1_c2:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>🌳</div>
        <div class='card-title'>Filogenia Evolutiva</div>
        <div class='card-desc'>Construye árboles genealógicos de las especies (árboles filogénicos) aplicando el método de agrupamiento jerárquico <b>UPGMA</b> basado en distancias genéticas.</div>
    </div>
    """, unsafe_allow_html=True)

with fila1_c3:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>🔬</div>
        <div class='card-title'>Modelado de Proteínas</div>
        <div class='card-desc'>Explora la estructura tridimensional (3D) de moléculas reales de la base de datos RCSB PDB usando <b>BioPython</b> y visulaízalas rotando en el espacio.</div>
    </div>
    """, unsafe_allow_html=True)


fila2_c1, fila2_c2, fila2_c3 = st.columns(3)

with fila2_c1:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>🕸️</div>
        <div class='card-title'>Ensamble de Fragmentos</div>
        <div class='card-desc'>Resuelve el rompecabezas genómico. Reconstruye secuencias de ADN trituradas modelando mapas de conexión mediante <b>Grafos de De Bruijn</b> y sus k-mers.</div>
    </div>
    """, unsafe_allow_html=True)

with fila2_c2:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>🔀</div>
        <div class='card-title'>Transcripción Genética</div>
        <div class='card-desc'>Simula el dogma central de la biología molecular. Convierte cadenas de ADN a ARN mensajero y descifra la traducción final a aminoácidos.</div>
    </div>
    """, unsafe_allow_html=True)

with fila2_c3:
    # Tarjeta especial informativa que equilibra la cuadrícula simétricamente
    st.markdown("""
    <div class='dashboard-card' style='border-bottom: 4px solid #a78bfa !important;'>
        <div class='card-icon'>🏆</div>
        <div class='card-title'>Evaluaciones Integradas</div>
        <div class='card-desc'>Recuerda que cada simulador contiene un <b>Quiz interactivo de autoevaluación</b> en su última pestaña para medir tus conocimientos de laboratorio.</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PIE DE PÁGINA (CRÉDITOS FIJOS)
# =====================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 13px; opacity: 0.8; color: #555555;'>
    <b>Suite de Simuladores Bioinformáticos Educativos</b><br>
    Asignatura: Bioinformática | Licenciatura en Biología Orientada a la Educación Secundaria (ISFODOSU)<br>
    Desarrollado por <b>Owen Ranyelis Luciano Valdez</b> y <b>Ruth Margarita Canela Herrera</b> | © 2026
</div>
""", unsafe_allow_html=True)
