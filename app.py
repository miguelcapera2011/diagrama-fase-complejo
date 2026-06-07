# =========================================================
# UMAP PROYECTO
# ---------------------------------------------------------
# Proyecto:
# Reducción de Dimensionalidad No Lineal
#
# Tema:
# UMAP para visualizar rostros humanos
#
# Autor:
# Proyecto de Análisis Multivariado
# =========================================================

# =========================================================
# LIBRERÍAS
# =========================================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import umap

from sklearn.datasets import fetch_lfw_people
from sklearn.preprocessing import StandardScaler

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="UMAP - Reducción Dimensional",
    page_icon="https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
    layout="wide"
)

# =========================================================
# CSS MODERNO E INYECCIÓN DE ÍCONOS POR ENLACE (BOOTSTRAP)
# =========================================================

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<style>

/* Fondo Principal - Colores más vivos y profundos */
.stApp {
    background:
    radial-gradient(circle at top left, #2e1065 0%, #090514 45%),
    radial-gradient(circle at bottom right, #083344 0%, #02243a 50%);
    color: #f8fafc;
}

/* Sidebar Estilizado con acento Neón */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0726 0%, #05020f 100%);
    border-right: 1px solid rgba(192, 132, 252, 0.15);
}

/* Encabezado del Menú Lateral */
.sidebar-title {
    font-size: 18px;
    font-weight: 800;
    line-height: 1.3;
    letter-spacing: 0.5px;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(192, 132, 252, 0.2);
    margin-bottom: 20px;
}

/* Estilo para los iconos en línea en títulos */
.title-icon {
    background: linear-gradient(135deg, #38bdf8, #e879f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-right: 12px;
    font-size: 30px;
    vertical-align: middle;
}

/* Tipografía Principal */
h1, h2, h3, h4 {
    color: #ffffff;
    font-weight: 700;
}

p, label, div {
    color: #e2e8f0;
}

/* Header Principal de Bienvenida - Gradiente de Alto Impacto */
.main-header {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.25) 0%, rgba(6, 182, 212, 0.15) 100%);
    padding: 35px;
    border-radius: 24px;
    border: 1px solid rgba(192, 132, 252, 0.3);
    box-shadow: 0 8px 32px 0 rgba(168, 85, 247, 0.1);
    margin-bottom: 30px;
}

.main-header h1 {
    font-size: 36px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #ffffff, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-header .subtitle {
    font-size: 16px;
    color: #38bdf8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
}

/* Métricas Estilo Dashboard - Efecto de brillo vivo al pasar el mouse */
.metric-card {
    background: linear-gradient(145deg, rgba(147, 51, 234, 0.15), rgba(15, 23, 42, 0.6));
    border-radius: 22px;
    padding: 24px;
    border: 1px solid rgba(56, 189, 248, 0.2);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: rgba(232, 121, 249, 0.6);
    box-shadow: 0px 0px 30px rgba(168, 85, 247, 0.35);
    background: linear-gradient(145deg, rgba(147, 51, 234, 0.25), rgba(15, 23, 42, 0.7));
}

.metric-card i {
    font-size: 26px;
    color: #38bdf8;
    display: block;
    margin-bottom: 8px;
}

.metric-card h3 {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
}

.metric-card h1 {
    font-size: 34px;
    color: #ffffff;
    font-weight: 800;
    margin: 0;
}

.metric-card p {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 5px;
}

/* Sliders y Selectores */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #38bdf8, #c084fc);
}

div[data-baseweb="select"] {
    background: #0f172a;
    border-radius: 12px;
    border: 1px solid rgba(192, 132, 252, 0.2);
}

img {
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
}

