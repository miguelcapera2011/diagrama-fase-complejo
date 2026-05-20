# =========================================================
# FACEEXPLORER AI
# ---------------------------------------------------------
# Reducción Dimensional No Lineal
#
# Proyecto de Análisis Multivariado
#
# Tema:
# Visualización de datos complejos usando UMAP y t-SNE
#
# Objetivo:
# Agrupar y visualizar rostros humanos
# en espacios 2D y 3D.
#
# Diseño:
# Inspirado en interfaces modernas de IA
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
# CONFIGURACIÓN DE LA APP
# =========================================================

st.set_page_config(
    page_title="FaceExplorer AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# CSS MODERNO
# =========================================================

st.markdown("""
<style>

/* ======================================================
FONDO PRINCIPAL
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
TEXTOS
====================================================== */

h1,h2,h3,h4{
    color:#F8FAFC;
}

p, label, div{
    color:#CBD5E1;
}

/* ======================================================
CARDS
====================================================== */

.card{

    background:
    rgba(17,24,39,0.75);

    border:
    1px solid rgba(255,255,255,0.06);

    border-radius:22px;

    padding:24px;

    backdrop-filter: blur(12px);

    box-shadow:
    0px 0px 25px rgba(0,0,0,0.35);

    margin-bottom:20px;
}

/* ======================================================
MÉTRICAS
====================================================== */

.metric-card{

    background:
    linear-gradient(
        145deg,
        rgba(139,92,246,0.12),
        rgba(17,24,39,0.9)
    );

    border-radius:20px;

    padding:24px;

    border:
    1px solid rgba(139,92,246,0.22);

    transition:0.3s;
}

.metric-card:hover{

    transform:translateY(-4px);

    box-shadow:
    0px 0px 22px rgba(139,92,246,0.35);
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

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🧠 FaceExplorer")

st.sidebar.markdown("""
Visualización de datos complejos mediante:

- UMAP
- t-SNE

Aplicado a rostros humanos de alta dimensionalidad.
""")

pagina = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Inicio",
        "📚 Dataset",
        "🚀 UMAP 2D",
        "🌌 UMAP 3D",
        "🧠 t-SNE",
        "🔬 Proceso Interno",
        "🖼️ Explorar Rostros",
        "📌 Conclusiones"
    ]
)

# =========================================================
# CARGA DEL DATASET
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
Utilizamos técnicas de reducción dimensional no lineal
para transformar datos complejos en visualizaciones 2D y 3D.
""")

    st.markdown("")

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Dimensionalidad</h3>
        <h1>{n_variables}</h1>
        <p>variables por imagen</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="metric-card">
        <h3>Métodos</h3>
        <h1>2</h1>
        <p>UMAP y t-SNE</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="metric-card">
        <h3>Visualización</h3>
        <h1>2D / 3D</h1>
        <p>interactiva</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown("""
        <div class="metric-card">
        <h3>Objetivo</h3>
        <h1>Agrupar</h1>
        <p>rostros similares</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1,col2 = st.columns([2,1])

    with col1:

        st.markdown("""
### 📘 ¿Qué hace esta aplicación?

Cada rostro humano contiene miles de píxeles.

Cada píxel representa una variable matemática,
por lo que cada imagen vive en un espacio de alta dimensionalidad.

UMAP transforma:

R^2914 → R^2

permitiendo visualizar agrupamientos y similitudes faciales.
""")

    with col2:

        st.image(images[0], use_container_width=True)

# =========================================================
# DATASET
# =========================================================

elif pagina == "📚 Dataset":

    st.title("📚 Dataset Facial")

    st.markdown("""
Trabajamos con:

## LFW — Labeled Faces in the Wild

Dataset utilizado en:
- biometría,
- reconocimiento facial,
- inteligencia artificial.
""")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric("Imágenes", n_imagenes)

    with c2:
        st.metric("Variables", n_variables)

    with c3:
        st.metric("Personas", n_personas)

    st.markdown("---")

    st.subheader("🖼️ Ejemplos")

    cols = st.columns(5)

    for i,col in enumerate(cols):

        with col:

            st.image(
                images[i],
                caption=names[y[i]],
                use_container_width=True
            )

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "🚀 UMAP 2D":

    st.title("🚀 UMAP — Visualización 2D")

    c1,c2,c3 = st.columns([1,1,1])

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

    with c3:

        metrica = st.selectbox(
            "Métrica",
            ["euclidean", "cosine"]
        )

    st.markdown("""
UMAP intenta preservar similitudes entre rostros.

Los puntos cercanos representan caras similares.
""")

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric=metrica,
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
        height=750
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
# UMAP 3D
# =========================================================

elif pagina == "🌌 UMAP 3D":

    st.title("🌌 UMAP — Visualización 3D")

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

    st.title("🧠 t-SNE")

    perplexity = st.slider(
        "Perplexity",
        5,
        50,
        30
    )

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
        height=750
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
# PROCESO INTERNO
# =========================================================

elif pagina == "🔬 Proceso Interno":

    st.title("🔬 ¿Qué ocurre internamente?")

    st.markdown("""
La aplicación realiza una transformación matemática
para convertir imágenes complejas en puntos visuales.
""")

    st.markdown("---")

    c1,c2,c3 = st.columns(3)

    with c1:

        st.subheader("1️⃣ Imagen Original")

        st.image(images[0], use_container_width=True)

        st.markdown("""
La computadora recibe una imagen facial.
""")

    with c2:

        st.subheader("2️⃣ Vector Matemático")

        vector = X[0][:20]

        st.write(vector)

        st.markdown("""
Cada píxel se convierte en una variable matemática.
""")

    with c3:

        st.subheader("3️⃣ Reducción UMAP")

        st.markdown("""
UMAP transforma:

R^2914 → R^2

para visualizar similitudes.
""")

    st.markdown("---")

    st.subheader("📘 Explicación")

    st.markdown("""
Antes de UMAP:

- cada rostro tiene 2914 dimensiones,
- imposible de visualizar.

Después de UMAP:

- cada rostro se convierte en:
(x,y)

permitiendo observar:
- agrupamientos,
- similitudes,
- estructuras ocultas.
""")

# =========================================================
# EXPLORAR ROSTROS
# =========================================================

elif pagina == "🖼️ Explorar Rostros":

    st.title("🖼️ Explorar Rostros")

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
## Resultados

- Los rostros humanos representan datos complejos.

- Cada imagen contiene miles de variables.

- UMAP y t-SNE reducen dimensionalidad
  preservando similitudes.

- La reducción dimensional permite visualizar
  agrupamientos en espacios 2D y 3D.

## Aplicaciones

- biometría,
- reconocimiento facial,
- visión computacional,
- inteligencia artificial.
""")
