# =========================================================
# FACEEXPLORER AI
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
    page_title="FaceExplorer AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# CSS MODERNO
# =========================================================

st.markdown("""
<style>

/* =====================================================
FONDO PRINCIPAL
===================================================== */

.stApp{
    background:
    radial-gradient(circle at top left, #1e1b4b 0%, #050816 40%),
    radial-gradient(circle at bottom right, #111827 0%, #050816 50%);
    color:white;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #0B1120 0%,
        #050816 100%
    );
    border-right:
    1px solid rgba(255,255,255,0.08);
}

/* =====================================================
TEXTOS
===================================================== */

h1,h2,h3,h4{
    color:#F8FAFC;
}

p, label, div{
    color:#CBD5E1;
}

/* =====================================================
CARDS
===================================================== */

.card{
    background:
    rgba(17,24,39,0.78);
    border:
    1px solid rgba(255,255,255,0.08);
    border-radius:24px;
    padding:25px;
    backdrop-filter: blur(10px);
    box-shadow:
    0px 0px 30px rgba(0,0,0,0.35);
    margin-bottom:25px;
}

/* =====================================================
METRICAS
===================================================== */

.metric-card{
    background:
    linear-gradient(
        145deg,
        rgba(139,92,246,0.12),
        rgba(17,24,39,0.92)
    );
    border-radius:22px;
    padding:24px;
    border:
    1px solid rgba(139,92,246,0.25);
    transition:0.3s;
}

.metric-card:hover{
    transform:translateY(-5px);
    box-shadow:
    0px 0px 24px rgba(139,92,246,0.35);
}

/* =====================================================
BOTONES
===================================================== */

.stButton > button{
    width:100%;
    background:
    linear-gradient(
        90deg,
        #8B5CF6,
        #7C3AED
    );
    color:white;
    border:none;
    border-radius:14px;
    padding:14px;
    font-size:16px;
    font-weight:600;
    transition:0.3s;
}

/* =====================================================
SLIDERS
===================================================== */

.stSlider > div > div > div > div{
    background:#8B5CF6;
}

/* =====================================================
SELECTBOX
===================================================== */

div[data-baseweb="select"]{
    background:#111827;
    border-radius:14px;
}

/* =====================================================
IMÁGENES
===================================================== */

img{
    border-radius:16px;
}

/* =====================================================
CAJAS EXPLICATIVAS
===================================================== */

.info-box{
    background:
    rgba(139,92,246,0.08);
    border-left:
    4px solid #8B5CF6;
    padding:18px;
    border-radius:12px;
    margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🧠 FaceExplorer AI")

st.sidebar.markdown("""
### Reducción Dimensional No Lineal
Visualización de rostros humanos mediante técnicas avanzadas.
""")

pagina = st.sidebar.radio(
    "Exploración",
    [
        "🏠 Introducción",
        "📖 Teoría e Historia de UMAP",
        "📚 Dataset Original",
        "🔢 Conversión Matemática",
        "📉 Reducción Dimensional",
        "🚀 UMAP 2D",
        "🌌 UMAP 3D",
        "🧠 t-SNE",
        "📌 Conclusiones"
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

if pagina == "🏠 Introducción":
    st.title("Explora la estructura oculta de los rostros 👋")
    st.markdown("Esta aplicación muestra cómo técnicas de reducción dimensional transforman imágenes complejas en mapas visuales 2D y 3D.")
    
    st.markdown("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><h3>Dimensiones</h3><h1>{n_variables}</h1><p>variables por imagen</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h3>Imágenes</h3><h1>{n_imagenes}</h1><p>rostros humanos</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><h3>Métodos</h3><h1>UMAP</h1><p>t-SNE</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><h3>Visualización</h3><h1>2D/3D</h1><p>interactiva</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ## 📘 ¿Qué problema resolvemos?
        Cada rostro humano contiene miles de píxeles. Cada píxel representa información matemática, por lo que una imagen vive en un espacio de alta dimensionalidad.
        Los humanos no podemos visualizar 2914 dimensiones. Por eso utilizamos algoritmos geométricos y probabilísticos para proyectar estas estructuras en espacios simples.
        """)
    with col2:
        st.image(images[0], use_container_width=True)
        st.markdown('<div class="info-box">La computadora no ve una cara. Ve miles de números alineados.</div>', unsafe_allow_html=True)

# =========================================================
# TEORÍA E HISTORIA DE UMAP
# =========================================================

