# =========================================================
# APP STREAMLIT — KMEANS 3D REAL PASO A PASO
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# =========================================================
# CONFIG STREAMLIT
# =========================================================

st.set_page_config(
    page_title="K-Means 3D Real",
    layout="wide"
)

st.title("🎯 Simulación REAL del algoritmo K-Means")

st.markdown("""
Esta aplicación muestra visualmente:

- Datos inicialmente del mismo color
- Aparición de centroides aleatorios
- Cálculo de distancias
- Líneas entre puntos y centroides
- Agrupamiento automático
- Movimiento de centroides
- Convergencia del algoritmo
""")

# =========================================================
# CARGAR EXCEL
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

    st.subheader("Vista previa")

    st.dataframe(datos.head())

    # =====================================================
    # LIMPIEZA
    # =====================================================

    datos = datos.dropna()

    # =====================================================
    # VARIABLES NUMÉRICAS
    # =====================================================

    numericas = datos.select_dtypes(
        include=['float64', 'int64']
    ).columns

    # =====================================================
    # ESTANDARIZAR
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
        "Número de Clusters",
        2,
        8,
        4
    )

    max_iter = st.sidebar.slider(
        "Iteraciones máximas",
        2,
        20,
        10
    )

    # =====================================================
    # PCA 3D
    # =====================================================

    pca = PCA(n_components=3)

    X3D = pca.fit_transform(
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
    # CENTROIDES ALEATORIOS
    # =====================================================

    np.random.seed(42)

    centroides = X3D[
        np.random.choice(
            len(X3D),
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
    # DATOS SOLOS
    # =====================================================

    frames.append(

        go.Frame(

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

                    name='Datos'
                )

            ],

            name='1. Datos Iniciales'
        )
    )

    # =====================================================
    # FRAME 2
    # CENTROIDES
    # =====================================================

    frames.append(

        go.Frame(

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

                    name='Centroides'
                )

            ],

            name='2. Centroides Aleatorios'
        )
    )

    # =====================================================
    # ITERACIONES KMEANS
    # =====================================================

    for iteracion in range(max_iter):

        # =================================================
        # DISTANCIAS
        # =================================================

        distancias = np.linalg.norm(
            X3D[:, np.newaxis] - centroides,
            axis=2
        )

        # =================================================
        # CLUSTER MÁS CERCANO
        # =================================================

        labels = np.argmin(
            distancias,
            axis=1
        )

        # =================================================
        # FRAME DISTANCIAS
        # =================================================

        traces = []

        # =============================================
        # DATOS COLOREADOS
        # =============================================

        for cluster_id in range(k):

            puntos = X3D[
                labels == cluster_id
            ]

            etiquetas = datos['State'][
                labels == cluster_id
            ]

            traces.append(

                go.Scatter3d(

                    x=puntos[:,0],
                    y=puntos[:,1],
                    z=puntos[:,2],

                    mode='markers+text',

                    text=etiquetas,
                    textposition='top center',

                    marker=dict(
                        size=5,
                        color=colores[cluster_id]
                    ),

                    name=f'Cluster {cluster_id}'
                )
            )

        # =============================================
        # LÍNEAS DISTANCIA
        # =============================================

        for punto_id in range(len(X3D)):

            for centroide_id in range(k):

                color_linea = 'rgba(255,255,255,0.05)'

                # centroide más cercano
                if labels[punto_id] == centroide_id:
                    color_linea = colores[centroide_id]

                traces.append(

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

        # =============================================
        # CENTROIDES ACTUALES
        # =============================================

        traces.append(

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

                data=traces,

                name=f'3. Distancias {iteracion+1}'
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

            # promedio del cluster

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

        traces_mov = []

        # =============================================
        # DATOS
        # =============================================

        for cluster_id in range(k):

            puntos = X3D[
                labels == cluster_id
            ]

            etiquetas = datos['State'][
                labels == cluster_id
            ]

            traces_mov.append(

                go.Scatter3d(

                    x=puntos[:,0],
                    y=puntos[:,1],
                    z=puntos[:,2],

                    mode='markers+text',

                    text=etiquetas,
                    textposition='top center',

                    marker=dict(
                        size=5,
                        color=colores[cluster_id]
                    ),

                    name=f'Cluster {cluster_id}'
                )
            )

        # =============================================
        # MOVIMIENTO CENTROIDES
        # =============================================

        for centroide_id in range(k):

            traces_mov.append(

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

        # centroides viejos

        traces_mov.append(

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

        # nuevos centroides

        traces_mov.append(

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

                data=traces_mov,

                name=f'4. Movimiento {iteracion+1}'
            )
        )

        # =================================================
        # CONVERGENCIA
        # =================================================

        movimiento = np.linalg.norm(
            nuevos_centroides - centroides
        )

        centroides = nuevos_centroides

        if movimiento < 0.0001:

            frames.append(

                go.Frame(

                    data=traces_mov,

                    name='5. Convergencia'
                )
            )

            break

    # =====================================================
    # FIGURA
    # =====================================================

    fig = go.Figure(

        data=frames[0].data,

        frames=frames
    )

    # =====================================================
    # BOTONES
    # =====================================================

    fig.update_layout(

        title='Simulación REAL K-Means 3D',

        width=1700,
        height=950,

        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',

        font=dict(
            color='white'
        ),

        scene=dict(

            bgcolor='black',

            xaxis_title='PC1',
            yaxis_title='PC2',
            zaxis_title='PC3'
        ),

        updatemenus=[

            dict(

                type='buttons',

                direction='left',

                x=0.02,
                y=1.15,

                buttons=[

                    dict(

                        label='▶ Reproducir',

                        method='animate',

                        args=[

                            None,

                            dict(

                                frame=dict(
                                    duration=1800,
                                    redraw=True
                                ),

                                transition=dict(
                                    duration=700
                                ),

                                fromcurrent=True
                            )
                        ]
                    ),

                    dict(

                        label='⏸ Pausa',

                        method='animate',

                        args=[

                            [None],

                            dict(

                                frame=dict(
                                    duration=0,
                                    redraw=False
                                ),

                                mode='immediate'
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # =====================================================
    # MOSTRAR
    # =====================================================

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "Suba el archivo Excel para comenzar."
    )
