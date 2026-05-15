import streamlit as st
import pandas as pd
import numpy as np
@@ -15,9 +14,9 @@
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial.distance import pdist, squareform


# =========================================================
# CONFIGURACIÓN GENERAL

# =========================================================

st.set_page_config(
    page_title="K-Means Profesional",
@@ -467,6 +466,16 @@
    - El proceso continúa hasta converger.
    """)

    # =====================================================
    # SIMULACIÓN PEDAGÓGICA REAL K-MEANS
    # =====================================================

    st.subheader("🎬 Simulación paso a paso REAL de K-Means")

    st.info(
        "La animación muestra exactamente cómo aprende K-Means desde cero."
    )

    # =====================================================
    # DATOS PCA 3D
    # =====================================================
@@ -475,13 +484,13 @@

    np.random.seed(42)

    colores_kmeans = [
    colores_k = [
        'red', 'green', 'blue', 'yellow',
        'purple', 'orange', 'cyan', 'magenta'
    ]

    # =====================================================
    # CENTROIDES INICIALES ALEATORIOS
    # CENTROIDES ALEATORIOS
    # =====================================================

    centroides = X3D[
@@ -491,80 +500,69 @@
    frames = []

    # =====================================================
    # FRAME 0
    # TODOS LOS DATOS IGUAL COLOR
    # FRAME 1
    # SOLO DATOS
    # =====================================================

    frame0 = []

    frame0.append(
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
                name='Datos'
            )
        ],
        name='1. Datos Iniciales'
    )

    frames.append(
        go.Frame(
            data=frame0,
            name='Datos Iniciales'
        )
    )
    frames.append(frame_datos)

    # =====================================================
    # FRAME 1
    # APARECEN LOS CENTROIDES
    # FRAME 2
    # APARECEN CENTROIDES
    # =====================================================

    frame1 = []

    frame1.append(
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
        )
    )

    frame1.append(
        go.Scatter3d(
            x=centroides[:,0],
            y=centroides[:,1],
            z=centroides[:,2],
            mode='markers',
            marker=dict(
                size=20,
                color='white',
                symbol='diamond'
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
            name='Centroides Iniciales'
        )
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

    frames.append(
        go.Frame(
            data=frame1,
            name='Centroides Iniciales'
        )
    )
    frames.append(frame_centroides)

    # =====================================================
    # ITERACIONES KMEANS
    # ITERACIONES
    # =====================================================

    for iteracion in range(iteraciones_animadas):
@@ -584,17 +582,16 @@
        # FRAME DISTANCIAS
        # ================================================

        frame_distancias = []
        traces_distancias = []

        # puntos coloreados según centroide más cercano
        # TODOS LOS DATOS COLOREADOS

        for cluster_id in range(k):

            puntos = X3D[labels == cluster_id]

            etiquetas = datos['State'][labels == cluster_id]

            frame_distancias.append(
            traces_distancias.append(
                go.Scatter3d(
                    x=puntos[:,0],
                    y=puntos[:,1],
@@ -604,24 +601,25 @@
                    textposition='top center',
                    marker=dict(
                        size=5,
                        color=colores_kmeans[cluster_id]
                        color=colores_k[cluster_id]
                    ),
                    name=f'Cluster {cluster_id}'
                )
            )

        # líneas distancia
        # LÍNEAS A TODOS LOS CENTROIDES

        for punto_id in range(len(X3D)):

            for centroide_id in range(k):

                color_linea = 'rgba(255,255,255,0.10)'
                color_linea = 'rgba(255,255,255,0.08)'

                if centroide_id == labels[punto_id]:
                    color_linea = colores_kmeans[centroide_id]
                # línea más cercana resaltada
                if labels[punto_id] == centroide_id:
                    color_linea = colores_k[centroide_id]

                frame_distancias.append(
                traces_distancias.append(
                    go.Scatter3d(
                        x=[X3D[punto_id,0], centroides[centroide_id,0]],
                        y=[X3D[punto_id,1], centroides[centroide_id,1]],
@@ -635,16 +633,16 @@
                    )
                )

        # centroides actuales
        # CENTROIDES ACTUALES

        frame_distancias.append(
        traces_distancias.append(
            go.Scatter3d(
                x=centroides[:,0],
                y=centroides[:,1],
                z=centroides[:,2],
                mode='markers',
                marker=dict(
                    size=18,
                    size=20,
                    color='white',
                    symbol='diamond'
                ),
@@ -654,8 +652,8 @@

        frames.append(
            go.Frame(
                data=frame_distancias,
                name=f'Distancias Iteración {iteracion+1}'
                data=traces_distancias,
                name=f'3. Distancias Iteración {iteracion+1}'
            )
        )

@@ -670,27 +668,28 @@
            puntos_cluster = X3D[labels == cluster_id]

            if len(puntos_cluster) > 0:
                nuevo_centroide = puntos_cluster.mean(axis=0)
                promedio = puntos_cluster.mean(axis=0)
            else:
                nuevo_centroide = centroides[cluster_id]
                promedio = centroides[cluster_id]

            nuevos_centroides.append(nuevo_centroide)
            nuevos_centroides.append(promedio)

        nuevos_centroides = np.array(nuevos_centroides)

        # ================================================
        # FRAME MOVIMIENTO
        # FRAME MOVIMIENTO CENTROIDES
        # ================================================

        frame_movimiento = []
        traces_movimiento = []

        # DATOS YA COLOREADOS

        for cluster_id in range(k):

            puntos = X3D[labels == cluster_id]

            etiquetas = datos['State'][labels == cluster_id]

            frame_movimiento.append(
            traces_movimiento.append(
                go.Scatter3d(
                    x=puntos[:,0],
                    y=puntos[:,1],
@@ -700,21 +699,30 @@
                    textposition='top center',
                    marker=dict(
                        size=5,
                        color=colores_kmeans[cluster_id]
                        color=colores_k[cluster_id]
                    ),
                    name=f'Cluster {cluster_id}'
                )
            )

        # líneas movimiento centroides
        # MOVIMIENTO DE CENTROIDES

        for centroide_id in range(k):

            frame_movimiento.append(
            traces_movimiento.append(
                go.Scatter3d(
                    x=[centroides[centroide_id,0], nuevos_centroides[centroide_id,0]],
                    y=[centroides[centroide_id,1], nuevos_centroides[centroide_id,1]],
                    z=[centroides[centroide_id,2], nuevos_centroides[centroide_id,2]],
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
@@ -724,74 +732,82 @@
                )
            )

        # centroides antiguos
        # CENTROIDES ANTIGUOS

        frame_movimiento.append(
        traces_movimiento.append(
            go.Scatter3d(
                x=centroides[:,0],
                y=centroides[:,1],
                z=centroides[:,2],
                mode='markers',
                marker=dict(
                    size=16,
                    size=18,
                    color='white',
                    symbol='diamond'
                ),
                name='Centroide Anterior'
                name='Centroide Viejo'
            )
        )

        # centroides nuevos
        # CENTROIDES NUEVOS

        frame_movimiento.append(
        traces_movimiento.append(
            go.Scatter3d(
                x=nuevos_centroides[:,0],
                y=nuevos_centroides[:,1],
                z=nuevos_centroides[:,2],
                mode='markers',
                marker=dict(
                    size=20,
                    size=24,
                    color='yellow',
                    symbol='diamond-open'
                    symbol='star'
                ),
                name='Nuevo Centroide'
            )
        )

        frames.append(
            go.Frame(
                data=frame_movimiento,
                name=f'Movimiento Iteración {iteracion+1}'
                data=traces_movimiento,
                name=f'4. Movimiento Iteración {iteracion+1}'
            )
        )

        # ================================================
        # CONVERGENCIA
        # ================================================
        # ACTUALIZAR

        movimiento_total = np.linalg.norm(
        movimiento = np.linalg.norm(
            nuevos_centroides - centroides
        )

        centroides = nuevos_centroides

        if movimiento_total < 0.0001:
        # CONVERGENCIA

        if movimiento < 0.0001:

            frame_final = go.Frame(
                data=traces_movimiento,
                name='5. Convergencia Final'
            )

            frames.append(frame_final)

            break

    # =====================================================
    # FIGURA PRINCIPAL
    # FIGURA
    # =====================================================

    fig_kmeans_real = go.Figure(
    fig_kmeans = go.Figure(
        data=frames[0].data,
        frames=frames
    )

    botones_iteraciones = []
    botones = []

    for i, frame in enumerate(frames):
    for frame in frames:

        botones_iteraciones.append(
        botones.append(
            dict(
                label=frame.name,
                method='animate',
@@ -800,19 +816,19 @@
                    {
                        'mode': 'immediate',
                        'frame': {
                            'duration': 1500,
                            'duration': 1800,
                            'redraw': True
                        },
                        'transition': {
                            'duration': 800
                            'duration': 700
                        }
                    }
                ]
            )
        )

    fig_kmeans_real.update_layout(
        title='Simulación REAL del algoritmo K-Means',
    fig_kmeans.update_layout(
        title='Aprendizaje paso a paso de K-Means',
        width=1700,
        height=950,
        paper_bgcolor='#0e1117',
@@ -829,7 +845,7 @@
                type='buttons',
                direction='right',
                x=0.02,
                y=1.18,
                y=1.15,
                buttons=[
                    dict(
                        label='▶ Reproducir K-Means',
@@ -838,7 +854,7 @@
                            None,
                            {
                                'frame': {
                                    'duration': 1500,
                                    'duration': 1800,
                                    'redraw': True
                                },
                                'transition': {
@@ -849,7 +865,7 @@
                        ]
                    ),
                    dict(
                        label='⏸ Pausar',
                        label='⏸ Pausa',
                        method='animate',
                        args=[
                            [None],
@@ -867,15 +883,15 @@
            dict(
                type='dropdown',
                direction='down',
                buttons=botones_iteraciones,
                x=0.35,
                y=1.18,
                buttons=botones,
                x=0.40,
                y=1.15,
                showactive=True
            )
        ]
    )

    st.plotly_chart(fig_kmeans_real, use_container_width=True)
    st.plotly_chart(fig_kmeans, use_container_width=True)

    # =====================================================
    # BOXPLOT
