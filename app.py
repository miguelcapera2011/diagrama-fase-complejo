# =========================================================
# FACEEXPLORER AI
# ---------------------------------------------------------
# Reducción Dimensional No Lineal
# UMAP y t-SNE
#
# NUEVA FUNCIÓN:
# Hover sobre vector matemático
# → ilumina pixel correspondiente en la imagen
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
# CSS
# =========================================================

st.markdown("""
<style>

/* FONDO */

.stApp{
    background:
    radial-gradient(circle at top left, #1e1b4b 0%, #050816 40%),
    radial-gradient(circle at bottom right, #111827 0%, #050816 50%);
    color:white;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #0B1120 0%,
        #050816 100%
    );
}

/* TEXTOS */

h1,h2,h3,h4{
    color:#F8FAFC;
}

p, label, div{
    color:#CBD5E1;
}

/* CARDS */

.card{
    background:
    rgba(17,24,39,0.78);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:24px;

    padding:25px;

    margin-bottom:25px;
}

/* METRIC */

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
}

/* BOTONES */

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
    font-weight:600;
}

/* SLIDERS */

.stSlider > div > div > div > div{
    background:#8B5CF6;
}

img{
    border-radius:16px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🧠 FaceExplorer AI")

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
# CARGAR DATOS
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
# INTRODUCCIÓN
# =========================================================

if pagina == "🏠 Introducción":

    st.title("Explora la estructura oculta de los rostros 👋")

    st.markdown("""
Esta aplicación muestra cómo técnicas de reducción dimensional
transforman imágenes complejas en visualizaciones 2D y 3D.
""")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("Dimensiones", n_variables)

    with c2:
        st.metric("Imágenes", n_imagenes)

    with c3:
        st.metric("Métodos", "UMAP / t-SNE")

    with c4:
        st.metric("Visualización", "2D / 3D")

    st.markdown("---")

    st.image(images[0], width=250)

# =========================================================
# DATASET
# =========================================================

elif pagina == "📚 Dataset Original":

    st.title("📚 Dataset Original")

    st.markdown("""
LFW — Labeled Faces in the Wild
""")

    cols = st.columns(5)

    for i in range(10):

        with cols[i % 5]:

            st.image(
                images[i],
                caption=names[y[i]],
                use_container_width=True
            )

# =========================================================
# CONVERSIÓN MATEMÁTICA
# =========================================================

elif pagina == "🔢 Conversión Matemática":

    st.title("🔢 Conversión de Imagen a Datos")

    st.markdown("""
Cada píxel de la imagen se convierte
en una variable matemática.
""")

    # =====================================================
    # IMAGEN ORIGINAL
    # =====================================================

    image = images[0]

    alto, ancho = image.shape

    vector = X[0]

    # =====================================================
    # SELECCIÓN DEL PIXEL
    # =====================================================

    pixel_index = st.slider(
        "Selecciona un valor del vector",
        0,
        len(vector)-1,
        100
    )

    valor_pixel = vector[pixel_index]

    # =====================================================
    # CONVERTIR ÍNDICE A FILA/COLUMNA
    # =====================================================

    fila = pixel_index // ancho
    columna = pixel_index % ancho

    # =====================================================
    # CREAR IMAGEN RESALTADA
    # =====================================================

    imagen_color = np.stack([image]*3, axis=-1)

    imagen_color = imagen_color / imagen_color.max()

    # PIXEL ROJO

    imagen_color[fila, columna] = [1,0,0]

    # =====================================================
    # COLUMNAS
    # =====================================================

    c1, c2 = st.columns([1,1])

    # =====================================================
    # IMAGEN
    # =====================================================

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

    # =====================================================
    # VECTOR
    # =====================================================

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

        # RESALTAR PIXEL

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
