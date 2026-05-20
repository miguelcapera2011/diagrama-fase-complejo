# =========================================================
# FACEEXPLORER AI
# ---------------------------------------------------------
# Proyecto:
# Reducción de Dimensionalidad No Lineal
#
# Técnicas:
# - UMAP (Principal)
# - t-SNE (Comparación)
#
# Objetivo:
# Agrupar y visualizar datos extremadamente complejos
# (rostros humanos) en gráficos simples 2D y 3D.
#
# App moderna estilo IA / Visual Analytics
# =========================================================

# =========================================================
# LIBRERÍAS
# =========================================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import umap

from sklearn.datasets import fetch_lfw_people
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="FaceExplorer AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# CSS AVANZADO
# =========================================================

st.markdown("""
<style>

/* ======================================================
FONDO GENERAL
====================================================== */

.stApp{
    background:
    radial-gradient(circle at top left, #1e1b4b 0%, #050816 35%),
    radial-gradient(circle at bottom right, #111827 0%, #050816 40%);
    color:white;
}

/* ======================================================
SIDEBAR
====================================================== */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #0B1120 0%,
        #050816 100%
    );

    border-right:
    1px solid rgba(255,255,255,0.08);
}

/* ======================================================
TÍTULOS
====================================================== */

h1{
    color:#F8FAFC;
    font-size:50px;
    font-weight:700;
}

h2,h3{
    color:#E2E8F0;
}

/* ======================================================
TEXTOS
====================================================== */

p, label, div{
    color:#CBD5E1;
}

/* ======================================================
CARDS
====================================================== */

.card{

    background:
    rgba(17,24,39,0.72);

    border:
    1px solid rgba(255,255,255,0.06);

    border-radius:22px;

    padding:22px;

    backdrop-filter: blur(12px);

    box-shadow:
    0px 0px 20px rgba(0,0,0,0.35);

    margin-bottom:20px;
}

/* ======================================================
METRIC CARDS
====================================================== */

.metric-card{

    background:
    linear-gradient(
        145deg,
        rgba(139,92,246,0.12),
        rgba(17,24,39,0.88)
    );

    border-radius:20px;

    padding:22px;

    border:
    1px solid rgba(139,92,246,0.25);

    transition:0.3s;
}

.metric-card:hover{

    transform:translateY(-5px);

    box-shadow:
    0px 0px 25px rgba(139,92,246,0.35);
}

/* ======================================================
BOTONES
====================================================== */

.stButton > button{

    width:100%;

    background:
    linear-gradient(
        90deg,
        #8B5CF6,
        #7C3AED
    );

    color:white;

    border:none;

    border-radius:14px;

    padding:14px;

    font-size:16px;

    font-weight:600;

    transition:0.3s;
}

.stButton > button:hover{

    transform:scale(1.02);

    box-shadow:
    0px 0px 18px rgba(139,92,246,0.45);
}

/* ======================================================
SLIDERS
====================================================== */

.stSlider > div > div > div > div{
    background:#8B5CF6;
}

/* ======================================================
SELECTBOX
====================================================== */

div[data-baseweb="select"]{
    background:#111827;
    border-radius:14px;
}

/* ======================================================
RADIO
====================================================== */

.stRadio > div{
    background:#111827;
    padding:10px;
    border-radius:14px;
}

/* ======================================================
IMÁGENES
====================================================== */

img{
    border-radius:16px;
}

/* ======================================================
HR
====================================================== */

hr{
    border:
    1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🧠 FaceExplorer AI")

st.sidebar.markdown("""
### Reducción Dimensional No Lineal

Visualización de rostros humanos usando:

- UMAP
- t-SNE

Aplicado a datos de alta dimensionalidad.
""")

pagina = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Inicio",
        "📚 Dataset",
        "🚀 UMAP 2D",
        "🌌 UMAP 3D",
        "🧠 t-SNE",
        "🖼️ Explorar Rostros",
        "📌 Conclusiones"
    ]
)

st.sidebar.markdown("---")

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
# ESCALAMIENTO
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
# INICIO
# =========================================================

if pagina == "🏠 Inicio":

    st.title("Explora la estructura oculta de los rostros 👋")

    st.markdown("""
Utilizamos reducción dimensional no lineal para visualizar
rostros humanos en espacios de 2D y 3D.

El objetivo es transformar datos extremadamente complejos
en representaciones visuales simples e interpretables.
""")

    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Imágenes</h3>
        <h1 style="font-size:40px;">{n_imagenes}</h1>
        <p>rostros humanos</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Dimensionalidad</h3>
        <h1 style="font-size:40px;">{n_variables}</h1>
        <p>variables por imagen</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="metric-card">
        <h3>Método Principal</h3>
        <h1 style="font-size:40px;">UMAP</h1>
        <p>no lineal</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown("""
        <div class="metric-card">
        <h3>Visualización</h3>
        <h1 style="font-size:40px;">2D / 3D</h1>
        <p>interactiva</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📘 ¿Qué está ocurriendo?")

    st.markdown("""
Cada rostro humano contiene miles de variables.

Cada píxel representa información visual, por lo que
una imagen facial vive en un espacio de alta dimensionalidad.

UMAP reduce estas dimensiones para visualizar:

R^2914 → R^2 o R^3

permitiendo observar agrupamientos y similitudes entre rostros.
""")

# =========================================================
# DATASET
# =========================================================

elif pagina == "📚 Dataset":

    st.title("📚 Dataset de Rostros Humanos")

    st.markdown("""
Trabajamos con el dataset:

## LFW — Labeled Faces in the Wild

Utilizado en:
- biometría,
- visión artificial,
- inteligencia artificial,
- reconocimiento facial.
""")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Imágenes", n_imagenes)

    with c2:
        st.metric("Variables", n_variables)

    with c3:
        st.metric("Personas", n_personas)

    st.markdown("---")

    st.subheader("🖼️ Ejemplos de Rostros")

    cols = st.columns(5)

    for i, col in enumerate(cols):

        with col:

            st.image(
                images[i],
                caption=names[y[i]],
                use_container_width=True
            )

    st.markdown("---")

    st.subheader("📘 Explicación Multivariada")

    st.markdown("""
Cada imagen facial puede representarse como:

x = (x1, x2, x3, ..., x2914)

donde cada variable corresponde a un píxel.

Esto convierte a las imágenes en datos
extremadamente complejos y de alta dimensionalidad.
""")

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "🚀 UMAP 2D":

    st.title("🚀 UMAP — Visualización 2D")

    c1, c2 = st.columns([3,1])

    with c1:

        n_neighbors = st.slider(
            "n_neighbors",
            5,
            50,
            15
        )

    with c2:

        min_dist = st.slider(
            "min_dist",
            0.0,
            1.0,
            0.1
        )

    st.markdown("""
UMAP preserva relaciones locales y globales.

Los puntos cercanos representan rostros similares.
""")

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        random_state=42
    )

    embedding = reducer.fit_transform(X_scaled)

    df = pd.DataFrame({
        "x": embedding[:,0],
        "y": embedding[:,1],
        "persona": [names[i] for i in y]
    })

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="persona",
        template="plotly_dark",
        height=760
    )

    fig.update_traces(
        marker=dict(
            size=7,
            opacity=0.82
        )
    )

    fig.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        legend_title="Personas"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# UMAP 3D
