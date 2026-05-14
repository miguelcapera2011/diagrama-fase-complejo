import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# Configuración de la interfaz
st.set_page_config(page_title="K-Means 3D", layout="wide")
st.title("Segmentación de Clientes: K-Means 3D Paso a Paso")

# 1. Generación de Datos (CORREGIDO: 3 valores para loc y 3 para scale)
@st.cache_data
def generate_data():
    np.random.seed(42)
    # Grupo 1: loc tiene 3 ejes, scale ahora también tiene 3 valores (o 1 solo para todos)
    g1 = np.random.normal(loc=[8], scale=[0.5, 0.5, 0.5], size=(20, 3))
    g2 = np.random.normal(loc=[2, 4, 9], scale=[1.0, 1.0, 1.0], size=(20, 3))
    g3 = np.random.normal(loc=[2, 9, 10], scale=[0.8, 0.8, 0.8], size=(20, 3))
    
    data = np.vstack([g1, g2, g3])
    # Basado en las fuentes: Saldo, Transacciones [8, 11] y añadimos Antigüedad para 3D
    df = pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])
    return df

df_raw = generate_data()

# 2. Preprocesamiento: Escalamiento (Fundamental según las fuentes [6, 7])
# El algoritmo es susceptible a escalas; llevamos todo al rango 0-1 [12]
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

# Sidebar para controles
st.sidebar.header("Parámetros del Algoritmo")
k = st.sidebar.slider("Número de Clusters (K)", 2, 6, 3)

# Inicialización del estado de la sesión para persistir datos entre pasos
if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar Algoritmo"):
    # Inicialización aleatoria de centroides en el plano de los datos [9]
    st.session_state.centroids = df_scaled.sample(k).values
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.step = 0
    st.session_state.converged = False

def run_iteration():
    """Ejecuta una iteración: Asignación y Actualización [2, 5]"""
    points = df_scaled.values
    centroids = st.session_state.centroids
    
    # PASO A: Asignación por Distancia Euclidiana (hipotenusa) [5]
    distances = np.linalg.norm(points[:, np.newaxis] - centroids, axis=2)
    new_labels = np.argmin(distances, axis=1)
    
    # PASO B: Actualización (Promedio de las posiciones de los puntos) [2, 3]
    new_centroids = np.array([
        points[new_labels == i].mean(axis=0) if len(points[new_labels == i]) > 0 else centroids[i]
        for i in range(k)
    ])
    
    # Verificar si el algoritmo ha terminado (los centroides no cambian) [13]
    if np.allclose(centroids, new_centroids):
        st.session_state.converged = True
    
    st.session_state.centroids = new_centroids
    st.session_state.labels = new_labels
    st.session_state.step += 1

# Interfaz de ejecución secuencial
if not st.session_state.converged:
    if st.button(f"Ejecutar Iteración {st.session_state.step + 1}"):
        run_iteration()
else:
    st.success(f"¡Convergencia lograda en el paso {st.session_state.step}!")

# 3. Visualización en 3D interactiva
fig = go.Figure()

# Dibujar Clientes con sus etiquetas de cluster actuales [14]
fig.add_trace(go.Scatter3d(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'], z=df_scaled['Antigüedad'],
    mode='markers',
    marker=dict(size=5, color=st.session_state.labels, colorscale='Viridis', opacity=0.7),
    name="Clientes"
))

# Dibujar Centroides como cruces rojas [15]
fig.add_trace(go.Scatter3d(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1], 
    z=st.session_state.centroids[:, 2],
    mode='markers',
    marker=dict(size=12, color='red', symbol='x', line=dict(width=2, color='black')),
    name="Centroides"
))

fig.update_layout(
    scene=dict(xaxis_title='Saldo (Escalado)', yaxis_title='Transacciones (Escalado)', zaxis_title='Antigüedad (Escalado)'),
    margin=dict(l=0, r=0, b=0, t=0), height=700
)
st.plotly_chart(fig, use_container_width=True)

# Métrica de Inercia (Explicada en la fuente [16, 17])
def calculate_inertia():
    pts = df_scaled.values
    labs = st.session_state.labels
    cents = st.session_state.centroids
    # Suma de distancias al cuadrado hacia el centroide asignado [17]
    return np.sum([np.linalg.norm(pts[i] - cents[int(labs[i])])**2 for i in range(len(pts))])

if st.session_state.step > 0:
    st.write(f"**Iteración:** {st.session_state.step}")
    st.write(f"**Inercia actual:** {calculate_inertia():.4f}")
    st.info("La inercia baja cuando los clientes están más cerca de sus centroides [18].")
