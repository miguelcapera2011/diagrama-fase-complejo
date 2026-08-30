from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer


# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Intento suicida",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# LOCALIZACIÓN DINÁMICA DEL ARCHIVO PDF
BASE_DIR = Path(__file__).parent if "__file__" in globals() else Path.cwd()
PDF_FILE_PATH = BASE_DIR / "intento suicida.pdf"

# Paleta de colores sobria
RED = "#D7263D"
NAVY = "#0F172A"
BLUE = "#2563EB"
GREEN = "#059669"
ORANGE = "#D97706"
PURPLE = "#7C3AED"
GRAY = "#475569"
LIGHT = "#F8FAFC"
BORDER = "#CBD5E1"

# ESTILOS CSS (INCLUYE MEJORAS ESTÉTICAS)
st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
        
        * {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .stApp {{
            background: {LIGHT};
            color: #0F172A !important;
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0F172A 0%, #172554 100%);
        }}
        [data-testid="stSidebar"] * {{
            color: #F8FAFC !important;
        }}
        
        /* ESTILO PARA LA BARRA LATERAL (CENTRADOS) */
        .sidebar-header-box {{
            text-align: center;
            padding: 0.5rem 0 1rem 0;
        }}
        .sidebar-icon {{
            font-size: 2.5rem;
            margin-bottom: 0.3rem;
            display: inline-block;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }}
        .sidebar-title {{
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 0.8px;
            color: #FFFFFF !important;
            text-transform: uppercase;
            margin: 0;
            line-height: 1.3;
        }}
        .sidebar-subtitle {{
            font-size: 0.8rem;
            font-weight: 600;
            color: #93C5FD !important;
            letter-spacing: 1px;
            margin-top: 0.3rem;
            text-transform: uppercase;
        }}

        /* ESTILO PARA EL TÍTULO PRINCIPAL CENTRADO */
        .title-container {{
            text-align: center;
            padding: 0.5rem 1rem 0.8rem 1rem;
            margin-bottom: 0.5rem;
        }}
        .main-title {{
            font-size: 2.2rem;
            font-weight: 800;
            color: {NAVY} !important;
            line-height: 1.2;
            letter-spacing: -0.5px;
            margin: 0 auto;
            max-width: 950px;
        }}
        .subtitle {{
            color: {GRAY} !important;
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 0.4rem;
            letter-spacing: 0.2px;
        }}
        
        .section-title {{
            font-size: 1.45rem;
            font-weight: 800;
            color: {NAVY} !important;
            margin-top: 0.2rem;
        }}
        .section-subtitle {{
            color: {GRAY} !important;
            margin-bottom: 0.8rem;
        }}
        .card {{
            background: #FFFFFF;
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 1.1rem 1.25rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            height: 100%;
            color: #1E293B !important;
        }}
        .card h4 {{
            margin: 0 0 .45rem 0;
            color: {NAVY} !important;
            font-weight: 700;
        }}
        .card p, .card div, .card span, .card b {{
            color: #1E293B !important;
        }}
        .interpretation {{
            background: #FFF7ED;
            border-left: 5px solid {ORANGE};
            border-top: 1px solid #FED7AA;
            border-right: 1px solid #FED7AA;
            border-bottom: 1px solid #FED7AA;
            padding: 1rem 1.1rem;
            border-radius: 8px;
            margin: .9rem 0;
            color: #7C2D12 !important;
        }}
        .interpretation b, .interpretation div, .interpretation p {{
            color: #7C2D12 !important;
        }}
        .math-box {{
            background: #EFF6FF;
            border: 1px solid #BFDBFE;
            border-radius: 12px;
            padding: 1.1rem;
            color: #1E3A8A !important;
            margin: 0.8rem 0;
        }}
        .math-box * {{
            color: #1E3A8A !important;
        }}
        .source-box {{
            background: #F1F5F9;
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: .75rem 1rem;
            font-size: .85rem;
            color: #334155 !important;
            margin-top: 0.8rem;
        }}
        .step {{
            background: #FFFFFF;
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: .9rem;
            text-align: center;
            min-height: 120px;
            color: #1E293B !important;
        }}
        .step p, .step div {{
            color: #334155 !important;
        }}
        .step-number {{
            font-size: .85rem;
            font-weight: 800;
            color: {RED} !important;
        }}
        .step-title {{
            font-weight: 800;
            color: {NAVY} !important;
        }}
        .small-note {{
            color: {GRAY} !important;
            font-size: .85rem;
            margin-top: 0.4rem;
        }}
        .big-question {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {NAVY} !important;
            background: #FFFFFF;
            border-radius: 14px;
            border: 1px solid {BORDER};
            padding: 1rem 1.2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}
        div[data-testid="stMetric"] {{
            background: #FFFFFF;
            border: 1px solid {BORDER};
            padding: .7rem;
            border-radius: 12px;
        }}
        div[data-testid="stMetric"] * {{
            color: {NAVY} !important;
        }}
        
        /* CORRECCIÓN PARA ELIMINAR EL BORDES Y LA FRANJA NEGRA DEL PDF */
        iframe[title="streamlit_pdf_viewer.pdf_viewer"] {{
            background-color: transparent !important;
            width: 100% !important;
            border: none !important;
        }}
        div[data-testid="stCustomComponentV1"] {{
            background-color: transparent !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
        }}
        .pdf-canvas-container, .pdf-viewer-container, .sdv-container {{
            background-color: transparent !important;
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
        }}
        canvas.pdf-canvas {{
            max-width: 100% !important;
            height: auto !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
            border-radius: 4px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ESTRUCTURAS DE DATOS DE TABLAS Y PREVALENCIA
age_groups = [
    "5 a 9", "10 a 14", "15 a 19", "20 a 24", "25 a 29",
    "30 a 34", "35 a 39", "40 a 44", "45 a 49", "50 a 54",
    "55 a 59", "60 a 64", "65 a 69", "70 a 74", "75 a 79", "80 y más"
]

prevalence = {
    2012: [0.0, 5.8, 16.9, 16.9, 8.8, 6.0, 4.1, 3.4, 1.1, 0.5, 1.1, 0.6, 0.0, 0.0, 0.0, 0.0],
    2013: [0.0, 9.6, 23.5, 21.4, 16.3, 6.8, 5.9, 5.1, 3.1, 2.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    2014: [0.0, 0.4, 16.9, 15.9, 11.7, 10.8, 5.0, 0.9, 0.0, 0.7, 2.2, 0.0, 0.0, 0.0, 0.0, 0.0],
    2015: [0.0, 4.2, 16.2, 17.0, 8.9, 5.9, 3.0, 0.9, 1.5, 0.7, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0],
    2016: [0.0, 9.4, 26.8, 15.2, 5.0, 2.0, 4.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7],
    2017: [0.0, 4.3, 21.0, 19.1, 9.0, 8.1, 5.0, 3.8, 3.1, 0.7, 2.0, 0.0, 0.0, 0.0, 0.0, 0.7],
}

prev_rows = []
for year, values in prevalence.items():
    for age, value in zip(age_groups, values):
        prev_rows.append({"Año": year, "Grupo de edad": age, "Prevalencia": value})
prev_df = pd.DataFrame(prev_rows)

table1 = [
    ["Área de ocurrencia", "Urbano", 94.0, 315, 89.8, 169, 92.0, 484, 0.02],
    ["Área de ocurrencia", "Rural disperso", 6.2, 21, 10.1, 19, 8.0, 40, 0.02],
    ["Edad agrupada", "3 a 11 años (niñez)", 0.9, 3, 1.6, 3, 1.1, 6, 0.000],
    ["Edad agrupada", "11 a 20 años (adolescencia)", 50.3, 169, 35.1, 66, 44.8, 235, 0.000],
    ["Edad agrupada", "20 a 40 (adultez temprana)", 42.0, 141, 45.7, 86, 43.3, 227, 0.000],
    ["Edad agrupada", "40 a 65 (adultez mediana y tardía)", 6.8, 23, 17.6, 33, 10.7, 56, 0.000],
    ["Estado civil", "Soltero", 64.8, 210, 54.4, 99, 61.7, 309, 0.115],
    ["Estado civil", "Casado", 31.2, 101, 3.9, 71, 34.0, 172, 0.115],
    ["Estado civil", "Separado", 3.1, 10, 5.5, 10, 4.0, 20, 0.115],
    ["Estado civil", "Viudo", 0.9, 3, 1.1, 2, 1.0, 5, 0.115],
    ["Ocupación", "Ama de casa", 30.2, 101, 1.1, 2, 20.2, 103, 0.000],
    ["Ocupación", "Estudiante", 47.6, 159, 35.4, 62, 43.4, 221, 0.000],
    ["Ocupación", "Empleado auxiliar", 3.89, 13, 2.6, 47, 11.9, 60, 0.000],
    ["Ocupación", "Empleado profesional", 2.9, 10, 5.7, 10, 3.9, 20, 0.000],
    ["Ocupación", "Independiente", 8.9, 30, 14.2, 25, 10.8, 55, 0.000],
    ["Ocupación", "Población carcelaria", 0.2, 1, 0.0, 0, 0.2, 1, 0.000],
    ["Ocupación", "Desempleado", 3.3, 11, 12.6, 22, 6.5, 33, 0.000],
    ["Ocupación", "Pensionado", 0.2, 1, 1.14, 2, 0.6, 3, 0.000],
    ["Forma de realización", "Impulsiva", 84.8, 279, 82.8, 149, 84.1, 428, 0.551],
    ["Forma de realización", "Planeada", 15.2, 50, 17.2, 31, 15.9, 81, 0.551],
    ["Antecedentes de intento", "No", 68.5, 24, 67.4, 120, 68.1, 44, 0.80],
    ["Antecedentes de intento", "Sí", 31.5, 103, 32.6, 58, 31.9, 161, 0.80],
    ["Método del intento", "Medicamentos", 54.4, 182, 40.0, 70, 49.2, 252, 0.000],
    ["Método del intento", "Plaguicidas", 21.8, 73, 29.1, 51, 24.2, 124, 0.000],
    ["Método del intento", "Sustancias psicoactivas (SPA)", 0.2, 1, 2.28, 4, 1.0, 5, 0.000],
    ["Método del intento", "Heridas", 18.5, 61, 17.9, 33, 18.3, 94, 0.000],
    ["Método del intento", "Otros métodos", 3.59, 12, 13.7, 24, 7.1, 36, 0.000],
    ["Método del intento", "Arma de fuego", 0.0, 0, 1.1, 2, 0.4, 2, 0.000],
    ["Posible desencadenante", "Conflicto con la pareja", 36.9, 118, 29.8, 54, 34.3, 172, 0.005],
    ["Posible desencadenante", "Conflicto familiar", 27.2, 87, 18.2, 33, 24.0, 120, 0.005],
    ["Posible desencadenante", "Indeterminado", 20.9, 67, 30.4, 55, 24.4, 122, 0.005],
    ["Posible desencadenante", "Consumo de alcohol", 9.1, 29, 12.7, 23, 10.4, 52, 0.005],
    ["Posible desencadenante", "Conflicto laboral o escolar", 3.4, 11, 2.2, 4, 3.0, 15, 0.005],
    ["Posible desencadenante", "Problemas económicos", 2.5, 8, 12.7, 12, 4.0, 20, 0.005],
    ["Enfermedad mental", "No", 65.8, 210, 67.6, 115, 66.5, 325, 0.68],
    ["Enfermedad mental", "Sí", 34.2, 109, 32.4, 55, 33.5, 164, 0.68],
    ["Violencia", "No", 46.0, 137, 62.5, 95, 51.6, 232, 0.001],
    ["Violencia", "Sí", 54.0, 161, 37.5, 57, 48.4, 218, 0.001],
    ["Consumo de alcohol", "No", 59.7, 181, 38.5, 65, 52.1, 246, 0.000],
    ["Consumo de alcohol", "Sí", 40.3, 122, 59.7, 104, 47.9, 226, 0.000],
    ["Relaciones familiares", "Disfuncionales", 79.7, 248, 78.2, 129, 79.2, 377, 0.69],
    ["Relaciones familiares", "Funcionales", 20.3, 63, 21.8, 36, 20.8, 99, 0.69],
    ["Redes de apoyo", "No", 9.2, 28, 12.7, 22, 10.4, 49, 0.23],
    ["Redes de apoyo", "Sí", 90.8, 278, 87.3, 145, 89.6, 423, 0.23],
]

table1_df = pd.DataFrame(
    table1,
    columns=[
        "Variable", "Categoría",
        "Mujer %", "Mujer N",
        "Hombre %", "Hombre N",
        "Total %", "Total N",
        "p"
    ]
)

table2 = [
    ["Edad", "Niñez", 0.32, 0.05, 0.83, 1.38, 0.08, 24.34],
    ["Edad", "Adolescencia", -1.04, 7.52, 0.01, 0.35, 0.17, 0.74],
    ["Edad", "Adultez temprana", -0.81, 4.81, 0.03, 0.45, 0.22, 0.92],
    ["Posible desencadenante", "Conflicto con la pareja", -0.84, 7.67, 0.01, 0.43, 0.24, 0.78],
    ["Posible desencadenante", "Conflicto familiar", -0.66, 3.81, 0.05, 0.52, 0.26, 1.00],
    ["Posible desencadenante", "Conflicto laboral o escolar", -0.70, 1.09, 0.30, 0.50, 0.13, 1.85],
    ["Posible desencadenante", "Problemas económicos", 0.74, 1.43, 0.23, 2.09, 0.62, 7.02],
    ["Posible desencadenante", "Consumo de alcohol", -0.81, 3.89, 0.05, 0.44, 0.20, 1.00],
    ["Posible desencadenante", "Violencia", -0.89, 13.80, 0.00, 0.41, 0.26, 0.66],
    ["Consumo de alcohol", "Sí", 1.28, 25.09, 0.00, 3.58, 2.17, 5.90],
    ["Constante", "Intercepto", 0.44, 1.33, 0.25, 1.55, None, None],
]

table2_df = pd.DataFrame(
    table2,
    columns=["Variable", "Categoría", "B", "Wald", "p", "OR", "IC95% inf.", "IC95% sup."]
)


# FUNCIONES AUXILIARES
def source_box(text):
    st.markdown(f'<div class="source-box">📌 {text}</div>', unsafe_allow_html=True)


def card(title, body, icon=""):
    st.markdown(
        f"""
        <div class="card">
            <h4>{icon} {title}</h4>
            <div>{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(number, title, subtitle):
    st.markdown(f'<div class="section-title">{number}. {title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def fmt_p(x):
    if pd.isna(x) or x is None:
        return "—"
    if x < 0.001:
        return "<0,001"
    return f"{x:.3f}".replace(".", ",")


def fmt_num(x):
    if pd.isna(x) or x is None:
        return "—"
    return f"{x:.2f}".replace(".", ",")


# BARRA LATERAL (NAVEGACIÓN CON MEJORAS ESTÉTICAS)
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-header-box">
            <div class="sidebar-icon">📈</div>
            <div class="sidebar-title">Modelos Lineales Generalizados</div>
            <div class="sidebar-subtitle">Universidad del Tolima</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Contenido:")
    section = st.radio(
        "Etapa de la exposición",
        [
            "01 · Introducción",
            "02 · Contexto y pregunta",
            "03 · Datos y diseño",
            "04 · Prevalencia",
            "05 · Tabla 1 · Descriptivos",
            "06 · Modelo logístico",
            "07 · Tabla 2 · Modelo final",
            "08 · Interpretación del OR",
            "09 · Evaluación del modelo",
            "10 · Discusión",
            "11 · Conclusiones",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 📚 Ficha del estudio")
    st.write("**Lugar:** Sogamoso, Boyacá")
    st.write("**Periodo:** 2012–2017")
    st.write("**Casos:** 524")
    st.write("**Mujeres:** 336 (64,2%)")
    st.write("**Hombres:** 188 (35,8%)")
    st.write("**Fuente:** SIVIGILA")
    st.write("**Diseño:** analítico transversal")

    st.markdown("---")
    st.caption("Fuente: Vásquez-Escobar & Benítez-Camargo (2021).")

page_map = {
    "01 · Introducción": 1,
    "02 · Contexto y pregunta": 3,
    "03 · Datos y diseño": 5,
    "04 · Prevalencia": 6,
    "05 · Tabla 1 · Descriptivos": 7,
    "06 · Modelo logístico": 8,
    "07 · Tabla 2 · Modelo final": 9,
    "08 · Interpretación del OR": 9,
    "09 · Evaluación del modelo": 9,
    "10 · Discusión": 11,
    "11 · Conclusiones": 13,
}

# Inicialización de estado para la página del PDF
if "pdf_page" not in st.session_state:
    st.session_state.pdf_page = page_map[section]

# Sincronizar cuando el usuario cambia la sección en la barra lateral
if "last_section" not in st.session_state or st.session_state.last_section != section:
    st.session_state.pdf_page = page_map[section]
    st.session_state.last_section = section

# ENCABEZADO PRINCIPAL CENTRADO
sub_html = (
    '<div class="subtitle">Sogamoso, Boyacá · Una lectura del artículo desde la estadística</div>'
    if section == "01 · Introducción"
    else ""
)

st.markdown(
    f"""
    <div class="title-container">
        <div class="main-title">Intento suicida: un análisis municipal de factores asociados 2012–2017</div>
        {sub_html}
    </div>
    """,
    unsafe_allow_html=True,
)

# SECCIÓN DE MÉTRICAS E IDEA DE LA EXPOSICIÓN (SOLO EN INTRODUCCIÓN)
if section == "01 · Introducción":
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 3.5])
    with c1:
        st.metric("Casos", "524")
    with c2:
        st.metric("Mujeres", "336")
    with c3:
        st.metric("Hombres", "188")
    with c4:
        st.markdown(
            '<div class="big-question">🎯 Idea de la exposición: reconstruir el camino desde los datos hasta la evidencia estadística.</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# CONTROLES Y VISUALIZADOR DE PDF
full_screen = st.checkbox("🔍 Expandir PDF a pantalla completa ")

# Ajuste de columnas según el modo de pantalla
if full_screen:
    left, right = st.container(), None
else:
    left, right = st.columns([1.1, 1.0], gap="large")

with left:
    st.markdown("### 📄 Artículo")

    # Barra superior de controles del visor
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1, 1, 2, 2])

    with ctrl_col1:
        if st.button("◀ Ant", use_container_width=True):
            if st.session_state.pdf_page > 1:
                st.session_state.pdf_page -= 1
                st.rerun()

    with ctrl_col2:
        if st.button("Sig ▶", use_container_width=True):
            if st.session_state.pdf_page < 15:
                st.session_state.pdf_page += 1
                st.rerun()

    with ctrl_col3:
        st.session_state.pdf_page = st.number_input(
            "Página",
            min_value=1,
            max_value=15,
            value=st.session_state.pdf_page,
            step=1,
            label_visibility="collapsed",
        )

    with ctrl_col4:
        viewer_height = st.slider(
            "Altura (px)",
            min_value=400,
            max_value=1200,
            value=700,
            step=50,
            label_visibility="collapsed",
        )

    possible_files = list(BASE_DIR.glob("*.pdf"))
    target_pdf = None

    if PDF_FILE_PATH.exists():
        target_pdf = PDF_FILE_PATH
    elif len(possible_files) > 0:
        target_pdf = possible_files[0]

    if target_pdf and target_pdf.exists():
        try:
            pdf_bytes = target_pdf.read_bytes()
            
            # Envoltura en un div personalizado para forzar el ajuste al 100% de ancho
            st.markdown('<div class="pdf-viewer-container">', unsafe_allow_html=True)
            try:
                pdf_viewer(
                    input=pdf_bytes,
                    page_to_render=st.session_state.pdf_page,
                    width="100%",
                    height=viewer_height,
                    render_text=False,
                    key=f"pdf_page_{st.session_state.pdf_page}_{viewer_height}",
                )
            except TypeError:
                pdf_viewer(
                    input=pdf_bytes,
                    pages_to_render=[st.session_state.pdf_page],
                    width="100%",
                    height=viewer_height,
                    render_text=False,
                    key=f"pdf_page_{st.session_state.pdf_page}_{viewer_height}",
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error al renderizar el archivo PDF: {e}")
    else:
        st.error(
            "⚠️ **No se encontró el archivo PDF.**\n\n"
            "Verifica que el archivo exista en la misma carpeta que `app.py` "
            "y que se llame exactamente `intento suicida.pdf`."
        )

# COLUMNA DE CONTENIDO (ANÁLISIS)
if not full_screen and right is not None:
    with right:
    
        # 01 INTRODUCCIÓN
        if section == "01 · Introducción":
            section_header(
                "1",
                "Adentrémonos en el estudio",
                "Antes de hablar de modelos, conozcamos qué estudiaron los autores y dónde ocurrió.",
            )
            a, b = st.columns(2)
            with a:
                card(
                    "¿Qué investigaron?",
                    "El comportamiento epidemiológico del intento de suicidio y las diferencias entre género y variables sociodemográficas, psicosociales y específicas durante 2012–2017.",
                    "🎯",
                )
            with b:
                card(
                    "¿Dónde?",
                    "Municipio de <b>Sogamoso, Boyacá, Colombia</b>. El estudio utilizó casos reportados al SIVIGILA.",
                    "📍",
                )

            st.markdown("<br>", unsafe_allow_html=True)
            a, b, c = st.columns(3)
            with a:
                card("Periodo", "<b>2012–2017</b>", "📅")
            with b:
                card("Casos analizados", "<b>524</b>", "👥")
            with c:
                card("Modelo", "<b>Regresión logística binaria</b>", "📐")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div class="interpretation"><b>Pregunta:</b><br>'
                '¿Qué diferencias existen entre hombres y mujeres entre los casos de intento de suicidio registrados en Sogamoso y qué variables aparecen asociadas estadísticamente con el género?</div>',
                unsafe_allow_html=True,
            )
            source_box("Resumen y objetivo del artículo.")

        # 02 CONTEXTO
        elif section == "02 · Contexto y pregunta":
            section_header(
                "2",
                "Del problema de salud pública a la pregunta estadística",
                "La investigación nace de un contexto territorial concreto.",
            )
            st.markdown(
                """
                <div class="card">
                <h4>🌎 ¿Por qué Sogamoso?</h4>
                <p>
                El artículo señala que Sogamoso reportaba, desde 2010, el mayor número de
                casos dentro del departamento y plantea la necesidad de caracterizar y
                comprender el comportamiento epidemiológico del intento de suicidio para
                orientar acciones de salud pública.
                </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div class="big-question">🔎 ¿Qué queremos explicar estadísticamente?</div>',
                unsafe_allow_html=True,
            )

            st.latex(r"Y = \text{género}")
            st.markdown(
                """
                **Variable dependiente / de interés:** género.

                **Variables explicativas:** edad o ciclo vital, área de ocurrencia,
                ocupación, estado civil, método del intento, posible desencadenante,
                violencia, enfermedad mental, consumo de alcohol, relaciones familiares,
                redes de apoyo, entre otras.
                """
            )
            source_box("El artículo define género como la variable de interés.")

        # 03 DATOS Y DISEÑO
        elif section == "03 · Datos y diseño":
            section_header(
                "3",
                "¿Cómo se construyó la información?",
                "Aquí seguimos el recorrido de los datos antes de analizarlos.",
            )
            cols = st.columns(5)
            steps = [
                ("01", "Caso", "Persona con intento de suicidio"),
                ("02", "UPGD", "Captación y notificación"),
                ("03", "SIVIGILA", "Sistema de vigilancia"),
                ("04", "Seguimiento", "Ficha e historia clínica"),
                ("05", "Análisis", "524 casos incluidos"),
            ]
            for col, (num, title, body) in zip(cols, steps):
                with col:
                    st.markdown(
                        f"""
                        <div class="step">
                            <div class="step-number">{num}</div>
                            <div class="step-title">{title}</div>
                            <p>{body}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            a, b, c = st.columns(3)
            with a:
                card("Casos potenciales", "<b>579</b>", "📥")
            with b:
                card("Excluidos", "<b>55</b>", "↘️")
            with c:
                card("Analizados", "<b>524</b>", "✅")

            st.markdown(
                '<div class="interpretation"><b>Importante:</b> los 55 casos excluidos correspondieron a personas que no residían en Sogamoso o casos sin seguimiento.</div>',
                unsafe_allow_html=True,
            )

            st.markdown("### Diseño")
            st.write(
                "El artículo describe un **estudio analítico transversal**, con datos recolectados entre 2012 y 2017."
            )
            st.write(
                "Para el análisis univariado se calcularon prevalencias ajustadas por edad mediante el método directo y una población estándar propuesta por la OMS."
            )
            source_box("Materiales y métodos del artículo.")

        # 04 PREVALENCIA
        elif section == "04 · Prevalencia":
            section_header(
                "4",
                "Prevalencia ajustada por edad: ¿dónde se concentra el fenómeno?",
                "Esta es una de las figuras centrales del artículo. Cruza año y grupo de edad.",
            )

            mode = st.radio(
                "Forma de observar la Figura 1",
                ["Curvas por año", "Mapa de calor", "Comparar un año"],
                horizontal=True,
            )

            if mode == "Curvas por año":
                fig = px.line(
                    prev_df,
                    x="Grupo de edad",
                    y="Prevalencia",
                    color="Año",
                    markers=True,
                    category_orders={"Grupo de edad": age_groups},
                    labels={
                        "Grupo de edad": "Grupo de edad (años)",
                        "Prevalencia": "Prevalencia ajustada",
                        "Año": "Año",
                    },
                )
                fig.update_layout(
                    height=510,
                    margin=dict(l=10, r=10, t=30, b=10),
                    legend_title="Año",
                    xaxis_tickangle=-45,
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(
                    """
                    <div class="interpretation">
                    <b>Lectura estadística:</b>
                    el patrón más marcado aparece en edades tempranas. El grupo de
                    <b>15–19 años</b> presenta valores elevados a lo largo del periodo.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            elif mode == "Mapa de calor":
                heat = prev_df.pivot(index="Grupo de edad", columns="Año", values="Prevalencia")
                heat = heat.reindex(age_groups)

                fig = px.imshow(
                    heat,
                    text_auto=".1f",
                    aspect="auto",
                    labels={"x": "Año", "y": "Grupo de edad", "color": "Prevalencia"},
                )
                fig.update_layout(
                    height=650,
                    margin=dict(l=10, r=10, t=30, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                selected_year = st.selectbox("Seleccione un año", sorted(prevalence.keys()))
                d = prev_df[prev_df["Año"] == selected_year]

                fig = px.bar(
                    d,
                    x="Grupo de edad",
                    y="Prevalencia",
                    text="Prevalencia",
                    labels={
                        "Grupo de edad": "Grupo de edad",
                        "Prevalencia": "Prevalencia ajustada",
                    },
                )
                fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
                fig.update_layout(
                    height=500,
                    margin=dict(l=10, r=10, t=30, b=10),
                    xaxis_tickangle=-45,
                )
                st.plotly_chart(fig, use_container_width=True)

            source_box("Figura 1 y texto de resultados del artículo.")

        # 05 TABLA 1
        elif section == "05 · Tabla 1 · Descriptivos":
            section_header(
                "5",
                "Tabla 1: descriptivos y cruce univariado",
                "La estadística descriptiva permite descubrir patrones antes de llegar al modelo.",
            )

            variable = st.selectbox(
                "Seleccione una variable de la Tabla 1",
                table1_df["Variable"].drop_duplicates().tolist(),
            )

            d = table1_df[table1_df["Variable"] == variable].copy()

            display = d[
                ["Categoría", "Mujer %", "Mujer N", "Hombre %", "Hombre N", "Total %", "Total N", "p"]
            ].copy()
            display["Mujer %"] = display["Mujer %"].map(lambda x: f"{x:.2f}%")
            display["Hombre %"] = display["Hombre %"].map(lambda x: f"{x:.2f}%")
            display["Total %"] = display["Total %"].map(lambda x: f"{x:.2f}%")
            display["p"] = display["p"].map(fmt_p)

            st.dataframe(display, use_container_width=True, hide_index=True)

            chart_df = d.melt(
                id_vars=["Categoría"],
                value_vars=["Mujer %", "Hombre %"],
                var_name="Sexo",
                value_name="Porcentaje",
            )
            chart_df["Sexo"] = chart_df["Sexo"].str.replace(" %", "", regex=False)

            fig = px.bar(
                chart_df,
                x="Categoría",
                y="Porcentaje",
                color="Sexo",
                barmode="group",
                text="Porcentaje",
                labels={"Porcentaje": "% dentro del sexo"},
            )
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig.update_layout(
                height=470,
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis_tickangle=-35,
            )
            st.plotly_chart(fig, use_container_width=True)

            source_box("Tabla 1 del artículo.")

        # 06 MODELO LOGÍSTICO
        elif section == "06 · Modelo logístico":
            section_header(
                "6",
                "¿Por qué aparece la regresión logística?",
                "Fundamentación matemática de la investigación.",
            )

            st.markdown(
                '<div class="big-question">La variable de interés es binaria: queremos modelar la probabilidad de ocurrencia según el género.</div>',
                unsafe_allow_html=True,
            )

            st.latex(
                r"""
                Y_i =
                \begin{cases}
                1 & \text{si la observación es Hombre}\\
                0 & \text{si la observación es Mujer}
                \end{cases}
                """
            )

            st.markdown("### 1️⃣ Queremos estimar la probabilidad:")
            st.latex(r"p_i=P(Y_i=1\mid X_1,\ldots,X_k)")

            st.markdown("### 2️⃣ Función logística:")
            st.latex(
                r"""
                p_i = \frac{1}{1+e^{-(\beta_0+\beta_1X_{i1}+\cdots+\beta_kX_{ik})}}
                """
            )

            st.markdown("### 3️⃣ Transformación Logit (Log-Odds):")
            st.latex(
                r"""
                \operatorname{logit}(p_i) = \ln\left(\frac{p_i}{1-p_i}\right) = \beta_0+\beta_1X_{i1}+\cdots+\beta_kX_{ik}
                """
            )

            st.markdown(
                """
                <div class="math-box">
                <b>La ventaja de la transformación Logit:</b><br>
                Permite relacionar de forma lineal los predictores con el logaritmo de la ventaja (Odds), acotando la probabilidad final siempre entre 0 y 1.
                </div>
                """,
                unsafe_allow_html=True,
            )