elif pagina == "📖 Teoría e Historia de UMAP":
    st.title("📖 Aproximación y Proyección de Variedades Uniformes (UMAP)")
    
    st.markdown("""
    ### ⏳ Origen e Historia
    **UMAP** (*Uniform Manifold Approximation and Projection*) fue desarrollado en **2018** por el matemático **McInnes, Healy y Melville**. Nació como una respuesta directa a las limitaciones de *t-SNE*, el cual era extremadamente lento con datasets gigantescos y fallaba en conservar la estructura global de los datos (la relación de distancia entre grupos muy separados).
    
    McInnes recurrió a la **geometría diferencial** y la **topología algebraica** para demostrar que se podía hacer reducción de dimensionalidad manteniendo tanto la vecindad local como la distribución global de los datos de manera extremadamente veloz.
    """)
    
    st.markdown("---")
    st.subheader("💡 Sentido del Funcionamiento (Metáfora Sencilla)")
    st.markdown("""
    Imagina que tu dataset de rostros es un **globo inflado lleno de puntos dibujados en su superficie**. 
    1. **Paso 1:** UMAP pasa un 'pegamento' sobre los puntos que están muy cerca creando una malla o esqueleto elástico (un *complejo simplicial*).
    2. **Paso 2:** El algoritmo desinfla el globo y lo estira sobre una mesa plana (2D).
    3. **Paso 3:** Mientras lo estira, intenta que las partes que estaban pegadas no se rompan y que las partes que estaban lejos en el globo sigan quedando lejos en la mesa.
    """)
    
    st.markdown("#### 🎨 Flujo Visual de UMAP de Principio a Fin")
    st.write("")
    
    st.markdown("---")
    st.subheader("🧬 El Proceso de Principio a Fin y su Fórmula")
    st.markdown("""
    El algoritmo opera en dos fases matemáticas estrictas:
    
    #### 1. Construcción del Grafo en Alta Dimensión
    Para cada punto $x_i$, se calcula la distancia con sus vecinos. Como los datos reales no están distribuidos de manera uniforme, UMAP asume una métrica local donde la distancia al vecino más cercano es $\rho_i$, y define la probabilidad de conexión entre el punto $i$ y el punto $j$ mediante la función exponencial decreciente:
    """)
    
    st.latex(r"p_{j|i} = \exp \left( -\frac{\max(0, d(x_i, x_j) - \rho_i)}{\sigma_i} \right)")
    
    st.markdown("""
    Donde $\sigma_i$ es un factor de escala adaptativo para que el número de vecinos efectivos coincida con el hiperparámetro `n_neighbors`. Para hacer la matriz simétrica (ya que $i$ puede ser vecino de $j$, pero $j$ no necesariamente de $i$), se calcula:
    """)
    st.latex(r"p_{ij} = p_{i|j} + p_{j|i} - p_{i|j}p_{j|i}")

    st.markdown("""
    #### 2. Optimización en Baja Dimensión
    En el espacio de destino (2D o 3D), la probabilidad de que dos puntos $y_i$ e $y_j$ estén conectados se modela usando una curva similar a la distribución t de Student:
    """)
    st.latex(r"q_{ij} = \left( 1 + a ||y_i - y_j||^{2b} \right)^{-1}")
    
    st.markdown("""
    Finalmente, para que el mapa de baja dimensión se parezca lo máximo posible al de alta dimensión, UMAP minimiza la **Entropía Cruzada Difusa** usando descenso de gradiente:
    """)
    st.latex(r"CE(P, Q) = \sum_{i \neq j} \left[ p_{ij} \log \left(\frac{p_{ij}}{q_{ij}}\right) + (1 - p_{ij}) \log \left(\frac{1 - p_{ij}}{1 - q_{ij}}\right) \right]")
    
    st.markdown("""
    * El **primer término** empuja a los puntos similares a estar muy cerca en 2D.
    * El **segundo término** empuja a los puntos disímiles a alejarse, preservando la estructura global.
    """)

# =========================================================
# DATASET ORIGINAL
# =========================================================

elif pagina == "📚 Dataset Original":
    st.title("📚 Dataset Original")
    st.markdown("Trabajamos con el dataset **LFW (Labeled Faces in the Wild)**, ampliamente utilizado en IA para el entrenamiento de sistemas de reconocimiento facial.")
    st.markdown("---")
    st.subheader("🖼️ ¿Cómo se ven los datos originales?")
    
    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            st.image(images[i], caption=names[y[i]], use_container_width=True)

# =========================================================
# CONVERSIÓN MATEMÁTICA
# =========================================================

