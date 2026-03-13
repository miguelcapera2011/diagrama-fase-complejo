import streamlit as st

st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="centered"
)

# ---- ESTILO ----

st.markdown("""
<style>

.main-title{
text-align:center;
font-size:50px;
font-weight:bold;
margin-top:100px;
}

.subtitle{
text-align:center;
font-size:22px;
}

.slide-title{
font-size:34px;
font-weight:600;
margin-top:40px;
}

.slide-text{
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ---- PORTADA ----

def portada():

    st.markdown('<div class="main-title">Ética del Análisis de Datos Agrícolas</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">

    Miguel Ángel Garatejo Capera  

    Universidad del Tolima  

    Curso: Minería de Datos

    </div>
    """, unsafe_allow_html=True)


# ---- FUNCION DE SECCION ----

def seccion(titulo, texto, img, extra, img2):

    st.markdown(f'<div class="slide-title">{titulo}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="slide-text">{texto}</div>', unsafe_allow_html=True)

    st.image(img, use_container_width=True)

    with st.expander("🔎 Ver más información"):

        st.write(extra)

        st.image(img2, use_container_width=True)


# ---- SECCIONES ----

def agricultura():

    seccion(
        "Agricultura Digital",

        "Uso de sensores, drones e inteligencia artificial para analizar datos agrícolas y mejorar la producción.",

        "https://images.unsplash.com/photo-1598514983318-2f64f8f4796c",

        """
La agricultura digital utiliza tecnologías avanzadas para recopilar
datos sobre suelos, cultivos, clima y maquinaria.

Estos datos permiten optimizar el uso de recursos como agua,
fertilizantes y energía.

Además, ayudan a anticipar riesgos climáticos o plagas,
permitiendo tomar decisiones más eficientes y sostenibles.
        """,

        "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )


def etica():

    seccion(
        "Problemas Éticos",

        "La digitalización agrícola genera desafíos relacionados con privacidad y propiedad de datos.",

        "https://images.unsplash.com/photo-1581092335397-9583eb92d232",

        """
La recopilación masiva de datos agrícolas plantea preguntas éticas importantes.

Por ejemplo, quién es el propietario de los datos generados
por sensores o maquinaria.

También existe el riesgo de que grandes empresas tecnológicas
controlen grandes cantidades de información agrícola,
lo que podría generar desigualdades en el sector.
        """,

        "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
    )


def privacidad():

    seccion(
        "Privacidad de los Agricultores",

        "Los sistemas agrícolas recopilan información sensible como ubicación y rendimiento de cultivos.",

        "https://images.unsplash.com/photo-1605000797499-95a51c5269ae",

        """
Los datos agrícolas pueden revelar información estratégica
sobre la producción de una finca.

Por ejemplo, ubicación exacta de parcelas,
rendimiento de cultivos o uso de insumos.

Si estos datos no se protegen adecuadamente,
podrían ser utilizados de forma indebida
o generar desventajas económicas para los agricultores.
        """,

        "https://images.unsplash.com/photo-1563986768609-322da13575f3"
    )


def empresas():

    seccion(
        "Empresas Tecnológicas",

        "Las plataformas agrícolas pueden concentrar grandes volúmenes de datos.",

        "https://images.unsplash.com/photo-1509395176047-4a66953fd231",

        """
Muchas empresas tecnológicas han transformado
la maquinaria agrícola en sistemas digitales conectados.

Esto permite recopilar datos de miles de agricultores.

Sin regulaciones claras,
los agricultores podrían perder control
sobre el valor económico de su información.
        """,

        "https://images.unsplash.com/photo-1464226184884-fa280b87c399"
    )


def gobernanza():

    seccion(
        "Gobernanza de Datos",

        "Modelos como cooperativas de datos permiten mayor control para los agricultores.",

        "https://images.unsplash.com/photo-1523741543316-beb7fc7023d8",

        """
Los modelos de gobernanza de datos buscan equilibrar
las relaciones entre agricultores y empresas tecnológicas.

Entre estos modelos se encuentran las cooperativas de datos,
donde los agricultores gestionan colectivamente su información.

También existen data trusts,
organizaciones que administran datos bajo principios éticos.
        """,

        "https://images.unsplash.com/photo-1592997572594-34be01bc36c7"
    )


def conclusion():

    seccion(
        "Conclusión",

        "La ética en datos agrícolas busca una digitalización justa y sostenible.",

        "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",

        """
La digitalización agrícola ofrece grandes oportunidades
para mejorar la producción y sostenibilidad.

Sin embargo,
es fundamental garantizar privacidad,
transparencia y control de los datos por parte de los agricultores.

Solo así la tecnología podrá contribuir
a un sistema agrícola más justo y equilibrado.
        """,

        "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )


# ---- MENU ----

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
