import os
import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sustentación Anteproyecto | Universidad del Tolima",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CARGA DEL LOGO DE LA UNIVERSIDAD DEL TOLIMA (LOCAL O SVG)
# ---------------------------------------------------------
def obtener_logo_ut():
    for raiz, _, archivos in os.walk("."):
        for archivo in archivos:
            if archivo.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".webp")):
                ruta = os.path.join(raiz, archivo)
                ext = archivo.split(".")[-1].lower()
                mime = "svg+xml" if ext == "svg" else ("jpeg" if ext in ["jpg", "jpeg"] else ext)
                with open(ruta, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                return f"data:image/{mime};base64,{b64}"
    
    svg_ut = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 135" width="90" height="100">
        <path d="M10,10 H110 V75 C110,105 60,128 60,128 C60,128 10,105 10,75 Z" fill="#B71C1C" stroke="#F0F6FC" stroke-width="4"/>
        <path d="M18,18 H102 V72 C102,97 60,118 60,118 C60,118 18,97 18,72 Z" fill="#161B22" stroke="#D4AF37" stroke-width="2"/>
        <text x="60" y="68" font-family="Georgia, serif" font-size="34" font-weight="bold" fill="#F0F6FC" text-anchor="middle">UT</text>
        <text x="60" y="90" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#D4AF37" text-anchor="middle">TOLIMA</text>
    </svg>
    """
    b64_svg = base64.b64encode(svg_ut.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64_svg}"

LOGO_SRC = obtener_logo_ut()

# ---------------------------------------------------------
# ESTILOS CSS SOBRIOS E INSTITUCIONALES
# ---------------------------------------------------------
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        background-color: #0E1117;
    }
    .inst-banner {
        background-color: #161B22;
        border-left: 5px solid #B71C1C;
        border-bottom: 1px solid #30363D;
        padding: 14px 20px;
        border-radius: 6px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .inst-title {
        color: #F0F6FC;
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.4px;
    }
    .inst-sub {
        color: #8B949E;
        font-size: 0.88rem;
        margin: 2px 0 0 0;
    }
    .doc-box {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-top: 4px solid #B71C1C;
        border-radius: 8px;
        padding: 22px;
        animation: fadeIn 0.4s ease-out;
    }
    .doc-header {
        color: #E6EDF3;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        font-weight: 700;
        margin-bottom: 12px;
        border-bottom: 1px solid #30363D;
        padding-bottom: 8px;
    }
    .doc-text {
        color: #C9D1D9;
        font-size: 0.94rem;
        line-height: 1.65;
        text-align: justify;
    }
    .doc-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.88rem;
        color: #C9D1D9;
    }
    .doc-table th, .doc-table td {
        border: 1px solid #30363D;
        padding: 6px 10px;
        text-align: left;
    }
    .doc-table th {
        background-color: #21262D;
        color: #F0F6FC;
    }
    .card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-left: 4px solid #388BFD;
        padding: 18px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        animation: fadeIn 0.5s ease-out;
    }
    .card-red {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-left: 4px solid #B71C1C;
        padding: 18px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        animation: fadeIn 0.5s ease-out;
    }
    .card-title {
        color: #F0F6FC;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .highlight-text {
        color: #C9D1D9;
        font-size: 0.96rem;
        line-height: 1.55;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CARGA ROBUSTA DE LA BASE REAL (BASE_ESPECIFICA.xlsx)
# ---------------------------------------------------------
@st.cache_data
def cargar_datos():
    try:
        ruta_archivo = None
        for raiz, _, archivos in os.walk("."):
            for archivo in archivos:
                if archivo.lower() == "base_especifica.xlsx":
                    ruta_archivo = os.path.join(raiz, archivo)
                    break
        if ruta_archivo:
            df_base = pd.read_excel(ruta_archivo, sheet_name="Base_Statico")
            df_dic = pd.read_excel(ruta_archivo, sheet_name="Diccionario")
            return df_base, df_dic, True, "OK"
        return None, None, False, f"No se encontró BASE_ESPECIFICA.xlsx. Archivos en el repositorio: {os.listdir('.')}"
    except Exception as e:
        return None, None, False, f"Error al leer Excel: {e}"

df_base, df_dic, base_cargada, estado_carga = cargar_datos()

# ---------------------------------------------------------
# 1. BARRA LATERAL: LOGO Y NOMBRE ARRIBA DEL MENÚ
# ---------------------------------------------------------
st.sidebar.markdown(
    f"""
    <div style="text-align: center; padding: 10px 0 15px 0;">
        <img src="{LOGO_SRC}" width="85" alt="Universidad del Tolima">
        <div style="color: #F0F6FC; font-weight: 700; font-size: 0.95rem; margin-top: 8px;">
        </div>
        <div style="color: #8B949E; font-size: 0.8rem;">
            Grupo de Investigación GINVAE-UT<br>Línea: Análisis Multivariado
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

seccion = st.sidebar.radio(
    "Estructura del Anteproyecto",
    [
        "I. Título, Autores y Resumen",
        "II. Justificación",
        "III. Planteamiento del Problema",
        "IV. Marco Referencial",
        "V. Objetivos",
        "VI. Diseño Metodológico y Cubo 3D",
        "VII. Aspectos Bioéticos y Cronograma",
        "VIII. Resultados Esperados y Evaluadores"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Panel izquierdo: Texto literal del formato oficial.\nPanel derecho: Síntesis gráfica e interactiva.")

# ---------------------------------------------------------
# 2. ENCABEZADO SUPERIOR INSTITUCIONAL (SIN LOGO)
# ---------------------------------------------------------
st.markdown(
    """
    <div class="inst-banner">
        <div>
            <p class="inst-title">SOCIALIZACIÓN DE ANTEPROYECTO DE TRABAJO DE GRADO</p>
            <p class="inst-sub">Análisis Departamental de indicadores de delitos y afectación a la fuerza pública en Colombia (2012–2024)</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# I. TÍTULO, AUTORES Y RESUMEN
# =========================================================
if seccion == "I. Título, Autores y Resumen":
    st.header("I. Identificación y Resumen del Anteproyecto")
    col_doc, col_app = st.columns([1.05, 1.1], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítems 1 al 6</div>
            <div class="doc-text">
                <b>1. TÍTULO:</b><br>
                Análisis Departamental de indicadores de delitos y afectación a la fuerza pública en Colombia: Un estudio mediante técnicas multivía.<br><br>
                <b>2. AUTORES:</b>
                <table class="doc-table">
                    <tr><th>Ítem</th><th>Nombres y apellidos</th><th>Identificación</th><th>Cargo</th></tr>
                    <tr><td>1</td><td>Miguel Ángel Garatejo Capera</td><td>1110174469</td><td>Estudiante</td></tr>
                    <tr><td>2</td><td>Edith Johana Medina Hernández</td><td>43909879</td><td>Profesora</td></tr>
                </table><br>
                <b>3. GRUPO DE INVESTIGACIÓN:</b><br>
                Grupo de investigación en Análisis Estadístico de la Universidad del Tolima (GINVAE-UT).<br><br>
                <b>4. LÍNEAS INSTITUCIONALES:</b> Análisis multivariado.<br><br>
                <b>5. RESUMEN:</b><br>
                En este trabajo de grado se busca analizar de forma conjunta la evolución de indicadores de delitos y de afectaciones a la fuerza pública en los departamentos de Colombia, mediante la exploración de indicadores publicados por el Observatorio de Derechos Humanos y Defensa Nacional del Ministerio de Defensa. Se propone modelar los datos en tres vías (departamentos, años e indicadores), a través de técnicas de la familia STATIS (particularmente X-STATIS y STATICO), buscando identificar trayectorias territoriales similares, evaluar la estabilidad de estos patrones a lo largo del tiempo, y determinar cuáles variables delictivas ejercen mayor peso en las desigualdades regionales observadas. Como resultado, se espera generar una caracterización multidimensional que sirva de insumo técnico para estudios posteriores asociados al diseño y focalización de políticas públicas de seguridad.<br><br>
                <b>6. DURACIÓN:</b> 6 meses.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Síntesis Ejecutiva")
        m1, m2, m3 = st.columns(3)
        m1.metric("Territorios (n)", "32 Dptos.", "Sin Bogotá D.C.")
        m2.metric("Serie Temporal (k)", "13 Años", "2012 – 2024")
        m3.metric("Indicadores", "10 Variables", "4 Bloque X | 6 Bloque Y")

        st.markdown("""
        <div class="card">
            <div class="card-title">Propósito Central del Estudio</div>
            <p class="highlight-text">
                Modelar de forma simultánea la estructura tridimensional <b>(32 Departamentos × 13 Años × 10 Indicadores)</b> 
                mediante técnicas multivía de la familia <b>STATIS (X-STATIS y STATICO)</b> para:
                <br><br>
                1. Identificar trayectorias departamentales comunes.<br>
                2. Evaluar la estabilidad o ruptura de patrones en el tiempo.<br>
                3. Determinar qué indicadores explican las desigualdades regionales.
            </p>
        </div>
        <div class="card-red">
            <div class="card-title">Aporte Institucional</div>
            <p class="highlight-text">
                Generar un insumo técnico cuantitativo que respalde el diseño y la focalización territorial de políticas públicas de seguridad.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# II. JUSTIFICACIÓN
# =========================================================
elif seccion == "II. Justificación":
    st.header("II. Justificación")
    col_doc, col_app = st.columns([1.05, 1.1], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítem 7</div>
            <div class="doc-text">
                El conflicto armado colombiano es el de mayor duración del hemisferio occidental, y desde más de seis décadas se relaciona con economías ilegales. Ortiz-Riomalo y Rettberg (2018) muestran que los grupos armados han financiado sus actividades sobre todo con el narcotráfico y más recientemente con la minería de oro, señalando que esa relación no es uniforme, cambia con las características de cada zona, con las capacidades del Estado y con la presencia de los grupos armados. El narcotráfico, por su parte, funciona como una cadena de valor en torno a la cual actúan distintos grupos armados ilegales (Observatorio de Derechos Humanos y Conflictividades de Indepaz, 2023). Por eso el conflicto se vive de manera distinta en cada territorio, y importa seguirlo con indicadores oficiales que muestren cómo se manifiesta en cada departamento, tanto en los delitos como en las afectaciones a la fuerza pública.<br><br>
                Las condiciones de cada territorio también hacen parte de esta discusión, y varias investigaciones han estudiado el conflicto, sus consecuencias y los factores que se le asocian. Por ejemplo, Rodríguez Takeuchi (2009) encontró que el conflicto afectó la capacidad de los gobiernos locales para prestar servicios de salud, educación y saneamiento. Fiandrino et al. (2023) analizaron qué factores se relacionan con el conflicto en los municipios del país. Sin embargo, es común que en las investigaciones se usen datos de un solo año, 2005 y 2018 como en el caso de estos dos autores, más todavía queda por explorar cómo se comportan, al mismo tiempo y a lo largo de varios años, los distintos delitos y las afectaciones a la fuerza pública en todos los departamentos del país.<br><br>
                Por ello, este estudio es pertinente a escala nacional y regional, porque identificar cómo se parecen y se diferencian los departamentos en términos de indicadores de delitos y de afectaciones a la fuerza pública, puede ayudar a que las políticas de seguridad reconozcan las particularidades de cada región, en lugar de aplicar el mismo esquema a todo el país.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Ejes de Pertinencia del Estudio")
        eje = st.radio(
            "Seleccione el eje argumentativo:",
            [
                "1. Dinámica territorial diferenciada de las economías ilegales",
                "2. Superación de análisis transversales (un solo año)",
                "3. Utilidad para la focalización de políticas públicas"
            ]
        )

        if "1." in eje:
            st.markdown("""
            <div class="card">
                <div class="card-title">Heterogeneidad Territorial</div>
                <p class="highlight-text">
                    El narcotráfico y la minería ilegal de oro no operan de manera homogénea en el país; su impacto depende de la capacidad estatal y la presencia de actores armados en cada departamento (Ortiz-Riomalo y Rettberg, 2018; Indepaz, 2023).
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif "2." in eje:
            st.markdown("""
            <div class="card">
                <div class="card-title">De Cortes Estáticos a Trayectorias Longitudinales</div>
                <p class="highlight-text">
                    Investigaciones previas (Rodríguez Takeuchi, 2009; Fiandrino et al., 2023) analizan años aislados (2005 o 2018). Este trabajo examina <b>13 años continuos (2012–2024)</b> de forma conjunta.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card-red">
                <div class="card-title">Políticas Diferenciales por Región</div>
                <p class="highlight-text">
                    Caracterizar qué departamentos comparten perfiles similares permite diseñar intervenciones adaptadas a cada región, superando esquemas uniformes a nivel nacional.
                </p>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# III. PLANTEAMIENTO DEL PROBLEMA
# =========================================================
elif seccion == "III. Planteamiento del Problema":
    st.header("III. Planteamiento del Problema")
    col_doc, col_app = st.columns([1.05, 1.1], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítem 8</div>
            <div class="doc-text">
                Colombia enfrenta fenómenos de violencia e ilegalidad que van más allá de los enfrentamientos armados. Los grupos armados organizados al margen de la ley (GAO) han financiado sus actividades a través de diversos delitos y acciones ilegales que afectan a la población civil de diferentes territorios en el país. Entre ellos están el terrorismo, el secuestro, el narcotráfico y la explotación ilegal de recursos naturales, como la minería ilegal.<br><br>
                Las cifras oficiales muestran la dimensión del problema. Según el Ministerio de Defensa Nacional de Colombia (2026), entre 2012 y 2024 se registraron en el país <b>18.630</b> integrantes de la fuerza pública heridos o asesinados (16.476 heridos y 2.154 asesinados), <b>9.164</b> casos de terrorismo, <b>3.042</b> secuestros y <b>22.720</b> capturas por minería ilegal. La afectación a la fuerza pública pasó de 2.848 integrantes en 2012 a 600 en 2024, el terrorismo subió de 666 a 1.126 casos y el secuestro, tras un mínimo de 160 en 2021, volvió a 313 en 2024. Las capturas por minería ilegal tuvieron su máximo en 2016, con 2.560, y bajaron a 1.148 en 2024.<br><br>
                <b>Pregunta Central:</b><br>
                ¿Cómo analizar, mediante técnicas multivía, los indicadores de delitos y afectación a la fuerza pública en Colombia, a partir de información del Ministerio de Defensa Nacional, para describir las similitudes y diferencias entre los departamentos y su evolución durante el periodo de estudio?<br><br>
                <b>Preguntas Articuladoras:</b><br>
                • ¿Qué departamentos siguen trayectorias similares en la ocurrencia de delitos y en las afectaciones a la fuerza pública?<br>
                • ¿Esas similitudes se mantienen durante todo el periodo de análisis o se observan cambios en años concretos (por ejemplo tras la firma del Acuerdo de Paz de 2016)?<br>
                • ¿Qué indicadores resultan más significativos para explicar las diferencias territoriales observadas y la evolución en el tiempo de los fenómenos estudiados?
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Comportamiento de Cifras Oficiales (2012–2024)")
        c1, c2 = st.columns(2)
        c1.metric("Afectación Fuerza Pública", "18.630 casos", "2.848 (2012) → 600 (2024)")
        c2.metric("Terrorismo", "9.164 casos", "666 (2012) → 1.126 (2024)")

        df_hitos = pd.DataFrame({
            "Indicador": ["Fuerza Pública", "Fuerza Pública", "Terrorismo", "Terrorismo", "Capturas Minería", "Capturas Minería"],
            "Corte Temporal": ["2012", "2024", "2012", "2024", "2016 (Máximo)", "2024"],
            "Registros": [2848, 600, 666, 1126, 2560, 1148]
        })
        fig = px.bar(
            df_hitos, x="Indicador", y="Registros", color="Corte Temporal", barmode="group",
            title="Dinámicas divergentes reportadas por MinDefensa",
            template="plotly_dark", color_discrete_sequence=["#388BFD", "#B71C1C", "#2EA043"],
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">Limitación del Análisis Univariado</div>
            <p class="highlight-text">
                Observar totales nacionales o indicadores aislados impide detectar si los departamentos con alta afectación a la Fuerza Pública coinciden con aquellos de mayor incidencia delictiva, o si esa relación cambió tras el <b>Acuerdo de Paz de 2016</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# IV. MARCO REFERENCIAL
# =========================================================
elif seccion == "IV. Marco Referencial":
    st.header("IV. Marco Referencial")
    col_doc, col_app = st.columns([1.05, 1.1], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítem 9</div>
            <div class="doc-text">
                <b>9.1 Estudios sobre criminalidad y seguridad en Colombia:</b><br>
                • <b>Holmes et al. (2006):</b> Compararon los departamentos del país y encontraron que los factores económicos y la erradicación de coca pesan más en la violencia que la sola producción.<br>
                • <b>Idrobo et al. (2014):</b> Estudiaron la relación entre minería ilegal de oro y violencia tras el auge posterior a 2008.<br>
                • <b>González et al. (2022):</b> Analizaron secuestros, robos y homicidios (2000–2013), destacando a Bolívar, Caquetá, Cesar, Meta y Tolima.<br>
                • <b>Fajardo-Steinhäuser (2024):</b> Evaluó los cambios en la violencia tras el cese al fuego y el Acuerdo de Paz de 2016.<br><br>
                <b>9.2 Referencias sobre las técnicas multivía (Familia STATIS):</b><br>
                • Propuestas por <b>L’Hermier des Plantes (1976)</b> y desarrolladas por <b>Thioulouse (2011)</b> para resumir secuencias de tablas en una estructura común (compromiso).<br>
                • <b>Medina Hernández (2022):</b> Aplicó STATICO al estudio de equidad de género y 22 metas de la Agenda 2030 en 115 países.<br>
                • <b>Rodríguez-Martínez et al. (2023):</b> Aplicaron X-STATIS a la evolución de participación electrónica entre 2008 y 2016.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Articulación Teórica y Metodológica")
        tab1, tab2 = st.tabs(["Antecedentes Temáticos", "Fundamento STATIS / STATICO"])

        with tab1:
            df_ref = pd.DataFrame({
                "Referencia": ["Holmes et al. (2006)", "Idrobo et al. (2014)", "González et al. (2022)", "Fajardo-Steinhäuser (2024)"],
                "Objeto de Estudio": ["Coca, erradicación y violencia", "Minería ilegal de oro", "Secuestro, hurto y homicidio", "Efectos Acuerdo de Paz 2016"],
                "Integra Fuerza Pública": ["No", "No", "No", "No"]
            })
            st.dataframe(df_ref, use_container_width=True, hide_index=True)
            st.markdown("""
            <div class="card-red">
                <div class="card-title">Vacío Identificado en la Literatura</div>
                <p class="highlight-text">
                    Los estudios previos analizan delitos específicos o economías ilegales, pero no integran longitudinalmente la <b>afectación física a la Fuerza Pública (heridos y asesinados)</b> junto con delitos ambientales, terrorismo y secuestro.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("""
            <div class="card">
                <div class="card-title">Familia STATIS (L’Hermier des Plantes, 1976; Thioulouse, 2011)</div>
                <p class="highlight-text">
                    • <b>X-STATIS:</b> Analiza una secuencia de <i>K</i> tablas con las mismas unidades y variables en distintos momentos.<br>
                    • <b>STATICO:</b> Analiza la co-estructura entre dos secuencias de tablas pareadas (<i>X</i> e <i>Y</i>) a lo largo del tiempo, con aplicaciones probadas en indicadores territoriales (Medina Hernández, 2022; Rodríguez-Martínez et al., 2023).
                </p>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# V. OBJETIVOS
# =========================================================
elif seccion == "V. Objetivos":
    st.header("V. Objetivos")
    col_doc, col_app = st.columns([1.05, 1.1], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítem 10</div>
            <div class="doc-text">
                <b>10.1 OBJETIVO GENERAL:</b><br>
                Analizar mediante técnicas multivía indicadores de delitos y afectación a la fuerza pública en Colombia, desde información del Ministerio de Defensa Nacional, describiendo las similitudes y diferencias observadas entre departamentos y su evolución en el tiempo.<br><br>
                <b>10.2 OBJETIVOS ESPECÍFICOS:</b><br>
                <b>1.</b> Identificar los departamentos que presentan trayectorias similares en la ocurrencia de delitos y en los indicadores de afectación a la fuerza pública.<br><br>
                <b>2.</b> Explorar si las similitudes entre departamentos se mantienen durante el periodo de estudio o cambian en años concretos, en especial después de la firma del Acuerdo de Paz.<br><br>
                <b>3.</b> Examinar las relaciones existentes entre los indicadores estudiados caracterizando los patrones territoriales observados.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Correspondencia Metodológica por Objetivo")
        st.markdown("""
        <div class="card-red">
            <div class="card-title">Objetivo General</div>
            <p class="highlight-text">Modelado multivía integral (2012–2024) de los 32 departamentos de Colombia a partir de registros del Ministerio de Defensa.</p>
        </div>
        <div class="card">
            <div class="card-title">Objetivo Específico 1 → Espacio Compromiso y Trayectorias</div>
            <p class="highlight-text">Agrupación y representación de los 32 departamentos según la similitud de sus perfiles y trayectorias en el periodo.</p>
        </div>
        <div class="card">
            <div class="card-title">Objetivo Específico 2 → Análisis de Interestructura</div>
            <p class="highlight-text">Evaluación de la estabilidad anual de las correlaciones entre tablas (2012–2024) para identificar puntos de quiebre (ej. posacuerdo 2016).</p>
        </div>
        <div class="card">
            <div class="card-title">Objetivo Específico 3 → Análisis de Intraestructura</div>
            <p class="highlight-text">Proyección de las variables (Bloque X y Bloque Y) para determinar qué indicadores impulsan las diferencias territoriales.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# VI. DISEÑO METODOLÓGICO Y CUBO 3D (CON BASE REAL)
# =========================================================
elif seccion == "VI. Diseño Metodológico y Cubo 3D":
    st.header("VI. Diseño Metodológico y Estructura Multivía")
    col_doc, col_app = st.columns([1.0, 1.2], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítem 11</div>
            <div class="doc-text">
                <b>11.1 Enfoque y Tipo de Estudio:</b> Cuantitativo, longitudinal, descriptivo y exploratorio (13 años: 2012–2024).<br>
                <b>11.2 Fuentes de Información:</b> Ministerio de Defensa Nacional (Observatorio de DD.HH.), DANE (proyecciones de población para cálculo de tasas) y TerriData - DNP.<br>
                <b>11.4 Indicadores de Interés (2 Bloques):</b><br>
                • <i>Bloque X (Afectación a la Fuerza Pública):</i> Heridos y asesinados de Fuerzas Militares y Policía Nacional.<br>
                • <i>Bloque Y (Delitos y Criminalidad):</i> Terrorismo, secuestro, capturas por minería ilegal, delitos contra el medio ambiente e incautación de oro y mercurio.<br><br>
                <b>11.5 Organización en Estructuras Multivía:</b><br>
                Cubos de datos de tres vías: <b>n = 32</b> departamentos (filas) × <b>k = 13</b> años (estudios) × <b>p + q</b> variables (columnas), evaluando <b>X-STATIS</b> (una K-tabla) y <b>STATICO</b> (dos K-tablas pareadas X e Y).<br><br>
                <b>11.6 Procesamiento (R / Python):</b> Revisión de calidad, armonización territorial/temporal y obtención de interestructura, compromiso e intraestructura.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Cubo Multivía Real: Departamento × Año × Variable")

        if base_cargada:
            f1, f2 = st.columns([1, 1])
            with f1:
                filtro_bloque = st.selectbox(
                    "Filtrar por Bloque de Variables:",
                    ["Todos los Indicadores (10)", "Bloque X: Fuerza Pública (4)", "Bloque Y: Delitos y Economías Ilegales (6)"]
                )
            with f2:
                deptos_disp = sorted(df_base["Departamento"].unique().tolist())
                filtro_deptos = st.multiselect(
                    "Resaltar departamentos específicos:",
                    options=deptos_disp,
                    default=[]
                )

            if "Bloque X" in filtro_bloque:
                vars_sel = ["FM_HER", "FM_ASE", "POL_HER", "POL_ASE"]
            elif "Bloque Y" in filtro_bloque:
                vars_sel = ["TERR", "SEC", "AFE_AMB", "CAP_MIN", "INC_ORO", "INC_MERC"]
            else:
                vars_sel = ["FM_HER", "FM_ASE", "POL_HER", "POL_ASE", "TERR", "SEC", "AFE_AMB", "CAP_MIN", "INC_ORO", "INC_MERC"]

            df_plot = df_base.copy()
            if filtro_deptos:
                df_plot = df_plot[df_plot["Departamento"].isin(filtro_deptos)]

            df_long = df_plot.melt(
                id_vars=["Abrev", "Departamento", "Anio"],
                value_vars=vars_sel,
                var_name="Codigo",
                value_name="Valor"
            )
            df_long = df_long.merge(df_dic[["Codigo", "Descripcion", "Cubos", "Unidad_base"]], on="Codigo", how="left")

            fig_3d = go.Figure(data=[go.Scatter3d(
                x=df_long["Codigo"],
                y=df_long["Departamento"],
                z=df_long["Anio"],
                mode="markers",
                marker=dict(
                    size=4.5 if not filtro_deptos else 6.5,
                    color=np.log1p(df_long["Valor"]),
                    colorscale="Viridis",
                    opacity=0.82,
                    colorbar=dict(title="Intensidad<br>log(1+tasa)", thickness=12)
                ),
                customdata=np.stack((
                    df_long["Departamento"],
                    df_long["Anio"],
                    df_long["Codigo"],
                    df_long["Descripcion"],
                    df_long["Cubos"],
                    df_long["Valor"].round(3)
                ), axis=-1),
                hovertemplate=(
                    "<b>Departamento:</b> %{customdata[0]}<br>"
                    "<b>Año:</b> %{customdata[1]}<br>"
                    "<b>Variable:</b> %{customdata[2]} (Bloque %{customdata[4]})<br>"
                    "<b>Detalle:</b> %{customdata[3]}<br>"
                    "<b>Valor / Tasa:</b> %{customdata[5]}<extra></extra>"
                )
            )])

            fig_3d.update_layout(
                title="Estructura Tridimensional (416 filas × 10 variables = 4.160 celdas)",
                scene=dict(
                    xaxis=dict(title="Variable (Bloques X / Y)", tickfont=dict(size=9)),
                    yaxis=dict(title="Departamento (n=32)", tickfont=dict(size=8)),
                    zaxis=dict(title="Año (2012–2024)", tickvals=list(range(2012, 2025, 2)), tickfont=dict(size=9))
                ),
                template="plotly_dark",
                height=440,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig_3d, use_container_width=True)

            with st.expander("Ver Diccionario de Variables de la Base (Bloques X e Y)"):
                st.dataframe(df_dic[["Codigo", "Descripcion", "Cubos", "Naturaleza", "Unidad_base"]], use_container_width=True, hide_index=True)
        else:
            st.error(estado_carga)

# =========================================================
# VII. ASPECTOS BIOÉTICOS Y CRONOGRAMA
# =========================================================
elif seccion == "VII. Aspectos Bioéticos y Cronograma":
    st.header("VII. Aspectos Bioéticos y Cronograma")
    col_doc, col_app = st.columns([1.05, 1.1], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítems 12 y 14</div>
            <div class="doc-text">
                <b>12. ASPECTOS BIOÉTICOS:</b><br>
                Este estudio no recoge información directamente de personas ni usa datos que identifiquen a individuos. La información proviene de registros administrativos de acceso público del Ministerio de Defensa Nacional, en los que cada registro describe un hecho con su fecha y lugar, sin nombres ni identificaciones. Los datos se procesarán solo por departamento y año, sin un nivel de detalle que permita identificar a víctimas, victimarios o testigos. Por eso el estudio se clasifica como <b>investigación sin riesgo</b>.<br><br>
                Como los indicadores se relacionan con hechos de violencia, los resultados se presentarán con rigor y sin estigmatizar a departamentos o regiones, junto con las limitaciones de los datos. Para cuidar la integridad científica, se documentarán las decisiones de procesamiento y el código de análisis, de modo que los resultados puedan reproducirse.<br><br>
                <b>14. CRONOGRAMA (6 MESES):</b><br>
                • <b>Meses 1–2:</b> Revisión bibliográfica y ajuste del marco referencial.<br>
                • <b>Mes 2:</b> Verificación de base de indicadores e implementación STATIS en Python/R.<br>
                • <b>Mes 3:</b> Análisis e interpretación de resultados y contraste con marco referencial.<br>
                • <b>Meses 4–5:</b> Redacción del documento final de tesis.<br>
                • <b>Mes 6:</b> Revisión, ajustes finales y entrega.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Plan de Ejecución (6 Meses)")
        df_crono = pd.DataFrame([
            dict(Actividad="1. Revisión bibliográfica y marco referencial", Inicio=1, Fin=2.9),
            dict(Actividad="2. Verificación y documentación de la base", Inicio=2, Fin=2.9),
            dict(Actividad="3. Implementación STATIS en Python / R", Inicio=2, Fin=2.9),
            dict(Actividad="4. Análisis e interpretación (Dpto-Año-Var)", Inicio=3, Fin=3.9),
            dict(Actividad="5. Contraste y elaboración de conclusiones", Inicio=3, Fin=3.9),
            dict(Actividad="6. Redacción del documento final de tesis", Inicio=4, Fin=5.9),
            dict(Actividad="7. Revisión, ajustes finales y entrega", Inicio=6, Fin=6.9),
        ])
        fig_gantt = go.Figure()
        for _, row in df_crono.iterrows():
            fig_gantt.add_trace(go.Bar(
                y=[row["Actividad"]],
                x=[row["Fin"] - row["Inicio"]],
                base=row["Inicio"],
                orientation="h",
                marker_color="#B71C1C",
                showlegend=False
            ))
        fig_gantt.update_layout(
            xaxis=dict(title="Mes de Ejecución", tickvals=[1, 2, 3, 4, 5, 6], ticktext=["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"]),
            yaxis=dict(autorange="reversed"),
            template="plotly_dark",
            height=310,
            margin=dict(l=0, r=10, b=20, t=20)
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">Consideraciones Éticas y Reproducibilidad</div>
            <p class="highlight-text">
                • <b>Clasificación:</b> Investigación sin riesgo (fuentes secundarias públicas agregadas).<br>
                • <b>Tratamiento territorial:</b> Análisis técnico sin estigmatización regional.<br>
                • <b>Ciencia abierta:</b> Scripts y decisiones metodológicas documentadas en R / Python.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# VIII. RESULTADOS ESPERADOS Y EVALUADORES
# =========================================================
elif seccion == "VIII. Resultados Esperados y Evaluadores":
    st.header("VIII. Resultados Esperados y Evaluadores Sugeridos")
    col_doc, col_app = st.columns([1.05, 1.1], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">Formato Oficial — Ítems 16 y 17</div>
            <div class="doc-text">
                <b>16. RESULTADOS ESPERADOS:</b><br>
                Se espera identificar los departamentos que siguen trayectorias similares en los indicadores de delitos y de afectación a la fuerza pública y los que se apartan del patrón general (estructura compromiso en los resultados de las técnicas de la familia STATIS). También se busca describir si esas similitudes se mantienen durante el periodo de análisis, o si cambian en años concretos, incluidos posibles cambios alrededor de acontecimientos importantes como la firma del Acuerdo de Paz.<br><br>
                Asimismo, se espera caracterizar las relaciones existentes entre los indicadores seleccionados y mostrar cuáles se as asociado más con las diferencias territoriales y con la trayectoria de los fenómenos estudiados. Igualmente, se espera dejar documentado el procesamiento de los datos y las decisiones tomadas sobre la estructura multivía y la técnica elegida, para que el análisis pueda repetirse con otros periodos o indicadores.<br><br>
                <b>17. SUGERENCIA DEL PERFIL DE EVALUADORES:</b><br>
                • <b>Julie Kimberly Ramírez Brinez</b> (jkramirezb@ut.edu.co) — Departamento de Matemáticas y Estadística, Universidad del Tolima.<br>
                • <b>Gisou Díaz Rojo</b> (gdiazrj@ut.edu.co) — Departamento de Matemáticas y Estadística, Universidad del Tolima.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("Productos Esperados de la Investigación")
        st.markdown("""
        <div class="card">
            <div class="card-title">1. Caracterización Multidimensional (Estructura Compromiso)</div>
            <p class="highlight-text">Identificación de tipologías y trayectorias departamentales en delitos y afectación a la Fuerza Pública (2012–2024).</p>
        </div>
        <div class="card">
            <div class="card-title">2. Protocolo Computacional Reproducible</div>
            <p class="highlight-text">Documentación completa del procesamiento y modelado multivía (X-STATIS / STATICO) replicable en R y Python.</p>
        </div>
        <div class="card-red">
            <div class="card-title">3. Documento de Trabajo de Grado e Insumo Técnico</div>
            <p class="highlight-text">Entrega de tesis y socialización académica orientada a la discusión de políticas públicas de seguridad focalizadas.</p>
        </div>
        """, unsafe_allow_html=True)
