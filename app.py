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
"Seguridad de Datos",
"Empresas Tecnológicas",
"Gobernanza",
"Conclusión",
"Referencias"
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
    
    Ibague - Tolima
    
    2026

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

    "https://circulotne.com/wp-content/uploads/2024/11/ia-agricultura.png",

    """
La agricultura digital utiliza tecnologías como sensores,
drones e inteligencia artificial para recopilar datos
sobre cultivos, suelos y clima.

Esto permite optimizar el uso de agua, fertilizantes
y otros recursos agrícolas.
    """,

    "https://imagenes.eleconomista.com.mx/files/webp_768_768/uploads/2025/06/18/6852f9dea9b60.jpeg"
    )


def etica():

    seccion(
    "Problemas Éticos",

    "La digitalización agrícola genera desafíos relacionados con privacidad y propiedad de datos.",

    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN-k1r3BQIRydUtV787uLt9F1OHVey8s9fnw&s",

    """
El análisis de datos agrícolas plantea preguntas éticas importantes.

Por ejemplo, quién es el propietario de los datos
generados por sensores o maquinaria agrícola.

También existe el riesgo de que empresas tecnológicas
acumulen grandes cantidades de información.
    """,

    "https://noticiassalamanca.com/wp-content/uploads/2023/05/La-privacidad-de-los-datos-y-la-importancia-de-la-seguridad-digital.jpg"
    )


def privacidad():

    seccion(
    "Privacidad de los Agricultores",

    "Los sistemas agrícolas recopilan información sensible como ubicación de parcelas y rendimiento.",

    "https://eos.com/wp-content/uploads/2022/12/data-manager-gis-agriculture.jpg.webp",

    """
Los datos agrícolas pueden revelar información estratégica
sobre producción y uso de insumos.

Si estos datos no se protegen adecuadamente,
pueden generar riesgos de privacidad
o pérdidas económicas para los agricultores.
    """,

    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOgdtxUN4b_-y6DhTnqiyimqqLePWIIeb-ng&s"
    )

def seguridad():

    seccion(
    "Seguridad de Datos",

    "Protección técnica de datos: Encriptación, Anonimización, Auditorías de seguridad",

    "https://www.timware.com.mx/wp-content/uploads/2023/02/cifrado-anonimizacion-tokenizacion-TIMWare.jpg",

    """
    Existen tecnologías para proteger la información agrícola, como la encriptación y la anonimización.
    Estas medidas ayudan a garantizar la seguridad y privacidad de los datos.
    """,

    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPrAty6MQRuvNQTvjhnzF2npf_S2ad-maSGA&s"
    )



def empresas():

    seccion(
    "Empresas Tecnológicas",

    "Las plataformas digitales pueden concentrar grandes volúmenes de datos agrícolas.",

    "https://farmonaut.com/wp-content/uploads/2024/10/Revoluciona-tu-Productividad-Agricola-Monitoreo-de-Cultivos-por-Satelite-y-Analisis-de-Datos-para-una-Agricultura-de-Precision_2.jpg",

    """
Muchas empresas tecnológicas han transformado
la maquinaria agrícola en sistemas conectados.

Esto permite recopilar datos de miles de productores,
pero también genera riesgos de concentración de poder.
    """,

    "https://clickpetroleoegas.com.br/wp-content/uploads/2025/07/Lider-em-acucar-e-etanol-no-Brasil-usa-5G-e-IA-para-conectar-3.000-maquinas-e-aumentar-produtividade-em-15-no-campo.jpg"
    )


def gobernanza():

    seccion(
    "Gobernanza de Datos",

    "Modelos como cooperativas de datos permiten mayor control para los agricultores.",

    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSp5J8dTVlKib6qHq1zAyStseI6cnPwXVa5_g&s",

    """
Las cooperativas de datos permiten que los agricultores
gestionen colectivamente su información.

También existen modelos como los data trusts,
donde los datos son administrados bajo principios éticos.
    """,

    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcST3Pnah1CE-ockFi_wQqDeMXHRpgDt5niPGA&s"
    )


def conclusion():

    seccion(
    "Conclusión",

    "La ética en datos agrícolas busca una digitalización justa y sostenible.",

    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQz6Q-t6n3-eX9_aXGvjnUfiUPwugFUqLR5uA&s",

    """
La digitalización agrícola ofrece grandes beneficios,
pero también requiere regulaciones claras.

La privacidad, la transparencia y la equidad
son fundamentales para un desarrollo agrícola sostenible.
    """,

    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyQYenm5dMNy6YWLPhHurLEEXUlvp6EKn2qw&s"
    )


# ------------------ REFERENCIAS ------------------

def referencias():

    st.markdown('<div class="slide-title">Referencias</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="slide-text">

1. Wolfert, S., Ge, L., Verdouw, C., & Bogaardt, M. (2017).  
Big Data in Smart Farming: A Review. Agricultural Systems.  
https://doi.org/10.1016/j.agsy.2017.01.023  

2. Carbonell, I. (2016).  
The Ethics of Big Data in Agriculture. Internet Policy Review.  

3. FAO (Food and Agriculture Organization).  
Digital Agriculture and Data Governance.  
https://www.fao.org  

4. OECD (2019).  
Enhancing Access to and Sharing of Data.  
https://www.oecd.org  

5. European Commission (2020).  
A European Strategy for Data.  
https://commission.europa.eu  

</div>
""", unsafe_allow_html=True)


# ------------------ NAVEGACION ------------------

if menu == "Portada":
    portada()

elif menu == "Agricultura Digital":
    agricultura()

elif menu == "Problemas Éticos":
    etica()

elif menu == "Privacidad":
    privacidad()

elif menu == "Seguridad de Datos":
    seguridad()

elif menu == "Empresas Tecnológicas":
    empresas()

elif menu == "Gobernanza":
    gobernanza()

elif menu == "Conclusión":
    conclusion()

elif menu == "Referencias":
    referencias()
