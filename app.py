import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# 1. Configuración de la App
st.set_page_config(page_title="K-Means 3D Lab", layout="wide")
st.title("🧶 Laboratorio K-Means 3D: USArrests")
st.markdown("Visualización del proceso: **Distancia Euclidiana** e **Iteración de Centroides**.")

# 2. Carga de Datos (Dataset Completo de 50 estados)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # Renombrar columnas para consistencia con las fuentes [1]
    df.columns = ['State', 'Murder', 'Assault', 'UrbanPop', 'Rape']
    return df

df_raw = load_data()
features = ['Murder', 'Assault', 'UrbanPop', 'Rape']

# 3. Preprocesamiento (Fuentes [3, 4])
# Escalamos los datos para que variables como Assault no dominen la distancia euclidiana.
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_raw[features])

# 4. Reducción a 3D con PCA (Fuentes [5, 6])
# Proyectamos las 4 variables en 3 componentes principales para el plano 3D.
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Controles
st.sidebar.header("Parámetros del Algoritmo")
k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
etapa = st.sidebar.select_slider("Fase del Proceso", options=[
    "Puntos Base", "Asignación (Distancias)", "Actualización (Movimiento)"
])

# 5. Lógica del Algoritmo (Semilla 42 para reproducibilidad [7])
np.random.seed(42)
idx_ini = np.random.choice(len(df_pca), k, replace=False)
centroids_ini = df_pca.iloc[idx_ini].values # Arreglo de tamaño (k, 3)

# Cálculo de distancias euclidianas (La "hipotenusa" [8])
distancias = pairwise_distances(df_pca, centroids_ini, metric='euclidean')
etiquetas = np.argmin(distancias, axis=1) # Etiquetas 0 a k-1 para los 50 estados [9]

# Cálculo de nuevos centroides (Promedio de puntos asignados [10, 11])
centroids_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k)])

# --- 6. VISUALIZACIÓN 3D INTERACTIVA ---
fig = go.Figure()
colores = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

# Capa de puntos de los Estados
fig.add_trace(go.Scatter3d(
    x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
    mode='markers',
    marker=dict(size=5, color=[colores[l] if etapa != "Puntos Base" else 'white' for l in etiquetas], opacity=0.8),
    text=df_raw['State'], name="Estados"
))

# Bucle sobre los CLUSTERS (Evita el error index 9 out of bounds)
for i in range(k):
    # Elegir qué posición del centroide mostrar
    c_actual = centroids_ini[i] if etapa != "Actualización (Movimiento)" else centroids_nuevos[i]
    
    # Dibujar Centroide (Diamante resaltado)
    fig.add_trace(go.Scatter3d(
        x=[c_actual], y=[c_actual[1]], z=[c_actual[12]],
        mode='markers',
        marker=dict(size=12, color=colores[i], symbol='diamond', line=dict(width=2, color='white')),
        name=f"Centroide {i}"
    ))

    # ENLACE EUCLIDIANO (Visualización de distancias [8, 13])
    if etapa == "Asignación (Distancias)":
        puntos_cluster = df_pca[etiquetas == i]
        for _, fila in puntos_cluster.iterrows():
            fig.add_trace(go.Scatter3d(
                x=[fila['PC1'], centroids_ini[i, 0]],
                y=[fila['PC2'], centroides_ini[i, 1]],
                z=[fila['PC3'], centroides_ini[i, 2]],
                mode='lines', line=dict(color=colores[i], width=1),
                opacity=0.2, showlegend=False
            ))

    # TRAYECTORIA DE MOVIMIENTO (Hacia el promedio [14, 15])
    if etapa == "Actualización (Movimiento)":
        fig.add_trace(go.Scatter3d(
            x=[centroids_ini[i, 0], centroids_nuevos[i, 0]],
            y=[centroids_ini[i, 1], centroids_nuevos[i, 1]],
            z=[centroids_ini[i, 2], centroids_nuevos[i, 2]],
            mode='lines+markers', line=dict(color='white', width=3, dash='dash'),
            marker=dict(size=4, color='white'), name=f"Desplazamiento C{i}"
        ))

# Estética del plano 3D
fig.update_layout(
    scene=dict(xaxis_title="PC1", yaxis_title="PC2", zaxis_title="PC3", bgcolor="#0e1117"),
    paper_bgcolor="#0e1117", font=dict(color="white"), height=800, margin=dict(l=0, r=0, b=0, t=30)
)

st.plotly_chart(fig, use_container_width=True)

# 7. Explicaciones Técnicas basadas en fuentes
if etapa == "Asignación (Distancias)":
    st.info("💡 **Mecánica:** Se calcula la **distancia euclidiana** entre cada estado y los centroides. Visualmente, estas líneas representan la 'hipotenusa' en el espacio de datos [8].")
elif etapa == "Actualización (Movimiento)":
    st.success("💡 **Mecánica:** Los centroides se desplazan hacia el **promedio** de las coordenadas de todos los estados asignados a su grupo [10].")

st.write("### Vista previa de los datos originales [1]")
st.dataframe(df_raw.head(10))
