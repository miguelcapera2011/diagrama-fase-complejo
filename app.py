import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# 1. CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="K-Means: Saldo vs Transacciones", layout="wide")
st.title("Segmentación Bancaria (K-Means 2D)")
st.markdown("""
Esta aplicación utiliza las **dos características** mencionadas en las fuentes: 
**Saldo** y **Transacciones** [1]. El objetivo es encontrar patrones naturales sin etiquetas previas [2].
""")

# 2. GENERACIÓN DE DATOS (Basado estrictamente en los 2 valores de la fuente)
@st.cache_data
def load_data():
    np.random.seed(42)
    # Grupo 1: Saldo bajo, pocas transacciones
    g1 = np.random.normal(loc=[3, 4], scale=[1, 2], size=(20, 2))
    # Grupo 2: Saldo medio, muchas transacciones 
    g2 = np.random.normal(loc=[5, 6], scale=[1, 7], size=(20, 2))
    # Grupo 3: Saldo alto, transacciones moderadas
    g3 = np.random.normal(loc=[8], scale=[4, 1.5], size=(20, 2))
    
    data = np.vstack([g1, g2, g3])
    # Usamos exactamente los nombres del video [9]
    return pd.DataFrame(data, columns=['Saldo', 'Transacciones'])

df_raw = load_data()

# 3. PREPROCESAMIENTO: ESCALAMIENTO (Concepto clave de la fuente [10, 11])
# Se usa MinMaxScaler porque el algoritmo es susceptible a las diferentes escalas [10].
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

# 4. MÉTODO DEL CODO (Mencionado en la fuente [12])
st.subheader("1. Análisis de Inercia (Método del Codo)")
inercias = []
for i in range(1, 11):
    km = KMeans(n_clusters=i, random_state=42, n_init=10)
    km.fit(df_scaled)
    inercias.append(km.inertia_)

fig_elbow = go.Figure(data=go.Scatter(x=list(range(1, 11)), y=inercias, mode='lines+markers'))
fig_elbow.update_layout(height=300, xaxis_title="K (Clusters)", yaxis_title="Inercia")
st.plotly_chart(fig_elbow, use_container_width=True)

# 5. EJECUCIÓN SECUENCIAL (Algoritmo Iterativo [3, 13])
st.divider()
st.subheader("2. Simulación Paso a Paso")
k_user = st.sidebar.slider("Selecciona K", 2, 6, 3)

if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar"):
    # Paso 1: Inicialización aleatoria de centroides [4]
    st.session_state.centroids = df_scaled.sample(k_user).values
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.iteration = 0
    st.session_state.current_inertia = 0

def run_step():
    data = df_scaled.values
    centroids = st.session_state.centroids
    
    # Paso 2: Asignación por Distancia Euclidiana [13]
    distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
    labels = np.argmin(distances, axis=1)
    
    # Paso 3: Actualización por Promedio [14, 15]
    new_centroids = np.array([data[labels == i].mean(axis=0) if len(data[labels == i]) > 0 
                             else centroids[i] for i in range(k_user)])
    
    # Cálculo de Inercia: Distancia al cuadrado [16]
    inertia = np.sum([np.linalg.norm(data[i] - new_centroids[labels[i]])**2 for i in range(len(data))])
    
    st.session_state.labels = labels
    st.session_state.centroids = new_centroids
    st.session_state.iteration += 1
    st.session_state.current_inertia = inertia

if st.button(f"Siguiente Paso (Iteración {st.session_state.iteration + 1})"):
    run_step()

st.write(f"Iteración: **{st.session_state.iteration}** | Inercia: **{st.session_state.current_inertia:.4f}**")

# 6. VISUALIZACIÓN 2D SIN CUADRÍCULAS
fig = go.Figure()

# Puntos de Clientes
fig.add_trace(go.Scatter(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'],
    mode='markers',
    marker=dict(size=10, color=st.session_state.labels, colorscale='Viridis', opacity=0.8),
    name="Clientes"
))

# Centroides (Cruces rojas como en el video [17])
fig.add_trace(go.Scatter(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1],
    mode='markers',
    marker=dict(size=15, color='red', symbol='x', line=dict(width=2, color='black')),
    name="Centroides"
))

# Diseño limpio sin cuadrículas ni ejes visibles
fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    plot_bgcolor='rgba(0,0,0,0)', # Fondo transparente
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.info("El proceso se detiene cuando la posición de las cruces rojas (centroides) ya no cambia [8].")
