import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Del artículo a la evidencia | Intento suicida",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta de colores académicos
RED = "#D7263D"
NAVY = "#0F172A"
BLUE = "#2563EB"
GREEN = "#059669"
ORANGE = "#D97706"
PURPLE = "#7C3AED"
GRAY = "#64748B"
LIGHT = "#F8FAFC"
BORDER = "#E2E8F0"

# ============================================================
# ESTILOS CSS CUSTOM
# ============================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background: {LIGHT};
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0F172A 0%, #172554 100%);
        }}
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span:not([data-baseweb]) {{
            color: #F8FAFC;
        }}
        [data-baseweb="select"] *, 
        div[role="listbox"] *,
        .stSelectbox label,
        .stRadio label {{
            color: #000000 !important;
        }}
        .main-title {{
            font-size: 2.0rem;
            font-weight: 800;
            color: {NAVY};
            margin-bottom: 0.1rem;
        }}
        .subtitle {{
            color: {GRAY};
            font-size: 1rem;
            margin-bottom: 1rem;
        }}
        .section-title {{
            font-size: 1.45rem;
            font-weight: 800;
            color: {NAVY};
            margin-top: 0.2rem;
        }}
        .section-subtitle {{
            color: {GRAY};
            margin-bottom: 0.8rem;
        }}
        .card {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 1rem 1.15rem;
            box-shadow: 0 2px 10px rgba(15,23,42,.05);
            height: 100%;
            color: #000000 !important;
        }}
        .card h4 {{
            margin: 0 0 .45rem 0;
            color: {NAVY} !important;
        }}
        .card p, .card div {{
            color: #000000 !important;
        }}
        .metric {{
            font-size: 1.7rem;
            font-weight: 800;
            color: {NAVY};
        }}
        .metric-label {{
            font-size: .85rem;
            color: {GRAY};
        }}
        .interpretation {{
            background: #FFF7ED;
            border-left: 5px solid {ORANGE};
            padding: .9rem 1rem;
            border-radius: 8px;
            margin: .7rem 0;
            color: #000000 !important;
        }}
        .math-box {{
            background: #EFF6FF;
            border: 1px solid #BFDBFE;
            border-radius: 12px;
            padding: 1rem;
            color: #000000 !important;
        }}
        .source-box {{
            background: #F1F5F9;
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: .75rem 1rem;
            font-size: .82rem;
            color: #000000 !important;
        }}
        .step {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: .9rem;
            text-align: center;
            min-height: 120px;
            color: #000000 !important;
        }}
        .step p {{
            color: #000000 !important;
        }}
        .step-number {{
            font-size: .8rem;
            font-weight: 700;
            color: {RED};
        }}
        .step-title {{
            font-weight: 800;
            color: {NAVY};
        }}
        .big-question {{
            font-size: 1.1rem;
            font-weight: 700;
            color: {NAVY};
            background: white;
            border-radius: 14px;
            border: 1px solid {BORDER};
            padding: 0.8rem 1.1rem;
        }}
        div[data-testid="stMetric"] {{
            background: white;
            border: 1px solid {BORDER};
            padding: .7rem;
            border-radius: 12px;
        }}
        div[data-testid="stMetric"] * {{
            color: #000000 !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATOS DEL ARTÍCULO
# ============================================================
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
    columns=["Variable", "Categoría", "Mujer %", "Mujer N", "Hombre %", "Hombre N", "Total %", "Total N", "p"]
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

# ============================================================
# CARGA Y VISUALIZACIÓN DEL ARCHIVO PDF
# ============================================================
def find_article_pdf():
    candidates = [
        Path("intento suicidad.pdf"),
        Path("intento suicida.pdf"),
        Path("intento_suicidad.pdf"),
        Path("intento_suicida.pdf"),
        Path("articulo.pdf"),
        Path("paper.pdf"),
    ]
    # Buscar también en subdirectorios
    for p in candidates:
        if p.exists():
            return p
    for path in Path(".").rglob("*.pdf"):
        return path
    return None

pdf_file = find_article_pdf()
pdf_bytes = pdf_file.read_bytes() if pdf_file else None

def display_pdf_viewer(bytes_data, file_path, page=1, height=820):
    encoded = base64.b64encode(bytes_data).decode("utf-8")
    
    # HTML embebido con PDF.js Viewer y objeto nativo
    html_code = f"""
    <div style="width: 100%; height: {height}px; font-family: sans-serif;">
        <object data="data:application/pdf;base64,{encoded}#page={page}&zoom=100" type="application/pdf" width="100%" height="100%">
            <iframe src="data:application/pdf;base64,{encoded}#page={page}" width="100%" height="100%" style="border:none;">
                <p>Tu navegador no soporta visualización directa. 
                <a href="data:application/pdf;base64,{encoded}" download="{file_path.name if file_path else 'articulo.pdf'}">
                Haz clic aquí para descargar el PDF</a>.</p>
            </iframe>
        </object>
    </div>
    """
    components.html(html_code, height=height + 10, scrolling=False)

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
    if pd.isna(x):
        return "—"
    if x < 0.001:
        return "<0,001"
    return f"{x:.3f}".replace(".", ",")

# ============================================================
# BARRA LATERAL Y NAVEGACIÓN
# ============================================================
with st.sidebar:
    st.markdown("## 📊 MODELOS LINEALES GENERALIZADOS")
    st.caption("UNIVERSIDAD DEL TOLIMA")
    st.markdown("---")
    st.markdown("### Navegación")
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
    st.write("**Diseño:** Analítico transversal")
    
    st.markdown("---")
    if pdf_file:
        st.success(f"📄 Archivo detectado: `{pdf_file.name}`")
        st.download_button(
            label="💾 Descargar PDF completo",
            data=pdf_bytes,
            file_name=pdf_file.name,
            mime="application/pdf"
        )
    else:
        st.error("⚠️ PDF no hallado en el repositorio.")

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

current_page = page_map[section]

# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================
st.markdown('<div class="main-title">Intento suicida: un análisis municipal de factores asociados 2012–2017</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sogamoso, Boyacá · Una lectura del artículo desde la estadística</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1, 1, 1, 3.2])
with c1:
    st.metric("Casos", "524")
with c2:
    st.metric("Mujeres", "336")
with c3:
    st.metric("Hombres", "188")
with c4:
    st.markdown('<div class="big-question">🎯 Idea de la exposición: reconstruir el camino desde los datos hasta la evidencia estadística.</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# LAYOUT PRINCIPAL: PDF DERECHA/IZQUIERDA + EXPLICACIÓN
# ============================================================
left, right = st.columns([1.05, 1.15], gap="medium")

with left:
    st.markdown(f"### 📄 Artículo original (Pág. {current_page})")
    if pdf_bytes is not None:
        display_pdf_viewer(pdf_bytes, pdf_file, page=current_page, height=800)
    else:
        st.warning("Coloque el archivo `intento suicidad.pdf` en la raíz de su repositorio GitHub / Streamlit para activar el visor integrado.")

with right:
    if section == "01 · Introducción":
        section_header("1", "Entrar al estudio", "Conozcamos qué estudiaron los autores y dónde ocurrió.")
        a, b = st.columns(2)
        with a:
            card("¿Qué investigaron?", "El comportamiento epidemiológico del intento de suicidio y diferencias sociodemográficas entre 2012–2017.", "🎯")
        with b:
            card("¿Dónde?", "Municipio de <b>Sogamoso, Boyacá, Colombia</b>. Datos del SIVIGILA.", "📍")
        st.markdown("<br>", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            card("Periodo", "<b>2012–2017</b>", "📅")
        with b:
            card("Casos analizados", "<b>524</b>", "👥")
        with c:
            card("Modelo", "<b>Regresión logística</b>", "📐")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="interpretation"><b>Pregunta para abrir la exposición:</b><br>¿Qué diferencias existen entre hombres y mujeres en los casos reportados en Sogamoso?</div>', unsafe_allow_html=True)
        source_box("Resumen y objetivo del artículo.")

    elif section == "02 · Contexto y pregunta":
        section_header("2", "Del problema a la pregunta estadística", "Contextualización territorial.")
        card("🌎 ¿Por qué Sogamoso?", "Sogamoso reportaba la mayor cantidad de casos en el departamento de Boyacá desde 2010.", "📍")
        st.markdown("<br>", unsafe_allow_html=True)
        st.latex(r"Y = \text{Género (Hombre / Mujer)}")
        st.markdown("**Variables explicativas:** edad, ocupación, estado civil, desencadenante, violencia, consumo de alcohol, etc.")
        source_box("Definición de variables del estudio.")

    elif section == "03 · Datos y diseño":
        section_header("3", "¿Cómo se construyó la información?", "Recorrido metodológico de los datos.")
        cols = st.columns(5)
        steps = [
            ("01", "Caso", "Persona con intento de suicidio"),
            ("02", "UPGD", "Notificación"),
            ("03", "SIVIGILA", "Registro"),
            ("04", "Seguimiento", "Ficha clínica"),
            ("05", "Análisis", "524 casos"),
        ]
        for col, (num, title, body) in zip(cols, steps):
            with col:
                st.markdown(f'<div class="step"><div class="step-number">{num}</div><div class="step-title">{title}</div><p>{body}</p></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a: card("Potenciales", "<b>579</b>", "📥")
        with b: card("Excluidos", "<b>55</b>", "↘️")
        with c: card("Analizados", "<b>524</b>", "✅")
        source_box("Diseño analítico transversal.")

    elif section == "04 · Prevalencia":
        section_header("4", "Prevalencia ajustada por edad", "Comportamiento por grupo de edad y año.")
        fig = px.line(prev_df, x="Grupo de edad", y="Prevalencia", color="Año", markers=True)
        fig.update_layout(height=450, margin=dict(l=10, r=10, t=20, b=10), xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="interpretation"><b>Pico principal:</b> El grupo de 15 a 19 años presenta la mayor prevalencia.</div>', unsafe_allow_html=True)

    elif section == "05 · Tabla 1 · Descriptivos":
        section_header("5", "Tabla 1: Análisis Descriptivo", "Patrones sociodemográficos.")
        variable = st.selectbox("Seleccione una variable de la Tabla 1", table1_df["Variable"].drop_duplicates().tolist())
        d = table1_df[table1_df["Variable"] == variable].copy()
        display = d[["Categoría", "Mujer %", "Mujer N", "Hombre %", "Hombre N", "Total %", "Total N", "p"]].copy()
        display["p"] = display["p"].map(fmt_p)
        st.dataframe(display, use_container_width=True, hide_index=True)

    elif section == "06 · Modelo logístico":
        section_header("6", "Fundamentos del Modelo Logístico", "Especificación del Modelo Lineal Generalizado.")
        st.latex(r"\ln\left(\frac{P(Y=1)}{1-P(Y=1)}\right) = \beta_0 + \beta_1 X_1 + \dots + \beta_k X_k")
        st.markdown("<div class="math-box">El enlace Logit permite modelar la probabilidad de ocurrencia en función de predictores.</div>", unsafe_allow_html=True)

    elif section == "07 · Tabla 2 · Modelo final":
        section_header("7", "Tabla 2: Modelo Regresión Logística Final", "Coeficientes y OR ajustados.")
        st.dataframe(table2_df, use_container_width=True, hide_index=True)

    elif section == "08 · Interpretación del OR":
        section_header("8", "Interpretación de Odds Ratios (OR)", "Análisis del riesgo relativo.")
        card("Consumo de Alcohol", "<b>OR = 3.58</b> (IC 95%: 2.17 - 5.90). El consumo de alcohol incrementa significativamente la asociación con el grupo de hombres.", "📊")

    elif section == "09 · Evaluación del modelo":
        section_header("9", "Bondad de Ajuste y Diagnóstico", "Verificación de supuestos.")
        st.write("Se evaluaron el test de Hosmer-Lemeshow y los residuos para asegurar la validez del modelo final.")

    elif section == "10 · Discusión":
        section_header("10", "Discusión de Resultados", "Contrastación con literatura.")
        card("Comparación", "Los picos en jóvenes coinciden con los reportes nacionales de salud pública en Colombia.", "💡")

    elif section == "11 · Conclusiones":
        section_header("11", "Conclusiones principales", "Cierre del análisis.")
        card("Conclusión final", "Es indispensable priorizar las estrategias de intervención en población joven y abordar el consumo de alcohol como factor clave.", "🏁")
