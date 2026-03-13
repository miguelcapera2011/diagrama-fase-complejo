import streamlit as st

st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="centered"
)

# ------------------ ESTILO ------------------

st.markdown("""
<style>

.main-title{
text-align:center;
font-size:50px;
font-weight:bold;
margin-top:120px;
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

.sidebar-title{
display:flex;
align-items:center;
gap:10px;
font-size:22px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)


# ------------------ SIDEBAR ------------------

st.sidebar.markdown("""
<div class="sidebar-title">
<img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" width="30">
<span>Minería de Datos</span>
</div>
""", unsafe_allow_html=True)


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


# ------------------ PORTADA ------------------

def portada():

    st.markdown(
    '<div class="main-title">Ética del Análisis de Datos Agrícolas</div>',
    unsafe_allow_html=True
    )

    st.markdown("""
    <div class="subtitle">

    Miguel Ángel Garatejo Capera  

    Universidad del Tolima  

    </div>
    """, unsafe_allow_html=True)



# ------------------ FUNCION SECCION ------------------

def seccion(titulo, texto, img, extra, img2):

    st.markdown(f'<div class="slide-title">{titulo}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="slide-text">{texto}</div>', unsafe_allow_html=True)

    st.image(img, use_container_width=True)

    with st.expander("🔎 Ver más información", key=titulo):

        st.write(extra)

        st.image(img2, use_container_width=True)



# ------------------ SECCIONES ------------------

def agricultura():

    seccion(
    "Agricultura Digital",

    "Uso de sensores, drones e inteligencia artificial para analizar datos agrícolas y mejorar la producción.",

    "https://images.unsplash.com/photo-1598514983318-2f64f8f4796c",

    """
La agricultura digital utiliza tecnologías como sensores,
drones e inteligencia artificial para recopilar datos
sobre cultivos, suelos y clima.

Esto permite optimizar el uso de agua, fertilizantes
y otros recursos agrícolas.
    """,

    "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )


def etica():

    seccion(
    "Problemas Éticos",

    "La digitalización agrícola genera desafíos relacionados con privacidad y propiedad de datos.",

    "https://images.unsplash.com/photo-1581092335397-9583eb92d232",

    """
El análisis de datos agrícolas plantea preguntas éticas importantes.

Por ejemplo, quién es el propietario de los datos
generados por sensores o maquinaria agrícola.

También existe el riesgo de que empresas tecnológicas
acumulen grandes cantidades de información.
    """,

    "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
    )


def privacidad():

    seccion(
    "Privacidad de los Agricultores",

    "Los sistemas agrícolas recopilan información sensible como ubicación de parcelas y rendimiento.",

    "https://images.unsplash.com/photo-1605000797499-95a51c5269ae",

    """
Los datos agrícolas pueden revelar información estratégica
sobre producción y uso de insumos.

Si estos datos no se protegen adecuadamente,
pueden generar riesgos de privacidad
o pérdidas económicas para los agricultores.
    """,

    "https://images.unsplash.com/photo-1563986768609-322da13575f3"
    )


def empresas():

    seccion(
    "Empresas Tecnológicas",

    "Las plataformas digitales pueden concentrar grandes volúmenes de datos agrícolas.",

    "https://images.unsplash.com/photo-1509395176047-4a66953fd231",

    """
Muchas empresas tecnológicas han transformado
la maquinaria agrícola en sistemas conectados.

Esto permite recopilar datos de miles de productores,
pero también genera riesgos de concentración de poder.
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

También existen modelos como los data trusts,
donde los datos son administrados bajo principios éticos.
    """,

    "https://images.unsplash.com/photo-1592997572594-34be01bc36c7"
    )


def conclusion():

    seccion(
    "Conclusión",

    "La ética en datos agrícolas busca una digitalización justa y sostenible.",

    "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",

    """
La digitalización agrícola ofrece grandes beneficios,
pero también requiere regulaciones claras.

La privacidad, la transparencia y la equidad
son fundamentales para un desarrollo agrícola sostenible.
    """,

    "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )


# ------------------ NAVEGACION ------------------

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
