# =========================================================
# FACEEXPLORER AI
# ---------------------------------------------------------
# Reducción de Dimensionalidad No Lineal
#
# Proyecto:
# UMAP y t-SNE sobre rostros humanos
#
# =========================================================

# =========================================================
# LIBRERÍAS A INSTALAR
# =========================================================

# pip install streamlit
# pip install numpy
# pip install pandas
# pip install plotly
# pip install scikit-learn
# pip install umap-learn
# pip install streamlit-plotly-events

# =========================================================
# IMPORTAR LIBRERÍAS
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

from streamlit_plotly_events import plotly_events

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
FONDO
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

    margin-bottom:20px;
}

/* =====================================================
HOVER
===================================================== */

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
}

/* =====================================================
SLIDERS
===================================================== */

.stSlider > div > div > div > div{

    background:#8B5CF6;
}

/* =====================================================
TABLAS
===================================================== */

[data-testid="stDataFrame"]{

    border-radius:18px;
}

/* =====================================================
CAJAS
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
IMÁGENES
===================================================== */

img{

    border-radius:16px;
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

Proyecto de Análisis Multivariado.
""")

pagina = st.sidebar.radio(
    "Navegación",
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

    lfw = fetch_lfw_people(
        min_faces_per_person=70
    )

    X = lfw.data
    y = lfw.target
    images = lfw.images
    names = lfw.target_names

    return X, y, images, names

X, y, images, names = cargar_datos()

# =========================================================
# ESCALAR
# =========================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# =========================================================
# MÉTRICAS
# =========================================================

n_imagenes = X.shape[0]
n_variables = X.shape[1]

# =========================================================
# INTRODUCCIÓN
# =========================================================

if pagina == "🏠 Introducción":

    st.title("Explora la estructura oculta de los rostros 👋")

    st.markdown("""
Esta aplicación muestra cómo técnicas
de reducción dimensional transforman
imágenes complejas en espacios visuales.
""")

    st.markdown("")

    c1,c2,c3 = st.columns(3)

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
        <p>y t-SNE</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.image(
        images[0],
        width=250
    )

# =========================================================
# DATASET ORIGINAL
# =========================================================

elif pagina == "📚 Dataset Original":

    st.title("📚 Dataset Original")

    st.markdown("""
## LFW Dataset

Dataset utilizado en:
- reconocimiento facial,
- biometría,
- inteligencia artificial.
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
# CONVERSIÓN MATEMÁTICA INTERACTIVA
# =========================================================

elif pagina == "🔢 Conversión Matemática":

    st.title("🔢 Conversión de Imagen a Datos")

    st.markdown("""
## Hover interactivo

Pasa el cursor sobre la imagen.

La aplicación detectará:

- fila,
- columna,
- índice vectorial,
- valor matemático,

y resaltará automáticamente
la fila correspondiente del vector.
""")

    st.markdown("---")

    imagen = images[0]

    alto, ancho = imagen.shape

    # =====================================================
    # HEATMAP INTERACTIVO
    # =====================================================

    fig = go.Figure(
        data=go.Heatmap(
            z=imagen,
            colorscale='Gray',
            showscale=False,

            hovertemplate=
            "<b>Fila:</b> %{y}<br>" +
            "<b>Columna:</b> %{x}<br>" +
            "<b>Valor:</b> %{z}<extra></extra>"
        )
    )

    fig.update_layout(

        height=500,

        template="plotly_dark",

        paper_bgcolor="#050816",

        plot_bgcolor="#050816",

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    # =====================================================
    # DETECTAR HOVER
    # =====================================================

    selected_points = plotly_events(
        fig,

        hover_event=True,

        click_event=False,

        select_event=False,

        override_height=500
    )

    # =====================================================
    # VALORES DEFAULT
    # =====================================================

    fila = 0
    columna = 0

    pixel_index = 0

    pixel_value = X[0][0]

    # =====================================================
    # SI HAY HOVER
    # =====================================================

    if selected_points:

        punto = selected_points[0]

        columna = int(punto["x"])

        fila = int(punto["y"])

        pixel_index = fila * ancho + columna

        pixel_value = X[0][pixel_index]

    # =====================================================
    # COLUMNAS
    # =====================================================

    col1, col2 = st.columns([1,2])

    # =====================================================
    # IMAGEN
    # =====================================================

    with col1:

        st.subheader("🖼️ Imagen")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(f"""
<div class="info-box">

### Pixel Detectado

- Fila: <b>{fila}</b>
- Columna: <b>{columna}</b>

### Índice Vectorial

<b>{pixel_index}</b>

### Valor Matemático

<b>{pixel_value:.2f}</b>

</div>
""", unsafe_allow_html=True)

    # =====================================================
    # VECTOR MATEMÁTICO
    # =====================================================

    with col2:

        st.subheader("🔢 Vector Matemático")

        vector = X[0][:500]

        vector_df = pd.DataFrame({

            "Índice": np.arange(500),

            "Valor": vector

        })

        # =================================================
        # RESALTAR FILA VERDE
        # =================================================

        def highlight_row(row):

            if row.name == pixel_index:

                return [
                    'background-color: #00ff99; color:black'
                ] * len(row)

            else:

                return [''] * len(row)

        styled_df = vector_df.style.apply(
            highlight_row,
            axis=1
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            height=700
        )

    st.markdown("---")

    st.markdown("""
## 📘 ¿Qué está ocurriendo?

La computadora convierte la imagen
en un vector matemático:

x = (x₁, x₂, x₃, ..., x₂₉₁₄)

Cada posición del vector representa:

- un píxel,
- una intensidad,
- información visual.

Ahora puedes explorar visualmente
la relación entre:

imagen ↔ píxel ↔ vector matemático.
""")

# =========================================================
# REDUCCIÓN DIMENSIONAL
# =========================================================

elif pagina == "📉 Reducción Dimensional":

    st.title("📉 Reducción Dimensional")

    st.markdown("""
Los humanos no podemos visualizar:

2914 dimensiones.

UMAP y t-SNE permiten transformar
estos datos en espacios 2D y 3D.
""")

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "🚀 UMAP 2D":

    st.title("🚀 UMAP — Visualización 2D")

    reducer = umap.UMAP(
        n_components=2,
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

        height=800
    )

    fig.update_layout(

        paper_bgcolor="#050816",

        plot_bgcolor="#050816"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# TSNE
# =========================================================

elif pagina == "🧠 t-SNE":

    st.title("🧠 t-SNE")

    tsne = TSNE(
        n_components=2,
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

        height=800
    )

    st.plotly_chart(
        fig,
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
- reconocimiento facial.
""")
