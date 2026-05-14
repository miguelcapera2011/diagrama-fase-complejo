# App Profesional de Clustering K-Means con Streamlit

## Archivo: `app.py`

```python
# =========================================================
# APP PROFESIONAL K-MEANS + PCA + VISUALIZACIONES DINÁMICAS
# Dataset: USArrests
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
    page_icon="📊",
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

.css-1d391kg {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("📊 App Profesional de Clustering K-Means")

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

    st.header("📁 Dataset")
    st.dataframe(datos)

    # =====================================================
    # INFORMACIÓN GENERAL
    # =====================================================

    st.header("📌 Información del Dataset")

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

    st.header("📈 Histogramas")

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

    # =====================================================
    # ESTANDARIZACIÓN
    # =====================================================

    st.header("⚖ Estandarización")

    scaler = StandardScaler()

    numericas = datos.select_dtypes(include=['float64', 'int64']).columns

    datos[numericas] = scaler.fit_transform(datos[numericas])

    st.write(datos.head())

    # =====================================================
    # MATRICES DE DISTANCIA
    # =====================================================

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

    st.plotly_chart(fig_manhattan, use_container_width=True)

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
    # KMEANS
    # =====================================================

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

    # =====================================================
    # ANIMACIÓN DE CONVERGENCIA
    # =====================================================

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

    # =====================================================
    # PCA
    # =====================================================

    st.header("🧠 PCA")

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
    # PCA 3D + ANIMACIÓN COMPLETA K-MEANS
    # =====================================================

    st.subheader("🎥 Simulación completa K-Means en 3D")

    st.markdown("""
    Esta simulación muestra paso a paso:

    1. Inicialización de centroides
    2. Cálculo de distancias
    3. Asignación de clusters
    4. Movimiento de centroides
    5. Repetición iterativa
    6. Convergencia final
    """)

    X3D = pca_df[['PC1', 'PC2', 'PC3']].values

    np.random.seed(42)

    centroides = X3D[np.random.choice(len(X3D), k, replace=False)]

    frames_3d = []

    colores_anim = [
        'red', 'green', 'blue', 'yellow', 'purple',
        'orange', 'cyan', 'magenta', 'lime', 'white'
    ]

    for iteracion in range(iteraciones_animadas):

        # ===============================================
        # DISTANCIAS
        # ===============================================

        distancias = np.linalg.norm(
            X3D[:, np.newaxis] - centroides,
            axis=2
        )

        labels_iter = np.argmin(distancias, axis=1)

        # ===============================================
        # NUEVOS CENTROIDES
        # ===============================================

        nuevos_centroides = []

        for i in range(k):

            puntos_cluster = X3D[labels_iter == i]

            if len(puntos_cluster) > 0:
                nuevo = puntos_cluster.mean(axis=0)
            else:
                nuevo = centroides[i]

            nuevos_centroides.append(nuevo)

        nuevos_centroides = np.array(nuevos_centroides)

        data_frame = []

        # ===============================================
        # PUNTOS POR CLUSTER
        # ===============================================

        for cluster_id in range(k):

            puntos = X3D[labels_iter == cluster_id]

            etiquetas = datos['State'][labels_iter == cluster_id]

            data_frame.append(
                go.Scatter3d(
                    x=puntos[:, 0],
                    y=puntos[:, 1],
                    z=puntos[:, 2],
                    mode='markers+text',
                    text=etiquetas,
                    textposition='top center',
                    marker=dict(
                        size=5,
                        color=colores_anim[cluster_id],
                        opacity=0.85
                    ),
                    name=f'Cluster {cluster_id}'
                )
            )

        # ===============================================
        # LÍNEAS DISTANCIA
        # ===============================================

        for punto_id in range(len(X3D)):

            cluster_actual = labels_iter[punto_id]

            centroide_actual = centroides[cluster_actual]

            data_frame.append(
                go.Scatter3d(
                    x=[X3D[punto_id, 0], centroide_actual[0]],
                    y=[X3D[punto_id, 1], centroide_actual[1]],
                    z=[X3D[punto_id, 2], centroide_actual[2]],
                    mode='lines',
                    line=dict(
                        color='gray',
                        width=2
                    ),
                    showlegend=False
                )
            )

        # ===============================================
        # CENTROIDES ACTUALES
        # ===============================================

        data_frame.append(
            go.Scatter3d(
                x=centroides[:, 0],
                y=centroides[:, 1],
                z=centroides[:, 2],
                mode='markers',
                marker=dict(
                    size=15,
                    color='black',
                    symbol='diamond'
                ),
                name='Centroides Actuales'
            )
        )

        # ===============================================
        # MOVIMIENTO CENTROIDES
        # ===============================================

        for centroide_id in range(k):

            data_frame.append(
                go.Scatter3d(
                    x=[centroides[centroide_id, 0], nuevos_centroides[centroide_id, 0]],
                    y=[centroides[centroide_id, 1], nuevos_centroides[centroide_id, 1]],
                    z=[centroides[centroide_id, 2], nuevos_centroides[centroide_id, 2]],
                    mode='lines',
                    line=dict(
                        color='white',
                        width=8
                    ),
                    showlegend=False
                )
            )

        # ===============================================
        # NUEVOS CENTROIDES
        # ===============================================

        data_frame.append(
            go.Scatter3d(
                x=nuevos_centroides[:, 0],
                y=nuevos_centroides[:, 1],
                z=nuevos_centroides[:, 2],
                mode='markers',
                marker=dict(
                    size=18,
                    color='yellow',
                    symbol='diamond-open'
                ),
                name='Nuevos Centroides'
            )
        )

        frames_3d.append(
            go.Frame(
                data=data_frame,
                name=f'Iteración {iteracion+1}'
            )
        )

        # ===============================================
        # CONVERGENCIA
        # ===============================================

        movimiento = np.linalg.norm(nuevos_centroides - centroides)

        centroides = nuevos_centroides

        if movimiento < 0.001:
            break

    # =====================================================
    # FIGURA PRINCIPAL
    # =====================================================

    fig_3d_anim = go.Figure(
        data=frames_3d[0].data,
        frames=frames_3d
    )

    botones = []

    for i in range(len(frames_3d)):

        botones.append(
            dict(
                label=f'Iteración {i+1}',
                method='animate',
                args=[
                    [frames_3d[i].name],
                    {
                        'mode': 'immediate',
                        'frame': {'duration': 1200, 'redraw': True},
                        'transition': {'duration': 500}
                    }
                ]
            )
        )

    fig_3d_anim.update_layout(
        title='Proceso Completo de Convergencia K-Means 3D',
        width=1600,
        height=950,
        scene=dict(
            xaxis_title='PC1',
            yaxis_title='PC2',
            zaxis_title='PC3',
            bgcolor='black'
        ),
        paper_bgcolor='#0e1117',
        font=dict(color='white'),
        updatemenus=[
            dict(
                type='buttons',
                direction='right',
                buttons=[
                    dict(
                        label='▶ Reproducir Todo',
                        method='animate',
                        args=[
                            None,
                            {
                                'frame': {'duration': 1200, 'redraw': True},
                                'transition': {'duration': 500},
                                'fromcurrent': True
                            }
                        ]
                    ),
                    dict(
                        label='⏸ Pausar',
                        method='animate',
                        args=[
                            [None],
                            {
                                'frame': {'duration': 0, 'redraw': False},
                                'mode': 'immediate'
                            }
                        ]
                    )
                ],
                pad={'r': 10, 't': 10},
                showactive=True,
                x=0.05,
                xanchor='left',
                y=1.15,
                yanchor='top'
            ),
            dict(
                type='dropdown',
                direction='down',
                buttons=botones,
                x=0.35,
                y=1.15,
                showactive=True
            )
        ]
    )

    st.plotly_chart(fig_3d_anim, use_container_width=True)

    # =====================================================
    # BOXPLOT
    # =====================================================

    st.header("📦 Boxplot Interactivo")

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
    # TABLA DE CLUSTERS
    # =====================================================

    st.header("📋 Estados por Cluster")

    grupos = pd.DataFrame()

    grupos['State'] = datos['State']
    grupos['Cluster'] = km4_clusters.labels_

    st.dataframe(
        grupos.sort_values(by='Cluster'),
        use_container_width=True
    )

    # =====================================================
    # CANTIDAD POR CLUSTER
    # =====================================================

    st.header("📊 Cantidad de individuos por Cluster")

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
    # VISUALIZACIÓN MURDER VS URBANPOP
    # =====================================================

    st.header("🎯 Murder vs UrbanPop")

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
    # VISUALIZACIÓN RAPE VS ASSAULT
    # =====================================================

    st.header("🎯 Rape vs Assault")

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

    st.header("📘 Explicación Matemática")

    st.markdown("""
    ## ¿Cómo funciona K-Means?

    1. Se eligen centroides aleatorios.

    2. Cada punto calcula su distancia al centroide más cercano.

    3. Los puntos se asignan al cluster más cercano.

    4. Los centroides se recalculan usando el promedio de los puntos.

    5. El proceso se repite hasta converger.

    ## Distancia Euclidiana

    La distancia usada normalmente es:

    d(x,y)=√((x1-y1)^2+(x2-y2)^2+...)

    ## Inercia

    La inercia mide qué tan compactos son los clusters.

    Menor inercia = mejores agrupaciones.
    """)

    st.success("✅ Aplicación cargada correctamente")

else:

    st.warning("⚠ Suba el archivo data_USArrests.xlsx para iniciar")

```

---

# Librerías necesarias

```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn scipy plotly openpyxl
```

---

# Ejecutar la app

```bash
streamlit run app.py
```

---

# Estructura recomendada

```bash
proyecto/
│
├── app.py
├── data_USArrests.xlsx
└── requirements.txt
```

---

# Archivo requirements.txt

```txt
streamlit
pandas
numpy
matplotlib
seaborn
scikit-learn
scipy
plotly
openpyxl
```
