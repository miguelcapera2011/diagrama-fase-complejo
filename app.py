import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# Configuración de la página
st.set_page_config(page_title="K-Means 3D Secuencial", layout="wide")
st.title("Visualización Secuencial de K-Means en 3D")

# 1. Generación de Datos Sintéticos (Basado en el contexto de las fuentes [10])
@st.cache_data
def generate_data():
    np.random.seed(42)
    # Creamos 3 grupos naturales para visualizar mejor el algoritmo
    g1 = np.random.normal(loc=[5, 11], scale=[10], size=(20, 3))
    g2 = np.random.normal(loc=[12], scale=[5, 9], size=(20, 3))
    g3 = np.random.normal(loc=[4, 13], scale=[5, 14], size=(20, 3))
    data = np.vstack([g1, g2, g3])
    df = pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])
    return df

df_raw = generate_data()

# 2. Preprocesamiento: Escalamiento (Paso crítico según las fuentes [3, 4])
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

# Sidebar para controles
st.sidebar.header("Configuración del Algoritmo")
k = st.sidebar.slider("Selecciona el valor de K (Clústeres)", min_value=2, max_value=6, value=3)
step = st.sidebar.number_input("Paso de la Iteración", min_value=0, value=0, step=1)

# Lógica del algoritmo paso a paso usando Session State
if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar Centroides"):
    # Inicialización aleatoria (Paso 1 del algoritmo [5])
    st.session_state.centroids = df_scaled.sample(k).values
    st.session_state.history = []
    st.session_state.current_step = 0

def run_kmeans_step(data, centroids):
    # Asignación por distancia euclidiana (Paso 2 [6])
    distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
    labels = np.argmin(distances, axis=1)
    
    # Actualización de centroides por promedio (Paso 3 [8, 9])
    new_centroids = np.array([data[labels == i].mean(axis=0) if len(data[labels == i]) > 0 
                             else centroids[i] for i in range(k)])
    return labels, new_centroids

# Ejecutar hasta el paso seleccionado
current_centroids = st.session_state.centroids
current_labels = np.zeros(len(df_scaled))

for i in range(step):
    current_labels, next_centroids = run_kmeans_step(df_scaled.values, current_centroids)
    if np.all(current_centroids == next_centroids): # Criterio de parada [11]
        st.sidebar.success(f"El algoritmo ha convergido en el paso {i}")
        break
    current_centroids = next_centroids

# 3. Visualización en 3D con Plotly
fig = go.Figure()

# Dibujar los puntos de datos
fig.add_trace(go.Scatter3d(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'], z=df_scaled['Antigüedad'],
    mode='markers',
    marker=dict(size=5, color=current_labels, colorscale='Viridis', opacity=0.8),
    name="Clientes"
))

# Dibujar los centroides (representados como cruces según la fuente [15])
fig.add_trace(go.Scatter3d(
    x=current_centroids[:, 0], y=current_centroids[:, 1], z=current_centroids[:, 2],
    mode='markers',
    marker=dict(size=10, color='red', symbol='x', line=dict(width=2, color='black')),
    name="Centroides"
))

fig.update_layout(
    scene=dict(
        xaxis_title='Saldo (Escalado)',
        yaxis_title='Transacciones (Escalado)',
        zaxis_title='Antigüedad (Escalado)'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# Explicación del estado actual
if step == 0:
    st.info("Paso 0: Centroides inicializados aleatoriamente en el espacio de datos [5].")
else:
    st.info(f"Paso {step}: Los puntos se asignaron al centroide más cercano y los centroides se movieron al promedio de sus grupos [8, 9].")