/* Cajas de Información */
.info-box {
    background: rgba(6, 182, 212, 0.08);
    border-left: 4px solid #06b6d4;
    padding: 16px;
    border-radius: 0 12px 12px 0;
    margin-top: 15px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown('<div class="sidebar-title"><i class="bi bi-cpu-fill" style="margin-right: 8px; color: #38bdf8;"></i>ANALISIS MULTIVARIADO</div>', unsafe_allow_html=True)

st.sidebar.markdown("""
<p style="font-size: 13px; color: #94a3b8; margin-top: -10px; margin-bottom: 25px;">
Reducción dimensional no lineal. Visualización y análisis morfológico de rostros humanos mediante algoritmos avanzados.
</p>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Contenido",
    [
        "Introducción",
        "Dataset Original",
        "Conversión Matemática",
        "Reducción Dimensional",
        "UMAP 2D",
        "UMAP 3D",
        "Conclusiones"
    ]
)

# =========================================================
# CARGAR DATASET
# =========================================================

@st.cache_data
def cargar_datos():
    lfw = fetch_lfw_people(min_faces_per_person=70)
    X = lfw.data
    y = lfw.target
    images = lfw.images
    names = lfw.target_names
    return X, y, images, names

X, y, images, names = cargar_datos()

# =========================================================
# ESCALAR DATOS
# =========================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================================================
# MÉTRICAS
# =========================================================

n_imagenes = X.shape[0]
n_variables = X.shape[1]
n_personas = len(names)

# =========================================================
# INTRODUCCIÓN
# =========================================================

if pagina == "Introducción":
    st.markdown("""
    <div class="main-header">
        <div class="subtitle"><i class="bi bi-diagram-3-fill" style="margin-right:6px;"></i> Uniform Manifold Approximation and Projection (UMAP)</div>
        <h1>Explora la estructura oculta de los rostros</h1>
        <p style="margin: 0; color: #cbd5e1; font-size: 15px;">
            Análisis visual e interactivo mediante técnicas avanzadas de reducción dimensional no lineal.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><i class="bi bi-bounding-box-circles"></i><h3>Dimensiones</h3><h1>{n_variables}</h1><p>Variables por imagen</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><i class="bi bi-people-fill"></i><h3>Imágenes</h3><h1>{n_imagenes}</h1><p>Rostros procesados</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><i class="bi bi-activity"></i><h3>Algoritmia</h3><h1>UMAP</h1><p>Geometría Riemanniana</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><i class="bi bi-projector-fill"></i><h3>Espacio</h3><h1>2D / 3D</h1><p>Mapas interactivos</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.8, 1])
    with col1:
        st.markdown("""
        ## <i class="bi bi-patch-question title-icon"></i>El Problema de la Alta Dimensionalidad
        Cada imagen de un rostro humano está compuesta por miles de píxeles interdependientes. Al tratar cada píxel como una variable numérica independiente, los datos resultantes quedan confinados en una matriz matemática hiperbólica de **2914 dimensiones**.
        
        Dado que la percepción cognitiva humana está limitada a entornos de tres dimensiones, se vuelve fundamental implementar algoritmos geométricos capaces de comprimir y proyectar estos espacios complejos sin destruir las relaciones de similitud latentes.
        """, unsafe_allow_html=True)
    with col2:
        st.image(images[0], use_container_width=True)
        st.markdown('<div class="info-box"><i class="bi bi-info-circle-fill" style="color:#06b6d4; margin-right:5px;"></i> <b>Nota técnica:</b> El sistema no interpreta facciones corporales; mapea densidades de matrices vectoriales consecutivas.</div>', unsafe_allow_html=True)

# =========================================================
# DATASET ORIGINAL
# =========================================================

elif pagina == "Dataset Original":
    st.markdown('<h1><i class="bi bi-images title-icon"></i>Dataset de Muestra</h1>', unsafe_allow_html=True)
    st.markdown("Análisis fundamentado sobre el compendio **LFW (Labeled Faces in the Wild)**, un estándar consolidado dentro del campo del Aprendizaje Profundo para tareas de verificación facial.")
    st.markdown("---")
    st.subheader("Muestras del Espacio de Entrada")
    
    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            st.image(images[i], caption=names[y[i]], use_container_width=True)

# =========================================================
# CONVERSIÓN MATEMÁTICA
# =========================================================

elif pagina == "Conversión Matemática":
    st.markdown('<h1><i class="bi bi-matrix-textbox title-icon"></i>Linealización de Matrices de Píxeles</h1>', unsafe_allow_html=True)
    st.markdown("Transformación topológica donde una matriz bidimensional de imagen es reestructurada fila por fila hasta consolidar un vector plano apto para el análisis multivariado.")
    
    image = images[0]
    alto, ancho = image.shape
    vector = X[0]
    
    pixel_index = st.slider(
        "Rastreo del píxel físico y su correspondiente indexación vectorial:",
        0, len(vector)-1, 100
    )
    
    valor_pixel = vector[pixel_index]
    fila = pixel_index // ancho
    columna = pixel_index % ancho
    
    imagen_color = np.stack([image]*3, axis=-1)
    imagen_color = imagen_color / imagen_color.max()
    imagen_color[fila, columna] = [1, 0, 0] 
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Localización Espacial")
        fig = px.imshow(imagen_color)
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=0, b=0), coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="info-box">
        <i class="bi bi-sliders2-vertical" style="color:#38bdf8; margin-right:5px;"></i> <b>Métricas del Elemento Seleccionado:</b><br>
        • Índice en Vector: Posición {pixel_index}<br>
        • Coordenada Matricial: Fila {fila}, Columna {columna}<br>
        • Magnitud de Intensidad: {valor_pixel:.2f}
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.subheader("Mapeo en Registro Estructurado")
        st.markdown("Vista dinámica de la distribución de memoria en el vector:")
        
        rango_min = max(0, pixel_index - 5)
        rango_max = min(len(vector), pixel_index + 6)
        
        indices_tabla = np.arange(rango_min, rango_max)
        valores_tabla = vector[rango_min:rango_max]
        roles = ["Vecino Adyacente" if idx != pixel_index else "PÍXEL SELECCIONADO" for idx in indices_tabla]
        
        tabla_df = pd.DataFrame({
            "ID Píxel (Posición en Vector)": indices_tabla,
            "Intensidad de Color (0-255)": np.round(valores_tabla, 4),
            "Fila en Imagen": indices_tabla // ancho,
            "Columna en Imagen": indices_tabla % ancho,
            "Rol en el Algoritmo": roles
        })
        
        styled_df = tabla_df.style.map(
            lambda v: 'background-color: rgba(168, 85, 247, 0.4); color: #FFFFFF; font-weight: bold;' if v == "PÍXEL SELECCIONADO" else '',
            subset=["Rol en el Algoritmo"]
        )
        
        st.dataframe(styled_df, use_container_width=True, height=420)

