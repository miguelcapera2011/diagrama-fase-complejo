import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# Configuración de estilo y página
st.set_page_config(page_title="K-Means Master", layout="wide")
st.title("Segmentación de Clientes: El Algoritmo K-Means Completo")

# --- 1. CONTEXTO Y DATOS (Basado en el video [1, 2]) ---
st.markdown("""
Esta app simula la segmentación de clientes bancarios basada en:
1. **Saldo** en cuenta de ahorros.
2. **Transacciones** con tarjeta de crédito.
3. **Antigüedad** del cliente (añadida para la visualización 3D).
""")

@st.cache_data
def load_data():
    np.random.seed(42)
    # Generamos 3 grupos naturales como en el video
    g1 = np.random.normal(loc=[1, 3, 4], scale=[2, 1, 0.5], size=(20, 3)) # Clientes "Básicos"
    g2 = np.random.normal(loc=[3, 5, 6], scale=[1, 4, 7], size=(20, 3)) # Clientes "Activos"
    g3 = np.random.normal(loc=[3, 8], scale=[1, 7, 9], size=(20, 3)) # Clientes "Ahorradores"
    data = np.vstack([g1, g2, g3])
    return pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])

df_raw = load_data()

# --- 2. PREPROCESAMIENTO (Paso crítico: Escalamiento [8, 10]) ---
# El video enfatiza que K-means es susceptible a las escalas (ej. 50,000 saldo vs 20 transacciones)
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Preprocesamiento (MinMaxScaler)")
    st.write("Datos originales vs Datos escalados (0 a 1) para evitar sesgos [8, 11].")
    st.dataframe(df_scaled.head(5))

# --- 3. MÉTODO DEL CODO (Para elegir K [5, 12, 13]) ---
with col2:
    st.subheader("2. Determinación de K (Método del Codo)")
    inercias = []
    k_range = range(1, 11)
    for i in k_range:
        km = KMeans(n_clusters=i, random_state=42, n_init=10)
        km.fit(df_scaled)
        inercias.append(km.inertia_)
    
    fig_elbow = go.Figure(data=go.Scatter(x=list(k_range), y=inercias, mode='lines+markers'))
    fig_elbow.update_layout(title="Inercia vs Número de Clusters", height=300, margin=dict(t=30, b=0))
    st.plotly_chart(fig_elbow, use_container_width=True)
    st.caption("El 'codo' indica el balance óptimo entre K pequeña e inercia baja [5].")

# --- 4. SIMULACIÓN SECUENCIAL (El corazón del algoritmo [4, 14, 15]) ---
st.divider()
st.subheader("3. Ejecución Secuencial del Algoritmo")

k_opt = st.sidebar.slider("Selecciona K para la simulación", 2, 6, 3)

if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar Centroides"):
    # Paso 1: Inicialización aleatoria [4, 16]
    st.session_state.centroids = df_scaled.sample(k_opt).values
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.iteration = 0
    st.session_state.history_inertia = []

def step_kmeans():
    data = df_scaled.values
    curr_centroids = st.session_state.centroids
    
    # Paso 2: Asignación por Distancia Euclidiana [14, 17]
    dist = np.linalg.norm(data[:, np.newaxis] - curr_centroids, axis=2)
    new_labels = np.argmin(dist, axis=1)
    
    # Paso 3: Actualización (Promedio de puntos) [15, 18]
    new_centroids = np.array([data[new_labels == i].mean(axis=0) if len(data[new_labels == i]) > 0 
                             else curr_centroids[i] for i in range(k_opt)])
    
    # Cálculo de Inercia (Distancia al cuadrado) [19]
    inertia = np.sum([np.linalg.norm(data[i] - new_centroids[new_labels[i]])**2 for i in range(len(data))])
    
    st.session_state.labels = new_labels
    st.session_state.centroids = new_centroids
    st.session_state.iteration += 1
    st.session_state.history_inertia.append(inertia)

c_ctrl1, c_ctrl2 = st.columns([9, 20])
with c_ctrl1:
    if st.button("Siguiente Paso (Iterar)"):
        step_kmeans()
    st.write(f"**Iteración:** {st.session_state.iteration}")
    if st.session_state.history_inertia:
        st.write(f"**Inercia:** {st.session_state.history_inertia[-1]:.4f}")

# --- 5. VISUALIZACIÓN 3D SIN CUADRÍCULAS ---
fig = go.Figure()

# Puntos de Clientes (con etiquetas de cluster [21, 22])
fig.add_trace(go.Scatter3d(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'], z=df_scaled['Antigüedad'],
    mode='markers',
    marker=dict(size=5, color=st.session_state.labels, colorscale='Viridis', opacity=0.8),
    name="Clientes"
))

# Centroides (Cruces rojas como en el video [23])
fig.add_trace(go.Scatter3d(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1], 
    z=st.session_state.centroids[:, 2],
    mode='markers',
    marker=dict(size=12, color='red', symbol='x', line=dict(width=3, color='black')),
    name="Centroides"
))

# Configuración para quitar cuadrículas y cajas
fig.update_layout(
    scene=dict(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
        zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=0), height=600
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
**¿Qué está pasando?**
1. Los centroides (X) se mueven al **promedio** de los puntos asignados [15].
2. Los clientes cambian de color cuando un centroide diferente queda más cerca (distancia euclidiana) [24, 25].
3. El proceso termina cuando los centroides dejan de moverse [25].
""")
