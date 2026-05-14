import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# 1. CONFIGURACIÓN DE LA INTERFAZ
st.set_page_config(page_title="K-Means Master 3D", layout="wide")
st.title("Segmentación de Clientes: Algoritmo K-Means Completo")
st.markdown("""
Esta aplicación simula el proceso de **aprendizaje no supervisado** para encontrar patrones naturales (clusters) en datos bancarios [1, 3].
""")

# 2. GENERACIÓN DE DATOS (Corregido para 3D)
@st.cache_data
def load_data():
    np.random.seed(42)
    # Definimos 3 grupos con 3 coordenadas cada uno: [Saldo, Transacciones, Antigüedad]
    # Grupo 1: Saldo bajo, pocas transacciones [1, 4]
    g1 = np.random.normal(loc=[1, 5, 6], scale=[2, 1, 0.5], size=(20, 3))
    # Grupo 2: Saldo medio, muchas transacciones
    g2 = np.random.normal(loc=[5, 7, 8], scale=[1, 6, 9], size=(20, 3))
    # Grupo 3: Saldo alto, transacciones moderadas
    g3 = np.random.normal(loc=[5, 10], scale=[1, 6, 11], size=(20, 3))
    
    data = np.vstack([g1, g2, g3])
    return pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])

df_raw = load_data()

# 3. PREPROCESAMIENTO: ESCALAMIENTO (Concepto clave de la fuente [12, 13])
# K-means es susceptible a las escalas (ej. Saldo de 60,000 vs 20 transacciones).
# Usamos MinMaxScaler para llevar todo al rango [3] [14].
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_raw), columns=df_raw.columns)

# Visualización de datos en la App
col_data, col_elbow = st.columns(2)
with col_data:
    st.subheader("1. Preprocesamiento (MinMaxScaler)")
    st.write("Datos escalados para evitar sesgos por magnitud [13].")
    st.dataframe(df_scaled.head(8))

# 4. MÉTODO DEL CODO (Para determinar K óptimo [7, 15])
with col_elbow:
    st.subheader("2. Método del Codo (Inercia)")
    inercias = []
    for i in range(1, 11):
        km = KMeans(n_clusters=i, random_state=42, n_init=10)
        km.fit(df_scaled)
        inercias.append(km.inertia_)
    
    fig_elbow = go.Figure(data=go.Scatter(x=list(range(1, 11)), y=inercias, mode='lines+markers'))
    fig_elbow.update_layout(title="Balance entre K e Inercia [7]", height=300, margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig_elbow, use_container_width=True)

# 5. SIMULACIÓN SECUENCIAL (Iteraciones del algoritmo [5, 16])
st.divider()
st.subheader("3. Ejecución Secuencial del Algoritmo")

k_user = st.sidebar.slider("Selecciona K (Clusters)", 2, 6, 3)

# Inicialización de estado
if 'centroids' not in st.session_state or st.sidebar.button("Reiniciar Algoritmo"):
    # Paso 1: Inicialización aleatoria de centroides [6]
    st.session_state.centroids = df_scaled.sample(k_user).values
    st.session_state.labels = np.zeros(len(df_scaled))
    st.session_state.iteration = 0
    st.session_state.history_inertia = []

def run_step():
    data = df_scaled.values
    curr_cents = st.session_state.centroids
    
    # PASO A: Asignación por Distancia Euclidiana (Hipotenusa) [16]
    distances = np.linalg.norm(data[:, np.newaxis] - curr_cents, axis=2)
    labels = np.argmin(distances, axis=1)
    
    # PASO B: Actualización (Promedio de los puntos asignados) [4, 11]
    new_cents = np.array([data[labels == i].mean(axis=0) if len(data[labels == i]) > 0 
                         else curr_cents[i] for i in range(k_user)])
    
    # Cálculo de Inercia: Suma de distancias al cuadrado [17]
    inertia = np.sum([np.linalg.norm(data[i] - new_cents[labels[i]])**2 for i in range(len(data))])
    
    st.session_state.labels = labels
    st.session_state.centroids = new_cents
    st.session_state.iteration += 1
    st.session_state.history_inertia.append(inertia)

# Botón de iteración
if st.button(f"Ejecutar Iteración {st.session_state.iteration + 1}"):
    run_step()

st.write(f"Iteración: **{st.session_state.iteration}** | Inercia Actual: **{st.session_state.history_inertia[-1] if st.session_state.history_inertia else 0:.4f}**")

# 6. VISUALIZACIÓN 3D SIN CUADRÍCULAS
fig = go.Figure()

# Puntos de Clientes
fig.add_trace(go.Scatter3d(
    x=df_scaled['Saldo'], y=df_scaled['Transacciones'], z=df_scaled['Antigüedad'],
    mode='markers',
    marker=dict(size=5, color=st.session_state.labels, colorscale='Viridis', opacity=0.8),
    name="Clientes"
))

# Centroides (Cruces rojas como en el video [18])
fig.add_trace(go.Scatter3d(
    x=st.session_state.centroids[:, 0], 
    y=st.session_state.centroids[:, 1], 
    z=st.session_state.centroids[:, 2],
    mode='markers',
    marker=dict(size=12, color='red', symbol='x', line=dict(width=3, color='black')),
    name="Centroides"
))

# Estilo para quitar cuadrículas, fondos y ejes (Vista limpia)
fig.update_layout(
    scene=dict(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
        zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", showbackground=False),
    ),
    margin=dict(l=0, r=0, b=0, t=0), height=700
)

st.plotly_chart(fig, use_container_width=True)

st.info("**Conceptos aplicados:** Escalamiento MinMaxScaler [14], Distancia Euclidiana [16], Actualización por Promedios [4] e Inercia como métrica de cohesión [19].")
