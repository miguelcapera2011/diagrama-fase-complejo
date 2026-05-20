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
# NUEVA FUNCIÓN:
# Hover conceptual entre vector y pixel
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
# CSS MODERNO
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

---

## 🔍 ¿Qué aprenderás en esta aplicación?

✅ Cómo se ve el dataset original  
✅ Cómo la computadora interpreta una imagen  
✅ Cómo una imagen se convierte en vectores matemáticos  
✅ Qué significa alta dimensionalidad  
✅ Cómo UMAP y t-SNE reducen dimensiones  
✅ Cómo aparecen agrupamientos visuales  

---

## 🧠 Idea principal

La reducción dimensional NO elimina información al azar.

El objetivo es:

preservar relaciones y similitudes
entre los datos originales.

Por eso:

rostros parecidos terminan cerca
en el espacio reducido.
""")

    with col2:

        st.image(images[0], use_container_width=True)

        st.markdown("""
<div class="info-box">

La computadora no ve una cara.

Ve miles de números.

</div>
""", unsafe_allow_html=True)

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

    st.markdown("""
Cada píxel de la imagen se convierte
en una variable matemática.
""")

    image = images[0]

    alto, ancho = image.shape

    vector = X[0]

    pixel_index = st.slider(
        "Selecciona un valor del vector",
        0,
        len(vector)-1,
        100
    )

    valor_pixel = vector[pixel_index]

    fila = pixel_index // ancho
    columna = pixel_index % ancho

    imagen_color = np.stack([image]*3, axis=-1)

    imagen_color = imagen_color / imagen_color.max()

    imagen_color[fila, columna] = [1,0,0]

    c1, c2 = st.columns([1,1])

    with c1:

        st.subheader("🖼️ Imagen")

        fig = px.imshow(imagen_color)

        fig.update_layout(
            height=500,
            margin=dict(l=0,r=0,t=0,b=0),
            coloraxis_showscale=False
        )

        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
### Pixel Seleccionado

- Índice: {pixel_index}
- Fila: {fila}
- Columna: {columna}
- Valor: {valor_pixel:.2f}
""")

    with c2:

        st.subheader("🔢 Vector Matemático")

        vector_df = pd.DataFrame({
            "Índice": np.arange(150),
            "Valor": vector[:150]
        })

        fig2 = px.bar(
            vector_df,
            x="Índice",
            y="Valor",
            template="plotly_dark"
        )

        colores = [
            "#8B5CF6" if i != pixel_index else "#ff004c"
            for i in range(150)
        ]

        fig2.update_traces(
            marker_color=colores
        )

        fig2.update_layout(
            height=500,
            paper_bgcolor="#050816",
            plot_bgcolor="#050816"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.markdown("""
## 📘 ¿Qué está ocurriendo?

La computadora NO ve una cara.

La computadora ve:

x = (x₁, x₂, x₃, ..., x₂₉₁₄)

Cada valor representa la intensidad de un píxel.

Cuando seleccionas un valor del vector:

- se ilumina el píxel correspondiente,
- mostrando la conexión entre:
    - imagen
    - matemáticas.
""")

# =========================================================
# REDUCCIÓN DIMENSIONAL
# =========================================================

elif pagina == "📉 Reducción Dimensional":

    st.title("📉 Reducción Dimensional")

    st.markdown("""
Ahora el rostro vive en un espacio de:

2914 dimensiones.

Los humanos NO podemos visualizar eso.
""")

    st.markdown("---")

    c1,c2,c3 = st.columns(3)

    with c1:

        st.markdown("""
### 🔴 Antes

- 2914 dimensiones
- imposible visualizar
""")

    with c2:

        st.markdown("""
### ⚡ UMAP / t-SNE

Preservan similitudes.
""")

    with c3:

        st.markdown("""
### 🟢 Después

- 2D / 3D
- visualizable
""")

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "🚀 UMAP 2D":

    st.title("🚀 UMAP — Visualización 2D")

    n_neighbors = st.slider(
        "n_neighbors",
        5,
        50,
        15
    )

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=n_neighbors,
        random_state=42
    )

    embedding = reducer.fit_transform(X_scaled)

    df = pd.DataFrame({
        "x": embedding[:,0],
        "y": embedding[:,1],
        "persona": [names[i] for i in y]
    })

    st.markdown("""
Cada punto representa un rostro humano.

Puntos cercanos:
→ rostros similares.
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

    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="persona",
        template="plotly_dark",
        height=850
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

    tsne = TSNE(
        n_components=2,
        perplexity=30,
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

    fig.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# CONCLUSIONES
# =========================================================

elif pagina == "📌 Conclusiones":

    st.title("📌 Conclusiones")

    st.markdown("""
## Resultados

- Las imágenes representan datos de alta dimensionalidad.
- Cada píxel es una variable matemática.
- UMAP y t-SNE reducen dimensionalidad.
- Los rostros similares quedan agrupados.
- Ahora podemos visualizar datos complejos en 2D y 3D.

## Aplicaciones

- IA
- biometría
- reconocimiento facial
- visión computacional
""")
