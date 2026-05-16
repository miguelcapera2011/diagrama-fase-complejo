#librerias
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


# CONFIGURACIÓN GENERAL


st.set_page_config(
    page_title="K-Means Profesional",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ESTILOS CSS
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

# SIDEBAR

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


# CARGA DE DATOS


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


    # LIMPIEZA


    datos = datos.dropna()

    # HISTOGRAMAS


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

   
    # ESTANDARIZACIÓN

    st.header("⚖ Estandarización")

    scaler = StandardScaler()

    numericas = datos.select_dtypes(include=['float64', 'int64']).columns

    datos[numericas] = scaler.fit_transform(datos[numericas])

    st.write(datos.head())

    # MATRICES DE DISTANCIA


    st.header("📏 Distancias Euclidianas")

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

    # DISTANCIAS MANHATTAN


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


    # MÉTODO DEL CODO
  

    st.header("🦴 Método del Codo")

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

    # =========================================================
    # COMPARACIÓN DE CLUSTERS Y TIEMPOS
    # =========================================================

    st.header("⏱ Comparación de Clusters y Tiempo de Ejecución")

    comparacion = []

    X_cluster = datos.drop(columns=['State'])

    for n_clusters in range(2, 11):

        inicio_comp = time.time()

        modelo_comp = KMeans(
            n_clusters=n_clusters,
            n_init=50,
            random_state=42
        )

        modelo_comp.fit(X_cluster)

        fin_comp = time.time()

        tiempo_ms = (fin_comp - inicio_comp) * 1000

        inercia = modelo_comp.inertia_

        comparacion.append({
            "Clusters": n_clusters,
            "Tiempo_ms": tiempo_ms,
            "Inercia": inercia
        })

    comparacion_df = pd.DataFrame(comparacion)

    # NORMALIZACIÓN

    comparacion_df["Tiempo_norm"] = (
        comparacion_df["Tiempo_ms"] /
        comparacion_df["Tiempo_ms"].max()
    )

    comparacion_df["Inercia_norm"] = (
        comparacion_df["Inercia"] /
        comparacion_df["Inercia"].max()
    )

    # SCORE FINAL

    comparacion_df["Score"] = (
        comparacion_df["Tiempo_norm"] * 0.3 +
        comparacion_df["Inercia_norm"] * 0.7
    )

    mejor_idx = comparacion_df["Score"].idxmin()
    peor_idx = comparacion_df["Score"].idxmax()

    colores_modelo = []

    for idx in comparacion_df.index:

        if idx == mejor_idx:
            colores_modelo.append("green")

        elif idx == peor_idx:
            colores_modelo.append("red")

        else:
            colores_modelo.append("orange")

    comparacion_df["Color"] = colores_modelo

    # TABLA

    st.subheader("📋 Tabla Comparativa")

    st.dataframe(
        comparacion_df[
            [
                "Clusters",
                "Tiempo_ms",
                "Inercia",
                "Score"
            ]
        ].style.format({
            "Tiempo_ms": "{:.2f}",
            "Inercia": "{:.2f}",
            "Score": "{:.4f}"
        }),
        use_container_width=True
    )

    # GRÁFICA TIEMPOS

    st.subheader("⚡ Tiempo de Ejecución por Número de Clusters")

    fig_tiempo = px.bar(
        comparacion_df,
        x="Clusters",
        y="Tiempo_ms",
        color="Color",
        color_discrete_map={
            "green": "green",
            "red": "red",
            "orange": "orange"
        },
        text="Tiempo_ms",
        title="Comparación de Tiempo de Ejecución"
    )

    fig_tiempo.update_traces(
        texttemplate='%{text:.2f} ms',
        textposition='outside'
    )

    st.plotly_chart(fig_tiempo, use_container_width=True)

    # GRÁFICA SCORE

    st.subheader("🎯 Calidad General del Modelo")

    fig_score = px.bar(
        comparacion_df,
        x="Clusters",
        y="Score",
        color="Color",
        color_discrete_map={
            "green": "green",
            "red": "red",
            "orange": "orange"
        },
        text="Score",
        title="Evaluación Global de Clusters"
    )

    fig_score.update_traces(
        texttemplate='%{text:.4f}',
        textposition='outside'
    )

    st.plotly_chart(fig_score, use_container_width=True)

    # DATOS MEJOR Y PEOR

    mejor_cluster = comparacion_df.loc[mejor_idx, "Clusters"]
    peor_cluster = comparacion_df.loc[peor_idx, "Clusters"]

    mejor_tiempo = comparacion_df.loc[mejor_idx, "Tiempo_ms"]
    peor_tiempo = comparacion_df.loc[peor_idx, "Tiempo_ms"]

    mejor_inercia = comparacion_df.loc[mejor_idx, "Inercia"]
    peor_inercia = comparacion_df.loc[peor_idx, "Inercia"]

    # ANÁLISIS AUTOMÁTICO

    st.subheader("🧠 Análisis Automático")

    st.success(
        f"""
        🟢 MEJOR MODELO DETECTADO

        Número de clusters: {mejor_cluster}

        Tiempo de ejecución: {mejor_tiempo:.2f} ms

        Inercia: {mejor_inercia:.2f}

        Este modelo tiene el mejor equilibrio entre:

        ✔ velocidad computacional

        ✔ compactación de grupos

        ✔ estabilidad del agrupamiento

        ✔ eficiencia matemática

        Una menor inercia significa que los puntos están
        más cerca de sus centroides.
        """
    )

    st.error(
        f"""
        🔴 PEOR MODELO DETECTADO

        Número de clusters: {peor_cluster}

        Tiempo de ejecución: {peor_tiempo:.2f} ms

        Inercia: {peor_inercia:.2f}

        Este modelo presenta el peor rendimiento general,
        debido a:

        ✖ exceso de dispersión

        ✖ peor compactación

        ✖ menor eficiencia computacional

        ✖ agrupamientos menos óptimos
        """
    )

    st.warning("""
    🟠 CLUSTERS INTERMEDIOS

    Los modelos naranjas representan soluciones balanceadas.

    Dependiendo del análisis pueden ser útiles para:

    • segmentación más detallada

    • exploración de patrones

    • reducción de complejidad

    • interpretabilidad del modelo

    En Machine Learning no siempre el modelo más rápido
    es el mejor.

    Tampoco el de menor inercia absoluta.

    El objetivo es encontrar equilibrio entre:

    ✔ precisión

    ✔ estabilidad

    ✔ interpretación

    ✔ costo computacional
    """)

    # KMEANS


    st.header("🤖 Algoritmo K-Means")

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

  
    # ANIMACIÓN DE CONVERGENCIA


    st.header("🎬 Animación de Convergencia")

    pca_anim = PCA(n_components=2)

    X_pca = pca_anim.fit_transform(datos[numericas])

    fig_anim = go.Figure()

    colores = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'pink', 'lime', 'white']

    centroides = X_pca[np.random.choice(len(X_pca), k, replace=False)]

    frames = []

    for frame_num in range(iteraciones_animadas):

        distancias = np.linalg.norm(
            X_pca[:, np.newaxis] - centroides,
            axis=2
        )

        labels = np.argmin(distancias, axis=1)

        nuevos_centroides = np.array([
            X_pca[labels == i].mean(axis=0)
            for i in range(k)
        ])

        scatter_data = []

        for i in range(k):

            puntos = X_pca[labels == i]

            scatter_data.append(
                go.Scatter(
                    x=puntos[:,0],
                    y=puntos[:,1],
                    mode='markers+text',
                    text=datos['State'],
                    textposition='top center',
                    marker=dict(size=10, color=colores[i]),
                    name=f'Cluster {i}'
                )
            )

        scatter_data.append(
            go.Scatter(
                x=nuevos_centroides[:,0],
                y=nuevos_centroides[:,1],
                mode='markers',
                marker=dict(
                    size=25,
                    color='black',
                    symbol='star'
                ),
                name='Centroides'
            )
        )

        # líneas distancia

        for i in range(len(X_pca)):
            centroide = nuevos_centroides[labels[i]]

            scatter_data.append(
                go.Scatter(
                    x=[X_pca[i,0], centroide[0]],
                    y=[X_pca[i,1], centroide[1]],
                    mode='lines',
                    line=dict(color='gray', width=1),
                    showlegend=False
                )
            )

        frames.append(go.Frame(data=scatter_data, name=str(frame_num)))

        centroides = nuevos_centroides

    fig_anim.frames = frames

    fig_anim.add_trace(
        go.Scatter(x=[], y=[])
    )

    fig_anim.update_layout(
        title='Movimiento de centroides y convergencia K-Means',
        width=1200,
        height=800,
        updatemenus=[
            {
                'type': 'buttons',
                'buttons': [
                    {
                        'label': '▶ Iniciar',
                        'method': 'animate',
                        'args': [None]
                    }
                ]
            }
        ]
    )

    st.plotly_chart(fig_anim, use_container_width=True)

    # PCA


    st.header("🧠 PCA")

    pca = PCA(n_components=4)

    pca_scores = pca.fit_transform(datos[numericas])

    pca_df = pd.DataFrame(
        pca_scores,
        columns=['PC1', 'PC2', 'PC3', 'PC4']
    )

    pca_df['Cluster'] = km4_clusters.labels_.astype(str)
    pca_df['Etiqueta'] = datos['State']

    # PCA 2D
  

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

    st.success("Aplicación cargada correctamente")

else:

    st.warning("⚠ Suba el archivo data_USArrests.xlsx para iniciar")
