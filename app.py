import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# 1. Configuración de la App
st.set_page_config(page_title="K-Means 3D Journey", layout="wide")
st.title("🧶 Proceso K-Means 3D: USArrests")
st.markdown("Visualización avanzada del algoritmo: desde la **distancia euclidiana** hasta el **reajuste de centroides**.")

# 2. Carga de Datos Segura (SOLUCIÓN AL TYPEERROR)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # Obtenemos la lista de nombres actual
    columnas_actuales = list(df.columns)
    # Cambiamos SOLO el primer elemento (que es el índice de estados)
    columnas_actuales = 'State'
    # Asignamos la lista completa de nuevo al DataFrame
    df.columns = columnas_actuales
    return df

try:
    df_raw = load_data()
    features = ['Murder', 'Assault', 'UrbanPop', 'Rape'] # Variables según fuentes [1, 2]

    # 3. Preprocesamiento: Escalado (Fundamental según fuentes [3, 4])
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_raw[features])

    # 4. PCA para Plano 3D "Bonito" (Fuentes [5, 6])
    pca = PCA(n_components=3)
    data_3d = pca.fit_transform(df_scaled)
    df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

    # 5. Controles del Algoritmo
    st.sidebar.header("Configuración")
    k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
    paso = st.sidebar.select_slider("Fase del Proceso", options=[
        "1. Puntos Iniciales", 
        "2. Inicializar Centroides",
        "3. Asignación (Distancia Euclidiana)", 
        "4. Actualización (Movimiento al Promedio)"
    ])

    # Lógica del Algoritmo (Semilla 42 para reproducibilidad [7])
    np.random.seed(42)
    idx_inicio = np.random.choice(len(df_pca), k, replace=False)
    centroides_ini = df_pca.iloc[idx_inicio].values

    # Cálculo de Distancias y Etiquetas (Asignación) [8, 9]
    distancias = pairwise_distances(df_pca, centroides_ini, metric='euclidean')
    etiquetas = np.argmin(distancias, axis=1)

    # Cálculo de Nueva Posición (Promedio de los puntos) [10, 11]
    centroides_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k)])

    # --- 6. VISUALIZACIÓN 3D INTERACTIVA ---
    fig = go.Figure()
    colores = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

    # Capa de puntos (Estados)
    color_puntos = [colores[l] if paso not in ["1. Puntos Iniciales", "2. Inicializar Centroides"] else 'white' for l in etiquetas]
    fig.add_trace(go.Scatter3d(
        x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
        mode='markers',
        marker=dict(size=5, color=color_puntos, opacity=0.8),
        text=df_raw['State'], name="Estados"
    ))

    if paso != "1. Puntos Iniciales":
        for i in range(k):
            # Determinar posición del centroide según la fase
            c_actual = centroides_ini[i] if paso != "4. Actualización (Movimiento al Promedio)" else centroides_nuevos[i]
            
            # Dibujar Centroide (Diamante brillante)
            fig.add_trace(go.Scatter3d(
                x=[c_actual], y=[c_actual[1]], z=[c_actual[12]],
                mode='markers',
                marker=dict(size=12, color=colores[i], symbol='diamond', line=dict(width=2, color='white')),
                name=f"Centroide {i}"
            ))

            # ENLACES DE DISTANCIA (Mecánica de la 'Hipotenusa' [9])
            if paso == "3. Asignación (Distancia Euclidiana)":
                puntos_cluster = df_pca[etiquetas == i]
                for _, fila in puntos_cluster.iterrows():
                    fig.add_trace(go.Scatter3d(
                        x=[fila['PC1'], centroides_ini[i, 0]],
                        y=[fila['PC2'], centroides_ini[i, 1]],
                        z=[fila['PC3'], centroides_ini[i, 2]],
                        mode='lines', line=dict(color=colores[i], width=1),
                        opacity=0.2, showlegend=False
                    ))

            # TRAYECTORIA DE MOVIMIENTO [13]
            if paso == "4. Actualización (Movimiento al Promedio)":
                fig.add_trace(go.Scatter3d(
                    x=[centroides_ini[i, 0], centroides_nuevos[i, 0]],
                    y=[centroides_ini[i, 1], centroides_nuevos[i, 1]],
                    z=[centroides_ini[i, 2], centroides_nuevos[i, 2]],
                    mode='lines+markers', line=dict(color='white', width=3, dash='dash'),
                    marker=dict(size=4, color='white'), name=f"Trayecto C{i}"
                ))

    # Estética del plano (Tema oscuro para que se vea "bonito")
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="PC1", backgroundcolor="#111", gridcolor="#333"),
            yaxis=dict(title="PC2", backgroundcolor="#111", gridcolor="#333"),
            zaxis=dict(title="PC3", backgroundcolor="#111", gridcolor="#333"),
            bgcolor="black"
        ),
        paper_bgcolor="black", font=dict(color="white"),
        height=800, margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 7. Explicación Dinámica (Fuentes)
    if paso == "3. Asignación (Distancia Euclidiana)":
        st.info("💡 **Mecánica:** Se calcula la **distancia euclidiana** (la hipotenusa en el espacio 3D) para enlazar cada estado al centroide más cercano [9, 14].")
    elif paso == "4. Actualización (Movimiento al Promedio)":
        st.success("💡 **Mecánica:** El centroide se desplaza a la nueva posición calculada mediante el **promedio** de las coordenadas de todos los estados asignados [10, 11].")

    st.write("### Vista previa del Dataset (USArrests)")
    st.dataframe(df_raw.head(10))

except Exception as e:
    st.error(f"Error en la aplicación: {e}")
    st.write("Detalles del error para depuración:")
    st.code(e)
