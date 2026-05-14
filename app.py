import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# Configuración de la página
st.set_page_config(page_title="K-Means 3D Secuencial", layout="wide")
st.title("Simulador Secuencial de K-Means 3D")
st.write("Basado en el algoritmo de aprendizaje no supervisado para segmentación [4].")

# 1. Generación de Datos Sintéticos en 3D
@st.cache_data
def generate_data():
    np.random.seed(42)
    # Creamos 3 grupos con coordenadas (Saldo, Transacciones, Antigüedad)
    g1 = np.random.normal(loc=[1, 5, 6], scale=[2, 1, 0.5], size=(20, 3))
    g2 = np.random.normal(loc=[7, 8], scale=[1, 6, 9], size=(20, 3))
    g3 = np.random.normal(loc=[5, 10], scale=[6, 9, 11], size=(20, 3))
    
    data = np.vstack([g1, g2, g3])
    df = pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])
    return df

df_raw = generate_data()

# 2. Preprocesamiento: Escalamiento (Paso crítico según las fuentes [3, 8])
# El algoritmo es susceptible a las escalas, por lo que llevamos todo al rango 0-1.
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

# Sidebar para controles
st.sidebar.header("Configuración")
k_valor = st.sidebar.slider("Selecciona K (Número de clusters)", min_value=2, max_value=6, value=3)

# Inicialización de estado para persistir datos entre interacciones de Streamlit
if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar Algoritmo"):
    # Inicialización aleatoria de centroides dentro del espacio de datos [1]
    st.session_state.centroids = df_scaled.sample(k_valor).values
    st.session_state.iteration = 0
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.converged = False

def run_step():
    """Ejecuta una iteración del algoritmo: Asignación y Actualización."""
    data = df_scaled.values
    centroids = st.session_state.centroids
    
    # PASO A: Asignación por Distancia Euclidiana [12]
    distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
    new_labels = np.argmin(distances, axis=1)
    
    # PASO B: Actualización (Promedio de los puntos asignados [2, 13])
    new_centroids = np.array([
        data[new_labels == i].mean(axis=0) if len(data[new_labels == i]) > 0 else centroids[i]
        for i in range(k_valor)
    ])
    
    # Verificar convergencia (si los centroides ya no cambian [14])
    if np.allclose(centroids, new_centroids):
        st.session_state.converged = True
    
    st.session_state.centroids = new_centroids
    st.session_state.labels = new_labels
    st.session_state.iteration += 1

# Botón para avanzar paso a paso
if not st.session_state.converged:
    if st.button(f"Ejecutar Iteración {st.session_state.iteration + 1}"):
        run_step()
else:
    st.success(f"El algoritmo ha convergido en la iteración {st.session_state.iteration}.")

# 3. Visualización 3D con Plotly
fig = go.Figure()

# Dibujar los puntos de datos con sus etiquetas actuales
fig.add_trace(go.Scatter3d(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'], z=df_scaled['Antigüedad'],
    mode='markers',
    marker=dict(size=5, color=st.session_state.labels, colorscale='Viridis', opacity=0.7),
    name="Clientes (Puntos)"
))

# Dibujar los centroides (como cruces rojas según el video [15])
fig.add_trace(go.Scatter3d(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1], 
    z=st.session_state.centroids[:, 2],
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
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# Mostrar métrica de Inercia (mencionada en la fuente [16, 17])
def calculate_inertia():
    data = df_scaled.values
    centroids = st.session_state.centroids
    labels = st.session_state.labels
    inertia = 0
    for i in range(len(data)):
        centroid = centroids[int(labels[i])]
        inertia += np.sum((data[i] - centroid)**2)
    return inertia

if st.session_state.iteration > 0:
    st.write(f"**Inercia actual:** {calculate_inertia():.4f}")
    st.info("La inercia mide qué tan pegados están los clientes a sus centroides [18].")
