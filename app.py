# =========================================================
# FACEEXPLORER AI
# ---------------------------------------------------------
# Proyecto:
# Reducción de Dimensionalidad No Lineal
#
# Tema:
# UMAP y t-SNE para visualizar rostros humanos
#
# Objetivo:
# Mostrar TODO el proceso:
#
# 1. Dataset original
# 2. Conversión a datos matemáticos
# 3. Alta dimensionalidad
# 4. Reducción dimensional
# 5. Visualización final 2D y 3D
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
import umap

from sklearn.datasets import fetch_lfw_people
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="FaceExplorer AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# CSS ULTRA MODERNO
# =========================================================

st.markdown("""
<style>

/* =====================================================
FONDO PRINCIPAL
===================================================== */

.stApp{

    background:
    radial-gradient(circle at top left, #1e1b4b 0%, #050816 40%),
    radial-gradient(circle at bottom right, #111827 0%, #050816 50%);

    color:white;
}

/* =====================================================
SIDEBAR
===================================================== */

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

/* =====================================================
TEXTOS
===================================================== */

h1,h2,h3,h4{

    color:#F8FAFC;
}

p, label, div{

    color:#CBD5E1;
}

/* =====================================================
CARDS
===================================================== */

.card{

    background:
    rgba(17,24,39,0.78);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:24px;

    padding:25px;

    backdrop-filter: blur(10px);

    box-shadow:
    0px 0px 30px rgba(0,0,0,0.35);

    margin-bottom:25px;
}

/* =====================================================
METRICAS
===================================================== */

.metric-card{

    background:
    linear-gradient(
        145deg,
        rgba(139,92,246,0.12),
        rgba(17,24,39,0.92)
    );

    border-radius:22px;

    padding:24px;

    border:
    1px solid rgba(139,92,246,0.25);

    transition:0.3s;
}

.metric-card:hover{

    transform:translateY(-5px);

    box-shadow:
    0px 0px 24px rgba(139,92,246,0.35);
}

/* =====================================================
BOTONES
===================================================== */

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
    0px 0px 20px rgba(139,92,246,0.4);
}

/* =====================================================
SLIDERS
===================================================== */

.stSlider > div > div > div > div{

    background:#8B5CF6;
}

/* =====================================================
SELECTBOX
===================================================== */

div[data-baseweb="select"]{

    background:#111827;
    border-radius:14px;
}

/* =====================================================
IMÁGENES
===================================================== */

img{

    border-radius:16px;
}

/* =====================================================
CAJAS EXPLICATIVAS
===================================================== */

.info-box{

    background:
    rgba(139,92,246,0.08);

    border-left:
    4px solid #8B5CF6;

    padding:18px;

    border-radius:12px;

    margin-top:15px;
}

/* =====================================================
SEPARADOR
===================================================== */

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

Visualización de rostros humanos mediante:

- UMAP
- t-SNE

Proyecto de Análisis Multivariado.
""")

