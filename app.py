import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# Configuración de la interfaz
st.set_page_config(page_title="K-Means 3D", layout="wide")
st.title("Segmentación de Clientes: Algoritmo K-Means 3D")
st.write("Visualización paso a paso del aprendizaje no supervisado [7].")

# 1. Generación de Datos (Corregido para 3D)
@st.cache_data
def generate_data():
    np.random.seed(42)
    # Cada grupo (loc) debe tener 3 valores para las 3 dimensiones (Saldo, Transacciones, Antigüedad)
    g1 = np.random.normal(loc=[3, 8, 9], scale=[3, 7], size=(20, 3))
    g2 = np.random.normal(loc=[10, 11], scale=[9, 12, 13], size=(20, 3))
    g3 = np.random.normal(loc=[8, 14], scale=[3, 12], size=(20, 3))
    
    data = np.vstack([g1, g2, g3])
    # Basado en las fuentes: Saldo y Transacciones + Antigüedad para el 3D [3, 4]
    df = pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])
    return df

df_raw = generate_data()

# 2. Escalamiento: El algoritmo es susceptible a las escalas [6, 10]
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

# Sidebar
st.sidebar.header("Parámetros")
k = st.sidebar.slider("Número de Clusters (K)", 2, 6, 3)

# Inicialización del estado de la sesión
if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar"):
    # Inicialización aleatoria de centroides [9, 15]
    st.session_state.centroids = df_scaled.sample(k).values
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.step = 0
    st.session_state.converged = False

# Lógica Secuencial: Asignación y Actualización [2, 5, 8]
def run_iteration():
    points = df_scaled.values
    centroids = st.session_state.centroids
    
    # Paso 1: Asignación por Distancia Euclidiana [5]
    distances = np.linalg.norm(points[:, np.newaxis] - centroids, axis=2)
    new_labels = np.argmin(distances, axis=1)
    
    # Paso 2: Actualización por Promedio [2, 16]
    new_centroids = np.array([
        points[new_labels == i].mean(axis=0) if len(points[new_labels == i]) > 0 else centroids[i]
        for i in range(k)
    ])
    
    if np.allclose(centroids, new_centroids):
        st.session_state.converged = True
    
    st.session_state.centroids = new_centroids
    st.session_state.labels = new_labels
    st.session_state.step += 1

# Botón para avanzar paso a paso
if not st.session_state.converged:
    if st.button(f"Ejecutar Paso {st.session_state.step + 1}"):
        run_iteration()
else:
    st.success(f"Convergencia alcanzada en el paso {st.session_state.step} [17].")

# 3. Gráfica 3D con Plotly
fig = go.Figure()

# Puntos de Clientes
fig.add_trace(go.Scatter3d(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'], z=df_scaled['Antigüedad'],
    mode='markers',
    marker=dict(size=5, color=st.session_state.labels, colorscale='Viridis', opacity=0.7),
    name="Clientes"
))

# Centroides (Cruces rojas según el video) [18]
fig.add_trace(go.Scatter3d(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1], 
    z=st.session_state.centroids[:, 2],
    mode='markers',
    marker=dict(size=10, color='red', symbol='x', line=dict(width=2, color='black')),
    name="Centroides"
))

fig.update_layout(scene=dict(xaxis_title='Saldo', yaxis_title='Transacciones', zaxis_title='Antigüedad'), height=700)
st.plotly_chart(fig, use_container_width=True)

# Métrica de Inercia [19, 20]
def calculate_inertia():
    pts = df_scaled.values
    labs = st.session_state.labels
    cents = st.session_state.centroids
    return np.sum([np.linalg.norm(pts[i] - cents[int(labs[i])])**2 for i in range(len(pts))])

if st.session_state.step > 0:
    st.write(f"**Inercia (Suma de distancias al cuadrado):** {calculate_inertia():.4f} [20]")