# =========================================================

elif pagina == "🌌 UMAP 3D":

    st.title("🌌 UMAP — Visualización 3D")

    st.markdown("""
Visualización tridimensional interactiva
de rostros humanos utilizando UMAP.
""")

    reducer = umap.UMAP(
        n_components=3,
        random_state=42
    )

    embedding = reducer.fit_transform(X_scaled)

    df = pd.DataFrame({
        "x": embedding[:,0],
        "y": embedding[:,1],
        "z": embedding[:,2],
        "persona": [names[i] for i in y]
    })

    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="persona",
        template="plotly_dark",
        height=850
    )

    fig.update_traces(
        marker=dict(
            size=4,
            opacity=0.8
        )
    )

    fig.update_layout(
        paper_bgcolor="#050816"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TSNE
# =========================================================

elif pagina == "🧠 t-SNE":

    st.title("🧠 t-SNE — Comparación")

    perplexity = st.slider(
        "Perplexity",
        5,
        50,
        30
    )

    st.markdown("""
t-SNE también es una técnica de reducción
dimensional no lineal.

Preserva relaciones locales entre observaciones.
""")

    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        random_state=42
    )

    embedding = tsne.fit_transform(X_scaled)

    df = pd.DataFrame({
        "x": embedding[:,0],
        "y": embedding[:,1],
        "persona": [names[i] for i in y]
    })

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="persona",
        template="plotly_dark",
        height=760
    )

    fig.update_traces(
        marker=dict(
            size=7,
            opacity=0.82
        )
    )

    fig.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# EXPLORAR ROSTROS
# =========================================================

elif pagina == "🖼️ Explorar Rostros":

    st.title("🖼️ Explorar Rostros")

    st.markdown("""
Galería interactiva del dataset facial.
""")

    cols = st.columns(5)

    for i in range(20):

        with cols[i % 5]:

            st.image(
                images[i],
                caption=names[y[i]],
                use_container_width=True
            )

# =========================================================
# CONCLUSIONES
# =========================================================

elif pagina == "📌 Conclusiones":

    st.title("📌 Conclusiones")

    st.markdown("""
## Resultados del Proyecto

- Los rostros humanos representan datos de alta dimensionalidad.

- UMAP y t-SNE realizan reducción dimensional no lineal.

- Estas técnicas permiten visualizar agrupamientos
  y relaciones ocultas entre rostros similares.

- La reducción dimensional transforma datos complejos
  en representaciones visuales simples de 2D y 3D.

## Aplicaciones Reales

- biometría,
- reconocimiento facial,
- inteligencia artificial,
- visión computacional,
- análisis multivariado.
""")
