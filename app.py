

import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# =========================================================
# CONFIGURACIÓN STREAMLIT
# =========================================================

st.set_page_config(
    page_title="K-Means Interactivo 3D",
    layout="wide"
)

st.title("🎯 Simulación Profesional K-Means 3D")

st.markdown(
    """
    Esta aplicación muestra paso a paso cómo funciona el algoritmo K-Means.
    """
)

# =========================================================
# CARGAR DATOS
# =========================================================

archivo = st.file_uploader(
    "Suba el archivo data_USArrests.xlsx",
    type=["xlsx"]
)

if archivo is not None:

    datos = pd.read_excel(
        archivo,
        header=0,
        usecols="A:E"
    )

    st.subheader("Datos originales")
    st.dataframe(datos.head())

    # =====================================================
    # LIMPIEZA
    # =====================================================

    datos = datos.dropna()

    # =====================================================
    # ESCALADO
    # =====================================================

    scaler = StandardScaler()

    numericas = datos.select_dtypes(
        include=['float64', 'int64']
    ).columns

    datos[numericas] = scaler.fit_transform(
        datos[numericas]
    )

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.header("Configuración")

    k = st.sidebar.slider(
        "Número de Clusters",
        min_value=2,
        max_value=8,
        value=4
    )

    iteraciones_animadas = st.sidebar.slider(
        "Máximo Iteraciones",
        min_value=2,
        max_value=20,
        value=10
    )

    # =====================================================
    # PCA
    # =====================================================

    pca = PCA(n_components=3)

    X3D = pca.fit_transform(
        datos[numericas]
    )

    pca_df = pd.DataFrame(
        X3D,
        columns=['PC1', 'PC2', 'PC3']
    )

    # =====================================================
    # SIMULACIÓN K-MEANS
    # =====================================================

    st.subheader("🎬 Simulación REAL de K-Means")

    st.markdown(
        """
        ### Etapas:

        1. Todos los datos comienzan iguales.
        2. Se crean centroides aleatorios.
        3. Se calculan distancias.
        4. Los puntos toman el color del centroide más cercano.
        5. Los centroides se mueven al promedio.
        6. El proceso continúa hasta converger.
        """
    )

    colores_k = [
        'red',
        'green',
        'blue',
        'yellow',
        'purple',
        'orange',
        'cyan',
        'magenta'
    ]

    np.random.seed(42)

    centroides = X3D[
        np.random.choice(
            len(X3D),
            k,
            replace=False
        )
    ]

    frames = []

    # =====================================================
    # FRAME 1
    # =====================================================

    frame_datos = go.Frame(

        data=[

            go.Scatter3d(
                x=X3D[:,0],
                y=X3D[:,1],
                z=X3D[:,2],

                mode='markers+text',

                text=datos['State'],
                textposition='top center',

                marker=dict(
                    size=5,
                    color='lightblue'
                ),

                name='Datos Iniciales'
            )
        ],

        name='1. Datos Iniciales'
    )

    frames.append(frame_datos)

    # =====================================================
    # FRAME 2
    # =====================================================

    frame_centroides = go.Frame(

        data=[

            go.Scatter3d(
                x=X3D[:,0],
                y=X3D[:,1],
                z=X3D[:,2],

                mode='markers',

                marker=dict(
                    size=5,
                    color='lightblue'
                ),

                name='Datos'
            ),

            go.Scatter3d(
                x=centroides[:,0],
                y=centroides[:,1],
                z=centroides[:,2],

                mode='markers',

                marker=dict(
                    size=20,
                    color='white',
                    symbol='diamond'
                ),

                name='Centroides Aleatorios'
            )
        ],

        name='2. Centroides Aleatorios'
    )

    frames.append(frame_centroides)

    # =====================================================
    # ITERACIONES
    # =====================================================

    for iteracion in range(iteraciones_animadas):

        distancias = np.linalg.norm(
            X3D[:, np.newaxis] - centroides,
            axis=2
        )

        labels = np.argmin(distancias, axis=1)

        # =================================================
        # FRAME DISTANCIAS
        # =================================================

        traces_distancias = []

        for cluster_id in range(k):

            puntos = X3D[
                labels == cluster_id
            ]

            etiquetas = datos['State'][
                labels == cluster_id
            ]

            traces_distancias.append(

                go.Scatter3d(
                    x=puntos[:,0],
                    y=puntos[:,1],
                    z=puntos[:,2],

                    mode='markers+text',

                    text=etiquetas,
                    textposition='top center',

                    marker=dict(
                        size=5,
                        color=colores_k[cluster_id]
                    ),

                    name=f'Cluster {cluster_id}'
                )
            )

        # =================================================
        # LÍNEAS DISTANCIA
        # =================================================

        for punto_id in range(len(X3D)):

            for centroide_id in range(k):

                color_linea = 'rgba(255,255,255,0.05)'

                if labels[punto_id] == centroide_id:
                    color_linea = colores_k[centroide_id]

                traces_distancias.append(

                    go.Scatter3d(

                        x=[
                            X3D[punto_id,0],
                            centroides[centroide_id,0]
                        ],

                        y=[
                            X3D[punto_id,1],
                            centroides[centroide_id,1]
                        ],

                        z=[
                            X3D[punto_id,2],
                            centroides[centroide_id,2]
                        ],

                        mode='lines',

                        line=dict(
                            color=color_linea,
                            width=2
                        ),

                        showlegend=False
                    )
                )

        traces_distancias.append(

            go.Scatter3d(
                x=centroides[:,0],
                y=centroides[:,1],
                z=centroides[:,2],

                mode='markers',

                marker=dict(
                    size=20,
                    color='white',
                    symbol='diamond'
                ),

                name='Centroides'
            )
        )

        frames.append(
            go.Frame(
                data=traces_distancias,
                name=f'3. Distancias Iteración {iteracion+1}'
            )
        )

        # =================================================
        # NUEVOS CENTROIDES
        # =================================================

        nuevos_centroides = []

        for cluster_id in range(k):

            puntos_cluster = X3D[
                labels == cluster_id
            ]

            if len(puntos_cluster) > 0:
                promedio = puntos_cluster.mean(axis=0)
            else:
                promedio = centroides[cluster_id]

            nuevos_centroides.append(promedio)

        nuevos_centroides = np.array(
            nuevos_centroides
        )

        # =================================================
        # FRAME MOVIMIENTO
        # =================================================

        traces_movimiento = []

        for cluster_id in range(k):

            puntos = X3D[
                labels == cluster_id
            ]

            etiquetas = datos['State'][
                labels == cluster_id
            ]

            traces_movimiento.append(

                go.Scatter3d(
                    x=puntos[:,0],
                    y=puntos[:,1],
                    z=puntos[:,2],

                    mode='markers+text',

                    text=etiquetas,
                    textposition='top center',

                    marker=dict(
                        size=5,
                        color=colores_k[cluster_id]
                    ),

                    name=f'Cluster {cluster_id}'
                )
            )

        # movimiento centroides

        for centroide_id in range(k):

            traces_movimiento.append(

                go.Scatter3d(
                    x=[
                        centroides[centroide_id,0],
                        nuevos_centroides[centroide_id,0]
                    ],

                    y=[
                        centroides[centroide_id,1],
                        nuevos_centroides[centroide_id,1]
                    ],

                    z=[
                        centroides[centroide_id,2],
                        nuevos_centroides[centroide_id,2]
                    ],

                    mode='lines',

                    line=dict(
                        color='white',
                        width=10
                    ),

                    showlegend=False
                )
            )

        traces_movimiento.append(

            go.Scatter3d(
                x=centroides[:,0],
                y=centroides[:,1],
                z=centroides[:,2],

                mode='markers',

                marker=dict(
                    size=18,
                    color='white',
                    symbol='square'
                ),

                name='Centroide Viejo'
            )
        )

        traces_movimiento.append(

            go.Scatter3d(
                x=nuevos_centroides[:,0],
                y=nuevos_centroides[:,1],
                z=nuevos_centroides[:,2],

                mode='markers',

                marker=dict(
                    size=24,
                    color='yellow',
                    symbol='diamond'
                ),

                name='Nuevo Centroide'
            )
        )

        frames.append(
            go.Frame(
                data=traces_movimiento,
                name=f'4. Movimiento Iteración {iteracion+1}'
            )
        )

        movimiento = np.linalg.norm(
            nuevos_centroides - centroides
        )

        centroides = nuevos_centroides

        if movimiento < 0.0001:

            frame_final = go.Frame(
                data=traces_movimiento,
                name='5. Convergencia Final'
            )

            frames.append(frame_final)

            break

    # =====================================================
    # FIGURA PRINCIPAL
    # =====================================================

    fig_kmeans = go.Figure(
        data=frames[0].data,
        frames=frames
    )

    botones = []

    for frame in frames:

        botones.append(
            dict(
                label=frame.name,
                method='animate',
                args=[
                    [frame.name],
                    {
                        'mode': 'immediate',
                        'frame': {
                            'duration': 1800,
                            'redraw': True
                        },
                        'transition': {
                            'duration': 700
                        }
                    }
                ]
            )
        )

    fig_kmeans.update_layout(

        title='Simulación REAL del algoritmo K-Means',

        width=1700,
        height=950,

        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',

        font=dict(color='white'),

        scene=dict(
            bgcolor='black',
            xaxis_title='PC1',
            yaxis_title='PC2',
            zaxis_title='PC3'
        ),

        updatemenus=[

            dict(
                type='buttons',
                direction='right',
                x=0.02,
                y=1.15,

                buttons=[

                    dict(
                        label='▶ Reproducir K-Means',
                        method='animate',
                        args=[
                            None,
                            {
                                'frame': {
                                    'duration': 1800,
                                    'redraw': True
                                },
                                'transition': {
                                    'duration': 700
                                },
                                'fromcurrent': True
                            }
                        ]
                    ),

                    dict(
                        label='⏸ Pausa',
                        method='animate',
                        args=[
                            [None],
                            {
                                'mode': 'immediate',
                                'frame': {
                                    'duration': 0,
                                    'redraw': False
                                }
                            }
                        ]
                    )
                ]
            ),

            dict(
                type='dropdown',
                direction='down',
                buttons=botones,
                x=0.40,
                y=1.15,
                showactive=True
            )
        ]
    )

    st.plotly_chart(
        fig_kmeans,
        use_container_width=True
    )

else:

    st.warning(
        "Suba el archivo Excel para comenzar."
    )
