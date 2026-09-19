```python
import streamlit as st
from pathlib import Path
import base64

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Biblioteca de Tesis",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background: #f4f7fb;
    }

    /* Ocultar menú y footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Título */
    .titulo {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #12355B;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitulo {
        text-align: center;
        font-size: 19px;
        color: #555555;
        margin-bottom: 30px;
    }

    /* Botones */
    div.stButton > button {
        width: 100%;
        height: 70px;
        border-radius: 15px;
        border: 2px solid #12355B;
        background: white;
        color: #12355B;
        font-size: 21px;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #12355B;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
    }

    /* Contenedor del carrusel */
    .carousel-container {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 20px 10px 30px 10px;
        scroll-behavior: smooth;
    }

    .carousel-container::-webkit-scrollbar {
        height: 10px;
    }

    .carousel-container::-webkit-scrollbar-thumb {
        background: #12355B;
        border-radius: 10px;
    }

    /* Tarjetas */
    .card {
        min-width: 280px;
        max-width: 280px;
        background: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.12);
    }

    .seccion {
        background: white;
        border-radius: 18px;
        padding: 25px;
        margin-top: 25px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    }

    .titulo-tesis {
        color: #12355B;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES
# ============================================================

def cargar_imagenes(carpeta):
    """
    Busca imágenes dentro de una carpeta.
    """

    extensiones = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.webp"
    ]

    imagenes = []

    carpeta = Path(carpeta)

    if carpeta.exists():

        for extension in extensiones:
            imagenes.extend(carpeta.glob(extension))

    return sorted(imagenes)


def mostrar_imagen_grande(imagen, numero):
    """
    Abre la imagen seleccionada en una ventana grande.
    """

    @st.dialog(f"Imagen {numero}", width="large")
    def ventana():

        st.image(
            str(imagen),
            use_container_width=True
        )

        st.caption(
            f"Imagen {numero} — {imagen.name}"
        )

    ventana()


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="titulo">🎓 Biblioteca de Tesis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Seleccione una tesis para explorar sus imágenes'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# MENÚ DE TESIS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📘 TESIS 1", key="tesis1"):
        st.session_state.tesis = 1

with col2:
    if st.button("📗 TESIS 2", key="tesis2"):
        st.session_state.tesis = 2

with col3:
    if st.button("📙 TESIS 3", key="tesis3"):
        st.session_state.tesis = 3


# ============================================================
# TESIS SELECCIONADA
# ============================================================

if "tesis" not in st.session_state:

    st.info(
        "👆 Seleccione una de las tres tesis para comenzar."
    )

else:

    tesis = st.session_state.tesis

    carpeta = f"imagenes/tesis{tesis}"

    imagenes = cargar_imagenes(carpeta)

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="seccion">
            <div class="titulo-tesis">
                📚 Tesis {tesis}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SI NO HAY IMÁGENES
    # --------------------------------------------------------

    if not imagenes:

        st.warning(
            f"No se encontraron imágenes en la carpeta: "
            f"`{carpeta}`"
        )

    else:

        st.write("### 🖼️ Galería de imágenes")

        # ----------------------------------------------------
        # CARRUSEL
        # ----------------------------------------------------

        cols = st.columns(4)

        for i, imagen in enumerate(imagenes):

            col = cols[i % 4]

            with col:

                st.image(
                    str(imagen),
                    use_container_width=True
                )

                if st.button(
                    "🔍 Ver imagen completa",
                    key=f"ver_{tesis}_{i}"
                ):

                    mostrar_imagen_grande(
                        imagen,
                        i + 1
                    )

                st.caption(
                    f"Imagen {i + 1}"
                )

        # ----------------------------------------------------
        # INFORMACIÓN
        # ----------------------------------------------------

        st.divider()

        st.write(
            f"**{len(imagenes)} imágenes disponibles**"
        )
```
