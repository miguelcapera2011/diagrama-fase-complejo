# =========================================================
# APP STREAMLIT — KMEANS 3D REAL
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# =========================================================
# CONFIGURACION
# =========================================================

st.set_page_config(
    page_title="K-Means 3D Real",
    layout="wide"
)

st.title("🎯 Simulación REAL K-Means 3D")

st.markdown("""
### Proceso mostrado

1. Datos inicialmente del mismo color
2. Aparición de centroides aleatorios
3. Cálculo de distancias
4. Líneas entre puntos y centroides
5. Cambio de color por centroide más cercano
6. Movimiento de centroides
7. Convergencia final
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
    # CARGAR DATOS
    # =====================================================

    datos = pd.read_excel(
        archivo,
        header=0,
        usecols="A:E"
    )

    # =====================================================
    # LIMPIEZA
    # =====================================================

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
        "Máximo iteraciones",
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
    # CENTROIDES ALEATORIOS
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
    # FRAME 0
    # SOLO DATOS
    # =====================================================

    frame0 = go.Frame(

        data=[

            go.Scatter3d(

                x=X[:,0],
                y=X[:,1],
                z=X[:,2],

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

        name='Datos Iniciales'
    )

    frames.append(frame0)

    # =====================================================
    # FRAME 1
    # CENTROIDES
    # =====================================================

    frame1 = go.Frame(

        data=[

            go.Scatter3d(

                x=X[:,0],
                y=X[:,1],
                z=X[:,2],

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
                    size=18,
                    color='white',
                    symbol='diamond'
                ),

                name='Centroides'
            )

        ],

        name='Centroides Iniciales'
    )

    frames.append(frame1)

    # =====================================================
    # ITERACIONES KMEANS
    # =====================================================

    for iteracion in range(max_iter):

        # =================================================
        # DISTANCIAS
        # =================================================

        distancias = np.linalg.norm(
            X[:, np.newaxis] - centroides,
            axis=2
        )

        # =================================================
        # LABELS
        # =================================================

        labels = np.argmin(
            distancias,
            axis=1
        )

        # =================================================
        # TRAZAS
        # =================================================

        traces = []

        # =================================================
        # PUNTOS COLOREADOS
        # =================================================

        for cluster_id in range(k):

            puntos = X[
                labels == cluster_id
            ]

            etiquetas = datos['State'][
                labels == cluster_id
            ]

            if len(puntos) > 0:

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

        # =================================================
        # LINEAS DISTANCIA
        # =================================================

        for punto_id in range(len(X)):

            centroide_cercano = labels[punto_id]

            traces.append(

                go.Scatter3d(

                    x=[
                        X[punto_id,0],
                        centroides[centroide_cercano,0]
                    ],

                    y=[
                        X[punto_id,1],
                        centroides[centroide_cercano,1]
                    ],

                    z=[
                        X[punto_id,2],
                        centroides[centroide_cercano,2]
                    ],

                    mode='lines',

                    line=dict(
                        color=colores[centroide_cercano],
                        width=3
                    ),

                    showlegend=False
                )
            )

        # =================================================
        # CENTROIDES ACTUALES
        # =================================================

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

        # =================================================
        # AGREGAR FRAME DISTANCIAS
        # =================================================

        frames.append(

            go.Frame(

                data=traces,

                name=f'Distancias {iteracion+1}'
            )
        )

        # =================================================
        # NUEVOS CENTROIDES
        # =================================================

        nuevos_centroides = []

        for cluster_id in range(k):

            puntos_cluster = X[
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
        # TRAZAS MOVIMIENTO
        # =================================================

        traces_mov = []

        # =================================================
        # DATOS
        # =================================================

        for cluster_id in range(k):

            puntos = X[
                labels == cluster_id
            ]

            etiquetas = datos['State'][
                labels == cluster_id
            ]

            if len(puntos) > 0:

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

        # =================================================
        # FLECHAS MOVIMIENTO
        # =================================================

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

        # =================================================
        # CENTROIDES VIEJOS
        # =================================================

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

        # =================================================
        # NUEVOS CENTROIDES
        # =================================================

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

        # =================================================
        # AGREGAR FRAME MOVIMIENTO
        # =================================================

        frames.append(

            go.Frame(

                data=traces_mov,

                name=f'Movimiento {iteracion+1}'
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

        title='Simulación REAL K-Means',

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

                x=0.05,
                y=1.15,

                buttons=[

                    dict(

                        label='▶ Reproducir',

                        method='animate',

                        args=[

                            None,

                            dict(

                                frame=dict(
                                    duration=2000,
                                    redraw=True
                                ),

                                transition=dict(
                                    duration=1000
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
        "Suba el archivo Excel para iniciar."
    )
