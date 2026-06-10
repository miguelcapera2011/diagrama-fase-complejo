
# LIBRERÍAS
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import umap

from sklearn.datasets import fetch_lfw_people
from sklearn.preprocessing import StandardScaler

# CONFIGURACIÓN

st.set_page_config(
    page_title="UMAP - Reducción Dimensional",
    page_icon="https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
    layout="wide"
)

# CSS E ICONOS

st.markdown("""
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<style>

/* Fondo principal */
.stApp {
    background:
    radial-gradient(circle at top left, #2e1065 0%, #090514 45%),
    radial-gradient(circle at bottom right, #083344 0%, #02243a 50%);
    color: #f8fafc;
}


/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0726 0%, #05020f 100%);
    border-right: 1px solid rgba(192,132,252,0.15);
}


/* Título del menú */
.sidebar-title {

    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.5px;

    background:
    linear-gradient(90deg,#38bdf8,#c084fc);

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    padding-bottom: 12px;
    border-bottom: 1px solid rgba(192,132,252,0.2);
    margin-bottom: 20px;
}


/* Iconos */
.title-icon {

    background:
    linear-gradient(135deg,#38bdf8,#e879f9);

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    font-size:30px;
    margin-right:12px;
}


/* Texto */
h1,h2,h3,h4 {

    color:white;
    font-weight:700;
}

p,label,div {

    color:#e2e8f0;
}


/* Encabezado principal */

.main-header {

    background:
    linear-gradient(
    135deg,
    rgba(168,85,247,0.25),
    rgba(6,182,212,0.15));

    padding:35px;

    border-radius:24px;

    border:
    1px solid rgba(192,132,252,0.3);

    margin-bottom:30px;

    box-shadow:
    0 8px 32px rgba(168,85,247,0.1);
}


.main-header h1 {

    font-size:36px;
    font-weight:800;
}


.subtitle {

    color:#38bdf8;
    font-size:15px;
    font-weight:700;

    letter-spacing:1.5px;
}


/* Tarjetas de métricas */

.metric-card {

    background:
    linear-gradient(
    145deg,
    rgba(147,51,234,0.15),
    rgba(15,23,42,0.6));

    border-radius:22px;

    padding:24px;

    text-align:center;

    border:
    1px solid rgba(56,189,248,0.2);
}


.metric-card i {

    font-size:26px;
    color:#38bdf8;
}


.metric-card h3 {

    color:#94a3b8;
    font-size:11px;
}


.metric-card h1 {

    font-size:34px;
}


.metric-card p {

    color:#94a3b8;
}


/* Imágenes */

img {

    border-radius:20px;

    box-shadow:
    0 15px 35px rgba(0,0,0,0.6);
}


/* Caja informativa */

.info-box {

    background:
    rgba(6,182,212,0.08);

    border-left:
    4px solid #06b6d4;

    padding:16px;

    border-radius:0 12px 12px 0;
}


</style>

""", unsafe_allow_html=True)

# SIDEBAR

st.sidebar.markdown(
"""
<div class="sidebar-title">
<i class="bi bi-cpu-fill"></i>
ANÁLISIS MULTIVARIADO
</div>
""",
unsafe_allow_html=True
)


st.sidebar.markdown(
"""
<p style="font-size:13px;color:#94a3b8;">
Reducción de dimensionalidad utilizando UMAP para transformar imágenes de rostros en representaciones más simples que permiten descubrir patrones y similitudes.
</p>
""",
unsafe_allow_html=True
)


pagina = st.sidebar.radio(
    "Contenido",
    [
        "Introducción",
        "Dataset Original",
        "Conversión Matemática",
        "Reducción Dimensional",
        "UMAP 2D",
        "UMAP 3D",
        "Conclusiones"
    ]
)

# CARGA DEL DATASET

@st.cache_data
def cargar_datos():

    lfw = fetch_lfw_people(
        min_faces_per_person=70
    )

    X = lfw.data
    y = lfw.target
    images = lfw.images
    names = lfw.target_names

    return X,y,images,names


X,y,images,names = cargar_datos()

# ESCALADO

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# MÉTRICAS


n_imagenes = X.shape[0]

n_variables = X.shape[1]

n_personas = len(names)

# INTRODUCCIÓN

