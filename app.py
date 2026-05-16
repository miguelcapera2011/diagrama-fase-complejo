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
        st.metric("Valores faltantes", datos.isnull().sum().sum())

    st.write(datos.describe())

    # =====================================================
    # LIMPIEZA
    # =====================================================

    datos = datos.dropna()

    # =====================================================
    # HISTOGRAMAS
    # =====================================================

    st.header("Histogramas")

    columnas_numericas = ['Murder', 'Assault', 'UrbanPop', 'Rape']

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

    # =====================================================
    # ESTANDARIZACIÓN
    # =====================================================

    st.header("Estandarización")

    scaler = StandardScaler()

    numericas = datos.select_dtypes(include=['float64', 'int64']).columns

    datos[numericas] = scaler.fit_transform(datos[numericas])

    st.write(datos.head())

    # =====================================================
    # DISTANCIAS EUCLIDIANAS
    # =====================================================

    st.header("Distancias Euclidianas")

    distancias = euclidean_distances(datos.drop(columns=['State']))

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

    # =====================================================
    # DISTANCIAS MANHATTAN
    # =====================================================

    st.header("Distancias Manhattan")

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

    # =====================================================
    # MÉTODO DEL CODO
    # =====================================================

    st.header("Método del Codo")

    wss = []

    for i in range(1, 11):

        modelo = KMeans(
            n_clusters=i,
            n_init=50,
            random_state=42
        )

        modelo.fit(datos.drop(columns=['State']))

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

    # =====================================================
    # TIEMPOS KMEANS
    # =====================================================

    st.header("Comparación de Tiempo de Ejecución por Clusters")

    tiempos_kmeans = []
    inercias_kmeans = []

    rangos_k = range(2, 11)

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, k_test in enumerate(rangos_k):

        status_text.text(f"Calculando K-Means con k = {k_test}...")

        inicio_k = time.time()

        modelo_k = KMeans(
            n_clusters=k_test,
            n_init=50,
            random_state=42
        )

        modelo_k.fit(datos.drop(columns=['State']))

        fin_k = time.time()

        tiempo_ms = (fin_k - inicio_k) * 1000

        tiempos_kmeans.append(tiempo_ms)
        inercias_kmeans.append(modelo_k.inertia_)

        progreso = (idx + 1) / len(rangos_k)
        progress_bar.progress(progreso)

    status_text.empty()

    tiempos_df = pd.DataFrame({
        'Clusters': list(rangos_k),
        'Tiempo_ms': tiempos_kmeans,
        'Inercia': inercias_kmeans
    })

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Tiempo mínimo",
            f"{tiempos_df['Tiempo_ms'].min():.2f} ms"
        )

    with col2:

        mejor_k = tiempos_df.loc[
            tiempos_df['Tiempo_ms'].idxmin(),
            'Clusters'
        ]

        st.metric(
            "Mejor rendimiento",
            f"k = {mejor_k}"
        )

    with col3:
        st.metric(
            "Tiempo promedio",
            f"{tiempos_df['Tiempo_ms'].mean():.2f} ms"
        )

    st.dataframe(tiempos_df, use_container_width=True)

    fig_tiempos = px.line(
        tiempos_df,
        x='Clusters',
        y='Tiempo_ms',
        markers=True,
        title='Tiempo de ejecución vs Número de Clusters',
        text='Tiempo_ms'
    )

    fig_tiempos.update_traces(
        texttemplate='%{text:.2f} ms',
        textposition='top center'
    )

    st.plotly_chart(fig_tiempos, use_container_width=True)

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

    st.success(f"Tiempo ejecución: {(fin - inicio)*1000:.2f} ms")

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

