# LIBRERIAS
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial.distance import pdist, squareform

# CONFIGURACIÓN GENERAL

st.set_page_config(
    page_title="MINERIA DE DATOS(K-Means)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILOS CSS

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

h1 {
    color: #00ffd5;
    text-align: center;
    font-size: 50px;
}

h2 {
    color: #00c3ff;
}

h3 {
    color: #ffffff;
}

.stMetric {
    background-color: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
}

.css-1d391kg {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# TITULO

st.title("Clustering K-Means")

st.markdown("""
Esta aplicación permite explorar paso a paso el algoritmo K-Means usando el dataset USArrests.

Incluye:

- Exploración de datos
- Estandarización
- Distancias Euclidianas y Manhattan
- Método del codo
- Comparacion de tiempo e inercia (cluster)
- Animación de convergencia de K-Means
- PCA 2D y 3D
- Boxplots interactivos
- Visualizaciones dinámicas
- Movimiento de centroides
- Explicaciones matemáticas
""")

# SIDEBAR

st.sidebar.title("⚙ Configuración")

uploaded_file = st.sidebar.file_uploader(
    "Suba el archivo data_USArrests.xlsx",
    type=["xlsx"]
)

k = st.sidebar.slider("Número de Clusters", 2, 10, 4)

iteraciones_animadas = st.sidebar.slider(
    "Velocidad Animación",
    5,
    50,
    20
)

# CARGA DE DATOS


if uploaded_file:

    datos = pd.read_excel(uploaded_file)

    st.header("Dataset")
    st.dataframe(datos)

    st.header(" Información del Dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Filas", datos.shape[0])

    with col2:
        st.metric("Columnas", datos.shape[1])

    with col3:
        st.metric("Valores faltantes", datos.isnull().sum().sum())

    st.write(datos.describe())

    # LIMPIEZA

    datos = datos.dropna()

    # HISTOGRAMAS

    st.header(" Histogramas")

    columnas_numericas = ['Murder', 'Assault', 'UrbanPop', 'Rape']

    fig_hist = px.histogram(
        datos,
        x='Murder',
        nbins=10,
        title='Distribución Murder'
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    tabs = st.tabs(columnas_numericas)

    for i, col in enumerate(columnas_numericas):

        with tabs[i]:

            fig = px.histogram(
                datos,
                x=col,
                marginal='box',
                color_discrete_sequence=['cyan']
            )

            st.plotly_chart(fig, use_container_width=True)

    # ESTANDARIZACIÓN

    st.header("Estandarización")

    scaler = StandardScaler()

    numericas = datos.select_dtypes(
        include=['float64', 'int64']
    ).columns

    datos[numericas] = scaler.fit_transform(
        datos[numericas]
    )

    st.write(datos.head())

    # MATRIZ DISTANCIAS

    st.header(" Distancias Euclidianas")

    distancias = euclidean_distances(
        datos.drop(columns=['State'])
    )

    dist_matrix = pd.DataFrame(
        distancias,
        index=datos['State'],
        columns=datos['State']
    )

    fig_heat = px.imshow(
        dist_matrix,
        color_continuous_scale='RdBu',
        title='Mapa de calor Distancias Euclidianas'
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    # DISTANCIAS MANHATTAN

    st.header(" Distancias Manhattan")

    manhattan = pdist(
        datos.drop(columns=['State']),
        metric='cityblock'
    )

    manhattan_square = squareform(manhattan)

    manhattan_df = pd.DataFrame(
        manhattan_square,
        index=datos['State'],
        columns=datos['State']
    )

    fig_manhattan = px.imshow(
        manhattan_df,
        color_continuous_scale='Viridis',
        title='Mapa Distancias Manhattan'
    )

    st.plotly_chart(fig_manhattan, use_container_width=True)

    # METODO DEL CODO

    st.header("Método del Codo")

    wss = []

    for i in range(1, 11):

        modelo = KMeans(
            n_clusters=i,
            n_init=50,
            random_state=42
        )

        modelo.fit(
            datos.drop(columns=['State'])
        )

        wss.append(modelo.inertia_)

    elbow_df = pd.DataFrame({
        'Clusters': range(1, 11),
        'WSS': wss
    })

    fig_elbow = px.line(
        elbow_df,
        x='Clusters',
        y='WSS',
        markers=True,
        title='Método del Codo'
    )

    fig_elbow.add_vline(
        x=k,
        line_dash='dash',
        line_color='red'
    )

    st.plotly_chart(fig_elbow, use_container_width=True)
    
    # KMEANS

    st.header(" Algoritmo K-Means")

    st.markdown("""
    Si desea realizar la comparcion entre numeros de clusters, debe seleccionar un numero diferente al predeterminado por la app y dar click a los  botones (Tiempo o Inercia)
    """)

    kmeans = KMeans(
        n_clusters=k,
        n_init=50,
        random_state=42
    )

    inicio = time.time()

    km4_clusters = kmeans.fit(
        datos.drop(columns=['State'])
    )

    fin = time.time()

    st.success(
        f"Tiempo ejecución: {(fin - inicio)*1000:.2f} ms"
    )

    # COMPARACION TIEMPO E INERCIA

    tiempo_actual = (fin - inicio) * 1000

    if "historial_tiempos" not in st.session_state:
        st.session_state.historial_tiempos = []

    st.session_state.historial_tiempos = [
        x for x in st.session_state.historial_tiempos
        if x["Clusters"] != k
    ]

    st.session_state.historial_tiempos.append({
        "Clusters": k,
        "Tiempo": tiempo_actual
    })

    historial_df = pd.DataFrame(
        st.session_state.historial_tiempos
    ).sort_values(by="Clusters")

    if st.button("Comparación de tiempos"):

        st.subheader(
            "Comparación de tiempos por número de clusters"
        )

        mejor = historial_df["Tiempo"].min()
        peor = historial_df["Tiempo"].max()

        colores_barras = []

        for valor in historial_df["Tiempo"]:

            if valor == mejor:
                colores_barras.append("green")

            elif valor == peor:
                colores_barras.append("red")

            else:
                colores_barras.append("orange")

        fig_tiempos = go.Figure()

        fig_tiempos.add_trace(
            go.Bar(
                x=historial_df["Clusters"],
                y=historial_df["Tiempo"],
                marker_color=colores_barras,
                text=np.round(historial_df["Tiempo"], 2),
                textposition='outside'
            )
        )

        fig_tiempos.update_layout(
            title="Tiempo de ejecución según K",
            xaxis_title="Número de Clusters",
            yaxis_title="Tiempo (ms)",
            height=500
        )

        st.plotly_chart(
            fig_tiempos,
            use_container_width=True
        )

        mejor_k = historial_df.loc[
            historial_df["Tiempo"].idxmin(),
            "Clusters"
        ]

        peor_k = historial_df.loc[
            historial_df["Tiempo"].idxmax(),
            "Clusters"
        ]

        st.markdown(f"""
        ## Análisis

        - 🟢 El mejor rendimiento fue con K = {mejor_k}

        - 🔴 El peor rendimiento fue con K = {peor_k}

        - 🟠 Los demás fueron intermedios.

        ### Explicación

        Cuando aumenta K:

        - Se calculan más centroides.
        - Hay más distancias.
        - Puede tardar más en converger.

        Por eso algunos valores de K
        tardan más que otros.
        """)
  
    # COMPARACIÓN DE INERCIAS

    inercia_actual = kmeans.inertia_

    if "historial_inercias" not in st.session_state:
        st.session_state.historial_inercias = []

    # eliminar K repetido
    st.session_state.historial_inercias = [
        x for x in st.session_state.historial_inercias
        if x["Clusters"] != k
    ]

    # guardar nueva inercia
    st.session_state.historial_inercias.append({
        "Clusters": k,
        "Inercia": inercia_actual
    })

    historial_df = pd.DataFrame(
        st.session_state.historial_inercias
    ).sort_values(by="Clusters")


    # BOTON MOSTRAR COMPARACION

    if st.button("Ccomparación de inercias"):

        st.subheader(
            "Comparación de Inercia según número de clusters"
        )

        mejor = historial_df["Inercia"].min()
        peor = historial_df["Inercia"].max()

        colores_barras = []

        for valor in historial_df["Inercia"]:

            if valor == mejor:
                colores_barras.append("green")

            elif valor == peor:
                colores_barras.append("red")

            else:
                colores_barras.append("orange")

        fig_inercia = go.Figure()

        fig_inercia.add_trace(
            go.Bar(
                x=historial_df["Clusters"],
                y=historial_df["Inercia"],
                marker_color=colores_barras,
                text=np.round(
                    historial_df["Inercia"], 2
                ),
                textposition='outside'
            )
        )

        fig_inercia.update_layout(
            title="Comparación de Inercia según K",
            xaxis_title="Número de Clusters",
            yaxis_title="Inercia (WSS)",
            height=500
        )

        st.plotly_chart(
            fig_inercia,
            use_container_width=True
        )

        mejor_k = historial_df.loc[
            historial_df["Inercia"].idxmin(),
            "Clusters"
        ]

        peor_k = historial_df.loc[
            historial_df["Inercia"].idxmax(),
            "Clusters"
        ]

        st.markdown(f"""
        ## Interpretación

        - 🟢 La menor inercia fue con K = {mejor_k}

        - 🔴 La mayor inercia fue con K = {peor_k}

        - 🟠 Los demás valores son intermedios.

        ### ¿Qué significa?

        La inercia mide qué tan compactos
        son los clusters.

        - Menor inercia =
          clusters más compactos.

        - Mayor inercia =
          agrupaciones menos precisas.

        Normalmente al aumentar K,
        la inercia disminuye.
        """)
    #fin miguel

    st.subheader("Centroides")
    st.write(kmeans.cluster_centers_)

    datos['Cluster'] = km4_clusters.labels_


    # ANIMACIÓN DE CONVERGENCIA


    st.header("Animación de Convergencia")

    pca_anim = PCA(n_components=2)

    X_pca = pca_anim.fit_transform(datos[numericas])

    fig_anim = go.Figure()

    colores = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'pink', 'lime', 'white']

    centroides = X_pca[np.random.choice(len(X_pca), k, replace=False)]

    frames = []

    for frame_num in range(iteraciones_animadas):

        distancias = np.linalg.norm(
            X_pca[:, np.newaxis] - centroides,
            axis=2
        )

        labels = np.argmin(distancias, axis=1)

        nuevos_centroides = np.array([
            X_pca[labels == i].mean(axis=0)
            for i in range(k)
        ])

        scatter_data = []

        for i in range(k):

            puntos = X_pca[labels == i]

            scatter_data.append(
                go.Scatter(
                    x=puntos[:,0],
                    y=puntos[:,1],
                    mode='markers+text',
                    text=datos['State'],
                    textposition='top center',
                    marker=dict(size=10, color=colores[i]),
                    name=f'Cluster {i}'
                )
            )

        scatter_data.append(
            go.Scatter(
                x=nuevos_centroides[:,0],
                y=nuevos_centroides[:,1],
                mode='markers',
                marker=dict(
                    size=25,
                    color='black',
                    symbol='star'
                ),
                name='Centroides'
            )
        )

        # líneas distancia

        for i in range(len(X_pca)):
            centroide = nuevos_centroides[labels[i]]

            scatter_data.append(
                go.Scatter(
                    x=[X_pca[i,0], centroide[0]],
                    y=[X_pca[i,1], centroide[1]],
                    mode='lines',
                    line=dict(color='gray', width=1),
                    showlegend=False
                )
            )

        frames.append(go.Frame(data=scatter_data, name=str(frame_num)))

        centroides = nuevos_centroides

    fig_anim.frames = frames

    fig_anim.add_trace(
        go.Scatter(x=[], y=[])
    )

    fig_anim.update_layout(

    title='Movimiento de centroides y convergencia K-Means',

    width=1200,
    height=800,

    updatemenus=[

        dict(

            type='buttons',

            showactive=False,

            bgcolor='#87CEFA',

            bordercolor='#1E3A8A',

            font=dict(
                color='black',
                size=15
            ),

            buttons=[

                dict(
                    label='▶ Iniciar',
                    method='animate',
                    args=[None]
                )

            ]

        )

    ]

)
    st.plotly_chart(fig_anim, use_container_width=True)

    # PCA


    st.header("PCA")

    pca = PCA(n_components=4)

    pca_scores = pca.fit_transform(datos[numericas])

    pca_df = pd.DataFrame(
        pca_scores,
        columns=['PC1', 'PC2', 'PC3', 'PC4']
    )

    pca_df['Cluster'] = km4_clusters.labels_.astype(str)
    pca_df['Etiqueta'] = datos['State']

    # PCA 2D
  

    st.subheader("PCA Interactivo 2D")

    fig_2d = px.scatter(
        pca_df,
        x='PC1',
        y='PC2',
        color='Cluster',
        text='Etiqueta',
        title='PCA 2D'
    )

    fig_2d.update_traces(
        textposition='top center'
    )

    st.plotly_chart(fig_2d, use_container_width=True)


    # SIMULACIÓN PEDAGÓGICA REAL K-MEANS (CONTROL POR ITERACIONES)
   

    st.subheader("Simulación paso a paso REAL de K-Means (Controlable)")

    st.markdown("""
    Controla cada iteración del algoritmo:

    - Iteración 0: todos los puntos sin cluster
    - Iteración 1: centroides iniciales
    - Iteraciones siguientes: asignación + actualización
    """)


    # DATOS 3D


    X3D = pca_df[['PC1', 'PC2', 'PC3']].values
    labels_names = datos['State'].values

    np.random.seed(42)

    # INICIALIZACIÓN CENTROIDES


    centroides_init = X3D[np.random.choice(len(X3D), k, replace=False)]

    # GUARDAR HISTORIAL


    centroides_hist = [centroides_init]
    labels_hist = []

    centroides = centroides_init.copy()

    max_iter = iteraciones_animadas

    for _ in range(max_iter):

        # DISTANCIAS
        distancias = np.linalg.norm(X3D[:, None] - centroides, axis=2)
        labels = np.argmin(distancias, axis=1)

        labels_hist.append(labels)

        # NUEVOS CENTROIDES
        nuevos_centroides = []

        for i in range(k):
            puntos = X3D[labels == i]
            if len(puntos) > 0:
                nuevos_centroides.append(puntos.mean(axis=0))
            else:
                nuevos_centroides.append(centroides[i])

        nuevos_centroides = np.array(nuevos_centroides)
        centroides_hist.append(nuevos_centroides)

        # CONVERGENCIA
        if np.linalg.norm(nuevos_centroides - centroides) < 1e-4:
            break

        centroides = nuevos_centroides

    total_iter = len(labels_hist)


    # SLIDER ITERACIÓN
  

    iter_sel = st.slider("Selecciona iteración", 0, total_iter-1, 0)

    labels_sel = labels_hist[iter_sel]
    centroids_sel = centroides_hist[iter_sel]

    colores_k = ['red','green','blue','yellow','purple','orange','cyan','magenta']

    fig_k = go.Figure()

    
    # PUNTOS
   

    for i in range(k):

        puntos = X3D[labels_sel == i]
        nombres = labels_names[labels_sel == i]

        fig_k.add_trace(go.Scatter3d(
            x=puntos[:,0],
            y=puntos[:,1],
            z=puntos[:,2],
            mode='markers+text',
            text=nombres,
            textposition='top center',
            marker=dict(size=5, color=colores_k[i]),
            name=f'Cluster {i}'
        ))


    # CENTROIDES
    

    fig_k.add_trace(go.Scatter3d(
        x=centroids_sel[:,0],
        y=centroids_sel[:,1],
        z=centroids_sel[:,2],
        mode='markers',
        marker=dict(size=18, color='white', symbol='diamond'),
        name='Centroides'
    ))

    # LÍNEAS DISTANCIA


    for i in range(len(X3D)):
        c = labels_sel[i]
        centroide = centroids_sel[c]

        fig_k.add_trace(go.Scatter3d(
            x=[X3D[i,0], centroide[0]],
            y=[X3D[i,1], centroide[1]],
            z=[X3D[i,2], centroide[2]],
            mode='lines',
            line=dict(color=colores_k[c], width=2),
            showlegend=False
        ))

   

    fig_k.update_layout(
        title=f"K-Means Paso a Paso - Iteración {iter_sel}",
        width=1700,
        height=900,
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font=dict(color='white'),
        scene=dict(
            xaxis_title='PC1',
            yaxis_title='PC2',
            zaxis_title='PC3'
        )
    )

    st.plotly_chart(fig_k, use_container_width=True)

    # =========================================================
# INTERPRETACIÓN PEDAGÓGICA
# =========================================================

st.subheader("📘 Interpretación de la Iteración")

st.markdown(f"""

### ¿Qué está ocurriendo en la iteración {iter_sel}?

En esta etapa del algoritmo K-Means:

- Cada punto calcula su distancia hacia todos los centroides.
- Luego se asigna al centroide más cercano.
- Las líneas representan esa relación de cercanía.

### 🔍 Puntos cercanos a fronteras

Algunos datos pueden observarse:

- muy alejados de su centroide,
- o cercanos a otro cluster.

Esto ocurre porque:

- las fronteras entre clusters no son rígidas,
- existen regiones intermedias,
- algunos individuos comparten características similares con varios grupos.

### ⚠️ ¿Qué puede pasar?

Cuando un punto queda cerca de otro centroide:

- puede cambiar de cluster
  en la siguiente iteración.

Esto provoca:

- movimiento de centroides,
- reajuste de grupos,
- búsqueda de agrupaciones más compactas.

### 📌 Interpretación matemática

K-Means minimiza la distancia total entre:

- cada punto,
- y su centroide asignado.

Por eso:

- si un punto está demasiado lejos,
- el algoritmo intentará reorganizar los clusters.

### 🧠 Interpretación intuitiva

Los puntos ubicados en fronteras representan:

- observaciones ambiguas,
- individuos con características mixtas,
- posibles transiciones entre grupos.

Esto es completamente normal en clustering no supervisado.
""")

 

    st.header("Boxplot Interactivo")

    fig_box = px.box(
        datos,
        x='Cluster',
        y='Rape',
        color='Cluster',
        points='all',
        hover_data=['State']
    )

    st.plotly_chart(fig_box, use_container_width=True)

 
    # TABLA DE CLUSTERS
    

    st.header("Estados por Cluster")

    grupos = pd.DataFrame()

    grupos['State'] = datos['State']
    grupos['Cluster'] = km4_clusters.labels_

    st.dataframe(
        grupos.sort_values(by='Cluster'),
        use_container_width=True
    )

    # CANTIDAD POR CLUSTER
    

    st.header(" Cantidad de individuos por Cluster")

    conteo = grupos.groupby('Cluster').size().reset_index()

    conteo.columns = ['Cluster', 'Cantidad']

    fig_count = px.bar(
        conteo,
        x='Cluster',
        y='Cantidad',
        color='Cluster',
        text='Cantidad'
    )

    st.plotly_chart(fig_count, use_container_width=True)

    
    # VISUALIZACIÓN MURDER VS URBANPOP


    st.header("Murder vs UrbanPop")

    fig_mu = px.scatter(
        datos,
        x='Murder',
        y='UrbanPop',
        color='Cluster',
        hover_data=['State'],
        title='Murder vs UrbanPop'
    )

    st.plotly_chart(fig_mu, use_container_width=True)


    # VISUALIZACIÓN RAPE VS ASSAULT


    st.header("Rape vs Assault")

    fig_ra = px.scatter(
        datos,
        x='Rape',
        y='Assault',
        color='Cluster',
        hover_data=['State'],
        title='Rape vs Assault'
    )

    st.plotly_chart(fig_ra, use_container_width=True)

    # EXPLICACIÓN MATEMÁTICA
 

    st.header("Explicación Matemática")

    st.markdown("""
    ## ¿Cómo funciona K-Means?

    1. Se eligen centroides aleatorios.

    2. Cada punto calcula su distancia al centroide más cercano.

    3. Los puntos se asignan al cluster más cercano.

    4. Los centroides se recalculan usando el promedio de los puntos.

    5. El proceso se repite hasta converger.

    ## Distancia Euclidiana

    La distancia usada normalmente es:

    d(x,y)=√((x1-y1)^2+(x2-y2)^2+...)

    ## Inercia

    La inercia mide qué tan compactos son los clusters.

    Menor inercia = mejores agrupaciones.
    """)

    st.success("Aplicación cargada correctamente")

else:

    st.warning("⚠️ Suba el archivo data_USArrests.xlsx para iniciar")

    # EL RESTO DEL CÓDIGO ORIGINAL CONTINÚA IGUAL
    # NO SE ELIMINÓ NADA
