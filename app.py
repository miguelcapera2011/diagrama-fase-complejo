mport streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la página
st.set_page_config(page_title="K-Means 3D Lab", layout="wide")

st.title("📊 Laboratorio K-Means: USArrests Completo")
st.markdown("""
Esta aplicación utiliza los 50 estados del dataset **USArrests** para demostrar el proceso de clustering 
paso a paso, tal como se explica en la teoría de minería de datos y el algoritmo de K-medias [3, 4].
""")

# 1. Carga de datos desde la URL proporcionada
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # Renombrar la primera columna a 'State'
    df.rename(columns={df.columns: 'State'}, inplace=True)
    return df

df_original = load_data()
features = ['Murder', 'Assault', 'UrbanPop', 'Rape']

# 2. Preprocesamiento: Escalado (Fuente [5, 6])
# Es vital normalizar porque variables como 'Assault' dominan la escala [7].
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_original[features])

# 3. Reducción a 3D con PCA (Fuente [8, 9])
# Para visualizar 4 dimensiones en un plano 3D "bonito".
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Controles detallados
st.sidebar.header("Parámetros del Experimento")
k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
step = st.sidebar.select_slider("Etapa del Algoritmo", options=[
    "Puntos Escaleados", 
    "Inicialización Aleatoria", 
    "Cálculo de Distancias", 
    "Actualización de Centroides"
])

# Semilla fija para reproducibilidad [10, 11]
np.random.seed(42)
initial_indices = np.random.choice(len(df_pca), k, replace=False)
centroids = df_pca.iloc[initial_indices].values

# Lógica del proceso (Fuentes [1, 2, 12-14])
distances = pairwise_distances(df_pca, centroids, metric='euclidean')
labels = np.argmin(distances, axis=1)
new_centroids = np.array([df_pca[labels == i].mean(axis=0) for i in range(k)])

# --- Visualización 3D Interactiva ---
fig = go.Figure()
colors = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

# Capas de visualización según el paso seleccionado
if step == "Puntos Escaleados":
    fig.add_trace(go.Scatter3d(
        x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
        mode='markers', marker=dict(size=5, color='white', opacity=0.8),
        text=df_original['State'], name="Estados"
    ))

elif step == "Inicialización Aleatoria":
    fig.add_trace(go.Scatter3d(
        x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
        mode='markers', marker=dict(size=4, color='gray', opacity=0.3),
        text=df_original['State'], name="Datos"
    ))
    for i in range(k):
        fig.add_trace(go.Scatter3d(
            x=[centroids[i, 0]], y=[centroids[i, 1]], z=[centroids[i, 2]],
            mode='markers', marker=dict(size=12, color=colors[i], symbol='diamond', line=dict(width=2, color='white')),
            name=f"Centroide Inicial {i}"
        ))

elif step == "Cálculo de Distancias":
    for i in range(k):
        cluster_points = df_pca[labels == i]
        # Puntos asignados
        fig.add_trace(go.Scatter3d(
            x=cluster_points['PC1'], y=cluster_points['PC2'], z=cluster_points['PC3'],
            mode='markers', marker=dict(size=6, color=colors[i]),
            text=df_original['State'][labels == i], name=f"Cluster {i}"
        ))
        # Líneas de distancia euclidiana (La hipotenusa [1])
        for _, row in cluster_points.iterrows():
            fig.add_trace(go.Scatter3d(
                x=[row['PC1'], centroids[i, 0]], y=[row['PC2'], centroids[i, 1]], z=[row['PC3'], centroids[i, 2]],
                mode='lines', line=dict(color=colors[i], width=1),
                opacity=0.2, showlegend=False
            ))
        # Centroide actual
        fig.add_trace(go.Scatter3d(
            x=[centroids[i, 0]], y=[centroids[i, 1]], z=[centroids[i, 2]],
            mode='markers', marker=dict(size=10, color=colors[i], symbol='diamond', line=dict(color='black', width=2)),
            showlegend=False
        ))

elif step == "Actualización de Centroides":
    for i in range(k):
        cluster_points = df_pca[labels == i]
        fig.add_trace(go.Scatter3d(
            x=cluster_points['PC1'], y=cluster_points['PC2'], z=cluster_points['PC3'],
            mode='markers', marker=dict(size=6, color=colors[i]),
            text=df_original['State'][labels == i], name=f"Cluster {i}"
        ))
        # Mostrar movimiento (Vector de actualización [2])
        fig.add_trace(go.Scatter3d(
            x=[centroids[i, 0], new_centroids[i, 0]],
            y=[centroids[i, 1], new_centroids[i, 1]],
            z=[centroids[i, 2], new_centroids[i, 2]],
            mode='lines+markers', line=dict(color='black', width=4, dash='dot'),
            marker=dict(size=, color='black', symbol='arrow-up'),
            name=f"Movimiento C{i}"
        ))
        # Nuevo Centroide (Promedio de los puntos [2])
        fig.add_trace(go.Scatter3d(
            x=[new_centroids[i, 0]], y=[new_centroids[i, 1]], z=[new_centroids[i, 2]],
            mode='markers', marker=dict(size=14, color=colors[i], symbol='star', line=dict(width=2, color='white')),
            name=f"Nuevo Centroide {i}"
        ))

# Estética del gráfico
fig.update_layout(
    scene=dict(
        xaxis_title='PC1 (Varianza Principal)',
        yaxis_title='PC2',
        zaxis_title='PC3',
        bgcolor="rgb(10, 10, 10)"
    ),
    paper_bgcolor="rgb(10, 10, 10)",
    font=dict(color="white"),
    margin=dict(l=0, r=0, b=0, t=50),
    height=800
)

st.plotly_chart(fig, use_container_width=True)

# 4. Explicación basada en fuentes
st.subheader("Explicación del Proceso Técnico")
if step == "Cálculo de Distancias":
    st.info("""
    **Distancia Euclidiana:** Se mide la distancia lineal de cada estado a todos los centroides [15]. 
    Cada punto se asigna al centroide donde esta distancia es mínima [1, 16].
    """)
elif step == "Actualización de Centroides":
    st.success("""
    **Recálculo del Promedio:** Una vez asignados los puntos, el centroide se desplaza al **promedio** de las coordenadas 
    de todos los estados de su grupo [2, 13]. Este proceso se repite hasta que los centroides dejan de moverse [17].
    """)

st.write("### Base de Datos Completa (GitHub)")
st.dataframe(df_original)
