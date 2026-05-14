import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Configuración de la página
st.set_page_config(page_title="K-Means 3D Visualizer", layout="wide")
st.title("Visualización Avanzada de K-Means en 3D")

# 1. Generación de datos (Simulando el contexto bancario del video pero en 3D)
# Agregamos una tercera variable: "Antigüedad del Cliente"
@st.cache_data
def get_data():
    np.random.seed(42)
    data = np.random.rand(100, 3) * 100
    return pd.DataFrame(data, columns=['Saldo', 'Transacciones', 'Antigüedad'])

df = get_data()

# Sidebar para controles
st.sidebar.header("Configuración")
k = st.sidebar.slider("Selecciona el número de clusters (k)", 2, 10, 3)
run_button = st.sidebar.button("Ejecutar K-Means")

# 2. Pre-procesamiento (Como se explica en el video [13, 16])
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df)

if run_button:
    # 3. Aplicación del Modelo
    model = KMeans(n_clusters=k, random_state=42)
    labels = model.fit_predict(df_scaled)
    centroids = model.cluster_centers_
    
    # 4. Creación del gráfico 3D con enlaces
    fig = go.Figure()

    # Colores para los clusters
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

    # Dibujar puntos y líneas de conexión (enlaces)
    for i in range(k):
        # Puntos del cluster actual
        cluster_points = df_scaled[labels == i]
        centroid = centroids[i]
        
        # Agregar puntos del cluster
        fig.add_trace(go.Scatter3d(
            x=cluster_points[:, 0], y=cluster_points[:, 1], z=cluster_points[:, 2],
            mode='markers',
            marker=dict(size=5, color=colors[i % len(colors)], opacity=0.8),
            name=f"Cluster {i}"
        ))

        # Agregar el centroide (X estilizada)
        fig.add_trace(go.Scatter3d(
            x=[centroid], y=[centroid[1]], z=[centroid[15]],
            mode='markers',
            marker=dict(size=10, symbol='x', color=colors[i % len(colors)], line=dict(width=2, color='black')),
            name=f"Centroide {i}"
        ))

        # Crear los enlaces (líneas del punto al centroide)
        for point in cluster_points:
            fig.add_trace(go.Scatter3d(
                x=[point, centroid],
                y=[point[1], centroid[1]],
                z=[point[15], centroid[15]],
                mode='lines',
                line=dict(color=colors[i % len(colors)], width=1),
                showlegend=False,
                opacity=0.2 # Transparencia para que se vea "bonito" y no saturado
            ))

    # Estética del plano 3D (quitando el "encierro" clásico)
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=True, title='Saldo (Escalado)'),
            yaxis=dict(showbackground=False, showgrid=True, title='Transacciones (Escalado)'),
            zaxis=dict(showbackground=False, showgrid=True, title='Antigüedad (Escalado)'),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        template="plotly_dark" # Fondo oscuro para resaltar los colores
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar métrica de Inercia explicada en el video [17, 18]
    st.write(f"**Inercia del modelo:** {model.inertia_:.4f}")
    st.info("La inercia representa la suma de las distancias al cuadrado de los puntos a su centroide. Menor inercia suele indicar clusters más compactos [18, 19].")

else:
    st.write("Ajusta el valor de **k** en la barra lateral y presiona **Ejecutar** para ver la magia de la agrupación.")
