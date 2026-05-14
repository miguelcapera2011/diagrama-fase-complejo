import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Configuración de la página para que se vea moderna
st.set_page_config(page_title="K-Means 3D Pro", layout="wide")

st.title("🤖 Segmentación K-Means 3D Interactiva")
st.markdown("""
Esta aplicación aplica el algoritmo de **K-means** basándose en la lógica del video: 
escalamiento de datos, asignación por distancia euclidiana y cálculo de centroides.
""")

# 1. GENERACIÓN DE DATOS (Simulando el contexto bancario del video en 3D)
@st.cache_data
def load_data():
    np.random.seed(42)
    # Creamos 3 dimensiones: Saldo, Transacciones y Antigüedad (fuente [3])
    data = np.random.rand(100, 3) * 100
    return pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])

df = load_data()

# 2. BARRA LATERAL (Entrada de K y controles)
st.sidebar.header("Parámetros del Modelo")
k_clusters = st.sidebar.slider("Selecciona el número de clusters (k)", 2, 10, 3) # Fuente [4]
show_links = st.sidebar.checkbox("Mostrar enlaces a centroides", value=True)

# 3. PRE-PROCESAMIENTO (Vital según la fuente [1, 5])
# El video explica que K-means es sensible a las escalas, por lo que usamos MinMaxScaler
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df)

# 4. EJECUCIÓN DEL MODELO K-MEANS
# Se ajusta el modelo automáticamente al cambiar el valor de K
kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
labels = kmeans.fit_predict(df_scaled)
centroids = kmeans.cluster_centers_

# 5. VISUALIZACIÓN 3D AVANZADA (Plotly)
fig = go.Figure()

# Paleta de colores estética
colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']

for i in range(k_clusters):
    # Filtrar puntos pertenecientes al cluster actual
    cluster_indices = np.where(labels == i)
    points = df_scaled[cluster_indices]
    centroid = centroids[i]
    color = colors[i % len(colors)]

    # A. Dibujar los puntos del cluster
    fig.add_trace(go.Scatter3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        mode='markers',
        marker=dict(size=4, color=color, opacity=0.8),
        name=f"Cluster {i}"
    ))

    # B. Dibujar el Centroide (como una X destacada) - Fuente [6, 7]
    fig.add_trace(go.Scatter3d(
        x=[centroid], y=[centroid[8]], z=[centroid[3]],
        mode='markers',
        marker=dict(size=10, symbol='x', color='white', line=dict(width=2, color='black')),
        name=f"Centroide {i}"
    ))

    # C. Dibujar enlaces (líneas del punto al centroide) - Fuente [9]
    if show_links:
        for p in points:
            fig.add_trace(go.Scatter3d(
                x=[p, centroid],
                y=[p[8], centroid[8]],
                z=[p[3], centroid[3]],
                mode='lines',
                line=dict(color=color, width=1),
                showlegend=False,
                opacity=0.2  # Opacidad baja para que sea "bonito" y no sature
            ))

# Estética del plano (Sin el cuadro "encerrado" clásico)
fig.update_layout(
    template="plotly_dark",
    scene=dict(
        xaxis=dict(title='Saldo (Escalado)', showbackground=False),
        yaxis=dict(title='Transacciones (Escalado)', showbackground=False),
        zaxis=dict(title='Antigüedad (Escalado)', showbackground=False),
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    height=700
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

# 6. MÉTRICAS (Como se muestra en el video [2, 10])
col1, col2 = st.columns(2)
with col1:
    st.metric("Inercia (Suma de distancias al cuadrado)", f"{kmeans.inertia_:.4f}")
with col2:
    st.info("Una inercia menor indica que los puntos están más 'pegados' a sus centroides [10, 11].")

st.dataframe(df.assign(Cluster=labels).head(10))
