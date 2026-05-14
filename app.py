import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración visual de la app
st.set_page_config(page_title="K-Means 3D Experience", layout="wide")

st.title("🧶 K-Means 3D: Visualización de Distancias y Movimiento")
st.markdown("Basado en el dataset **USArrests**, exploramos el algoritmo paso a paso.")

# 1. CARGA DE DATOS (Corrección del error previo)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # Corrección: Accedemos al índice 0 para renombrar la columna de estados
    df.rename(columns={df.columns: 'State'}, inplace=True)
    return df

df_raw = load_data()
variables = ['Murder', 'Assault', 'UrbanPop', 'Rape']

# 2. PREPROCESAMIENTO (Fuentes: [1], [2])
# Estandarizamos para evitar sesgos por escalas (ej. Assault vs Murder)
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_raw[variables])

# 3. PCA PARA 3D (Fuentes: [3], [4])
# Reducimos las 4 variables originales a 3 dimensiones visuales
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Control de la simulación
st.sidebar.header("Control del Algoritmo")
k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
paso = st.sidebar.select_slider("Fase del Proceso", options=[
    "1. Puntos Base", 
    "2. Inicializar Centroides", 
    "3. Enlazar por Distancia", 
    "4. Nueva Posición (Promedio)"
])

# Lógica del algoritmo (Semilla fija 42 como en la fuente [5])
np.random.seed(42)
idx_inicio = np.random.choice(len(df_pca), k, replace=False)
centroides_ini = df_pca.iloc[idx_inicio].values

# Cálculo de distancias y etiquetas (Fuentes: [6], [7])
distancias = pairwise_distances(df_pca, centroides_ini, metric='euclidean')
etiquetas = np.argmin(distancias, axis=1)

# Cálculo de nuevos centroides (Fuentes: [8], [9])
centroides_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k)])

# --- CONSTRUCCIÓN DEL GRÁFICO 3D ---
fig = go.Figure()
colores = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

# Visualización de los puntos de los Estados
fig.add_trace(go.Scatter3d(
    x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
    mode='markers',
    marker=dict(size=5, color=[colores[l] if paso != "1. Puntos Base" else 'white' for l in etiquetas], opacity=0.7),
    text=df_raw['State'], name="Estados"
))

if paso != "1. Puntos Base":
    for i in range(k):
        # Elegir posición del centroide según la fase
        pos_centroide = centroides_ini[i] if paso != "4. Nueva Posición (Promedio)" else centroides_nuevos[i]
        
        # Dibujar Centroide (Diamante grande)
        fig.add_trace(go.Scatter3d(
            x=[pos_centroide], y=[pos_centroide[10]], z=[pos_centroide[11]],
            mode='markers',
            marker=dict(size=12, color=colores[i], symbol='diamond', line=dict(width=2, color='white')),
            name=f"Centroide {i}"
        ))

        # VISUALIZACIÓN DE DISTANCIA EUCLIDIANA (Líneas de enlace)
        if paso == "3. Enlazar por Distancia":
            puntos_cluster = df_pca[etiquetas == i]
            for _, fila in puntos_cluster.iterrows():
                fig.add_trace(go.Scatter3d(
                    x=[fila['PC1'], centroides_ini[i, 0]],
                    y=[fila['PC2'], centroides_ini[i, 1]],
                    z=[fila['PC3'], centroides_ini[i, 2]],
                    mode='lines', line=dict(color=colores[i], width=1),
                    opacity=0.2, showlegend=False
                ))

        # VISUALIZACIÓN DEL MOVIMIENTO (Trayectoria al promedio)
        if paso == "4. Nueva Posición (Promedio)":
            fig.add_trace(go.Scatter3d(
                x=[centroides_ini[i, 0], centroides_nuevos[i, 0]],
                y=[centroides_ini[i, 1], centroides_nuevos[i, 1]],
                z=[centroides_ini[i, 2], centroides_nuevos[i, 2]],
                mode='lines+markers',
                line=dict(color='white', width=3, dash='dash'),
                marker=dict(size=4, color='white'),
                name=f"Trayecto C{i}"
            ))

# Configuración estética del escenario
fig.update_layout(
    scene=dict(
        xaxis=dict(title="PC1 (Homicidios/Asaltos)", backgroundcolor="#111", gridcolor="#333"),
        yaxis=dict(title="PC2 (Pob. Urbana)", backgroundcolor="#111", gridcolor="#333"),
        zaxis=dict(title="PC3 (Violaciones)", backgroundcolor="#111", gridcolor="#333"),
        bgcolor="black"
    ),
    paper_bgcolor="black",
    font=dict(color="white"),
    margin=dict(l=0, r=0, b=0, t=30),
    height=800
)

st.plotly_chart(fig, use_container_width=True)

# 4. EXPLICACIÓN DIDÁCTICA (Basada en fuentes)
if paso == "3. Enlazar por Distancia":
    st.info("**Concepto:** Se calcula la **distancia euclidiana** (la hipotenusa entre puntos) para asignar cada estado al centroide más cercano [7].")
elif paso == "4. Nueva Posición (Promedio)":
    st.success("**Concepto:** El centroide se mueve al **promedio geométrico** de todos los estados que tiene asignados, optimizando la agrupación [8].")

st.write("### Datos Originales (USArrests)")
st.dataframe(df_raw)
