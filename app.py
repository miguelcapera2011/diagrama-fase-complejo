# =========================================================
# FACEEXPLORER - REDUCCIÓN DIMENSIONAL NO LINEAL
# Autor: Tu Proyecto de Análisis Multivariado
#
# Tecnologías:
# - Streamlit
# - Plotly
# - Scikit-learn
# - UMAP
#
# Objetivo:
# Visualizar datos de alta dimensionalidad
# (rostros humanos) usando:
# PCA, t-SNE y UMAP.
# =========================================================


# =========================================================
# LIBRERÍAS
# =========================================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dataset de rostros
from sklearn.datasets import fetch_lfw_people

# Reducción dimensional
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap.umap_ as umap

# Escalamiento
from sklearn.preprocessing import StandardScaler

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="FaceExplorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILOS CSS PERSONALIZADOS
# =========================================================

st.markdown("""
<style>

/* ===== FONDO GENERAL ===== */

.stApp {
    background-color: #050816;
    color: white;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background-color: #0b1120;
    border-right: 1px solid #1f2a44;
}

/* ===== TITULOS ===== */

h1, h2, h3 {
    color: #E2E8F0;
}

/* ===== TARJETAS ===== */

.card {
    background: linear-gradient(
        145deg,
        rgba(15,23,42,0.95),
        rgba(30,41,59,0.95)
    );

    padding: 25px;
    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0px 0px 20px rgba(0,0,0,0.4);

    margin-bottom: 20px;
}

/* ===== MÉTRICAS ===== */

.metric-card {
    background: linear-gradient(
        145deg,
        rgba(88,28,135,0.25),
        rgba(15,23,42,0.95)
    );

    padding: 20px;
    border-radius: 18px;

    border: 1px solid rgba(168,85,247,0.3);

    text-align: center;
}

/* ===== BOTONES ===== */

.stButton>button {

    background: linear-gradient(
        90deg,
        #9333ea,
        #7c3aed
    );

    color: white;

    border: none;

    border-radius: 12px;

    padding: 12px 22px;

    font-size: 16px;

    font-weight: bold;

    transition: 0.3s;
}

.stButton>button:hover {

    transform: scale(1.03);

    box-shadow:
        0px 0px 15px rgba(168,85,247,0.5);
}

/* ===== SELECTBOX ===== */

div[data-baseweb="select"] {
    background-color: #111827;
    border-radius: 12px;
}

/* ===== SLIDERS ===== */

.stSlider > div > div {
    color: #9333ea;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧠 FaceExplorer")

st.sidebar.markdown("""
Visualización de rostros humanos usando:

- PCA
- t-SNE
- UMAP

Aplicado a datos de alta dimensionalidad.
""")

# =========================================================
# PARÁMETROS
# =========================================================

metodo = st.sidebar.selectbox(
    "Selecciona el algoritmo",
    ["PCA", "t-SNE", "UMAP"]
)

dimension = st.sidebar.radio(
    "Dimensión de visualización",
    ["2D", "3D"]
)

n_neighbors = st.sidebar.slider(
    "n_neighbors (UMAP)",
    5,
    50,
    15
)

min_dist = st.sidebar.slider(
    "min_dist (UMAP)",
    0.0,
    1.0,
    0.1
)

perplexity = st.sidebar.slider(
    "Perplexity (t-SNE)",
    5,
    50,
    30
)

# =========================================================
# TÍTULO PRINCIPAL
# =========================================================

st.title("🧠 Exploración de Rostros en Alta Dimensionalidad")

st.markdown("""
Transformación de datos complejos usando técnicas de
reducción dimensional no lineal.

Visualizamos rostros humanos en espacios 2D y 3D
mediante:

- PCA
- t-SNE
- UMAP
""")

# =========================================================
# CARGA DEL DATASET
# =========================================================

with st.spinner("Cargando dataset de rostros..."):

    # Dataset de rostros humanos
    lfw = fetch_lfw_people(min_faces_per_person=70)

    # Variables
    X = lfw.data

    # Etiquetas
    y = lfw.target

    # Nombres de personas
    target_names = lfw.target_names

    # Imágenes originales
    images = lfw.images

# =========================================================
# INFORMACIÓN GENERAL
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <h2>{X.shape[0]}</h2>
        <p>Imágenes</p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <h2>{X.shape[1]}</h2>
        <p>Dimensiones Originales</p>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <h2>{len(target_names)}</h2>
        <p>Personas</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# EXPLICACIÓN MATEMÁTICA
# =========================================================

st.markdown("""
### 📘 ¿Qué está ocurriendo?

Cada rostro humano está representado por miles de variables.

Cada píxel de la imagen representa una dimensión.

El objetivo es transformar:

R^2914 → R^2 o R^3

para visualizar relaciones ocultas entre rostros similares.
""")

# =========================================================
# ESCALAMIENTO
# =========================================================

# Normalización de datos
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# =========================================================
# REDUCCIÓN DIMENSIONAL
# =========================================================

st.subheader(f"🔬 Aplicando {metodo}")

# =========================================================
# PCA
# =========================================================

if metodo == "PCA":

    if dimension == "2D":

        reducer = PCA(n_components=2)

    else:

        reducer = PCA(n_components=3)

# =========================================================
# t-SNE
# =========================================================

elif metodo == "t-SNE":

    if dimension == "2D":

        reducer = TSNE(
            n_components=2,
            perplexity=perplexity,
            random_state=42
        )

    else:

        reducer = TSNE(
            n_components=3,
            perplexity=perplexity,
            random_state=42
        )

# =========================================================
# UMAP
# =========================================================

else:

    if dimension == "2D":

        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            random_state=42
        )

    else:

        reducer = umap.UMAP(
            n_components=3,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            random_state=42
        )

# =========================================================
# EJECUCIÓN DEL MODELO
# =========================================================

with st.spinner("Reduciendo dimensionalidad..."):

    embedding = reducer.fit_transform(X_scaled)

# =========================================================
# DATAFRAME
# =========================================================

df = pd.DataFrame()

df["label"] = y
df["person"] = [target_names[i] for i in y]

# =========================================================
# VISUALIZACIÓN 2D
# =========================================================

if dimension == "2D":

    df["x"] = embedding[:,0]
    df["y"] = embedding[:,1]

    fig = px.scatter(

        df,

        x="x",
        y="y",

        color="person",

        hover_data=["person"],

        template="plotly_dark",

        title=f"{metodo} - Visualización 2D",

        width=1200,
        height=700
    )

    fig.update_traces(
        marker=dict(
            size=7,
            opacity=0.8
        )
    )

    fig.update_layout(

        paper_bgcolor="#050816",
        plot_bgcolor="#050816",

        font=dict(color="white"),

        legend_title="Personas"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# VISUALIZACIÓN 3D
# =========================================================

else:

    df["x"] = embedding[:,0]
    df["y"] = embedding[:,1]
    df["z"] = embedding[:,2]

    fig = px.scatter_3d(

        df,

        x="x",
        y="y",
        z="z",

        color="person",

        hover_data=["person"],

        template="plotly_dark",

        title=f"{metodo} - Visualización 3D",

        width=1200,
        height=800
    )

    fig.update_traces(
        marker=dict(
            size=4,
            opacity=0.8
        )
    )

    fig.update_layout(

        paper_bgcolor="#050816",

        scene=dict(
            bgcolor="#050816"
        ),

        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# GALERÍA DE ROSTROS
# =========================================================

st.subheader("🖼️ Ejemplos de Rostros")

cols = st.columns(5)

for i, col in enumerate(cols):

    with col:

        st.image(
            images[i],
            caption=target_names[y[i]],
            use_container_width=True
        )

# =========================================================
# CONCLUSIONES
# =========================================================

st.markdown("""
## 📌 Conclusiones

- Los rostros humanos son datos de alta dimensionalidad.

- PCA realiza reducción lineal.

- t-SNE preserva relaciones locales.

- UMAP conserva estructuras complejas y es más rápido.

- La reducción dimensional permite visualizar patrones ocultos
  y agrupamientos faciales.

- Estas técnicas son ampliamente utilizadas en:
    - biometría,
    - inteligencia artificial,
    - reconocimiento facial,
    - visión computacional.
""")
