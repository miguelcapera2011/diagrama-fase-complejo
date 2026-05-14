import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la página
st.set_page_config(page_title="K-Means 3D: Proceso Visual", layout="wide")

st.title("Explorador Interactivo de K-Means (USArrests)")
st.write("Visualización del proceso de clustering basado en los componentes principales del dataset.")

# 1. Carga de datos (Basado en la fuente [2])
@st.cache_data
def load_data():
    # Simulación de la estructura de USArrests mencionada en las fuentes
    data = {
        'State': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia'],
        'Murder': [13.2, 10.0, 8.1, 8.8, 9.0, 7.9, 3.3, 5.9, 15.4, 17.4],
        'Assault': [5],
        'UrbanPop': [4, 6-13],
        'Rape': [21.2, 44.5, 31.0, 19.5, 40.6, 38.7, 11.1, 15.8, 31.9, 25.8]
    }
    # Nota: En una app real, usarías pd.read_excel("data_USArrests.xlsx") [2]
    return pd.DataFrame(data)

df = load_data()
features = ['Murder', 'Assault', 'UrbanPop', 'Rape']

# 2. Preprocesamiento: Escalado (Fuente [14])
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# 3. Reducción a 3D con PCA (Fuente [4, 15])
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Controles del algoritmo
st.sidebar.header("Parámetros de K-Means")
k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 3)
max_iter = st.sidebar.slider("Iteraciones a mostrar", 1, 10, 1)

# Inicialización manual de centroides (Fuente [16])
np.random.seed(42)
initial_indices = np.random.choice(len(df_pca), k, replace=False)
centroids = df_pca.iloc[initial_indices].values

# Simulación del proceso iterativo
history = []
current_centroids = centroids.copy()

for i in range(max_iter):
    # Paso de Asignación: Distancia Euclidiana (Fuente [17, 18])
    distances = pairwise_distances(df_pca, current_centroids, metric='euclidean')
    labels = np.argmin(distances, axis=1)
    
    # Guardar estado para visualización
    history.append({'centroids': current_centroids.copy(), 'labels': labels.copy()})
    
    # Paso de Actualización: Nuevo centroide = promedio (Fuente [9, 19])
    new_centroids = np.array([df_pca[labels == j].mean(axis=0) for j in range(k)])
    if np.all(current_centroids == new_centroids):
        break
    current_centroids = new_centroids

# Visualización 3D "Bonita" con Plotly
st.subheader(f"Iteración {max_iter}: Asignación y Distancias")

fig = go.Figure()

# Dibujar puntos de datos
colors = ['red', 'green', 'blue', 'yellow', 'purple']
for j in range(k):
    cluster_points = df_pca[history[-1]['labels'] == j]
    fig.add_trace(go.Scatter3d(
        x=cluster_points['PC1'], y=cluster_points['PC2'], z=cluster_points['PC3'],
        mode='markers',
        marker=dict(size=6, color=colors[j]),
        name=f"Cluster {j}",
        text=df['State'][history[-1]['labels'] == j]
    ))

    # Dibujar Centroides (Fuente [20, 21])
    fig.add_trace(go.Scatter3d(
        x=[history[-1]['centroids'][j, 0]], 
        y=[history[-1]['centroids'][j, 1]], 
        z=[history[-1]['centroids'][j, 2]],
        mode='markers',
        marker=dict(size=12, color=colors[j], symbol='diamond', line=dict(width=2, color='black')),
        name=f"Centroide {j}"
    ))

    # Visualizar Distancia Euclidiana (Líneas de enlace)
    for idx, row in cluster_points.iterrows():
        fig.add_trace(go.Scatter3d(
            x=[row['PC1'], history[-1]['centroids'][j, 0]],
            y=[row['PC2'], history[-1]['centroids'][j, 1]],
            z=[row['PC3'], history[-1]['centroids'][j, 2]],
            mode='lines',
            line=dict(color=colors[j], width=1),
            showlegend=False,
            opacity=0.3
        ))

fig.update_layout(
    scene=dict(xaxis_title='PC1', yaxis_title='PC2', zaxis_title='PC3'),
    width=900, height=700,
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# Explicación del proceso
st.info("""
**Proceso Visualizado:**
1. **Escalado:** Los datos de arrestos se normalizan para que variables con escalas grandes (como Assault) no dominen la distancia [22, 23].
2. **Asignación (Líneas):** Cada estado se enlaza al centroide más cercano usando la **distancia euclidiana** [17, 18].
3. **Actualización:** En la siguiente iteración, el centroide se moverá al promedio geométrico de todos sus puntos enlazados [9].
""")
