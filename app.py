import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la página
st.set_page_config(page_title="K-Means 3D Experience", layout="wide")

st.title("🧶 Laboratorio K-Means 3D: USArrests")
st.markdown("Visualización del proceso técnico: distancias euclidianas y movimiento de centroides.")

# 1. Carga de datos (Solución al error 'unhashable type: Index')
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # CORRECCIÓN: Se agrega  para tomar solo el nombre de la primera columna
    df.rename(columns={df.columns: 'State'}, inplace=True) 
    return df

df_raw = load_data()
features = ['Murder', 'Assault', 'UrbanPop', 'Rape']

# 2. Estandarización (Fuente [2, 3])
# El algoritmo es sensible a las escalas (ej. Assault vs Murder)
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_raw[features])

# 3. PCA para visualización 3D (Fuente [4, 5])
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Controles
st.sidebar.header("Parámetros")
k = st.sidebar.slider("Clusters (k)", 2, 5, 4)
fase = st.sidebar.select_slider("Fase del proceso", options=[
    "1. Datos Base", "2. Asignación (Distancias)", "3. Actualización (Movimiento)"
])

# Lógica del Algoritmo (Fuente [6-8])
np.random.seed(42)
idx_ini = np.random.choice(len(df_pca), k, replace=False)
centroides_ini = df_pca.iloc[idx_ini].values

# Cálculo de Distancia Euclidiana (Fuente [9, 10])
distancias = pairwise_distances(df_pca, centroides_ini, metric='euclidean')
etiquetas = np.argmin(distancias, axis=1)

# Cálculo de Nueva Posición (Promedio) (Fuente [11, 12])
centroides_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k)])

# --- Visualización 3D Interactiva ---
fig = go.Figure()
colores = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

# Puntos de los Estados
fig.add_trace(go.Scatter3d(
    x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
    mode='markers',
    marker=dict(size=5, color=[colores[l] if fase != "1. Datos Base" else 'white' for l in etiquetas], opacity=0.7),
    text=df_raw['State'], name="Estados"
))

if fase != "1. Datos Base":
    for i in range(k):
        # Centroide según la fase
        c_actual = centroides_ini[i] if fase != "3. Actualización (Movimiento)" else centroides_nuevos[i]
        
        fig.add_trace(go.Scatter3d(
            x=[c_actual], y=[c_actual[13]], z=[c_actual[14]],
            mode='markers',
            marker=dict(size=12, color=colores[i], symbol='diamond', line=dict(width=2, color='white')),
            name=f"Centroide {i}"
        ))

        # Visualizar Distancia Euclidiana (Líneas de enlace)
        if fase == "2. Asignación (Distancias)":
            puntos_c = df_pca[etiquetas == i]
            for _, fila in puntos_c.iterrows():
                fig.add_trace(go.Scatter3d(
                    x=[fila['PC1'], centroides_ini[i, 0]],
                    y=[fila['PC2'], centroides_ini[i, 1]],
                    z=[fila['PC3'], centroides_ini[i, 2]],
                    mode='lines', line=dict(color=colores[i], width=1),
                    opacity=0.2, showlegend=False
                ))

        # Visualizar Movimiento (Trayectoria al promedio)
        if fase == "3. Actualización (Movimiento)":
            fig.add_trace(go.Scatter3d(
                x=[centroides_ini[i, 0], centroides_nuevos[i, 0]],
                y=[centroides_ini[i, 1], centroides_nuevos[i, 1]],
                z=[centroides_ini[i, 2], centroides_nuevos[i, 2]],
                mode='lines+markers', line=dict(color='white', width=3, dash='dash'),
                marker=dict(size=4, color='white'), name=f"Trayecto C{i}"
            ))

fig.update_layout(
    scene=dict(xaxis_title="PC1", yaxis_title="PC2", zaxis_title="PC3", bgcolor="black"),
    paper_bgcolor="black", font=dict(color="white"), height=800, margin=dict(l=0, r=0, b=0, t=30)
)

st.plotly_chart(fig, use_container_width=True)

# Explicación basada en fuentes
if fase == "2. Asignación (Distancias)":
    st.info("Cada estado se enlaza al centroide más cercano calculando la **distancia euclidiana** (la hipotenusa en el espacio) [9, 10].")
elif fase == "3. Actualización (Movimiento)":
    st.success("El centroide se desplaza a la nueva posición calculada mediante el **promedio** de los puntos asignados [11, 12].")

st.dataframe(df_raw.head(10))
