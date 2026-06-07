# =========================================================
# UMAP PROYECTO
# ---------------------------------------------------------
# Proyecto:
# Reducción de Dimensionalidad No Lineal
#
# Tema:
# UMAP y t-SNE para visualizar rostros humanos
#
# Autor:
# Proyecto de Análisis Multivariado
# =========================================================

# =========================================================
# LIBRERÍAS
# =========================================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import umap

from sklearn.datasets import fetch_lfw_people
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="UMAP - Reducción Dimensional",
    page_icon="brain",
    layout="wide"
)

# =========================================================
# CSS MODERNO Y ESTILIZADO
# =========================================================

st.markdown("""
<style>

/* Fondo Principal */
.stApp {
    background:
    radial-gradient(circle at top left, #1e1b4b 0%, #050816 40%),
    radial-gradient(circle at bottom right, #111827 0%, #050816 50%);
    color: white;
}

/* Sidebar Estilizado */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1120 0%, #050816 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Título de la Barra Lateral (Contenido Descriptivo) */
.sidebar-title {
    font-size: 18px;
    font-weight: 700;
    line-height: 1.3;
    letter-spacing: -0.3px;
    background: linear-gradient(90deg, #c084fc, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

/* Tipografía Principal */
h1, h2, h3, h4 {
    color: #F8FAFC;
    font-weight: 700;
}

p, label, div {
    color: #CBD5E1;
}

/* Header Principal de Bienvenida (Efecto Gradiente Bonito) */
.main-header {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(30, 27, 75, 0.4) 100%);
    padding: 35px;
    border-radius: 24px;
    border: 1px solid rgba(139, 92, 246, 0.2);
    margin-bottom: 30px;
}

.main-header h1 {
    font-size: 34px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 10px;
    letter-spacing: -0.8px;
    background: linear-gradient(90deg, #FFFFFF, #E2E8F0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-header .subtitle {
    font-size: 18px;
    color: #A78BFA;
    font-weight: 600;
    letter-spacing: -0.2px;
    margin-bottom: 5px;
}

/* Métricas Estilo Dashboard Premium */
.metric-card {
    background: linear-gradient(145deg, rgba(139,92,246,0.08), rgba(17,24,39,0.7));
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 0.3s ease;
    text-align: center;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(139,92,246,0.3);
    box-shadow: 0px 10px 30px rgba(139,92,246,0.15);
}

.metric-card h3 {
    font-size: 14px;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
}

.metric-card h1 {
    font-size: 36px;
    color: #F8FAFC;
    margin: 0;
}

.metric-card p {
    font-size: 13px;
    color: #64748B;
    margin-top: 5px;
}

/* Botones, Sliders y Selectores */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #8B5CF6, #7C3AED);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-weight: 600;
    transition: 0.3s;
}

.stSlider > div > div > div > div {
    background: #8B5CF6;
}

div[data-baseweb="select"] {
    background: #111827;
    border-radius: 12px;
}

img {
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}

/* Cajas de Información */
.info-box {
    background: rgba(139,92,246,0.05);
    border-left: 4px solid #8B5CF6;
    padding: 16px;
    border-radius: 0 12px 12px 0;
    margin-top: 15px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

# Ahora colocamos la descripción corta del contenido como el encabezado de la barra lateral
st.sidebar.markdown('<div class="sidebar-title">Reducción Dimensional No Lineal</div>', unsafe_allow_html=True)

st.sidebar.markdown("""
<p style="font-size: 14px; color: #94A3B8; margin-top: -10px; margin-bottom: 25px;">
Visualización y análisis morfológico de rostros humanos mediante algoritmos avanzados.
</p>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Menú de Exploración",
    [
        "Introducción",
        "Dataset Original",
        "Conversión Matemática",
        "Reducción Dimensional",
        "UMAP 2D",
        "UMAP 3D",
        "t-SNE",
        "Conclusiones"
    ]
)

# =========================================================
# CARGAR DATASET
# =========================================================

@st.cache_data
def cargar_datos():
    lfw = fetch_lfw_people(min_faces_per_person=70)
    X = lfw.data
    y = lfw.target
    images = lfw.images
    names = lfw.target_names
    return X, y, images, names

X, y, images, names = cargar_datos()

# =========================================================
# ESCALAR DATOS
# =========================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================================================
# MÉTRICAS
# =========================================================

n_imagenes = X.shape[0]
n_variables = X.shape[1]
n_personas = len(names)

# =========================================================
# INTRODUCCIÓN
# =========================================================

