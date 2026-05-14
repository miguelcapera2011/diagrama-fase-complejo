
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la página
st.set_page_config(page_title="K-Means 3D Journey", layout="wide")

st.title("🧶 Visualizador K-Means: Proceso Técnico Completo")
st.markdown("""
Esta aplicación utiliza el dataset **USArrests** para mostrar la mecánica del algoritmo: 
desde la **distancia euclidiana** hasta la **actualización por promedios**.
""")

# 1. Carga de datos robusta (Solución al error de Index/State)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # Definimos la lista completa de nombres para evitar errores de escalares
    df.columns = ['State', 'Murder', 'Assault', 'UrbanPop', 'Rape']
    return df

try:
    df_raw = load_data()
    features = ['Murder', 'Assault', 'UrbanPop', 'Rape']

    # 2. Preprocesamiento: Escalado (Fuente [4, 5])
    # K-means es sensible a las escalas; normalizamos para que tengan media 0 y varianza 1.
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_raw[features])

    # 3. PCA para visualización 3D (Fuente [6])
    # Reducimos las 4 variables a 3 componentes principales para el plano 3D.
    pca = PCA(n_components=3)
    data_3d = pca.fit_transform(df_scaled)
    df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

    # Sidebar: Controles
    st.sidebar.header("Parámetros del Algoritmo")
    k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
    etapa = st.sidebar.select_slider("Fase del Proceso", options=[
        "1. Datos Escalados", 
        "2. Inicializar Centroides", 
        "3. Asignación (Distancia Euclidiana)", 
        "4. Actualización (Movimiento al Promedio)"
    ])

    # Lógica del Algoritmo (Semilla 42 para reproducibilidad [7])
    np.random.seed(42)
    idx_inicio = np.random.choice(len(df_pca), k, replace=False)
    centroides_ini = df_pca.iloc[idx_inicio].values

    # Cálculo de distancias y etiquetas
    distancias = pairwise_distances(df_pca, centroides_ini, metric='euclidean')
    etiquetas = np.argmin(distancias, axis=1)

    # Cálculo de nuevos centroides (Promedio de los puntos [2, 3])
    centroides_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k)])

    # --- 4. VISUALIZACIÓN 3D "BONITA" ---
    fig = go.Figure()
    colores = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

    # Puntos de los Estados
    fig.add_trace(go.Scatter3d(
        x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
        mode='markers',
        marker=dict(size=5, color=[colores[l] if etapa not in ["1. Datos Escalados", "2. Inicializar Centroides"] else 'white' for l in etiquetas], opacity=0.8),
        text=df_raw['State'], name="Estados"
    ))

    if etapa != "1. Datos Escalados":
        for i in range(k):
            # Posición del centroide según la etapa
            c_pos = centroides_ini[i] if etapa != "4. Actualización (Movimiento al Promedio)" else centroides_nuevos[i]
            
            # Dibujar Centroide (Diamante brillante [8])
            fig.add_trace(go.Scatter3d(
                x=[c_pos], y=[c_pos[9]], z=[c_pos[10]],
                mode='markers',
                marker=dict(size=12, color=colores[i], symbol='diamond', line=dict(width=2, color='white')),
                name=f"Centroide {i}"
            ))

            # LÍNEAS DE DISTANCIA (La hipotenusa [1])
            if etapa == "3. Asignación (Distancia Euclidiana)":
                puntos_cluster = df_pca[etiquetas == i]
                for _, fila in puntos_cluster.iterrows():
                    fig.add_trace(go.Scatter3d(
                        x=[fila['PC1'], centroides_ini[i, 0]],
                        y=[fila['PC2'], centroides_ini[i, 1]],
                        z=[fila['PC3'], centroides_ini[i, 2]],
                        mode='lines', line=dict(color=colores[i], width=1),
                        opacity=0.2, showlegend=False
                    ))

            # TRAYECTORIA DE MOVIMIENTO
            if etapa == "4. Actualización (Movimiento al Promedio)":
                fig.add_trace(go.Scatter3d(
                    x=[centroides_ini[i, 0], centroides_nuevos[i, 0]],
                    y=[centroides_ini[i, 1], centroides_nuevos[i, 1]],
                    z=[centroides_ini[i, 2], centroides_nuevos[i, 2]],
                    mode='lines+markers', line=dict(color='white', width=3, dash='dash'),
                    marker=dict(size=4, color='white'), name=f"Trayecto C{i}"
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

    # 5. Explicación Dinámica (Fuentes [1, 2])
    if etapa == "3. Asignación (Distancia Euclidiana)":
        st.info("💡 **Mecánica:** Se calcula la **distancia euclidiana** para enlazar cada estado al centroide más cercano. Visualmente, estas líneas representan la 'hipotenusa' [1].")
    elif etapa == "4. Actualización (Movimiento al Promedio)":
        st.success("💡 **Mecánica:** El centroide se desplaza hacia el **promedio** de las coordenadas de todos los estados asignados [2, 3].")

    st.write("### Vista previa de los datos")
    st.dataframe(df_raw.head(10))

except Exception as e:
    st.error(f"Error técnico: {e}")
