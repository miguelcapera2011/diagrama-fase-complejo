import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# 1. Configuración de Estilo y Página
st.set_page_config(page_title="K-Means Pro Style", layout="wide")
st.title("Segmentación Bancaria: K-Means con Estilo Visual")

# Contexto basado en la fuente: Saldo y Transacciones [1]
st.markdown("""
Visualización del algoritmo **K-means** utilizando las variables de **Saldo** y **Transacciones**.
El objetivo es encontrar grupos naturales mediante **distancia euclidiana** e iteraciones [2, 5].
""")

# 2. Generación de Datos (2D) [1]
@st.cache_data
def load_data():
    np.random.seed(42)
    # Grupo 1: Saldo bajo, pocas transacciones
    g1 = np.random.normal(loc=[6, 7], scale=[1, 2], size=(20, 2))
    # Grupo 2: Saldo medio, muchas transacciones 
    g2 = np.random.normal(loc=[8, 9], scale=[1, 10], size=(20, 2))
    # Grupo 3: Saldo alto, transacciones moderadas [11]
    g3 = np.random.normal(loc=[6], scale=[4, 1.5], size=(20, 2))
    
    data = np.vstack([g1, g2, g3])
    return pd.DataFrame(data, columns=['Saldo', 'Transacciones'])

df_raw = load_data()

# 3. Preprocesamiento: Escalamiento [4]
# Convertimos valores a rango 0-1 para evitar sesgos por escalas diferentes [12]
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

# Sidebar: Configuración de K [10]
st.sidebar.header("Configuración de K")
k_val = st.sidebar.slider("Número de Clusters (K)", 2, 6, 3)

# Estado de la sesión para iteraciones secuenciales [5, 6]
if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar Algoritmo"):
    # Inicialización aleatoria dentro del plano de datos [7]
    st.session_state.centroids = df_scaled.sample(k_val).values
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.iteration = 0

def run_step():
    """Ejecuta un paso: Asignación y Actualización [5, 13]."""
    data = df_scaled.values
    curr_cents = st.session_state.centroids
    
    # PASO 1: Asignación por Distancia Euclidiana (Hipotenusa) [5]
    distances = np.linalg.norm(data[:, np.newaxis] - curr_cents, axis=2)
    labels = np.argmin(distances, axis=1)
    
    # PASO 2: Actualización (Promedio de las posiciones) [11, 13]
    new_cents = np.array([data[labels == i].mean(axis=0) if len(data[labels == i]) > 0 
                         else curr_cents[i] for i in range(k_val)])
    
    st.session_state.labels = labels
    st.session_state.centroids = new_cents
    st.session_state.iteration += 1

# Botón de control secuencial
if st.button(f"Siguiente Iteración ({st.session_state.iteration + 1})"):
    run_step()

# 4. Visualización con Estilo (Efecto 3D en Plano 2D y Ejes Invisibles)
fig = go.Figure()

# Sombra/Efecto de profundidad para los puntos (Círculos exteriores)
fig.add_trace(go.Scatter(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'],
    mode='markers',
    marker=dict(size=14, color='lightgrey', opacity=0.3),
    showlegend=False
))

# Puntos de Clientes con colores de cluster [14]
fig.add_trace(go.Scatter(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'],
    mode='markers',
    marker=dict(
        size=10, 
        color=st.session_state.labels, 
        colorscale='Viridis', 
        line=dict(width=1, color='white'), # Borde blanco para resaltar
        opacity=0.9
    ),
    name="Clientes"
))

# Centroides representados como cruces estilizadas [15]
fig.add_trace(go.Scatter(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1],
    mode='markers',
    marker=dict(
        size=18, 
        color='red', 
        symbol='x-thin', 
        line=dict(width=3, color='darkred')
    ),
    name="Centroides"
))

# Configuración de Ejes Casi Invisibles
fig.update_layout(
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        title="", 
        visible=False # Hace el eje casi invisible
    ),
    yaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        title="", 
        visible=False
    ),
    plot_bgcolor='white', # Fondo limpio
    margin=dict(l=20, r=20, t=20, b=20),
    height=600,
    showlegend=True,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

st.plotly_chart(fig, use_container_width=True)

# Información de Inercia (Métrica de calidad mencionada en la fuente) [16, 17]
def get_inertia():
    pts = df_scaled.values
    labs = st.session_state.labels
    cents = st.session_state.centroids
    return np.sum([np.linalg.norm(pts[i] - cents[int(labs[i])])**2 for i in range(len(pts))])

st.write(f"**Iteración:** {st.session_state.iteration} | **Inercia actual:** {get_inertia():.4f}")
st.info("La inercia indica qué tan pegados están los clientes a sus centroides; buscamos que este valor baje [17, 18].")
