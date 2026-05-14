import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la página
st.set_page_config(page_title="K-Means 3D Journey", layout="wide")

st.title("🧶 Visualizador K-Means: Del Enlace al Movimiento")
st.markdown("""
Esta app desglosa el algoritmo **K-medias** utilizando el dataset **USArrests**. 
Observa cómo se miden las distancias y cómo los centroides buscan el 'centro' de los datos [4, 5].
""")

# 1. Carga de datos desde la fuente oficial
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # Renombrar la primera columna para identificar los estados [6, 7]
    cols = list(df.columns)
    cols = 'State'
    df.columns = cols
    return df

df_raw = load_data()
features = ['Murder', 'Assault', 'UrbanPop', 'Rape'] # Variables del estudio [6, 8]

# 2. Preprocesamiento: Escalado y PCA [9-11]
# El escalado es vital porque variables como Assault dominan la escala [12, 13].
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_raw[features])

# Usamos PCA para proyectar 4 variables en un plano 3D visualizable [14, 15].
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Controles de la simulación
st.sidebar.header("Parámetros del Algoritmo")
k = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
etapa = st.sidebar.select_slider("Fase del Proceso", options=[
    "Puntos Iniciales", 
    "Asignación (Distancias)", 
    "Actualización (Movimiento)"
])

# Lógica del Algoritmo (Semilla 42 para reproducibilidad como en la fuente [16, 17])
np.random.seed(42)
indices_ini = np.random.choice(len(df_pca), k, replace=False)
centroides_ini = df_pca.iloc[indices_ini].values

# Cálculo de Distancia Euclidiana y Etiquetas [1, 18, 19]
distancias = pairwise_distances(df_pca, centroides_ini, metric='euclidean')
etiquetas = np.argmin(distancias, axis=1)

# Cálculo de Nueva Posición (Promedio de los puntos) [20, 21]
centroides_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k)])

# --- CONSTRUCCIÓN DEL GRÁFICO 3D INTERACTIVO ---
fig = go.Figure()
colores = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

# Visualización de los Estados (Datos)
fig.add_trace(go.Scatter3d(
    x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
    mode='markers',
    marker=dict(size=5, color=[colores[l] if etapa != "Puntos Iniciales" else 'white' for l in etiquetas], opacity=0.8),
    text=df_raw['State'], name="Estados"
))

for i in range(k):
    # Definir centroide a mostrar
    pos_c = centroides_ini[i] if etapa != "Actualización (Movimiento)" else centroides_nuevos[i]
    
    # Dibujar Centroide (Diamante resaltado [22, 23])
    fig.add_trace(go.Scatter3d(
        x=[pos_c], y=[pos_c[6]], z=[pos_c[24]],
        mode='markers',
        marker=dict(size=14, color=colores[i], symbol='diamond', line=dict(width=3, color='white')),
        name=f"Centroide {i}"
    ))

    # ENLACE POR DISTANCIA EUCLIDIANA (Mecánica de la 'Hipotenusa' [19, 25])
    if etapa == "Asignación (Distancias)":
        cluster_points = df_pca[etiquetas == i]
        for _, fila in cluster_points.iterrows():
            fig.add_trace(go.Scatter3d(
                x=[fila['PC1'], centroides_ini[i, 0]],
                y=[fila['PC2'], centroides_ini[i, 1]],
                z=[fila['PC3'], centroides_ini[i, 2]],
                mode='lines', line=dict(color=colores[i], width=1.5),
                opacity=0.3, showlegend=False
            ))

    # TRAYECTORIA DE ACTUALIZACIÓN (Movimiento hacia el promedio [2, 26])
    if etapa == "Actualización (Movimiento)":
        fig.add_trace(go.Scatter3d(
            x=[centroides_ini[i, 0], centroides_nuevos[i, 0]],
            y=[centroides_ini[i, 1], centroides_nuevos[i, 1]],
            z=[centroides_ini[i, 2], centroides_nuevos[i, 2]],
            mode='lines+markers',
            line=dict(color='white', width=4, dash='dash'),
            marker=dict(size=5, color='white'),
            name=f"Trayecto C{i}"
        ))

# Estética del escenario 3D
fig.update_layout(
    scene=dict(
        xaxis=dict(title="PC1 (Homicidios/Asaltos)", backgroundcolor="#0e1117", gridcolor="#333"),
        yaxis=dict(title="PC2 (Población)", backgroundcolor="#0e1117", gridcolor="#333"),
        zaxis=dict(title="PC3 (Violaciones)", backgroundcolor="#0e1117", gridcolor="#333"),
        bgcolor="#0e1117"
    ),
    paper_bgcolor="#0e1117", font=dict(color="white"),
    height=850, margin=dict(l=0, r=0, b=0, t=30)
)

st.plotly_chart(fig, use_container_width=True)

# Explicaciones teóricas extraídas de las fuentes
if etapa == "Asignación (Distancias)":
    st.info("💡 **Concepto:** Cada estado se une al centroide más cercano calculando la **distancia euclidiana**. Visualmente, es la línea más corta entre el punto y el diamante [1, 18].")
elif etapa == "Actualización (Movimiento)":
    st.success("💡 **Concepto:** El centroide se desplaza al **promedio** de las coordenadas de todos los estados que tiene asignados. La línea punteada muestra este 'viaje' [2, 21].")

st.write("### Base de Datos Original (USArrests) [6, 24]")
st.dataframe(df_raw)
