import streamlit as st

st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="centered"
)

# -------- COLORES Y ESTILO --------

st.markdown("""
<style>

body {
background-color:#f4f8f6;
}

.header{
display:flex;
align-items:center;
gap:10px;
font-size:20px;
font-weight:bold;
color:#2c6e49;
}

.main-title{
text-align:center;
font-size:48px;
font-weight:bold;
margin-top:80px;
color:#2c6e49;
}

.subtitle{
text-align:center;
font-size:22px;
color:#555;
}

.slide-title{
font-size:34px;
font-weight:600;
margin-top:30px;
color:#1b4332;
}

.slide-text{
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# -------- HEADER --------

st.markdown("""
<div class="header">
<img src="https://cdn-icons-png.flaticon.com/512/4149/4149670.png" width="40">
Minería de Datos
</div>
""", unsafe_allow_html=True)

# -------- PORTADA --------

def portada():

    st.markdown('<div class="main-title">Ética del Análisis de Datos Agrícolas</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">

    Miguel Ángel Garatejo Capera  

    Universidad del Tolima  

    Curso: Minería de Datos

    </div>
    """, unsafe_allow_html=True)

# -------- CONTROL PARA OCULTAR INFO --------

if "expander_state" not in st.session_state:
    st.session_state.expander_state = False

# -------- FUNCION SECCION --------

def seccion(titulo, texto, img, extra, img2):

    st.markdown(f'<div class="slide-title">{titulo}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="slide-text">{texto}</div>', unsafe_allow_html=True)

    st.image(img, use_container_width=True)

    with st.expander("🔎 Ver más información", expanded=False):

        st.write(extra)

        st.image(img2, use_container_width=True)

# -------- SECCIONES --------

def agricultura():

    seccion(
        "Agricultura Digital",

        "Uso de sensores, drones e inteligencia artificial para analizar datos agrícolas y mejorar la producción.",

        "https://images.unsplash.com/photo-1598514983318-2f64f8f4796c",

        """
La agricultura digital utiliza sensores, drones y plataformas digitales
para recopilar información sobre suelos, cultivos y clima.

Esto permite mejorar la productividad, optimizar recursos y tomar
decisiones basadas en datos en lugar de solo experiencia.
        """,

        "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )


def etica():

    seccion(
        "Problemas Éticos",

        "La digitalización agrícola genera desafíos relacionados con privacidad y propiedad de datos.",

        "https://images.unsplash.com/photo-1581092335397-9583eb92d232",

        """
El uso de datos agrícolas plantea preguntas importantes sobre quién
controla la información y cómo se utiliza.

Si grandes empresas tecnológicas concentran los datos,
los agricultores podrían perder control sobre su propio conocimiento agrícola.
        """,

        "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
    )


def privacidad():

    seccion(
        "Privacidad de los Agricultores",

        "Los sistemas agrícolas recopilan información sensible como ubicación y producción.",

        "https://images.unsplash.com/photo-1605000797499-95a51c5269ae",

        """
Los datos agrícolas pueden revelar información estratégica
sobre el rendimiento de cultivos o prácticas agrícolas.

Por eso es necesario aplicar medidas de seguridad como
anonimización y cifrado de datos.
        """,

        "https://images.unsplash.com/photo-1563986768609-322da13575f3"
    )


def empresas():

    seccion(
        "Empresas Tecnológicas",

        "Las plataformas agrícolas pueden concentrar grandes volúmenes de información.",

        "https://images.unsplash.com/photo-1509395176047-4a66953fd231",

        """
Muchas empresas tecnológicas ahora gestionan plataformas de datos agrícolas.

Esto puede generar dependencia tecnológica y concentración de poder
si los agricultores no tienen control sobre su información.
        """,

        "https://images.unsplash.com/photo-1464226184884-fa280b87c399"
    )


def gobernanza():

    seccion(
        "Gobernanza de Datos",

        "Modelos como cooperativas de datos permiten mayor control para los agricultores.",

        "https://images.unsplash.com/photo-1523741543316-beb7fc7023d8",

        """
Las cooperativas de datos permiten que los agricultores
gestionen colectivamente su información.

Esto ayuda a equilibrar las relaciones entre agricultores
y empresas tecnológicas.
        """,

        "https://images.unsplash.com/photo-1592997572594-34be01bc36c7"
    )


def conclusion():

    seccion(
        "Conclusión",

        "La ética en datos agrícolas busca una digitalización justa y sostenible.",

        "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",

        """
La digitalización agrícola puede mejorar la producción,
pero requiere principios éticos claros.

La privacidad, transparencia y control de datos
son fundamentales para un futuro agrícola sostenible.
        """,

        "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )

# -------- MENU --------

menu = st.sidebar.radio(
    "Secciones",
    [
        "Portada",
        "Agricultura Digital",
        "Problemas Éticos",
        "Privacidad",
        "Empresas Tecnológicas",
        "Gobernanza",
        "Conclusión"
    ]
)

# Reinicia el estado al cambiar sección
st.session_state.expander_state = False

if menu == "Portada":
    portada()

elif menu == "Agricultura Digital":
    agricultura()

elif menu == "Problemas Éticos":
    etica()

elif menu == "Privacidad":
    privacidad()

elif menu == "Empresas Tecnológicas":
    empresas()

elif menu == "Gobernanza":
    gobernanza()

elif menu == "Conclusión":
    conclusion()
