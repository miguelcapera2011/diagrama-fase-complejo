# =========================================================
# LIBRERÍAS
# =========================================================

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

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="K-Means Profesional",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILOS CSS
# =========================================================

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
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.stMetric {
    background-color: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("Clustering K-Means")

st.markdown("""
Aplicación profesional e interactiva para explorar el algoritmo K-Means paso a paso.
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ Configuración")

uploaded_file = st.sidebar.file_uploader(
    "Suba el archivo data_USArrests.xlsx",
    type=["xlsx"]
)

k = st.sidebar.slider(
    "Número de Clusters",
    2,
    10,
    4
)

iteraciones_animadas = st.sidebar.slider(
    "Frames Animación",
    5,
    50,
    20
)

# =========================================================
# MEMORIA DE HISTORIAL
# =========================================================

if 'historial_tiempos' not in st.session_state:

    st.session_state.historial_tiempos = pd.DataFrame(
        columns=['k', 'Tiempo_ms']
    )

# =========================================================
# CARGA DE DATOS
# =========================================================

if uploaded_file:

    datos = pd.read_excel(uploaded_file)

    # =====================================================
    # DATASET
    # =====================================================

    st.header("📊 Dataset")

    st.dataframe(datos)

    st.header("📌 Información del Dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Filas", datos.shape[0])

    with col2:
        st.metric("Columnas", datos.shape[1])

    with col3:
        st.metric(
            "Valores faltantes",
            datos.isnull().sum().sum()
        )

    st.write(datos.describe())

    # =====================================================
    # LIMPIEZA
    # =====================================================

    datos = datos.dropna()

    # =====================================================
    # HISTOGRAMAS
    # =====================================================

    st.header("📈 Histogramas")

    columnas_numericas = [
        'Murder',
        'Assault',
        'UrbanPop',
        'Rape'
    ]

    tabs = st.tabs(columnas_numericas)

    for i, col in enumerate(columnas_numericas):

        with tabs[i]:

            fig = px.histogram(
                datos,
                x=col,
                marginal='box',
                color_discrete_sequence=['cyan']
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # =====================================================
    # ESTANDARIZACIÓN
    # =====================================================

    st.header("⚖ Estandarización")

    scaler = StandardScaler()

    numericas = datos.select_dtypes(
        include=['float64', 'int64']
    ).columns

    datos[numericas] = scaler.fit_transform(
        datos[numericas]
    )

    st.write(datos.head())

    # =====================================================
    # DISTANCIAS EUCLIDIANAS
    # =====================================================

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

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

    # =====================================================
    # DISTANCIAS MANHATTAN
    # =====================================================

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

    st.plotly_chart(
        fig_manhattan,
        use_container_width=True
    )

    # =====================================================
    # MÉTODO DEL CODO
    # =====================================================

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

    st.plotly_chart(
        fig_elbow,
        use_container_width=True
    )

    # =====================================================
    # KMEANS
    # =====================================================

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

    tiempo_actual = (fin - inicio) * 1000

    st.success(
        f"Tiempo ejecución: {tiempo_actual:.2f} ms"
    )

    # =====================================================
    # GUARDAR HISTORIAL
    # =====================================================

    nueva_fila = pd.DataFrame({
        'k': [k],
        'Tiempo_ms': [tiempo_actual]
    })

    st.session_state.historial_tiempos = pd.concat(
        [
            st.session_state.historial_tiempos,
            nueva_fila
        ],
        ignore_index=True
    )

    historial = (
        st.session_state.historial_tiempos
        .drop_duplicates(
            subset=['k'],
            keep='last'
        )
        .sort_values(by='k')
    )

    st.session_state.historial_tiempos = historial

    # =====================================================
    # MEJOR Y PEOR TIEMPO
    # =====================================================

    mejor_tiempo = historial['Tiempo_ms'].min()

    peor_tiempo = historial['Tiempo_ms'].max()

    mejor_k = historial.loc[
        historial['Tiempo_ms'].idxmin(),
        'k'
    ]

    peor_k = historial.loc[
        historial['Tiempo_ms'].idxmax(),
        'k'
    ]

    # =====================================================
    # MÉTRICAS
    # =====================================================

    st.header("⏱ Comparación de Rendimiento")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🟢 Mejor K",
            f"k = {mejor_k}"
        )

    with col2:
        st.metric(
            "⚡ Mejor Tiempo",
            f"{mejor_tiempo:.2f} ms"
        )

    with col3:
        st.metric(
            "🔴 Peor K",
            f"k = {peor_k}"
        )

    # =====================================================
    # FUNCIÓN COLORES
    # =====================================================

    def colorear_filas(row):

        if row['Tiempo_ms'] == mejor_tiempo:

            return [
                'background-color: green; color: white'
            ] * len(row)

        elif row['Tiempo_ms'] == peor_tiempo:

            return [
                'background-color: red; color: white'
            ] * len(row)

        else:

            return [
                'background-color: orange; color: black'
            ] * len(row)

    # =====================================================
    # TABLA HISTORIAL
    # =====================================================

    st.subheader("📋 Historial Acumulado")

    st.dataframe(
        historial.style
        .apply(colorear_filas, axis=1)
        .format({
            'Tiempo_ms': '{:.2f} ms'
        }),
        use_container_width=True
    )

    # =====================================================
    # GRÁFICA TIEMPOS
    # =====================================================

    colores_barras = []

    for valor in historial['Tiempo_ms']:

        if valor == mejor_tiempo:

            colores_barras.append('green')

        elif valor == peor_tiempo:

            colores_barras.append('red')

        else:

            colores_barras.append('orange')

    fig_tiempos = go.Figure()

    fig_tiempos.add_trace(go.Bar(
        x=historial['k'],
        y=historial['Tiempo_ms'],
        marker_color=colores_barras,
        text=np.round(
            historial['Tiempo_ms'],
            2
        ),
        textposition='outside'
    ))

    fig_tiempos.update_layout(
        title='Tiempo de Ejecución por Número de Clusters',
        xaxis_title='Número de Clusters',
        yaxis_title='Tiempo (ms)',
        template='plotly_dark',
        height=500
    )

    st.plotly_chart(
        fig_tiempos,
        use_container_width=True
    )

    # =====================================================
    # CENTROIDES
    # =====================================================

    st.subheader("Centroides")

    st.write(kmeans.cluster_centers_)

    datos['Cluster'] = km4_clusters.labels_

    # =====================================================
    # PCA
    # =====================================================

    st.header("🧠 PCA")

    pca = PCA(n_components=4)

    pca_scores = pca.fit_transform(
        datos[numericas]
    )

    pca_df = pd.DataFrame(
        pca_scores,
        columns=['PC1', 'PC2', 'PC3', 'PC4']
    )

    pca_df['Cluster'] = (
        km4_clusters.labels_.astype(str)
    )

    pca_df['Etiqueta'] = datos['State']

    # =====================================================
    # PCA 2D
    # =====================================================

    st.subheader("PCA Interactivo 2D")

    fig_2d = px.scatter(
        pca_df,
        x='PC1',
        y='PC2',
        color='Cluster',
        text='Etiqueta',
        title='PCA 2D'
    )

    fig_2d.update_traces(
        textposition='top center'
    )

    st.plotly_chart(
        fig_2d,
        use_container_width=True
    )

    st.success("Aplicación cargada correctamente")

else:

    st.warning(
        "⚠ Suba el archivo data_USArrests.xlsx para iniciar"
    )
