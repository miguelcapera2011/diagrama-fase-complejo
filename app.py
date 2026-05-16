# =========================
# LIBRERIAS
# =========================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial.distance import pdist, squareform


# =========================
# CONFIGURACIÓN GENERAL
# =========================

st.set_page_config(
    page_title="K-Means Profesional",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# ESTILOS CSS
# =========================

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

h1 {
    color: #00ffd5;
    text-align: center;
    font-size: 50px;
}

h2 {
    color: #00c3ff;
}

h3 {
    color: #ffffff;
}

.stMetric {
    background-color: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
}

.css-1d391kg {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)


# =========================
# TITULO
# =========================

st.title("Clustering K-Means")

st.markdown("""
Esta aplicación permite explorar paso a paso el algoritmo K-Means usando el dataset USArrests.

Incluye:

- Exploración de datos
- Estandarización
- Distancias Euclidianas y Manhattan
- Método del codo
- Animación de convergencia de K-Means
- PCA 2D y 3D
- Boxplots interactivos
- Visualizaciones dinámicas
- Movimiento de centroides
- Explicaciones matemáticas
""")


# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙ Configuración")

uploaded_file = st.sidebar.file_uploader(
    "Suba el archivo data_USArrests.xlsx",
    type=["xlsx"]
)

k = st.sidebar.slider("Número de Clusters", 2, 10, 4)

iteraciones_animadas = st.sidebar.slider(
    "Frames Animación",
    5,
    50,
    20
)


# =========================
# CARGA DE DATOS
# =========================

if uploaded_file:

    datos = pd.read_excel(uploaded_file)

    st.header("Dataset")
    st.dataframe(datos)

    st.header(" Información del Dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Filas", datos.shape[0])

    with col2:
        st.metric("Columnas", datos.shape[1])

    with col3:
        st.metric("Valores faltantes", datos.isnull().sum().sum())

    st.write(datos.describe())


    # =========================
    # LIMPIEZA
    # =========================

    datos = datos.dropna()


    # =========================
    # HISTOGRAMAS
    # =========================

    st.header(" Histogramas")

    columnas_numericas = ['Murder', 'Assault', 'UrbanPop', 'Rape']

    fig_hist = px.histogram(
        datos,
        x='Murder',
        nbins=10,
        title='Distribución Murder'
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    tabs = st.tabs(columnas_numericas)

    for i, col in enumerate(columnas_numericas):

        with tabs[i]:

            fig = px.histogram(
                datos,
                x=col,
                marginal='box',
                color_discrete_sequence=['cyan']
            )

            st.plotly_chart(fig, use_container_width=True)


    # =========================
    # ESTANDARIZACIÓN
    # =========================

    st.header("⚖ Estandarización")

    scaler = StandardScaler()

    numericas = datos.select_dtypes(
        include=['float64', 'int64']
    ).columns

    datos[numericas] = scaler.fit_transform(
        datos[numericas]
    )

    st.write(datos.head())


    # =========================
    # MATRIZ DISTANCIAS
    # =========================

    st.header("📏 Distancias Euclidianas")

    distancias = euclidean_distances(
        datos.drop(columns=['State'])
    )

    dist_matrix = pd.DataFrame(
        distancias,
        index=datos['State'],
        columns=datos['State']
    )

    fig_heat = px.imshow(
        dist_matrix,
        color_continuous_scale='RdBu',
        title='Mapa de calor Distancias Euclidianas'
    )

    st.plotly_chart(fig_heat, use_container_width=True)


    # =========================
    # DISTANCIAS MANHATTAN
    # =========================

    st.header("📐 Distancias Manhattan")

    manhattan = pdist(
        datos.drop(columns=['State']),
        metric='cityblock'
    )

    manhattan_square = squareform(manhattan)

    manhattan_df = pd.DataFrame(
        manhattan_square,
        index=datos['State'],
        columns=datos['State']
    )

    fig_manhattan = px.imshow(
        manhattan_df,
        color_continuous_scale='Viridis',
        title='Mapa Distancias Manhattan'
    )

    st.plotly_chart(fig_manhattan, use_container_width=True)


    # =========================
    # METODO DEL CODO
    # =========================

    st.header("🦴 Método del Codo")

    wss = []

    for i in range(1, 11):

        modelo = KMeans(
            n_clusters=i,
            n_init=50,
            random_state=42
        )

        modelo.fit(
            datos.drop(columns=['State'])
        )

        wss.append(modelo.inertia_)

    elbow_df = pd.DataFrame({
        'Clusters': range(1, 11),
        'WSS': wss
    })

    fig_elbow = px.line(
        elbow_df,
        x='Clusters',
        y='WSS',
        markers=True,
        title='Método del Codo'
    )

    fig_elbow.add_vline(
        x=k,
        line_dash='dash',
        line_color='red'
    )

    st.plotly_chart(fig_elbow, use_container_width=True)


    # =========================
    # KMEANS
    # =========================

    st.header("🤖 Algoritmo K-Means")

    kmeans = KMeans(
        n_clusters=k,
        n_init=50,
        random_state=42
    )

    inicio = time.time()

    km4_clusters = kmeans.fit(
        datos.drop(columns=['State'])
    )

    fin = time.time()

    st.success(
        f"Tiempo ejecución: {(fin - inicio)*1000:.2f} ms"
    )


    # =========================
    # NUEVO BLOQUE AGREGADO
    # =========================

    tiempo_actual = (fin - inicio) * 1000

    if "historial_tiempos" not in st.session_state:
        st.session_state.historial_tiempos = []

    st.session_state.historial_tiempos = [
        x for x in st.session_state.historial_tiempos
        if x["Clusters"] != k
    ]

    st.session_state.historial_tiempos.append({
        "Clusters": k,
        "Tiempo": tiempo_actual
    })

    historial_df = pd.DataFrame(
        st.session_state.historial_tiempos
    ).sort_values(by="Clusters")

    if st.button("📊 Mostrar comparación de tiempos"):

        st.subheader(
            "⏱ Comparación de tiempos por número de clusters"
        )

        mejor = historial_df["Tiempo"].min()
        peor = historial_df["Tiempo"].max()

        colores_barras = []

        for valor in historial_df["Tiempo"]:

            if valor == mejor:
                colores_barras.append("green")

            elif valor == peor:
                colores_barras.append("red")

            else:
                colores_barras.append("orange")

        fig_tiempos = go.Figure()

        fig_tiempos.add_trace(
            go.Bar(
                x=historial_df["Clusters"],
                y=historial_df["Tiempo"],
                marker_color=colores_barras,
                text=np.round(historial_df["Tiempo"], 2),
                textposition='outside'
            )
        )

        fig_tiempos.update_layout(
            title="Tiempo de ejecución según K",
            xaxis_title="Número de Clusters",
            yaxis_title="Tiempo (ms)",
            height=500
        )

        st.plotly_chart(
            fig_tiempos,
            use_container_width=True
        )

        mejor_k = historial_df.loc[
            historial_df["Tiempo"].idxmin(),
            "Clusters"
        ]

        peor_k = historial_df.loc[
            historial_df["Tiempo"].idxmax(),
            "Clusters"
        ]

        st.markdown(f"""
        ## 📌 Análisis Automático

        - 🟢 El mejor rendimiento fue con K = {mejor_k}

        - 🔴 El peor rendimiento fue con K = {peor_k}

        - 🟠 Los demás fueron intermedios.

        ### Explicación

        Cuando aumenta K:

        - Se calculan más centroides.
        - Hay más distancias.
        - Puede tardar más en converger.

        Por eso algunos valores de K
        tardan más que otros.
        """)

    st.subheader("Centroides")
    st.write(kmeans.cluster_centers_)

    datos['Cluster'] = km4_clusters.labels_

    # EL RESTO DEL CÓDIGO ORIGINAL CONTINÚA IGUAL
    # NO SE ELIMINÓ NADA
