import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la interfaz
st.set_page_config(page_title="K-Means 3D Lab", layout="wide")

st.title("🧶 K-Means 3D: Visualización de Distancias y Movimiento")
st.markdown("Análisis interactivo del dataset **USArrests** con el proceso paso a paso.")

# 1. CARGA DE DATOS (Solución al TypeError)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # CORRECCIÓN: Usamos  para obtener solo el nombre de la primera columna
    df.rename(columns={df.columns: 'State'}, inplace=True)
    return df

try:
    df_raw = load_data()
    variables = ['Murder', 'Assault', 'UrbanPop', 'Rape']

    # 2. PREPROCESAMIENTO: Estandarización (Fuentes [1-3])
    # K-means es sensible a las escalas; normalizamos para que tengan media 0 y varianza 1.
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_raw[variables])

    # 3. REDUCCIÓN A 3D CON PCA (Fuentes [4-6])
    # Para visualizar 4 variables en un plano 3D atractivo.
    pca = PCA(n_components=3)
    data_3d = pca.fit_transform(df_scaled)
    df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

    # Controles en el Sidebar
    st.sidebar.header("Parámetros del Experimento")
    k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
    etapa = st.sidebar.select_slider("Fase del Proceso", options=[
        "1. Puntos Originales", 
        "2. Inicializar Centroides", 
        "3. Enlazar por Distancia", 
        "4. Nueva Posición (Promedio)"
    ])

    # Lógica del algoritmo (Semilla fija 42 para reproducibilidad [7, 8])
    np.random.seed(42)
    idx_inicio = np.random.choice(len(df_pca), k, replace=False)
    centroides_ini = df_pca.iloc[idx_inicio].values

    # Cálculo de distancias y etiquetas (Fuentes [9, 10])
    distancias = pairwise_distances(df_pca, centroides_ini, metric='euclidean')
    etiquetas = np.argmin(distancias, axis=1)

    # Cálculo de nuevos centroides (Fuentes [11, 12])
    centroides_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k)])

    # --- CONSTRUCCIÓN DEL GRÁFICO 3D ---
    fig = go.Figure()
    colores = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

    # Visualización de los puntos de los Estados
    fig.add_trace(go.Scatter3d(
        x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
        mode='markers',
        marker=dict(size=5, color=[colores[l] if etapa != "1. Puntos Originales" else 'white' for l in etiquetas], opacity=0.7),
        text=df_raw['State'], name="Estados"
    ))

    if etapa != "1. Puntos Originales":
        for i in range(k):
            # Posición del centroide según la etapa
            pos_c = centroides_ini[i] if etapa != "4. Nueva Posición (Promedio)" else centroides_nuevos[i]
            
            # Dibujar Centroide (Diamante resaltado)
            fig.add_trace(go.Scatter3d(
                x=[pos_c], y=[pos_c[13]], z=[pos_c[14]],
                mode='markers',
                marker=dict(size=14, color=colores[i], symbol='diamond', line=dict(width=3, color='white')),
                name=f"Centroide {i}"
            ))

            # LÍNEAS DE DISTANCIA EUCLIDIANA (Visualización de la hipotenusa [10])
            if etapa == "3. Enlazar por Distancia":
                puntos_cluster = df_pca[etiquetas == i]
                for _, fila in puntos_cluster.iterrows():
                    fig.add_trace(go.Scatter3d(
                        x=[fila['PC1'], centroides_ini[i, 0]],
                        y=[fila['PC2'], centroides_ini[i, 1]],
                        z=[fila['PC3'], centroides_ini[i, 2]],
                        mode='lines', line=dict(color=colores[i], width=1.5),
                        opacity=0.3, showlegend=False
                    ))

            # MOVIMIENTO DE LOS CENTROIDES (Trayectoria al promedio [11, 15])
            if etapa == "4. Nueva Posición (Promedio)":
                fig.add_trace(go.Scatter3d(
                    x=[centroides_ini[i, 0], centroides_nuevos[i, 0]],
                    y=[centroides_ini[i, 1], centroides_nuevos[i, 1]],
                    z=[centroides_ini[i, 2], centroides_nuevos[i, 2]],
                    mode='lines+markers',
                    line=dict(color='white', width=4, dash='dash'),
                    marker=dict(size=5, color='white'),
                    name=f"Trayecto C{i}"
                ))

    # Estética del plano 3D
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="PC1", backgroundcolor="#111", gridcolor="#333"),
            yaxis=dict(title="PC2", backgroundcolor="#111", gridcolor="#333"),
            zaxis=dict(title="PC3", backgroundcolor="#111", gridcolor="#333"),
            bgcolor="black"
        ),
        paper_bgcolor="black", font=dict(color="white"),
        height=850, margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Explicación técnica interactiva
    if etapa == "3. Enlazar por Distancia":
        st.info("**Concepto:** Se calcula la **distancia euclidiana** para asignar cada estado al centroide más cercano. Visualmente, son las líneas que conectan cada punto con el diamante [10].")
    elif etapa == "4. Nueva Posición (Promedio)":
        st.success("**Concepto:** El centroide 'viaja' hacia el **promedio** de las coordenadas de sus puntos asignados, optimizando la compactación del grupo [11, 15].")

    st.write("### Tabla de Datos (USArrests)")
    st.dataframe(df_raw)

except Exception as e:
    st.error(f"Error detectado: {e}")
    st.warning("Asegúrate de que la URL de GitHub sea accesible y que las librerías estén instaladas.")
