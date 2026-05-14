import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

# Configuración de la página
st.set_page_config(page_title="K-Means 3D: Análisis de USArrests", layout="wide")

st.title("🧶 Visualizador K-Means: Proceso Completo en 3D")
st.markdown("""
Esta aplicación permite entender el algoritmo K-means paso a paso, desde la asignación por **distancia euclidiana** 
hasta el movimiento de los **centroides** basándose en el promedio de sus puntos.
""")

# 1. Carga de datos completa (Fuente: URL proporcionada)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv"
    df = pd.read_csv(url)
    # Renombrar la columna de estados para que sea descriptiva [1, 2]
    df.rename(columns={df.columns: 'State'}, inplace=True)
    return df

df_original = load_data()
features = ['Murder', 'Assault', 'UrbanPop', 'Rape'] # Variables del dataset [1]

# 2. Preprocesamiento: Escalado (Fuente)
# El escalado es crítico porque variables como Assault tienen magnitudes mucho mayores [3, 4].
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_original[features])

# 3. Reducción a 3D con PCA (Fuente)
# Reducimos las 4 variables originales a 3 Componentes Principales para visualizar en 3D [5-7].
pca = PCA(n_components=3)
data_3d = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data_3d, columns=['PC1', 'PC2', 'PC3'])

# Sidebar: Controles de la simulación
st.sidebar.header("Parámetros del Algoritmo")
k_val = st.sidebar.slider("Número de Clusters (k)", 2, 5, 4)
fase = st.sidebar.radio("Selecciona la Fase:", 
                         ["Puntos Base", "Asignación (Distancia)", "Actualización (Movimiento)"])

# Lógica del algoritmo (Semilla fija para reproducibilidad [8, 9])
np.random.seed(42)
indices_iniciales = np.random.choice(len(df_pca), k_val, replace=False)
centroides_iniciales = df_pca.iloc[indices_iniciales].values

# Cálculo de distancias euclidianas y etiquetas [10, 11]
distancias = pairwise_distances(df_pca, centroides_iniciales, metric='euclidean')
etiquetas = np.argmin(distancias, axis=1)

# Cálculo de la nueva posición de centroides (Promedio [12, 13])
centroides_nuevos = np.array([df_pca[etiquetas == i].mean(axis=0) for i in range(k_val)])

# --- Visualización 3D Interactiva con Plotly ---
fig = go.Figure()
colores = ['#EF553B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']

# Capa de puntos de datos
fig.add_trace(go.Scatter3d(
    x=df_pca['PC1'], y=df_pca['PC2'], z=df_pca['PC3'],
    mode='markers',
    marker=dict(size=5, color=[colores[l] if fase != "Puntos Base" else 'white' for l in etiquetas], opacity=0.8),
    text=df_original['State'],
    name="Estados (Datos)"
))

for i in range(k_val):
    # Definir centroide a mostrar según la fase
    centroide_actual = centroides_iniciales[i] if fase != "Actualización (Movimiento)" else centroides_nuevos[i]
    
    # Dibujar Centroide
    fig.add_trace(go.Scatter3d(
        x=[centroide_actual], y=[centroide_actual[1]], z=[centroide_actual[2]],
        mode='markers',
        marker=dict(size=12, color=colores[i], symbol='diamond', line=dict(width=2, color='black')),
        name=f"Centroide {i}"
    ))

    # ENLACE DE DISTANCIA EUCLIDIANA (Visualización de la hipotenusa [11, 14])
    if fase == "Asignación (Distancia)":
        puntos_cluster = df_pca[etiquetas == i]
        for _, fila in puntos_cluster.iterrows():
            fig.add_trace(go.Scatter3d(
                x=[fila['PC1'], centroides_iniciales[i, 0]],
                y=[fila['PC2'], centroides_iniciales[i, 1]],
                z=[fila['PC3'], centroides_iniciales[i, 2]],
                mode='lines',
                line=dict(color=colores[i], width=1),
                opacity=0.2, showlegend=False
            ))

    # MOVIMIENTO DE LOS CENTROIDES (Trayectoria al promedio [12, 15])
    if fase == "Actualización (Movimiento)":
        fig.add_trace(go.Scatter3d(
            x=[centroides_iniciales[i, 0], centroides_nuevos[i, 0]],
            y=[centroides_iniciales[i, 1], centroides_nuevos[i, 1]],
            z=[centroides_iniciales[i, 2], centroides_nuevos[i, 2]],
            mode='lines+markers',
            line=dict(color='black', width=3, dash='dot'),
            marker=dict(size=4, color='black'),
            name=f"Trayectoria C{i}"
        ))

fig.update_layout(
    scene=dict(
        xaxis_title='PC1 (Componente Principal 1)',
        yaxis_title='PC2',
        zaxis_title='PC3',
        bgcolor="rgb(20, 20, 20)"
    ),
    paper_bgcolor="rgb(20, 20, 20)",
    font=dict(color="white"),
    height=800,
    margin=dict(l=0, r=0, b=0, t=40)
)

st.plotly_chart(fig, use_container_width=True)

# Explicaciones teóricas dinámicas
if fase == "Asignación (Distancia)":
    st.info("**Mecánica de Asignación:** Se mide la **distancia euclidiana** entre cada estado y los centroides. Visualmente, estas son las líneas que conectan cada punto con el diamante más cercano [11, 14].")
elif fase == "Actualización (Movimiento)":
    st.success("**Mecánica de Actualización:** El centroide se desplaza hacia el **promedio** de las coordenadas de todos los estados que tiene asignados [12, 16]. La línea punteada negra muestra este trayecto.")

st.write("### Vista previa de los datos escalados")
st.dataframe(df_pca.head(10))
