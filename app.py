import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Del artículo a la evidencia | Intento suicida",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta sobria para una exposición académica
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
# ESTILOS
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

        [data-testid="stSidebar"] * {{
            color: #F8FAFC !important;
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
        }}

        .card h4 {{
            margin: 0 0 .45rem 0;
            color: {NAVY};
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
        }}

        .math-box {{
            background: #EFF6FF;
            border: 1px solid #BFDBFE;
            border-radius: 12px;
            padding: 1rem;
        }}

        .source-box {{
            background: #F1F5F9;
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: .75rem 1rem;
            font-size: .82rem;
            color: {GRAY};
        }}

        .step {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: .9rem;
            text-align: center;
            min-height: 120px;
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

        .small-note {{
            color: {GRAY};
            font-size: .82rem;
        }}

        .big-question {{
            font-size: 1.25rem;
            font-weight: 750;
            color: {NAVY};
            background: white;
            border-radius: 14px;
            border: 1px solid {BORDER};
            padding: 1rem 1.2rem;
        }}

        div[data-testid="stMetric"] {{
            background: white;
            border: 1px solid {BORDER};
            padding: .7rem;
            border-radius: 12px;
        }}

        .footer {{
            color: {GRAY};
            text-align: center;
            font-size: .78rem;
            margin-top: 1.5rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATOS TRANSCRITOS DEL ARTÍCULO
# ============================================================
# Figura 1: prevalencia ajustada por grupo de edad y año de ocurrencia.
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

# Tabla 1: variables sociodemográficas y específicas.
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

# Tabla 2: modelo final reportado por los autores.
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
# FUNCIONES
# ============================================================
def article_path():
    candidates = [
        Path("intento suicida(1).pdf"),
        Path("intento_suicida.pdf"),
        Path("articulo.pdf"),
        Path("paper.pdf"),
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def pdf_viewer(pdf_bytes, page=1, height=850):
    encoded = base64.b64encode(pdf_bytes).decode("utf-8")
    html = f"""
    <iframe
        src="data:application/pdf;base64,{encoded}#page={page}&zoom=page-width"
        width="100%"
        height="{height}px"
        style="border:1px solid #E2E8F0;border-radius:12px;background:white;"
        type="application/pdf">
    </iframe>
    """
    components.html(html, height=height + 15, scrolling=False)


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


def fmt_num(x):
    if pd.isna(x):
        return "—"
    return f"{x:.2f}".replace(".", ",")


# ============================================================
# PDF: carga
# ============================================================
local_pdf = article_path()

with st.sidebar:
    st.markdown("## 📊 DEL ARTÍCULO A LA EVIDENCIA")
    st.caption("Presentación interactiva del estudio")

    uploaded = st.file_uploader(
        "Si no está en la carpeta, carga aquí el PDF",
        type=["pdf"],
        help="En Streamlit Cloud puedes subir el PDF mediante este control o dejarlo junto a app.py.",
    )

    if uploaded is not None:
        pdf_bytes = uploaded.read()
    elif local_pdf is not None:
        pdf_bytes = local_pdf.read_bytes()
    else:
        pdf_bytes = None

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
    st.write("**Diseño:** analítico transversal")

    st.markdown("---")
    st.caption("Fuente de los resultados: Vásquez-Escobar & Benítez-Camargo (2021).")

# ============================================================
# MAPA DE PÁGINAS DEL ARTÍCULO
# ============================================================
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
# ENCABEZADO
# ============================================================
st.markdown(
    '<div class="main-title">Intento suicida: un análisis municipal de factores asociados 2012–2017</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Sogamoso, Boyacá · Una lectura del artículo desde la estadística</div>',
    unsafe_allow_html=True,
)

# Barra superior
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

# ============================================================
# LAYOUT PRINCIPAL: PDF + EXPLICACIÓN
# ============================================================
left, right = st.columns([1.02, 1.18], gap="large")

with left:
    st.markdown("### 📄 Artículo original")
    st.caption(f"Página mostrada: {current_page} de 15")
    if pdf_bytes is not None:
        pdf_viewer(pdf_bytes, page=current_page, height=820)
    else:
        st.warning(
            "No se encontró el PDF. Colócalo junto a app.py con el nombre "
            "'intento suicida(1).pdf' o cárgalo desde la barra lateral."
        )
        st.info(
            "La parte analítica de la aplicación seguirá funcionando aunque no se cargue el PDF."
        )

with right:
    # ========================================================
    # 01 INTRODUCCIÓN
    # ========================================================
    if section == "01 · Introducción":
        section_header(
            "1",
            "Entrar al estudio",
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
            '<div class="interpretation"><b>Pregunta para abrir la exposición:</b><br>'
            '¿Qué diferencias existen entre hombres y mujeres entre los casos de intento de suicidio registrados en Sogamoso y qué variables aparecen asociadas estadísticamente con el género?</div>',
            unsafe_allow_html=True,
        )
        source_box("Resumen y objetivo del artículo.")

    # ========================================================
    # 02 CONTEXTO
    # ========================================================
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
            redes de apoyo, entre otras consideradas por los autores.
            """
        )

        source_box("El artículo define género como la variable de interés y describe las variables sociodemográficas, específicas y psicosociales.")

    # ========================================================
    # 03 DATOS Y DISEÑO
    # ========================================================
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
            "Para el análisis univariado se calcularon prevalencias ajustadas por edad mediante el método directo y una población estándar propuesta por la OMS. Para las variables asociadas al género se utilizó regresión logística bivariada."
        )

        source_box("Materiales y métodos del artículo.")

    # ========================================================
    # 04 PREVALENCIA
    # ========================================================
    elif section == "04 · Prevalencia":
        section_header(
            "4",
            "Prevalencia ajustada por edad: ¿dónde se concentra el fenómeno?",
            "Esta es una de las figuras centrales del artículo. No es una tasa anual simple: cruza año y grupo de edad.",
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
                <b>15–19 años</b> presenta valores elevados a lo largo del periodo;
                el artículo señala un pico de 22,3 por 100.000 habitantes al inicio
                y 21 por 100.000 al final del periodo.
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

            st.info(
                "El mapa de calor permite identificar rápidamente dónde se concentran los valores altos: principalmente en adolescencia y adultez temprana."
            )

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

        st.markdown("### ¿Cómo interpretarla sin equivocarnos?")

        a, b = st.columns(2)
        with a:
            card(
                "No mirar solamente el máximo",
                "La figura debe leerse como una estructura de edades a través del tiempo. El interés está en la concentración y en su comportamiento, no solo en encontrar el año con el valor más alto.",
                "👁️",
            )
        with b:
            card(
                "Conclusión de los autores",
                "Las prevalencias ajustadas por edad no muestran una reducción significativa desde el inicio hasta el final del periodo y existe concentración en edades tempranas.",
                "📌",
            )

        source_box("Figura 1 y texto de resultados: prevalencia ajustada por grupo de edad y año de ocurrencia.")

    # ========================================================
    # 05 TABLA 1
    # ========================================================
    elif section == "05 · Tabla 1 · Descriptivos":
        section_header(
            "5",
            "Tabla 1: primero conozcamos quiénes están en los datos",
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

        # Gráfico
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

        st.markdown("### 🧠 ¿Qué debe decir el expositor?")

        interpretation_map = {
            "Área de ocurrencia": "La mayoría de los casos corresponde al área urbana. La diferencia por sexo aparece estadísticamente significativa según el valor p reportado (0,02).",
            "Edad agrupada": "La adolescencia concentra 50,3% de los casos de mujeres, mientras que en hombres la adultez temprana representa 45,7%. El valor p reportado es <0,001.",
            "Estado civil": "Soltero es la categoría más frecuente en ambos grupos, pero el valor p reportado para la comparación global es 0,115.",
            "Ocupación": "Estudiante es la categoría de mayor representación en ambos sexos; también aparecen diferencias marcadas en ama de casa, desempleo y otras categorías. El valor p reportado es <0,001.",
            "Forma de realización": "La forma impulsiva es predominante en ambos grupos. El valor p es 0,551, por lo que no se observa evidencia de diferencia estadísticamente significativa bajo el umbral de 0,05.",
            "Antecedentes de intento": "La distribución entre presencia y ausencia de antecedentes es parecida entre sexos; el valor p reportado es 0,80.",
            "Método del intento": "La intoxicación con medicamentos es la categoría más frecuente en mujeres y también representa una proporción importante en hombres. El valor p reportado es <0,001.",
            "Posible desencadenante": "El conflicto con la pareja es el desencadenante con mayor porcentaje en mujeres y uno de los principales en hombres. El valor p reportado es 0,005.",
            "Enfermedad mental": "No se observa una diferencia marcada entre mujeres y hombres en la presencia de diagnóstico; el valor p es 0,68.",
            "Violencia": "La proporción de violencia reportada es mayor en mujeres (54%) que en hombres (37,5%). El valor p reportado es 0,001.",
            "Consumo de alcohol": "El consumo de alcohol aparece en 40,3% de mujeres y 59,7% de hombres. El valor p reportado es <0,001.",
            "Relaciones familiares": "Las relaciones familiares disfuncionales son muy frecuentes en ambos grupos, con porcentajes cercanos al 80%. El valor p es 0,69.",
            "Redes de apoyo": "La mayoría reporta redes de apoyo en ambos grupos. El valor p reportado es 0,23.",
        }

        st.markdown(
            f'<div class="interpretation">{interpretation_map.get(variable, "Revise las diferencias descriptivas y el valor p reportado.")}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="small-note">⚠️ El valor p de la Tabla 1 describe la comparación reportada por los autores; no es todavía el resultado del modelo logístico.</div>',
            unsafe_allow_html=True,
        )
        source_box("Tabla 1 del artículo. Los porcentajes y frecuencias fueron transcritos de la tabla publicada.")

    # ========================================================
    # 06 MODELO LOGÍSTICO
    # ========================================================
    elif section == "06 · Modelo logístico":
        section_header(
            "6",
            "¿Por qué aparece la regresión logística?",
            "Aquí comienza la parte matemática de la exposición.",
        )

        st.markdown(
            '<div class="big-question">La variable de interés es binaria: queremos modelar la pertenencia al grupo de género.</div>',
            unsafe_allow_html=True,
        )

        st.latex(
            r"""
            Y_i =
            \begin{cases}
            1 & \text{si la observación pertenece a la categoría codificada como 1}\\
            0 & \text{si pertenece a la categoría codificada como 0}
            \end{cases}
            """
        )

        st.markdown("### 1️⃣ Queremos una probabilidad")
        st.latex(r"p_i=P(Y_i=1\mid X_1,\ldots,X_k)")

        st.markdown("### 2️⃣ La probabilidad debe permanecer entre 0 y 1")

        st.latex(
            r"""
            p_i=
            \frac{1}{1+e^{-(\beta_0+\beta_1X_{i1}+\cdots+\beta_kX_{ik})}}
            """
        )

        st.markdown("### 3️⃣ Transformamos la probabilidad en log-odds")

        st.latex(
            r"""
            \operatorname{logit}(p_i)
            =
            \ln\left(\frac{p_i}{1-p_i}\right)
            =
            \beta_0+\beta_1X_{i1}+\cdots+\beta_kX_{ik}
            """
        )

        st.markdown(
            """
            <div class="math-box">
            <b>La conexión clave para explicar en clase:</b><br><br>
            Probabilidad → Odds → Log-Odds → combinación lineal de variables.
            <br><br>
            Cuando exponenciamos un coeficiente:
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.latex(r"OR=e^{\beta}")

        st.markdown(
            """
            Esto permite interpretar el coeficiente mediante el **odds ratio**.
            Un OR igual a 1 representa ausencia de diferencia en odds respecto a
            la categoría de referencia; OR mayor que 1 indica mayores odds y OR
            menor que 1 indica menores odds, siempre respecto a la referencia y
            bajo la codificación del modelo.
            """
        )

        st.markdown("### Cómo entraron las variables al modelo")

        stages = [
            ("Modelo 1", "Ciclo vital / edad", "Punto de partida"),
            ("Modelo 2", "+ Posible desencadenante", "Se incorpora contexto del evento"),
            ("Modelo 3", "+ Violencia", "Aparece asociación significativa"),
            ("Modelo 4", "+ Consumo de alcohol", "Modelo final reportado"),
        ]

        cols = st.columns(4)
        for col, (name, vars_, desc) in zip(cols, stages):
            with col:
                st.markdown(
                    f"""
                    <div class="step">
                        <div class="step-number">{name}</div>
                        <div class="step-title">{vars_}</div>
                        <p>{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        source_box("Métodos y descripción de los modelos. Los autores indican que las variables se introdujeron una a una según el orden de presentación.")

    # ========================================================
    # 07 TABLA 2
    # ========================================================
    elif section == "07 · Tabla 2 · Modelo final":
        section_header(
            "7",
            "Tabla 2: del dato descriptivo a la asociación ajustada",
            "Ahora dejamos de preguntar solamente '¿cuánto hay?' y preguntamos '¿cómo se asocia con el género dentro del modelo?'",
        )

        st.dataframe(
            table2_df.style.format({
                "B": "{:.2f}",
                "Wald": "{:.2f}",
                "p": lambda x: "<0,001" if x < 0.001 else f"{x:.2f}",
                "OR": "{:.2f}",
                "IC95% inf.": "{:.2f}",
                "IC95% sup.": "{:.2f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### 🔍 Filtro para interpretar")

        sig_only = st.checkbox("Mostrar solamente filas con p ≤ 0,05", value=True)

        d = table2_df.copy()
        if sig_only:
            d = d[d["p"] <= 0.05]

        plot_d = d[d["OR"].notna()].copy()

        fig = go.Figure()

        for _, row in plot_d.iterrows():
            if row["OR"] > 0:
                fig.add_trace(
                    go.Scatter(
                        x=[row["OR"]],
                        y=[row["Categoría"]],
                        mode="markers",
                        error_x=dict(
                            type="data",
                            symmetric=False,
                            array=[row["IC95% sup."] - row["OR"]],
                            arrayminus=[row["OR"] - row["IC95% inf."]],
                        ),
                        name=row["Categoría"],
                        showlegend=False,
                    )
                )

        fig.add_vline(x=1, line_dash="dash")
        fig.update_layout(
            height=560,
            xaxis_type="log",
            xaxis_title="Odds Ratio (escala logarítmica)",
            yaxis_title="Categoría",
            margin=dict(l=10, r=10, t=30, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "La línea vertical OR=1 es la referencia. Si el intervalo de confianza incluye 1, la evidencia de asociación al 5% es débil/no significativa para esa categoría bajo la lectura habitual del intervalo."
        )

        source_box("Tabla 2 del artículo: B, Wald, significancia, OR e intervalo de confianza del 95%.")

    # ========================================================
    # 08 OR
    # ========================================================
    elif section == "08 · Interpretación del OR":
        section_header(
            "8",
            "OR: convertir la tabla en una explicación comprensible",
            "Elegimos resultados centrales del artículo y los interpretamos cuidadosamente.",
        )

        choice = st.selectbox(
            "Seleccione el resultado",
            [
                "Consumo de alcohol",
                "Adolescencia",
                "Adultez temprana",
                "Conflicto con la pareja",
                "Violencia",
            ],
        )

        results = {
            "Consumo de alcohol": {
                "beta": 1.28,
                "or": 3.58,
                "low": 2.17,
                "high": 5.90,
                "p": "<0,001",
                "text": "El modelo reporta OR=3,58 para consumo de alcohol. En la parametrización de la tabla, este valor es mayor que 1 y su IC95% (2,17–5,90) no contiene 1.",
                "warning": "No decir '3,58 veces más probable'. OR es una razón de odds, no una razón directa de probabilidades.",
            },
            "Adolescencia": {
                "beta": -1.04,
                "or": 0.35,
                "low": 0.17,
                "high": 0.74,
                "p": "0,01",
                "text": "El modelo reporta OR=0,35 para adolescencia respecto a la categoría de referencia indicada en la tabla. Los autores invierten este OR para facilitar una lectura en términos del grupo femenino: 1/0,35 ≈ 2,86.",
                "warning": "La inversión cambia la forma de expresar la comparación; no cambia la evidencia contenida en el modelo.",
            },
            "Adultez temprana": {
                "beta": -0.81,
                "or": 0.45,
                "low": 0.22,
                "high": 0.92,
                "p": "0,03",
                "text": "El OR reportado es 0,45 respecto a la referencia. Los autores expresan el resultado inversamente: 1/0,45 ≈ 2,2 para facilitar la comparación hacia las mujeres.",
                "warning": "Siempre hay que mencionar la categoría de referencia y la dirección de la comparación.",
            },
            "Conflicto con la pareja": {
                "beta": -0.84,
                "or": 0.43,
                "low": 0.24,
                "high": 0.78,
                "p": "0,01",
                "text": "El OR de la tabla es 0,43. Los autores lo expresan como 1/0,43 ≈ 2,32 para interpretar la asociación hacia las mujeres.",
                "warning": "No confundir 'asociado con el género' con causalidad del intento de suicidio.",
            },
            "Violencia": {
                "beta": -0.89,
                "or": 0.41,
                "low": 0.26,
                "high": 0.66,
                "p": "<0,001",
                "text": "El OR reportado es 0,41 y los autores lo invierten: 1/0,41 ≈ 2,43, expresando la asociación hacia las mujeres.",
                "warning": "La interpretación depende de la codificación y de la categoría de referencia.",
            },
        }

        r = results[choice]

        a, b, c = st.columns(3)
        with a:
            st.metric("B", f"{r['beta']:.2f}")
        with b:
            st.metric("OR", f"{r['or']:.2f}")
        with c:
            st.metric("IC 95%", f"{r['low']:.2f} – {r['high']:.2f}")

        st.markdown("### La matemática detrás")

        st.latex(rf"OR=e^\beta=e^{{{r['beta']:.2f}}}\approx {r['or']:.2f}")

        if r["or"] < 1:
            st.latex(rf"\frac{{1}}{{OR}}=\frac{{1}}{{{r['or']:.2f}}}\approx {1/r['or']:.2f}")

        st.markdown(
            f'<div class="interpretation"><b>Interpretación:</b> {r["text"]}</div>',
            unsafe_allow_html=True,
        )
        st.warning(r["warning"])

        st.markdown("### Tres reglas para no equivocarnos")

        rules = [
            ("OR = 1", "No diferencia en odds respecto a la referencia."),
            ("OR > 1", "Mayores odds respecto a la referencia."),
            ("OR < 1", "Menores odds respecto a la referencia."),
        ]

        cols = st.columns(3)
        for col, (title, body) in zip(cols, rules):
            with col:
                card(title, body, "📐")

        source_box("Resultados e interpretación del modelo final reportado por los autores.")

    # ========================================================
    # 09 EVALUACIÓN
    # ========================================================
    elif section == "09 · Evaluación del modelo":
        section_header(
            "9",
            "¿Qué tan adecuado es el modelo?",
            "No basta con obtener OR significativos: también debemos mirar la información de evaluación que reporta el artículo.",
        )

        metrics = [
            ("Durbin-Watson", "1,94", "Los autores lo relacionan con el supuesto de independencia de errores."),
            ("VIF", "1", "Los autores reportan ausencia de multicolinealidad según este indicador."),
            ("Hosmer-Lemeshow", "p > 0,05", "No se rechaza el buen ajuste bajo esta prueba, según lo reportado."),
            ("Clasificación", "71,1%", "Porcentaje de acierto reportado para la clasificación del género."),
            ("Cox & Snell", "0,13", "Pseudo-R²; no debe interpretarse igual que un R² de regresión lineal."),
        ]

        cols = st.columns(2)
        for i, (name, value, explanation) in enumerate(metrics):
            with cols[i % 2]:
                card(name, f"<div class='metric'>{value}</div><p>{explanation}</p>", "📊")

        st.markdown("### ¿Qué significa estadísticamente?")

        st.markdown(
            """
            **1. VIF = 1:** los autores reportan que no existe problema de
            multicolinealidad según este indicador.

            **2. Hosmer-Lemeshow:** el artículo utiliza esta prueba como evidencia
            de ajuste del modelo.

            **3. 71,1% de acierto:** describe la proporción de clasificaciones
            correctas reportada por los autores; no significa que el modelo tenga
            una 'probabilidad de verdad' de 71,1%.

            **4. Cox & Snell = 0,13:** es un pseudo-R² y debe interpretarse con
            precaución; no equivale al R² clásico de mínimos cuadrados.
            """
        )

        st.markdown(
            '<div class="interpretation"><b>Punto crítico para la exposición:</b> un modelo puede tener asociaciones estadísticamente significativas y, al mismo tiempo, una capacidad explicativa limitada. Por eso conviene separar significancia, ajuste y capacidad predictiva.</div>',
            unsafe_allow_html=True,
        )

        source_box("Indicadores de evaluación reportados en el artículo.")

    # ========================================================
    # 10 DISCUSIÓN
    # ========================================================
    elif section == "10 · Discusión":
        section_header(
            "10",
            "¿Cómo conectan los autores los resultados?",
            "Aquí volvemos de la estadística al fenómeno que están intentando comprender.",
        )

        a, b = st.columns(2)
        with a:
            card(
                "Mujeres",
                "<b>Adolescencia + adultez temprana + violencia + conflictos de pareja/familia</b> aparecen como elementos importantes en la interpretación de los autores.",
                "👩",
            )
        with b:
            card(
                "Hombres",
                "<b>Consumo de alcohol</b> aparece como una variable significativamente asociada con el género hombre en el modelo final.",
                "👨",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            ### Una lectura estadística importante

            El artículo habla de **factores asociados**. Por tratarse de un estudio
            analítico transversal, la presentación debe evitar transformar
            automáticamente una asociación estadística en una afirmación causal.

            Por ejemplo:

            ❌ “El alcohol causa el intento de suicidio.”

            ✅ “El consumo de alcohol presentó una asociación estadísticamente
            significativa con el género en los casos analizados.”
            """
        )

        st.markdown(
            '<div class="interpretation"><b>La pregunta crítica:</b> ¿qué nos permite afirmar el modelo y qué cosas quedan fuera de su alcance?</div>',
            unsafe_allow_html=True,
        )

        source_box("Discusión y conclusiones del artículo; la distinción entre asociación y causalidad es una lectura estadística prudente del diseño reportado.")

    # ========================================================
    # 11 CONCLUSIONES
    # ========================================================
    elif section == "11 · Conclusiones":
        section_header(
            "11",
            "Cerrar la historia: del dato a la evidencia",
            "Una conclusión fuerte debe responder la pregunta inicial y reconocer los límites de la evidencia.",
        )

        st.markdown(
            """
            <div class="card">
            <h4>1. El fenómeno se concentra en edades tempranas</h4>
            <p>
            La Figura 1 muestra valores altos de prevalencia ajustada en grupos
            adolescentes y de adultez temprana. Los autores concluyen que no hubo
            una reducción significativa de las prevalencias ajustadas por edad
            entre el inicio y el final del periodo.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="card">
            <h4>2. Existen diferencias según género</h4>
            <p>
            El modelo identifica asociaciones diferentes. Los autores reportan
            asociaciones hacia las mujeres en adolescencia, adultez temprana,
            conflicto de pareja y violencia, mientras que el consumo de alcohol
            aparece asociado con el género hombre.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="card">
            <h4>3. La estadística permite pasar de describir a modelar</h4>
            <p>
            La exposición puede resumirse como una cadena:
            <b>población → datos → descriptivos → pregunta → modelo logístico →
            OR/IC/p → evaluación → interpretación crítica.</b>
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="big-question">🎤 Frase final sugerida: “Más que memorizar un OR, lo importante es entender cómo una pregunta sobre una población se convierte en una estructura matemática capaz de resumir la evidencia disponible.”</div>',
            unsafe_allow_html=True,
        )

        source_box("Síntesis construida a partir de los resultados y conclusiones del artículo.")

# ============================================================
# NAVEGACIÓN EXTRA: página manual
# ============================================================
st.markdown("---")
st.markdown("### 🎛️ Control rápido del artículo")

manual_page = st.slider(
    "Si durante la exposición quieres mover el PDF independientemente de la sección",
    min_value=1,
    max_value=15,
    value=current_page,
)

if manual_page != current_page and pdf_bytes is not None:
    st.caption(f"Vista manual: página {manual_page}")
    pdf_viewer(pdf_bytes, page=manual_page, height=500)

st.markdown(
    '<div class="footer">Aplicación educativa para exposición académica · Datos y resultados transcritos del artículo proporcionado.</div>',
    unsafe_allow_html=True,
)
