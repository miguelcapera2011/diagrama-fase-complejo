import streamlit as st

st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="centered"
)

# --- ESTILO VISUAL ---
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

# --- PORTADA ---

def portada():

    st.markdown('<div class="main-title">Ética del Análisis de Datos Agrícolas</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">
    Miguel Ángel Garatejo Capera  
    <br>
    Universidad del Tolima  
    <br>
    Curso: Minería de Datos
    </div>
    """, unsafe_allow_html=True)

# --- FUNCION GENERICA PARA SECCIONES ---

def seccion(titulo, texto, img, extra, img2):

    st.markdown(f'<div class="slide-title">{titulo}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="slide-text">{texto}</div>', unsafe_allow_html=True)

    st.image(img, use_container_width=True)

    if st.button(f"Ver más sobre {titulo}"):

        with st.modal(titulo):

            st.write(extra)

            st.image(img2, use_container_width=True)


# --- CONTENIDO ---

def agricultura():

    seccion(
        "Agricultura Digital",

        "Uso de sensores, drones e inteligencia artificial para analizar datos agrícolas y mejorar la producción.",

        "https://images.unsplash.com/photo-1598514983318-2f64f8f4796c",

        """
La agricultura digital se basa en la recolección masiva de datos sobre suelos,
clima, cultivos y maquinaria agrícola.

Estos datos permiten a los agricultores tomar decisiones más informadas,
optimizar el uso de recursos como agua o fertilizantes y anticipar riesgos
como plagas o cambios climáticos.

Esta transformación forma parte de la llamada agricultura de precisión,
donde cada decisión se basa en información detallada obtenida mediante tecnología.
        """,

        "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )


def etica():

    seccion(
        "Problemas Éticos",

        "La digitalización agrícola genera desafíos relacionados con privacidad, propiedad de datos y uso por empresas tecnológicas.",

        "https://images.unsplash.com/photo-1581092335397-9583eb92d232",

        """
El análisis de datos agrícolas plantea preguntas fundamentales:

¿Quién es el propietario de los datos generados en las fincas?

Muchas plataformas digitales recopilan información que puede ser utilizada
para fines comerciales sin que los agricultores tengan control total.

Esto puede generar desigualdades en el sector agrícola y dependencia
tecnológica hacia grandes empresas que controlan la infraestructura digital.
        """,

        "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
    )


def privacidad():

    seccion(
        "Privacidad de los Agricultores",

        "Los sistemas agrícolas recopilan información sensible como ubicación de parcelas y rendimiento de cultivos.",

        "https://images.unsplash.com/photo-1605000797499-95a51c5269ae",

        """
Los datos generados por sensores, drones o maquinaria pueden revelar
información estratégica sobre la producción agrícola.

Si estos datos se utilizan sin protección adecuada,
los agricultores pueden perder privacidad o incluso ventajas económicas.

Por esta razón, es necesario aplicar medidas de seguridad como
encriptación, anonimización y políticas claras de protección de datos.
        """,

        "https://images.unsplash.com/photo-1563986768609-322da13575f3"
    )


def empresas():

    seccion(
        "Empresas Tecnológicas",

        "Las plataformas digitales agrícolas pueden concentrar grandes cantidades de información.",

        "https://images.unsplash.com/photo-1509395176047-4a66953fd231",

        """
Muchas empresas tecnológicas han pasado de fabricar maquinaria
a convertirse en proveedores de servicios de análisis de datos.

Esto significa que pueden almacenar información sobre millones de hectáreas
de cultivo alrededor del mundo.

Si no existen regulaciones adecuadas,
los agricultores podrían perder control sobre el valor económico de sus propios datos.
        """,

        "https://images.unsplash.com/photo-1464226184884-fa280b87c399"
    )


def gobernanza():

    seccion(
        "Gobernanza de Datos",

        "Existen modelos alternativos como cooperativas de datos y plataformas colaborativas.",

        "https://images.unsplash.com/photo-1523741543316-beb7fc7023d8",

        """
Para equilibrar el poder entre agricultores y empresas,
han surgido modelos de gobernanza de datos.

Entre ellos destacan las cooperativas de datos,
donde los agricultores gestionan colectivamente su información.

También existen los llamados data trusts,
entidades que administran datos bajo principios éticos
y garantizan que los beneficios se distribuyan de forma justa.
        """,

        "https://images.unsplash.com/photo-1592997572594-34be01bc36c7"
    )


def conclusion():

    seccion(
        "Conclusión",

        "La agricultura digital ofrece grandes beneficios, pero requiere principios éticos claros.",

        "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",

        """
La ética del análisis de datos agrícolas busca garantizar que la tecnología
beneficie realmente a los agricultores y a la sociedad.

Esto implica proteger la privacidad, garantizar transparencia,
promover inclusión y crear regulaciones justas.

Si estos principios se respetan,
la digitalización puede contribuir a una agricultura más sostenible,
eficiente y equitativa.
        """,

        "https://images.unsplash.com/photo-1500382017468-9049fed747ef"
    )


# --- MENU ---

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
