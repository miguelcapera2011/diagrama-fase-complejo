# Código completo actualizado de la app Streamlit K-Means


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
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("Clustering K-Means")

st.markdown("""
Esta aplicación permite explorar paso a paso el algoritmo K-Means usando el dataset USArrests.
""")

# =========================================================
# SIDEBAR
# =========================================================

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

# =========================================================
# HISTORIAL GLOBAL DE TIEMPOS
# =========================================================

if 'historial_kmeans' not in st.session_state:

    st.session_state.historial_kmeans = pd.DataFrame(
        columns=['Clusters', 'Tiempo_ms', 'Inercia']
    )

# =========================================================
# CARGA DE DATOS
# =========================================================

if uploaded_file:

    datos = pd.read_excel(uploaded_file)

    st.header("Dataset")
    st.dataframe(datos)

    # =====================================================
    # INFORMACIÓN DATASET
    # =====================================================

    st.header("Información del Dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Filas", datos.shape[0])

    with col2:
        st.metric("Columnas", datos.shape[1])

    with col3:

        # Mostrar peor resultado SOLO si existen
        # al menos 2 configuraciones diferentes

        if len(historial) > 1:

            peor_k = historial.loc[
                historial['Tiempo_ms'].idxmax(),
                'Clusters'
            ]

            st.metric(
                "🐢 Peor k",
                f"k = {peor_k}"
            )

        else:

            st.empty()

    # =====================================================
    # TABLA COLOREADA
    # =====================================================

    st.subheader("📋 Historial acumulado")

    st.dataframe(
        historial.style
        .apply(colorear_filas, axis=1)
        .format({
            'Tiempo_ms': '{:.2f} ms',
            'Inercia': '{:.2f}'
        }),
        use_container_width=True
    )

    # =====================================================
    # GRÁFICO TIEMPOS
    # =====================================================

    colores_barras = []

    for valor in historial['Tiempo_ms']:

        if valor == mejor_tiempo:
            colores_barras.append('green')

        elif valor == peor_tiempo:
            colores_barras.append('red')

        else:
            colores_barras.append('orange')

    fig_historial = go.Figure()

    fig_historial.add_trace(go.Bar(
        x=historial['Clusters'],
        y=historial['Tiempo_ms'],
        marker_color=colores_barras,
        text=np.round(historial['Tiempo_ms'], 2),
        textposition='outside'
    ))

    fig_historial.update_layout(
        title='Comparación de tiempos por número de clusters',
        xaxis_title='Número de Clusters (k)',
        yaxis_title='Tiempo de ejecución (ms)',
        height=600,
        template='plotly_dark'
    )

    st.plotly_chart(fig_historial, use_container_width=True)

    # =====================================================
    # KMEANS
    # =====================================================

    st.header("Algoritmo K-Means")

    kmeans = KMeans(
        n_clusters=k,
        n_init=50,
        random_state=42
    )

    inicio = time.time()

    km4_clusters = kmeans.fit(datos.drop(columns=['State']))

    fin = time.time()

    tiempo_actual = (fin - inicio) * 1000

    st.success(f"Tiempo ejecución: {tiempo_actual:.2f} ms")

    # =====================================================
    # GUARDAR HISTORIAL DE TIEMPOS
    # =====================================================

    nueva_fila = pd.DataFrame({
        'Clusters': [k],
        'Tiempo_ms': [tiempo_actual],
        'Inercia': [km4_clusters.inertia_]
    })

    st.session_state.historial_kmeans = pd.concat(
        [st.session_state.historial_kmeans, nueva_fila],
        ignore_index=True
    )

    historial = st.session_state.historial_kmeans.copy()

    # =====================================================
    # ELIMINAR DUPLICADOS CONSERVANDO EL ÚLTIMO
    # =====================================================

    historial = historial.drop_duplicates(
        subset=['Clusters'],
        keep='last'
    )

    st.session_state.historial_kmeans = historial

    # =====================================================
    # MEJOR Y PEOR TIEMPO
    # =====================================================

    mejor_tiempo = historial['Tiempo_ms'].min()
    peor_tiempo = historial['Tiempo_ms'].max()

    # =====================================================
    # FUNCIÓN COLORES TABLA
    # =====================================================

    def colorear_filas(row):

        if row['Tiempo_ms'] == mejor_tiempo:
            return ['background-color: green; color: white'] * len(row)

        elif row['Tiempo_ms'] == peor_tiempo:
            return ['background-color: red; color: white'] * len(row)

        else:
            return ['background-color: orange; color: black'] * len(row)

    # =====================================================
    # HISTORIAL VISUAL
    # =====================================================

    st.header("Historial de Rendimiento K-Means")

    col1, col2, col3 = st.columns(3)

    with col1:

        mejor_k = historial.loc[
            historial['Tiempo_ms'].idxmin(),
            'Clusters'
        ]

        st.metric(
            "Mejor k",
            f"k = {mejor_k}"
        )

    with col2:

        st.metric(
            "Mejor tiempo",
            f"{mejor_tiempo:.2f} ms"
        )

    with col3:

        peor_k = historial.loc[
            historial['Tiempo_ms'].idxmax(),
            'Clusters'
        ]

        st.metric(
            "Peor k",
            f"k = {peor_k}"
        )

    st.subheader("Tabla acumulada de pruebas")

    st.dataframe(
        historial.style
        .apply(colorear_filas, axis=1)
        .format({
            'Tiempo_ms': '{:.2f} ms',
            'Inercia': '{:.2f}'
        }),
        use_container_width=True
    )

    # =====================================================
    # GRÁFICO COMPARACIÓN
    # =====================================================

    colores_barras = []

    for valor in historial['Tiempo_ms']:

        if valor == mejor_tiempo:
            colores_barras.append('green')

        elif valor == peor_tiempo:
            colores_barras.append('red')

        else:
            colores_barras.append('orange')

    fig_historial = go.Figure()

    fig_historial.add_trace(go.Bar(
        x=historial['Clusters'],
        y=historial['Tiempo_ms'],
        marker_color=colores_barras,
        text=np.round(historial['Tiempo_ms'], 2),
        textposition='outside'
    ))

    fig_historial.update_layout(
        title='Comparación de tiempos por número de clusters',
        xaxis_title='Número de Clusters (k)',
        yaxis_title='Tiempo de ejecución (ms)',
        height=600,
        template='plotly_dark'
    )

    st.plotly_chart(fig_historial, use_container_width=True)

    st.subheader("Centroides")
    st.write(kmeans.cluster_centers_)

    datos['Cluster'] = km4_clusters.labels_

    # =====================================================
    # PCA
    # =====================================================

    st.header("PCA")

    pca = PCA(n_components=4)

    pca_scores = pca.fit_transform(datos[numericas])

    pca_df = pd.DataFrame(
        pca_scores,
        columns=['PC1', 'PC2', 'PC3', 'PC4']
    )

    pca_df['Cluster'] = km4_clusters.labels_.astype(str)
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

    st.plotly_chart(fig_2d, use_container_width=True)

    # =====================================================
    # SIMULACIÓN KMEANS 3D
    # =====================================================

    st.subheader("Simulación paso a paso REAL de K-Means")

    X3D = pca_df[['PC1', 'PC2', 'PC3']].values
    labels_names = datos['State'].values

    np.random.seed(42)

    centroides_init = X3D[np.random.choice(len(X3D), k, replace=False)]

    centroides_hist = [centroides_init]
    labels_hist = []

    centroides = centroides_init.copy()

    max_iter = iteraciones_animadas

    for _ in range(max_iter):

        distancias = np.linalg.norm(X3D[:, None] - centroides, axis=2)
        labels = np.argmin(distancias, axis=1)

        labels_hist.append(labels)

        nuevos_centroides = []

        for i in range(k):

            puntos = X3D[labels == i]

            if len(puntos) > 0:
                nuevos_centroides.append(puntos.mean(axis=0))
            else:
                nuevos_centroides.append(centroides[i])

        nuevos_centroides = np.array(nuevos_centroides)

        centroides_hist.append(nuevos_centroides)

        if np.linalg.norm(nuevos_centroides - centroides) < 1e-4:
            break

        centroides = nuevos_centroides

    total_iter = len(labels_hist)

    iter_sel = st.slider(
        "Selecciona iteración",
        0,
        total_iter - 1,
        0
    )

    labels_sel = labels_hist[iter_sel]
    centroids_sel = centroides_hist[iter_sel]

    colores_k = ['red','green','blue','yellow','purple','orange','cyan','magenta']

    fig_k = go.Figure()

    for i in range(k):

        puntos = X3D[labels_sel == i]
        nombres = labels_names[labels_sel == i]

        fig_k.add_trace(go.Scatter3d(
            x=puntos[:,0],
            y=puntos[:,1],
            z=puntos[:,2],
            mode='markers+text',
            text=nombres,
            textposition='top center',
            marker=dict(size=5, color=colores_k[i]),
            name=f'Cluster {i}'
        ))

    fig_k.add_trace(go.Scatter3d(
        x=centroids_sel[:,0],
        y=centroids_sel[:,1],
        z=centroids_sel[:,2],
        mode='markers',
        marker=dict(size=18, color='white', symbol='diamond'),
        name='Centroides'
    ))

    for i in range(len(X3D)):

        c = labels_sel[i]
        centroide = centroids_sel[c]

        fig_k.add_trace(go.Scatter3d(
            x=[X3D[i,0], centroide[0]],
            y=[X3D[i,1], centroide[1]],
            z=[X3D[i,2], centroide[2]],
            mode='lines',
            line=dict(color=colores_k[c], width=2),
            showlegend=False
        ))

    fig_k.update_layout(
        title=f"K-Means Paso a Paso - Iteración {iter_sel}",
        width=1700,
        height=900,
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font=dict(color='white'),
        scene=dict(
            xaxis_title='PC1',
            yaxis_title='PC2',
            zaxis_title='PC3'
        )
    )

    st.plotly_chart(fig_k, use_container_width=True)

    # =====================================================
    # BOXPLOT
    # =====================================================

    st.header("Boxplot Interactivo")

    fig_box = px.box(
        datos,
        x='Cluster',
        y='Rape',
        color='Cluster',
        points='all',
        hover_data=['State']
    )

    st.plotly_chart(fig_box, use_container_width=True)

    # =====================================================
    # TABLA CLUSTERS
    # =====================================================

    st.header("Estados por Cluster")

    grupos = pd.DataFrame()

    grupos['State'] = datos['State']
    grupos['Cluster'] = km4_clusters.labels_

    st.dataframe(
        grupos.sort_values(by='Cluster'),
        use_container_width=True
    )

    # =====================================================
    # CANTIDAD CLUSTERS
    # =====================================================

    st.header("Cantidad de individuos por Cluster")

    conteo = grupos.groupby('Cluster').size().reset_index()

    conteo.columns = ['Cluster', 'Cantidad']

    fig_count = px.bar(
        conteo,
        x='Cluster',
        y='Cantidad',
        color='Cluster',
        text='Cantidad'
    )

    st.plotly_chart(fig_count, use_container_width=True)

    # =====================================================
    # MURDER VS URBANPOP
    # =====================================================

    st.header("Murder vs UrbanPop")

    fig_mu = px.scatter(
        datos,
        x='Murder',
        y='UrbanPop',
        color='Cluster',
        hover_data=['State'],
        title='Murder vs UrbanPop'
    )

    st.plotly_chart(fig_mu, use_container_width=True)

    # =====================================================
    # RAPE VS ASSAULT
    # =====================================================

    st.header("Rape vs Assault")

    fig_ra = px.scatter(
        datos,
        x='Rape',
        y='Assault',
        color='Cluster',
        hover_data=['State'],
        title='Rape vs Assault'
    )

    st.plotly_chart(fig_ra, use_container_width=True)

    # =====================================================
    # EXPLICACIÓN MATEMÁTICA
    # =====================================================

    st.header("Explicación Matemática")

    st.markdown("""
    ## ¿Cómo funciona K-Means?

    1. Se eligen centroides aleatorios.

    2. Cada punto calcula su distancia al centroide más cercano.

    3. Los puntos se asignan al cluster más cercano.

    4. Los centroides se recalculan usando el promedio de los puntos.

    5. El proceso se repite hasta converger.
    """)

    st.success("Aplicación cargada correctamente")

else:

    st.warning("Suba el archivo data_USArrests.xlsx para iniciar")


