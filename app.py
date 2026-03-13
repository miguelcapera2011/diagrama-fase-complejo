import streamlit as st

# CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="wide"
)

# ----- PORTADA -----

def portada():
    st.title("🌱 Ética del Análisis de Datos Agrícolas")

    st.subheader("Digitalización, privacidad y gobernanza de datos")

    st.markdown(
    """
    **Miguel Ángel Garatejo Capera**  
    Universidad del Tolima  
    """
    )

    st.image(
        "https://images.unsplash.com/photo-1500382017468-9049fed747ef",
        caption="Agricultura moderna y tecnología",
        use_container_width=True
    )

    st.markdown("""
    Esta aplicación presenta los principales aspectos éticos relacionados con el uso de datos en la agricultura digital.
    """)


# ----- SECCIONES -----

def agricultura_digital():

    st.header("Agricultura Digital")

    st.write("""
    Uso de tecnologías como sensores, drones e inteligencia artificial para analizar datos agrícolas y mejorar la producción.
    """)

    st.image(
        "https://images.unsplash.com/photo-1598514983318-2f64f8f4796c",
        caption="Drones y tecnología en agricultura",
        use_container_width=True
    )


def problema_etico():

    st.header("Problemas Éticos en los Datos Agrícolas")

    st.write("""
    La digitalización agrícola plantea desafíos importantes relacionados con la privacidad,
    propiedad de los datos, transparencia y control de la información.
    """)

    st.image(
        "https://images.unsplash.com/photo-1581092335397-9583eb92d232",
        caption="Datos y tecnología en el campo",
        use_container_width=True
    )


def privacidad():

    st.header("Privacidad de los Agricultores")

    st.write("""
    Los sistemas digitales recopilan información como ubicación de parcelas,
    rendimiento de cultivos y uso de insumos, lo que requiere medidas para proteger la privacidad.
    """)

    st.image(
        "https://images.unsplash.com/photo-1605000797499-95a51c5269ae",
        caption="Tecnología agrícola y monitoreo de cultivos",
        use_container_width=True
    )


def empresas():

    st.header("Empresas Tecnológicas")

    st.write("""
    Muchas empresas ofrecen plataformas para recopilar y analizar datos agrícolas,
    lo que puede generar concentración de información y dependencia tecnológica.
    """)

    st.image(
        "https://images.unsplash.com/photo-1509395176047-4a66953fd231",
        caption="Tecnología digital aplicada a la agricultura",
        use_container_width=True
    )


def transparencia():

    st.header("Transparencia en el Uso de Datos")

    st.write("""
    Los agricultores deben conocer qué datos se recopilan, cómo se utilizan
    y quién tiene acceso a esa información.
    """)

    st.image(
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
        caption="Visualización y análisis de datos",
        use_container_width=True
    )


def consentimiento():

    st.header("Consentimiento Informado")

    st.write("""
    Los agricultores deben aceptar el uso de sus datos de manera libre
    y comprender claramente los riesgos y beneficios del uso de la información.
    """)

    st.image(
        "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c",
        caption="Acuerdos y consentimiento digital",
        use_container_width=True
    )


def gobernanza():

    st.header("Gobernanza de Datos")

    st.write("""
    Existen modelos alternativos como cooperativas de datos,
    data trusts y plataformas colaborativas que permiten a los agricultores
    controlar mejor su información.
    """)

    st.image(
        "https://images.unsplash.com/photo-1523741543316-beb7fc7023d8",
        caption="Trabajo colaborativo en agricultura",
        use_container_width=True
    )


def impacto():

    st.header("Impactos Sociales")

    st.write("""
    El análisis de datos agrícolas puede mejorar la productividad,
    pero también puede generar desigualdades si no todos los agricultores
    tienen acceso a la tecnología.
    """)

    st.image(
        "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
        caption="Producción agrícola sostenible",
        use_container_width=True
    )


def inclusion():

    st.header("Inclusión y Equidad")

    st.write("""
    La digitalización agrícola debe incluir a mujeres, jóvenes y comunidades rurales,
    garantizando acceso a tecnología y capacitación.
    """)

    st.image(
        "https://images.unsplash.com/photo-1592997572594-34be01bc36c7",
        caption="Comunidades rurales y agricultura",
        use_container_width=True
    )


def seguridad():

    st.header("Seguridad de Datos")

    st.write("""
    Para proteger la información agrícola se utilizan técnicas como
    encriptación, anonimización y auditorías de seguridad.
    """)

    st.image(
        "https://images.unsplash.com/photo-1563986768609-322da13575f3",
        caption="Seguridad de datos digitales",
        use_container_width=True
    )


def conclusion():

    st.header("Conclusión")

    st.write("""
    La agricultura digital ofrece grandes beneficios, pero requiere
    regulaciones éticas que protejan la privacidad, promuevan la transparencia
    y garanticen el control de los datos por parte de los agricultores.
    """)

    st.image(
        "https://images.unsplash.com/photo-1464226184884-fa280b87c399",
        caption="Agricultura sostenible con tecnología",
        use_container_width=True
    )


# ----- MENU LATERAL -----

menu = st.sidebar.selectbox(
    "Navegación",
    [
        "Portada",
        "Agricultura Digital",
        "Problemas Éticos",
        "Privacidad",
        "Empresas Tecnológicas",
        "Transparencia",
        "Consentimiento",
        "Gobernanza de Datos",
        "Impactos Sociales",
        "Inclusión",
        "Seguridad",
        "Conclusión"
    ]
)

# ----- CONTROL DE PAGINAS -----

if menu == "Portada":
    portada()

elif menu == "Agricultura Digital":
    agricultura_digital()

elif menu == "Problemas Éticos":
    problema_etico()

elif menu == "Privacidad":
    privacidad()

elif menu == "Empresas Tecnológicas":
    empresas()

elif menu == "Transparencia":
    transparencia()

elif menu == "Consentimiento":
    consentimiento()

elif menu == "Gobernanza de Datos":
    gobernanza()

elif menu == "Impactos Sociales":
    impacto()

elif menu == "Inclusión":
    inclusion()

elif menu == "Seguridad":
    seguridad()

elif menu == "Conclusión":
    conclusion()