elif pagina == "🔢 Conversión Matemática":
    st.title("🔢 Conversión de Imagen a Vector Matemático")
    st.markdown("Cada píxel de la imagen se extrae ordenadamente de izquierda a derecha y de arriba a abajo, convirtiéndose en una celda dentro de un vector de características unidimensional.")
    
    image = images[0]
    alto, ancho = image.shape
    vector = X[0]
    
    pixel_index = st.slider(
        "Mueve el slider para rastrear la equivalencia entre el píxel físico y su representación en la tabla:",
        0, len(vector)-1, 100
    )
    
    valor_pixel = vector[pixel_index]
    fila = pixel_index // ancho
    columna = pixel_index % ancho
    
    # Marcador visual en la imagen: Duplicamos a RGB y pintamos el pixel seleccionado de rojo intenso
    imagen_color = np.stack([image]*3, axis=-1)
    imagen_color = imagen_color / imagen_color.max()
    imagen_color[fila, columna] = [1, 0, 0] 
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("🖼️ Ubicación Espacial (Píxel en Imagen)")
        fig = px.imshow(imagen_color)
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=0, b=0), coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="info-box">
        <strong>Propiedades del Punto Actual:</strong><br>
        • <b>ID en Vector lineal:</b> Elemento número {pixel_index}<br>
        • <b>Coordenada Espacial:</b> Fila {fila}, Columna {columna}<br>
        • <b>Valor de Intensidad numérica:</b> {valor_pixel:.2f}
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.subheader("📊 Estructura de la Tabla Vectorial")
        st.markdown("Ventana de datos dinámicos que muestra cómo la computadora almacena las secciones del rostro consecutivamente:")
        
        # Crear ventana de visualización alrededor del pixel seleccionado
        rango_min = max(0, pixel_index - 5)
        rango_max = min(len(vector), pixel_index + 6)
        
        indices_tabla = np.arange(rango_min, rango_max)
        valores_tabla = vector[rango_min:rango_max]
        roles = ["Vecino Adyacente" if idx != pixel_index else "📌 PÍXEL SELECCIONADO" for idx in indices_tabla]
        
        # Tabla organizada con nombres claros tal como fue solicitado
        tabla_df = pd.DataFrame({
            "ID Píxel (Posición en Vector)": indices_tabla,
            "Intensidad de Color (0-255)": np.round(valores_tabla, 4),
            "Fila en Imagen": indices_tabla // ancho,
            "Columna en Imagen": indices_tabla % ancho,
            "Rol en el Algoritmo": roles
        })
        
        # Resaltar la fila seleccionada usando estilos nativos de Pandas
        styled_df = tabla_df.style.map(
            lambda v: 'background-color: rgba(139, 92, 246, 0.3); color: #FFFFFF; font-weight: bold;' if v == "📌 PÍXEL SELECCIONADO" else '',
            subset=["Rol en el Algoritmo"]
        )
        
        st.dataframe(styled_df, use_container_width=True, height=420)

# =========================================================
# REDUCCIÓN DIMENSIONAL
# =========================================================

elif pagina == "📉 Reducción Dimensional":
    st.title("📉 El Proceso de Reducción Dimensional")
    st.markdown("Cada rostro vive en un espacio inaccesible para nuestra mente de **2914 dimensiones**. Los algoritmos colapsan ese espacio en solo 2 o 3 ejes geométricos.")
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🔴 Alta Dimensión (Antes)\n- 2914 variables independientes por rostro.\n- Estructura geométrica hiperbólica imposible de mapear visualmente.")
    with c2:
        st.markdown("### ⚡ Compresión No Lineal\n- El algoritmo detecta qué pixeles varían juntos (correlaciones complejas) y crea macro-componentes de similitud.")
    with c3:
        st.markdown("### 🟢 Baja Dimensión (Después)\n- Coordenadas proyectadas en planos cartesianos básicos.\n- Preservación perfecta de rasgos genéricos.")

# =========================================================
# UMAP 2D
# =========================================================

elif pagina == "🚀 UMAP 2D":
    st.title("🚀 UMAP — Visualización Interactiva 2D")
    
    n_neighbors = st.slider("n_neighbors (A mayor valor, más enfoque en la estructura global)", 5, 50, 15)
    
    reducer = umap.UMAP(n_components=2, n_neighbors=n_neighbors, random_state=42)
    embedding = reducer.fit_transform(X_scaled)
    
    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "persona": [names[i] for i in y]
    })
    
    st.markdown("Cada punto representa un rostro. Rostros con características morfológicas parecidas son atraídos magnéticamente por las fuerzas del esqueleto simplicial.")
    
    fig = px.scatter(df, x="x", y="y", color="persona", template="plotly_dark", height=650)
    fig.update_traces(marker=dict(size=7, opacity=0.82))
    fig.update_layout(paper_bgcolor="#050816", plot_bgcolor="#050816")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# UMAP 3D
# =========================================================

elif pagina == "🌌 UMAP 3D":
    st.title("🌌 UMAP — Hiperespacio Proyectado en 3D")
    
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

elif pagina == "🧠 t-SNE":
    st.title("🧠 Comparativa con t-SNE")
    st.markdown("t-SNE distribuye los datos basándose en probabilidades Gaussianas locales. Tiende a dispersar más los grupos pero rompe la relación de distancias macroscópicas.")
    
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

elif pagina == "📌 Conclusiones":
    st.title("📌 Conclusiones Estadísticas y Aplicaciones")
    st.markdown("""
    ## Hallazgos Clave
    - **UMAP** demuestra una velocidad y consistencia matemática superior a t-SNE al mantener la coherencia espacial general.
    - Los clusters visibles demuestran que expresiones, orientaciones de rostros y rasgos genómicos se agrupan sin necesidad de darle etiquetas de nombres al algoritmo (aprendizaje no supervisado).
    
    ## Aplicaciones en la Industria
    - **Sistemas Biométricos:** Agrupación rápida de bases de datos criminalísticas.
    - **Compresión de Modelos de IA:** Reducción de costos de procesamiento en redes neuronales convolucionales.
    """)