pagina = st.sidebar.radio(
    "Exploración",
    [
        "🏠 Introducción",
        "📚 Dataset Original",
        "🔢 Conversión Matemática",
        "📉 Reducción Dimensional",
        "🚀 UMAP 2D",
        "🌌 UMAP 3D",
        "🧠 t-SNE",
        "🖼️ Exploración Facial",
        "📌 Conclusiones"
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

if pagina == "🏠 Introducción":

    st.title("Explora la estructura oculta de los rostros 👋")

    st.markdown("""
Esta aplicación muestra cómo técnicas de reducción dimensional
transforman imágenes complejas en mapas visuales 2D y 3D.
""")

    st.markdown("")

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Dimensiones</h3>
        <h1>{n_variables}</h1>
        <p>variables por imagen</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Imágenes</h3>
        <h1>{n_imagenes}</h1>
        <p>rostros humanos</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="metric-card">
        <h3>Métodos</h3>
        <h1>UMAP</h1>
        <p>t-SNE</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown("""
        <div class="metric-card">
        <h3>Visualización</h3>
        <h1>2D/3D</h1>
        <p>interactiva</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1,col2 = st.columns([2,1])

    with col1:

        st.markdown("""
## 📘 ¿Qué problema resolvemos?

Cada rostro humano contiene miles de píxeles.

Cada píxel representa información matemática,
por lo que una imagen vive en un espacio de alta dimensionalidad.

Los humanos no podemos visualizar 2914 dimensiones.

Por eso utilizamos:

- UMAP
- t-SNE

para transformar esos datos en espacios visuales simples.
""")

    with col2:

        st.image(images[0], use_container_width=True)

# =========================================================
# DATASET ORIGINAL
# =========================================================

elif pagina == "📚 Dataset Original":

    st.title("📚 Dataset Original")

    st.markdown("""
Trabajamos con el dataset:

## LFW — Labeled Faces in the Wild

Utilizado en:
- reconocimiento facial,
- biometría,
- inteligencia artificial.
""")

    st.markdown("---")

    st.subheader("🖼️ ¿Cómo se ven los datos originales?")

    cols = st.columns(5)

    for i in range(10):

        with cols[i % 5]:

            st.image(
                images[i],
                caption=names[y[i]],
                use_container_width=True
            )

    st.markdown("---")

    st.markdown("""
<div class="info-box">

La computadora NO ve rostros.

La computadora ve matrices numéricas
compuestas por miles de píxeles.

</div>
""", unsafe_allow_html=True)

# =========================================================
# CONVERSIÓN MATEMÁTICA
# =========================================================

elif pagina == "🔢 Conversión Matemática":

    st.title("🔢 Conversión de Imagen a Datos")

    col1,col2 = st.columns([1,2])

    with col1:

        st.subheader("🖼️ Imagen")

        st.image(images[0], use_container_width=True)

    with col2:

        st.subheader("🔢 Vector Matemático")

        vector = X[0][:80]

        st.write(vector)

    st.markdown("---")

    st.markdown("""
## 📘 ¿Qué está ocurriendo?

Cada píxel de la imagen se transforma
en una variable matemática.

La imagen facial:

50 x 37 pixeles

se convierte en:

2914 variables numéricas.
""")

    st.markdown("""
<div class="info-box">

Ahora el rostro vive matemáticamente
en un espacio de 2914 dimensiones.

</div>
""", unsafe_allow_html=True)

# =========================================================
# REDUCCIÓN DIMENSIONAL
# =========================================================

elif pagina == "📉 Reducción Dimensional":

    st.title("📉 Reducción Dimensional")

    st.markdown("""
Los humanos no podemos visualizar:

2914 dimensiones.

Por eso necesitamos reducir dimensionalidad.
""")

    st.markdown("---")

    col1,col2,col3 = st.columns([1,1,1])

    with col1:

        st.markdown("""
### 🔴 Antes

- 2914 dimensiones
- imposible visualizar
- espacio complejo
""")

    with col2:

        st.markdown("""
### ⚡ UMAP / t-SNE

Conservan:
- similitudes,
- relaciones,
- estructuras.
""")

    with col3:

        st.markdown("""
### 🟢 Después

- 2 dimensiones
- visualización simple
- agrupamientos visibles
""")

    st.markdown("---")

    st.markdown("""
## Transformación Matemática

R^2914 → R^2

o

R^2914 → R^3
""")

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "🚀 UMAP 2D":

    st.title("🚀 UMAP — Visualización 2D")

    c1,c2,c3 = st.columns(3)

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

        metric = st.selectbox(
            "Métrica",
            ["euclidean", "cosine"]
        )

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric=metric,
        random_state=42
    )

    embedding = reducer.fit_transform(X_scaled)

    df = pd.DataFrame({
        "x": embedding[:,0],
        "y": embedding[:,1],
        "persona": [names[i] for i in y]
    })

    st.markdown("""
## 📘 ¿Qué representa este gráfico?

Cada punto representa:

UN rostro humano.

Puntos cercanos:
→ rostros similares.

Puntos alejados:
→ rostros diferentes.
""")

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

    st.markdown("""
La reducción dimensional también puede
visualizarse en espacios tridimensionales.
""")

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

    st.markdown("""
t-SNE es otra técnica de reducción dimensional
no lineal.
""")

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
# EXPLORACIÓN FACIAL
# =========================================================

elif pagina == "🖼️ Exploración Facial":

    st.title("🖼️ Exploración de Rostros")

    st.markdown("""
Galería interactiva del dataset.
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
## Resultados

- Los rostros humanos representan datos complejos.

- Cada imagen contiene miles de variables.

- UMAP y t-SNE reducen dimensionalidad
preservando similitudes.

- La reducción dimensional permite visualizar
estructuras ocultas y agrupamientos.

## Aplicaciones

- biometría,
- inteligencia artificial,
- visión computacional,
- reconocimiento facial,
- análisis multivariado.
""")
