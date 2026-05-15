# =========================================================
# STREAMLIT — KMEANS 3D REAL ANIMADO
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="K-Means 3D REAL",
    layout="wide"
)

st.title("🎯 K-Means 3D REAL")

st.markdown("""
Simulación REAL del algoritmo K-Means:

1. Datos inicialmente de un solo color
2. Aparición de centroides aleatorios
3. Cálculo de distancias
4. Cambio de color según centroide más cercano
5. Movimiento de centroides
6. Convergencia
""")

# =========================================================
# SUBIR ARCHIVO
# =========================================================

archivo = st.file_uploader(
    "Suba data_USArrests.xlsx",
    type=["xlsx"]
)

# =========================================================
# SI HAY ARCHIVO
# =========================================================

if archivo is not None:

    # =====================================================
    # LEER DATOS
    # =====================================================

    datos = pd.read_excel(
        archivo,
        header=0,
        usecols="A:E"
    )

    datos = datos.dropna()

    # =====================================================
    # VARIABLES NUMERICAS
    # =====================================================

    numericas = datos.select_dtypes(
        include=['float64', 'int64']
    ).columns

    # =====================================================
    # ESCALADO
    # =====================================================

    scaler = StandardScaler()

    datos[numericas] = scaler.fit_transform(
        datos[numericas]
    )

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.header("⚙ Configuración")

    k = st.sidebar.slider(
        "Número de clusters",
        2,
        8,
        4
    )

    max_iter = st.sidebar.slider(
        "Iteraciones",
        2,
        15,
        8
    )

    # =====================================================
    # PCA 3D
    # =====================================================

    pca = PCA(n_components=3)

    X = pca.fit_transform(
        datos[numericas]
    )

    # =====================================================
    # COLORES
    # =====================================================

    colores = [
        'red',
        'green',
        'blue',
        'yellow',
        'purple',
        'orange',
        'cyan',
        'magenta'
    ]

    # =====================================================
    # CENTROIDES INICIALES
    # =====================================================

    np.random.seed(42)

    centroides = X[
        np.random.choice(
            len(X),
            k,
            replace=False
        )
    ]

    # =====================================================
    # FRAMES
    # =====================================================

    frames = []

    # =====================================================
    # FRAME 1
    # SOLO DATOS
    # =====================================================

    frame0 = go.Frame(

        data=[

            go.Scatter3d(

                x=X[:,0],
                y=X[:,1],
                z=X[:,2],

                mode='markers',

                marker=dict(
                    size=
