import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# 1. CONFIGURACIÓN Y CONTEXTO (Basado en la fuente [3])
st.set_page_config(page_title="K-Means Master", layout="wide")
st.title("Segmentación Bancaria: Algoritmo K-Means 3D")
st.markdown("""
Esta aplicación recrea el proceso completo de **aprendizaje no supervisado** para agrupar clientes según su **Saldo**, **Transacciones** y **Antigüedad** [3, 4].
""")

@st.cache_data
def load_data():
    np.random.seed(42)
    # CORRECCIÓN DE DIMENSIONES: Cada grupo tiene 3 coordenadas para loc y scale
    # Clientes con poco saldo y pocas transacciones
    g1 = np.random.normal(loc=[3, 5, 6], scale=[2, 1, 0.5], size=(20, 3)) 
    # Clientes con saldo medio y transacciones altas
    g2 = np.random.normal(loc=[5, 7, 8], scale=[1, 3, 4], size=(20, 3)) 
    # Clientes con mucho saldo pero pocas transacciones (Ahorradores)
    g3 = np.random.normal(loc=[2, 9], scale=[3, 10], size=(20, 3)) 
    
    data = np.vstack([g1, g2, g3])
    return pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])

df_raw = load_data()

# 2. PREPROCESAMIENTO: ESCALAMIENTO (Basado en las fuentes [9, 11])
# Es crítico porque el algoritmo es susceptible a las diferentes escalas de los datos.
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

col_data, col_elbow = st.columns(2)

with col_data:
    st.subheader("1. Datos Escalados (MinMaxScaler)")
    st.write("Convertimos los valores al rango [4] para evitar sesgos [12].")
    st.dataframe(df_scaled.head(5))

# 3. MÉTODO DEL CODO (Basado en la fuente [13])
with col_elbow:
    st.subheader("2. Método del Codo")
    inercias = []
    for i in range(1, 11):
        km = KMeans(n_clusters=i, random_state=42, n_init=10)
        km.fit(df_scaled)
        inercias.append(km.inertia_)
    
    fig_elbow = go.Figure(data=go.Scatter(x=list(range(1, 11)), y=inercias, mode='lines+markers'))
    fig_elbow.update_layout(title="Inercia vs Número de Clusters", height=300, margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig_elbow, use_container_width=True)

# 4. SIMULACIÓN SECUENCIA (Basado en las fuentes [2, 5, 6])
st.divider()
st.subheader("3. Ejecución Iterativa")

k_opt = st.sidebar.slider("Selecciona K para simular", 2, 6, 3)

if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar Algoritmo"):
    # Inicialización aleatoria de centroides [6]
    st.session_state.centroids = df_scaled.sample(k_opt).values
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.iteration = 0
    st.session_state.history_inertia = []

def run_step():
    data = df_scaled.values
    curr_cents = st.session_state.centroids
    
    # Asignación por Distancia Euclidiana [14]
    distances = np.linalg.norm(data[:, np.newaxis] - curr_cents, axis=2)
    labels = np.argmin(distances, axis=1)
    
    # Actualización por Promedio [2, 15]
    new_cents = np.array([data[labels == i].mean(axis=0) if len(data[labels == i]) > 0 
                         else curr_cents[i] for i in range(k_opt)])
    
    # Cálculo de Inercia (Distancia al cuadrado) [16]
    inertia = np.sum([np.linalg.norm(data[i] - new_cents[labels[i]])**2 for i in range(len(data))])
    
    st.session_state.labels = labels
    st.session_state.centroids = new_cents
    st.session_state.iteration += 1
    st.session_state.history_inertia.append(inertia)

if st.button(f"Ejecutar Iteración {st.session_state.iteration + 1}"):
    run_step()

st.write(f"Iteración actual: **{st.session_state.iteration}** | Inercia: **{st.session_state.history_inertia[-1] if st.session_state.history_inertia else 0:.4f}**")

# 5. VISUALIZACIÓN 3D SIN CUADRÍCULAS
fig = go.Figure()

# Clientes
fig.add_trace(go.Scatter3d(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'], z=df_scaled['Antigüedad'],
    mode='markers',
    marker=dict(size=5, color=st.session_state.labels, colorscale='Viridis', opacity=0.8),
    name="Clientes"
))

# Centroides (Cruces rojas [17])
fig.add_trace(go.Scatter3d(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1], 
    z=st.session_state.centroids[:, 2],
    mode='markers',
    marker=dict(size=12, color='red', symbol='x', line=dict(width=3, color='black')),
    name="Centroides"
))

# Eliminar cuadrículas y fondos para vista limpia
fig.update_layout(
    scene=dict(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
        zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
    ),
    margin=dict(l=0, r=0, b=0, t=0), height=600
)

st.plotly_chart(fig, use_container_width=True)
st.info("Nota: Los centroides se mueven iterativamente hacia el promedio de sus puntos asignados hasta que ya no cambian de posición [18].")