# =========================================================
# REDUCCIÓN DIMENSIONAL
# =========================================================

elif pagina == "Reducción Dimensional":
    st.markdown('<h1><i class="bi bi-funnel-fill title-icon"></i>Mecánica de la Compresión Espacial</h1>', unsafe_allow_html=True)
    st.markdown("Los algoritmos no lineales identifican correlaciones complejas en el hiperespacio y colapsan las 2914 dimensiones originales en coordenadas geométricas asimilables.")
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Alta Dimensión\n- 2914 descriptores ortogonales por espécimen.\n- Geometría abstracta ininterpretable mediante análisis visual directo.")
    with c2:
        st.markdown("### Proyección No Lineal\n- Detección de patrones y varianzas conjuntas mediante cálculo de vecindades de grafos difusos basados en geometría algebraica.")
    with c3:
        st.markdown("### Baja Dimensión\n- Reducción compacta a coordenadas Cartesianas.\n- Preservación óptima de la topología y de los agrupamientos familiares.")

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "UMAP 2D":
    st.markdown('<h1><i class="bi bi-grid-3x3 title-icon"></i>Proyección Bidimensional UMAP</h1>', unsafe_allow_html=True)
    
    n_neighbors = st.slider("Ajuste de n_neighbors (Control de balance Local vs Global)", 5, 50, 15)
    
    reducer = umap.UMAP(n_components=2, n_neighbors=n_neighbors, random_state=42)
    embedding = reducer.fit_transform(X_scaled)
    
    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "persona": [names[i] for i in y]
    })
    
    st.markdown("Cada vector transformado se representa como un punto. El algoritmo aproxima subvariedades riemannianas para cohesionar rostros con similitudes estructurales.")
    
    fig = px.scatter(df, x="x", y="y", color="persona", color_discrete_sequence=px.colors.sequential.Plasma_r, template="plotly_dark", height=650)
    fig.update_traces(marker=dict(size=7, opacity=0.85))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15, 23, 42, 0.5)")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# UMAP 3D
# =========================================================

elif pagina == "UMAP 3D":
    st.markdown('<h1><i class="bi bi-box-seam title-icon"></i>Proyección Tridimensional UMAP</h1>', unsafe_allow_html=True)
    
    reducer = umap.UMAP(n_components=3, random_state=42)
    embedding = reducer.fit_transform(X_scaled)
    
    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "z": embedding[:, 2],
        "persona": [names[i] for i in y]
    })
    
    fig = px.scatter_3d(df, x="x", y="y", z="z", color="persona", color_discrete_sequence=px.colors.sequential.Plasma_r, template="plotly_dark", height=750)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# CONCLUSIONES
# =========================================================

elif pagina == "Conclusiones":
    st.markdown('<h1><i class="bi bi-award title-icon"></i>Análisis y Evaluaciones Estadísticas</h1>', unsafe_allow_html=True)
    st.markdown("""
    ## Hallazgos Clave
    - **Optimización Topológica:** UMAP demuestra una velocidad y consistencia matemática superior al mantener la coherencia espacial general tanto a nivel micro como macroscópico.
    - **Aprendizaje No Supervisado:** Los clusters visibles demuestran que expresiones, orientaciones de rostros y rasgos genómicos se agrupan de manera natural sin necesidad de proveer etiquetas de nombres al algoritmo durante el entrenamiento.
    
    ## Dinámica del Algoritmo
    - **Preservación Estructural:** Al balancear la estructura local y global, UMAP permite interpretar de forma matemática qué tan distantes o similares son los diferentes grupos de rostros entre sí en el hiperespacio completo.
    - **Sensibilidad a los Hiperparámetros:** El ajuste del parámetro `n_neighbors` altera la topología del mapa resultante. Valores bajos aíslan patrones finos (como una inclinación de cabeza específica), mientras que valores altos unifican identidades completas bajo un criterio global.
    - **Importancia del Escalado:** La reducción dimensional no lineal es altamente sensible a las magnitudes de entrada. Sin un escalado estándar previo (`StandardScaler`), los píxeles con variaciones extremas de iluminación dominarían por completo la geometría de la proyección, ocultando los rasgos morfológicos reales de los rostros.
    """)