if pagina == "Introducción":


    st.markdown(
    """
    <div class="main-header">

    <div class="subtitle">
    <i class="bi bi-diagram-3-fill"></i>
    <h2>
    Uniform Manifold Approximation and Projection (UMAP)
    </h2>
    </div>


    <h1>
    Descubriendo patrones ocultos en los rostros
    </h1>


    <p style="color:#cbd5e1; font-size:15px;">

    Esta aplicación muestra cómo una computadora convierte una imagen en datos numéricos y cómo UMAP reduce miles de características a una representación más sencilla en 2D o 3D, permitiendo observar similitudes entre diferentes rostros.

    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    c1,c2,c3,c4 = st.columns(4)


    with c1:

        st.markdown(f"""
        <div class="metric-card">
        <i class="bi bi-bounding-box-circles"></i>
        <h3>DIMENSIONES</h3>
        <h1>{n_variables}</h1>
        <p>valores por imagen</p>
        </div>
        """, unsafe_allow_html=True)


    with c2:

        st.markdown(f"""
        <div class="metric-card">
        <i class="bi bi-people-fill"></i>
        <h3>IMÁGENES</h3>
        <h1>{n_imagenes}</h1>
        <p>rostros del dataset</p>
        </div>
        """, unsafe_allow_html=True)


    with c3:

        st.markdown("""
        <div class="metric-card">
        <i class="bi bi-activity"></i>
        <h3>ALGORITMO</h3>
        <h1>UMAP</h1>
        <p>reducción dimensional</p>
        </div>
        """, unsafe_allow_html=True)


    with c4:

        st.markdown("""
        <div class="metric-card">
        <i class="bi bi-projector-fill"></i>
        <h3>VISUALIZACIÓN</h3>
        <h1>2D / 3D</h1>
        <p>mapas interactivos</p>
        </div>
        """, unsafe_allow_html=True)


    col1,col2 = st.columns([1.8,1])


    with col1:


        st.markdown("""

## ¿Por qué necesitamos reducir dimensiones?

Cada imagen está formada por miles de píxeles. Cada píxel contiene un valor numérico que representa la intensidad de luz en una posición determinada.

Cuando reunimos todos esos valores, un rostro queda representado por 2914 características numéricas. Esto crea un espacio de alta dimensionalidad que no podemos visualizar directamente.

UMAP permite transformar este espacio complejo en una representación de dos o tres dimensiones, intentando conservar la relación de similitud entre los rostros originales.

""")

    with col2:


        st.image(
            images[0],
            use_container_width=True
        )


        st.markdown("""
        <div class="info-box">

        <b>Idea principal:</b>
        La computadora no ve un rostro como nosotros. Para ella una imagen es una colección de números donde cada valor corresponde a un píxel.

        </div>
        """,
        unsafe_allow_html=True
        )
        
# DATASET ORIGINAL

elif pagina == "Dataset Original":

    st.markdown(
    """
    <h1>
    <i class="bi bi-images title-icon"></i>
    Dataset Original: LFW
    </h1>
    """,
    unsafe_allow_html=True
    )


    st.markdown("""
    Trabajamos con el conjunto de datos 
    <b>LFW (Labeled Faces in the Wild)</b>, una colección de fotografías reales de diferentes personas.

    Este dataset es ampliamente utilizado en investigaciones de reconocimiento facial y aprendizaje automático, ya que permite estudiar cómo una computadora puede encontrar similitudes y diferencias entre distintos rostros.
    """,
    unsafe_allow_html=True
    )


    st.markdown("---")


    st.subheader("Ejemplos de imágenes del conjunto de datos")


    cols = st.columns(5)


    for i in range(10):

        with cols[i % 5]:

            st.image(
                images[i],
                caption=names[y[i]],
                use_container_width=True
            )


    st.markdown(
    """
    <div class="info-box">

    <b>Dato importante:</b>
    Aunque nosotros vemos una fotografía de una persona, la computadora almacena esta imagen como una matriz de valores numéricos donde cada número representa la intensidad de un píxel.

    </div>
    """,
    unsafe_allow_html=True
    )

# CONVERSIÓN MATEMÁTICA

elif pagina == "Conversión Matemática":


    st.markdown(
    """
    <h1>
    <i class="bi bi-calculator title-icon"></i>
    De una imagen a un vector matemático
    </h1>
    """,
    unsafe_allow_html=True
    )


    st.markdown("""
    Una imagen está organizada inicialmente como una matriz de píxeles. Para que un algoritmo matemático pueda analizarla, la imagen se transforma en un vector, donde cada posición corresponde a un píxel y su valor indica la intensidad de ese píxel.
    """)


    image = images[0]

    alto, ancho = image.shape


    vector = X[0]


    pixel_index = st.slider(
        "Selecciona una posición del vector para identificar el píxel correspondiente:",
        0,
        len(vector) - 1,
        100
    )


    valor_pixel = vector[pixel_index]


    fila = pixel_index // ancho

    columna = pixel_index % ancho


    imagen_color = np.stack([image] * 3, axis=-1)

    imagen_color = imagen_color / imagen_color.max()


    # Se resalta el píxel seleccionado en color rojo
    imagen_color[fila, columna] = [1, 0, 0]


    c1, c2 = st.columns([1, 1])

    # Imagen original con píxel resaltado

    with c1:


        st.subheader("Ubicación del píxel dentro de la imagen")


        fig = px.imshow(imagen_color)


        fig.update_layout(
            height=420,
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            ),
            coloraxis_showscale=False
        )


        fig.update_xaxes(showticklabels=False)

        fig.update_yaxes(showticklabels=False)


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.markdown(
        f"""
        <div class="info-box">

        <b>Información del píxel seleccionado:</b><br><br>

        • Posición en el vector: {pixel_index}<br>
        • Ubicación en la imagen: fila {fila}, columna {columna}<br>
        • Intensidad del píxel: {valor_pixel:.2f}

        </div>
        """,
        unsafe_allow_html=True
        )
        
    # Representación del vector


    with c2:


        st.subheader(
            "Representación del vector de la imagen"
        )


        st.markdown("""
        A continuación observamos una pequeña parte del vector que representa la imagen. Cada posición corresponde a un píxel de la fotografía original.
        """)


        rango_min = max(
            0,
            pixel_index - 5
        )

        rango_max = min(
            len(vector),
            pixel_index + 6
        )


        indices_tabla = np.arange(
            rango_min,
            rango_max
        )


        valores_tabla = vector[
            rango_min:rango_max
        ]


        estado = [
            "Píxel cercano"
            if idx != pixel_index
            else "PÍXEL SELECCIONADO"
            for idx in indices_tabla
        ]


        tabla_df = pd.DataFrame({

            "Posición en el vector": indices_tabla,

            "Valor de intensidad": np.round(
                valores_tabla,
                4
            ),

            "Fila en la imagen":
            indices_tabla // ancho,


            "Columna en la imagen":
            indices_tabla % ancho,


            "Descripción":
            estado
        })


        styled_df = tabla_df.style.map(

            lambda valor:
            "background-color: rgba(168,85,247,0.4);"
            "color:white;font-weight:bold;"
            if valor == "PÍXEL SELECCIONADO"
            else "",

            subset=["Descripción"]

        )


        st.dataframe(
            styled_df,
            use_container_width=True,
            height=420
        )


    st.markdown("---")


    st.markdown("""
    ## Idea clave

    Una imagen que nosotros observamos como un rostro, para la computadora es simplemente una gran lista de números.

    En este caso, cada rostro queda representado por un vector de 2914 valores, donde cada número guarda la información de un píxel específico.

    Esta representación matemática es la que permite aplicar algoritmos como UMAP para encontrar patrones y similitudes entre las imágenes.
    """)
# REDUCCIÓN DIMENSIONAL

elif pagina == "Reducción Dimensional":

    st.markdown("""
    <h1>
    <i class="bi bi-funnel-fill title-icon"></i>
    Reducción de Dimensionalidad
    </h1>
    """,
    unsafe_allow_html=True)


    st.markdown("""
    Después de convertir cada imagen en un vector de 2914 valores, cada rostro se representa como un punto dentro de un espacio de 2914 dimensiones.

    Este espacio es demasiado complejo para ser visualizado por una persona. Por esta razón utilizamos UMAP, un algoritmo capaz de encontrar una representación más pequeña de los datos conservando, en la medida de lo posible, la relación de similitud entre los rostros.
    """)


    st.markdown("---")


    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown("""
        ### 🔴 Espacio original

        - Cada rostro está descrito por 2914 características.
        - Es un espacio matemático muy grande que no podemos visualizar directamente.
        """)


    with c2:

        st.markdown("""
        ### 🧠 Algoritmo UMAP

        - Analiza qué rostros son más similares entre sí.
        - Construye una representación más sencilla manteniendo esas relaciones de cercanía.
        """)


    with c3:

        st.markdown("""
        ### 🟢 Nuevo espacio

        - Los datos se representan en 2 o 3 dimensiones.
        - Podemos observar agrupamientos y patrones entre rostros similares.
        """)

# UMAP 2D

elif pagina == "UMAP 2D":

    st.markdown("""
    <h1>
    <i class="bi bi-grid-3x3 title-icon"></i>
    Visualización UMAP en 2 Dimensiones
    </h1>
    """,
    unsafe_allow_html=True)


    st.markdown("""
    En esta representación, cada punto corresponde a un rostro del conjunto de datos.

    Cuando dos puntos aparecen cercanos significa que UMAP encontró características similares entre esos rostros. Por el contrario, puntos alejados indican rostros con mayores diferencias.
    """)


    n_neighbors = st.slider(
        "Parámetro n_neighbors (cantidad de vecinos que UMAP analiza)",
        5,
        50,
        15
    )


    st.markdown("""
    El parámetro **n_neighbors** controla cuánta información del entorno cercano utiliza UMAP.

    Valores pequeños se enfocan en detalles locales y grupos pequeños, mientras que valores mayores intentan conservar una estructura más general de todos los datos.
    """)


    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=n_neighbors,
        random_state=42
    )


    embedding = reducer.fit_transform(X_scaled)


    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "persona": [names[i] for i in y]
    })


    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="persona",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        template="plotly_dark",
        height=650
    )


    fig.update_traces(
        marker=dict(
            size=7,
            opacity=0.85
        )
    )


    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.5)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# UMAP 3D

elif pagina == "UMAP 3D":

    st.markdown("""
    <h1>
    <i class="bi bi-box-seam title-icon"></i>
    Visualización UMAP en 3 Dimensiones
    </h1>
    """,
    unsafe_allow_html=True)


    st.markdown("""
    Esta visualización utiliza el mismo principio de UMAP 2D, pero agrega una tercera dimensión que permite observar con mayor detalle la separación y los grupos existentes entre los diferentes rostros.
    """)


    reducer = umap.UMAP(
        n_components=3,
        random_state=42
    )


    embedding = reducer.fit_transform(X_scaled)


    df = pd.DataFrame({
        "x": embedding[:, 0],
        "y": embedding[:, 1],
        "z": embedding[:, 2],
        "persona": [names[i] for i in y]
    })


    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="persona",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        template="plotly_dark",
        height=750
    )


    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# CONCLUSIONES


elif pagina == "Conclusiones":

    st.markdown("""
    <h1>
    <i class="bi bi-award title-icon"></i>
    Conclusiones
    </h1>
    """,
    unsafe_allow_html=True)


    st.markdown("""
    ## Principales resultados

    - Una imagen puede transformarse en un conjunto de miles de valores numéricos, donde cada número representa la intensidad de un píxel.

    - Cada rostro queda representado como un punto en un espacio de 2914 dimensiones, un espacio imposible de visualizar directamente.

    - UMAP permite reducir este espacio complejo a una representación en 2 o 3 dimensiones conservando la información de similitud entre los rostros.

    - Los grupos observados en los gráficos muestran que los rostros con características parecidas tienden a ubicarse cerca unos de otros.

    ---

    ## Aspectos importantes del proceso

    - El escalado mediante **StandardScaler** permite que todos los píxeles tengan una influencia equilibrada durante el análisis.

    - El parámetro **n_neighbors** controla si UMAP se concentra más en relaciones locales entre pocos rostros o en la estructura general del conjunto de datos.

    - La reducción de dimensionalidad facilita la exploración visual de grandes conjuntos de datos y ayuda a descubrir patrones ocultos que no son evidentes en espacios de alta dimensión.
    """)