if pagina == "Introducción":
    # Ubicación del nombre matemático completo sobre el título principal de la aplicación
    st.markdown("""
    <div class="main-header">
        <div class="subtitle">Uniform Manifold Approximation and Projection (UMAP)</div>
        <h1>Explora la estructura oculta de los rostros</h1>
        <p style="margin: 0; color: #94A3B8; font-size: 15px;">
            Análisis visual e interactivo mediante técnicas avanzadas de reducción dimensional no lineal.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de métricas
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><h3>Dimensiones</h3><h1>{n_variables}</h1><p>Variables por imagen</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h3>Imágenes</h3><h1>{n_imagenes}</h1><p>Rostros procesados</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><h3>Algoritmia</h3><h1>UMAP</h1><p>Y modelo t-SNE</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><h3>Espacio</h3><h1>2D / 3D</h1><p>Mapas interactivos</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.8, 1])
    with col1:
        st.markdown("""
        ## El Problema de la Alta Dimensionalidad
        Cada imagen de un rostro humano está compuesta por miles de píxeles interdependientes. Al tratar cada píxel como una variable numérica independiente, los datos resultantes quedan confinados en una matriz matemática hiperbólica de **2914 dimensiones**.
        
        Dado que la percepción cognitiva humana está limitada a entornos de tres dimensiones, se vuelve fundamental implementar algoritmos geométricos capaces de comprimir y proyectar estos espacios complejos sin destruir las relaciones de similitud latentes.
        """)
    with col2:
        st.image(images[0], use_container_width=True)
        st.markdown('<div class="info-box"><b>Nota técnica:</b> El sistema no interpreta facciones corporales; mapea densidades de matrices vectoriales consecutivas.</div>', unsafe_allow_html=True)

# =========================================================
# DATASET ORIGINAL
# =========================================================

elif pagina == "Dataset Original":
    st.title("Dataset de Muestra")
    st.markdown("Análisis fundamentado sobre el compendio **LFW (Labeled Faces in the Wild)**, un estándar consolidado dentro del campo del Aprendizaje Profundo para tareas de verificación facial.")
    st.markdown("---")
    st.subheader("Muestras del Espacio de Entrada")
    
    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            st.image(images[i], caption=names[y[i]], use_container_width=True)

# =========================================================
# CONVERSIÓN MATEMÁTICA
# =========================================================

elif pagina == "Conversión Matemática":
    st.title("Linealización de Matrices de Píxeles")
    st.markdown("Transformación topológica donde una matriz bidimensional de imagen es reestructurada fila por fila hasta consolidar un vector plano apto para el análisis multivariado.")
    
    image = images[0]
    alto, ancho = image.shape
    vector = X[0]
    
    pixel_index = st.slider(
        "Rastreo del píxel físico y su correspondiente indexación vectorial:",
        0, len(vector)-1, 100
    )
    
    valor_pixel = vector[pixel_index]
    fila = pixel_index // ancho
    columna = pixel_index % ancho
    
    imagen_color = np.stack([image]*3, axis=-1)
    imagen_color = imagen_color / imagen_color.max()
    imagen_color[fila, columna] = [1, 0, 0] 
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Localización Espacial")
        fig = px.imshow(imagen_color)
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=0, b=0), coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="info-box">
        <b>Métricas del Elemento Seleccionado:</b><br>
        • Índice en Vector: Posición {pixel_index}<br>
        • Coordenada Matricial: Fila {fila}, Columna {columna}<br>
        • Magnitud de Intensidad: {valor_pixel:.2f}
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.subheader("Mapeo en Registro Estructurado")
        st.markdown("Vista dinámica de la distribución de memoria en el vector:")
        
        rango_min = max(0, pixel_index - 5)
        rango_max = min(len(vector), pixel_index + 6)
        
        indices_tabla = np.arange(rango_min, rango_max)
        valores_tabla = vector[rango_min:rango_max]
        roles = ["Vecino Adyacente" if idx != pixel_index else "PÍXEL SELECCIONADO" for idx in indices_tabla]
        
        tabla_df = pd.DataFrame({
            "ID Píxel (Posición en Vector)": indices_tabla,
            "Intensidad de Color (0-255)": np.round(valores_tabla, 4),
            "Fila en Imagen": indices_tabla // ancho,
            "Columna en Imagen": indices_tabla % ancho,
            "Rol en el Algoritmo": roles
        })
        
        styled_df = tabla_df.style.map(
            lambda v: 'background-color: rgba(139, 92, 246, 0.25); color: #FFFFFF; font-weight: bold;' if v == "PÍXEL SELECCIONADO" else '',
            subset=["Rol en el Algoritmo"]
        )
        
        st.dataframe(styled_df, use_container_width=True, height=420)

# =========================================================
# REDUCCIÓN DIMENSIONAL
# =========================================================

elif pagina == "Reducción Dimensional":
    st.title("Mecánica de la Compresión Espacial")
    st.markdown("Los algoritmos no lineales identifican correlaciones complejas en el hiperespacio y colapsan las 2914 dimensiones originales en coordenadas geométricas asimilables.")
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Alta Dimensión\n- 2914 descriptores ortogonales por espécimen.\n- Geometría abstracta ininterpretable mediante análisis visual directo.")
    with c2:
        st.markdown("### Proyección No Lineal\n- Detección de patrones y varianzas conjuntas mediante cálculo de vecindades y optimizaciones probabilísticas.")
    with c3:
        st.markdown("### Baja Dimensión\n- Reducción compacta a coordenadas Cartesianas.\n- Preservación óptima de la topología y de los agrupamientos familiares.")

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "UMAP 2D":
    st.title("Proyección Bidimensional UMAP")
    
    n_neighbors = st.slider("Ajuste de n_neighbors (Control de balance Local vs Global)", 5, 50, 15)
    
    reducer = umap.UMAP(n_components=2, n_neighbors=n_neighbors, random_state=42)
    embedding = reducer.fit_transform(X_scaled)
    
    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "persona": [names[i] for i in y]
    })
    
    st.markdown("Cada vector transformado se representa como un punto. El algoritmo aproxima subvariedades riemannianas para cohesionar rostros con similitudes estructurales.")
    
    fig = px.scatter(df, x="x", y="y", color="persona", template="plotly_dark", height=650)
    fig.update_traces(marker=dict(size=7, opacity=0.85))
    fig.update_layout(paper_bgcolor="#050816", plot_bgcolor="#050816")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# UMAP 3D
# =========================================================

elif pagina == "UMAP 3D":
    st.title("Proyección Tridimensional UMAP")
    
    reducer = umap.UMAP(n_components=3, random_state=42)
    embedding = reducer.fit_transform(X_scaled)
    
    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "z": embedding[:, 2],
        "persona": [names[i] for i in y]
    })
    
    fig = px.scatter_3d(df, x="x", y="y", z="z", color="persona", template="plotly_dark", height=750)
    fig.update_layout(paper_bgcolor="#050816")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TSNE
# =========================================================

elif pagina == "t-SNE":
    st.title("Mapeo Comparativo vía t-SNE")
    st.markdown("Modelado de proximidades fundamentado en distribuciones de probabilidad condicional. Tiende a maximizar la dispersión inter-clase, fragmentando la continuidad global.")
    
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    embedding = tsne.fit_transform(X_scaled)
    
    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "persona": [names[i] for i in y]
    })
    
    fig = px.scatter(df, x="x", y="y", color="persona", template="plotly_dark", height=650)
    fig.update_layout(paper_bgcolor="#050816", plot_bgcolor="#050816")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# CONCLUSIONES
# =========================================================

elif pagina == "Conclusiones":
    st.title("Análisis y Evaluaciones Estadísticas")
    st.markdown("""
    ## Hallazgos Clave
    - **UMAP** demuestra una velocidad y consistencia matemática superior a t-SNE al mantener la coherencia espacial general.
    - Los clusters visibles demuestran que expresiones, orientaciones de rostros y rasgos genómicos se agrupan sin necesidad de darle etiquetas de nombres al algoritmo (aprendizaje no supervisado).
    
    ## Dinámica de los Algoritmos
    - **Preservación Estructural:** Mientras que t-SNE prioriza de manera casi exclusiva las relaciones de vecindad local (creando "islas" aisladas), UMAP logra balancear la microestructura y la macroestructura, permitiendo interpretar qué tan distantes o similares son los grupos de rostros entre sí en el espacio completo.
    - **Sensibilidad a los Hiperparámetros:** El ajuste de parámetros como `n_neighbors` altera drásticamente la topología del mapa resultante. Valores bajos aíslan patrones finos (como una inclinación de cabeza específica), mientras que valores altos unifican identidades completas bajo un criterio global.
    - **Importancia del Escalado:** La reducción dimensional no lineal es altamente sensible a las magnitudes. Sin un escalado estándar previo (`StandardScaler`), los píxeles con variaciones extremas de iluminación dominarían por completo la geometría de la proyección, ocultando los rasgos morfológicos reales de los rostros.
    """)
