import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la página
st.set_page_config(page_title="K-Means 3D: Paso a Paso", layout="wide")

st.title("🚀 Visualizador Interactivo de K-Means (USArrests)")
st.markdown("""
Esta aplicación recrea el proceso técnico del algoritmo K-means detallado en las fuentes, 
utilizando los datos de criminalidad de EE.UU. y mostrando la mecánica de distancias en 3D.
""")

# 1. Carga de datos reales de la fuente [1]
@st.cache_data
def load_data():
    data = {
        'State': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia'],
        'Murder': [13.2, 10.0, 8.1, 8.8, 9.0, 7.9, 3.3, 5.9, 15.4, 17.4],
        'Assault': [2],
        'UrbanPop': [3-11],
        'Rape': [21.2, 44.5, 31.0, 19.5, 40.6, 38.7, 11.1, 15.8, 31.9, 25.8]
    }
    return pd.DataFrame(data)

df = load_data()
features = ['Murder', 'Assault', 'UrbanPop', 'Rape']

# 2. Preprocesamiento: Estandarización (Fuente [12-14])
# El algoritmo es sensible a las escalas, por lo que convertimos a media 0 y varianza 1.
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# 3. Reducción a 3D para visualización (Fuente [4, 15])
# Usamos PCA para proyectar las 4 variables originales en 3 dimensiones visuales.
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Controles de la simulación
st.sidebar.header("Configuración del Algoritmo")
k_clusters = st.sidebar.slider("Número de Clusters (k)", 2, 4, 3)
iteration_step = st.sidebar.select_slider("Paso del proceso", options=[
    "Puntos Originales", 
    "Inicializar Centroides", 
    "Asignación (Distancia)", 
    "Actualizar Centroides"
])

# Lógica del Algoritmo Paso a Paso
np.random.seed(42)
initial_indices = np.random.choice(len(df_pca), k_clusters, replace=False)
initial_centroids = df_pca.iloc[initial_indices].values

# Visualización con Plotly
fig = go.Figure()

colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']

if iteration_step == "Puntos Originales":
    fig.add_trace(go.Scatter3d(
        x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
        mode='markers', marker=dict(size=6, color='gray'),
        text=df['State'], name="Estados"
    ))

elif iteration_step == "Inicializar Centroides":
    # Muestra los puntos y los centroides en sus posiciones aleatorias iniciales [16]
    fig.add_trace(go.Scatter3d(
        x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
        mode='markers', marker=dict(size=5, color='gray', opacity=0.5),
        text=df['State'], name="Datos"
    ))
    for i in range(k_clusters):
        fig.add_trace(go.Scatter3d(
            x=[initial_centroids[i, 0]], y=[initial_centroids[i, 1]], z=[initial_centroids[i, 2]],
            mode='markers', marker=dict(size=12, color=colors[i], symbol='diamond', line=dict(width=2, color='white')),
            name=f"Centroide Inicial {i}"
        ))

elif iteration_step == "Asignación (Distancia)":
    # Paso 1: Medir distancia euclidiana y asignar al centroide más cercano [17, 18]
    distances = pairwise_distances(df_pca, initial_centroids, metric='euclidean')
    labels = np.argmin(distances, axis=1)
    
    for i in range(k_clusters):
        cluster_data = df_pca[labels == i]
        # Dibujar puntos del cluster
        fig.add_trace(go.Scatter3d(
            x=cluster_data['PC1'], y=cluster_data['PC2'], z=cluster_data['PC3'],
            mode='markers', marker=dict(size=7, color=colors[i]),
            text=df['State'][labels == i], name=f"Cluster {i}"
        ))
        # Dibujar líneas de enlace (Distancia Euclidiana) [17]
        for _, row in cluster_data.iterrows():
            fig.add_trace(go.Scatter3d(
                x=[row['PC1'], initial_centroids[i, 0]],
                y=[row['PC2'], initial_centroids[i, 1]],
                z=[row['PC3'], initial_centroids[i, 2]],
                mode='lines', line=dict(color=colors[i], width=2),
                showlegend=False, opacity=0.3
            ))
        # Centroide
        fig.add_trace(go.Scatter3d(
            x=[initial_centroids[i, 0]], y=[initial_centroids[i, 1]], z=[initial_centroids[i, 2]],
            mode='markers', marker=dict(size=12, color=colors[i], symbol='diamond', line=dict(width=2, color='black')),
            name=f"Centroide {i}"
        ))

elif iteration_step == "Actualizar Centroides":
    # Paso 2: Recalcular centroides como el promedio de los puntos asignados [7, 19]
    distances = pairwise_distances(df_pca, initial_centroids, metric='euclidean')
    labels = np.argmin(distances, axis=1)
    new_centroids = np.array([df_pca[labels == i].mean(axis=0) for i in range(k_clusters)])
    
    for i in range(k_clusters):
        cluster_data = df_pca[labels == i]
        fig.add_trace(go.Scatter3d(
            x=cluster_data['PC1'], y=cluster_data['PC2'], z=cluster_data['PC3'],
            mode='markers', marker=dict(size=7, color=colors[i]),
            text=df['State'][labels == i], name=f"Cluster Final {i}"
        ))
        # Dibujar flecha o línea de movimiento desde la posición vieja a la nueva [20]
        fig.add_trace(go.Scatter3d(
            x=[initial_centroids[i, 0], new_centroids[i, 0]],
            y=[initial_centroids[i, 1], new_centroids[i, 1]],
            z=[initial_centroids[i, 2], new_centroids[i, 2]],
            mode='lines+markers', line=dict(color='black', width=4, dash='dash'),
            marker=dict(size=[21], color='black', symbol='arrow-up'),
            name=f"Movimiento C{i}"
        ))
        # Nuevo Centroide
        fig.add_trace(go.Scatter3d(
            x=[new_centroids[i, 0]], y=[new_centroids[i, 1]], z=[new_centroids[i, 2]],
            mode='markers', marker=dict(size=14, color=colors[i], symbol='star', line=dict(width=2, color='white')),
            name=f"Nuevo Centroide {i}"
        ))

fig.update_layout(
    scene=dict(
        xaxis=dict(backgroundcolor="rgb(230, 230,230)", gridcolor="white", showbackground=True),
        yaxis=dict(backgroundcolor="rgb(230, 230,230)", gridcolor="white", showbackground=True),
        zaxis=dict(backgroundcolor="rgb(230, 230,230)", gridcolor="white", showbackground=True),
        xaxis_title='Componente 1', yaxis_title='Componente 2', zaxis_title='Componente 3'
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

st.plotly_chart(fig, use_container_width=True)

# Sección de explicación dinámica
if iteration_step == "Asignación (Distancia)":
    st.info("**Concepto Clave:** Cada punto se une al centroide más cercano calculando la **hipotenusa en el espacio (distancia euclidiana)** [17].")
elif iteration_step == "Actualizar Centroides":
    st.success("**Concepto Clave:** El centroide se desplaza al **promedio geométrico** de todos los puntos que tiene asignados, optimizando la compactación del cluster [7].")

st.write("### Datos de los Estados (Fuente [1])")
st.dataframe(df)
