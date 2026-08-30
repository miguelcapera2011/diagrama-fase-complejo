import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
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

# Estilos de interfaz
st.markdown(
    """
    <style>
        .main-title { font-size: 2.0rem; font-weight: 800; color: #0F172A; margin-bottom: 0.1rem; }
        .subtitle { color: #64748B; font-size: 1rem; margin-bottom: 1rem; }
        .card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1rem; color: black; }
        .source-box { background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px; padding: .6rem; font-size: .85rem; color: black; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CARGA SEGURA DEL PDF
# ============================================================
def buscar_pdf():
    # Intenta encontrar el archivo incluso si hay variaciones en el nombre o espacios
    posibles_nombres = [
        "intento suicida.pdf",
        "intento suicida .pdf",
        "intento_suicida.pdf",
        "intento suicidad.pdf"
    ]
    for nombre in posibles_nombres:
        p = Path(nombre)
        if p.exists():
            return p
    # Búsqueda flexible por cualquier .pdf en la carpeta
    archivos_pdf = list(Path(".").glob("*.pdf"))
    if archivos_pdf:
        return archivos_pdf[0]
    return None

pdf_path = buscar_pdf()

# ============================================================
# DATOS
# ============================================================
age_groups = ["5 a 9", "10 a 14", "15 a 19", "20 a 24", "25 a 29", "30 a 34", "35 a 39", "40 a 44"]
prevalence_data = pd.DataFrame({
    "Grupo de edad": age_groups * 2,
    "Prevalencia": [0.0, 5.8, 22.3, 16.9, 8.8, 6.0, 4.1, 3.4, 0.0, 9.6, 23.5, 21.4, 16.3, 6.8, 5.9, 5.1],
    "Año": [2012]*8 + [2013]*8
})

table1_df = pd.DataFrame([
    ["Área", "Urbano", 94.0, 315, 89.8, 169],
    ["Área", "Rural disperso", 6.2, 21, 10.1, 19],
    ["Edad", "Adolescencia (11-20)", 50.3, 169, 35.1, 66],
    ["Edad", "Adultez temprana (20-40)", 42.0, 141, 45.7, 86]
], columns=["Variable", "Categoría", "Mujer %", "Mujer N", "Hombre %", "Hombre N"])

table2_df = pd.DataFrame([
    ["Consumo de alcohol", "Sí", 1.28, 0.00, 3.58, 2.17, 5.90],
    ["Violencia", "Sí", -0.89, 0.00, 0.41, 0.26, 0.66]
], columns=["Variable", "Categoría", "B", "p", "OR", "IC95% inf.", "IC95% sup."])

# ============================================================
# BARRA LATERAL
# ============================================================
with st.sidebar:
    st.markdown("## 📊 MENÚ DE NAVEGACIÓN")
    seccion = st.radio(
        "Seleccione la etapa:",
        [
            "01 · Introducción",
            "02 · Prevalencia",
            "03 · Tabla 1 · Descriptivos",
            "04 · Tabla 2 · Modelo Final",
            "05 · Conclusiones"
        ]
    )
    st.markdown("---")
    st.caption("📌 **Datos del estudio:** Sogamoso, Boyacá (2012–2017) | N = 524")

# ============================================================
# PANEL PRINCIPAL
# ============================================================
st.markdown('<div class="main-title">Intento suicida: Análisis Multivariado (2012–2017)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sogamoso, Boyacá · Análisis de Evidencia Estadística</div>', unsafe_allow_html=True)

col_pdf, col_content = st.columns([1, 1], gap="medium")

# PANEL IZQUIERDO: VISOR DE PDF
with col_pdf:
    st.markdown("### 📄 Visor del documento PDF")
    if pdf_path:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Objeto embed genérico para mayor compatibilidad
        pdf_display = f'''
            <object data="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="700px">
                <p>Tu navegador no admite la visualización directa del PDF. 
                <a href="data:application/pdf;base64,{base64_pdf}" download="{pdf_path.name}">Haz clic aquí para descargarlo.</a></p>
            </object>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error(f"❌ No se encontró el archivo `.pdf` en la misma carpeta que `app.py`.")
        st.info("💡 Asegúrate de colocar el archivo PDF en la misma carpeta donde ejecutas el comando `streamlit run app.py`.")

# PANEL DERECHO: CONTENIDO DINÁMICO
with col_content:
    if "01 · Introducción" in seccion:
        st.markdown("### 🎯 Introducción al Estudio")
        st.write("El objetivo principal es identificar la prevalencia y factores asociados al intento suicida atendido por el sistema SIVIGILA.")
        st.markdown('<div class="card"><b>Muestra analizada:</b> 524 casos confirmados en Sogamoso.</div>', unsafe_allow_html=True)
        
    elif "02 · Prevalencia" in seccion:
        st.markdown("### 📈 Prevalencia por Edad")
        fig = px.line(prevalence_data, x="Grupo de edad", y="Prevalencia", color="Año", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
    elif "03 · Tabla 1" in seccion:
        st.markdown("### 📊 Caracterización Demográfica")
        st.dataframe(table1_df, use_container_width=True)
        
    elif "04 · Tabla 2" in seccion:
        st.markdown("### 🔬 Modelo de Regresión Logística")
        st.dataframe(table2_df, use_container_width=True)
        
    elif "05 · Conclusiones" in seccion:
        st.markdown("### 📝 Conclusiones Principales")
        st.write("1. El consumo de alcohol representa un factor de riesgo significativo (OR > 3.0).")
        st.write("2. Es prioritario enfocar la prevención en grupos adolescentes y adultos jóvenes.")
