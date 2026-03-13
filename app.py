import streamlit as st

st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="wide"
)

# ---------------- ESTILO ----------------

st.markdown("""
<style>

body{
background-color:#f5f7f6;
}

.title{
text-align:center;
font-size:48px;
font-weight:bold;
color:#2e7d32;
}

.subtitle{
text-align:center;
font-size:22px;
}

.section{
font-size:36px;
font-weight:bold;
color:#1b5e20;
}

.text{
font-size:20px;
}

.footer{
text-align:center;
color:gray;
}

</style>
""", unsafe_allow_html=True)

# ---------------- DIAPOSITIVAS ----------------

slides = [

{
"title":"Ética del Análisis de Datos Agrícolas",
"text":[
"Digitalización, privacidad y gobernanza de datos",
"Miguel Ángel Garatejo Capera",
"Universidad del Tolima"
],
"image":"https://images.unsplash.com/photo-1500382017468-9049fed747ef"
},

{
"title":"Agricultura Digital",
"text":[
"Uso de sensores, drones e inteligencia artificial",
"Análisis de datos para mejorar producción",
"Optimización del uso de recursos"
],
"image":"https://images.unsplash.com/photo-1598514982841-6e3f8c6b3f4a"
},

{
"title":"Problemas Éticos",
"text":[
"Privacidad de los agricultores",
"Propiedad de los datos",
"Uso por empresas tecnológicas",
"Necesidad de transparencia"
],
"image":"https://images.unsplash.com/photo-1555949963-aa79dcee981c"
},

{
"title":"Privacidad de los Agricultores",
"text":[
"Ubicación de parcelas mediante GPS",
"Producción agrícola",
"Uso de fertilizantes y recursos",
"Datos personales del agricultor"
],
"image":"https://images.unsplash.com/photo-1560493676-04071c5f467b"
},

{
"title":"Empresas Tecnológicas",
"text":[
"Plataformas digitales recolectan datos",
"Grandes empresas concentran información",
"Riesgo de dependencia tecnológica"
],
"image":"https://images.unsplash.com/photo-1581091870627-3a5c9f7f6a1b"
},

{
"title":"Transparencia en el Uso de Datos",
"text":[
"Qué datos se recolectan",
"Cómo se procesan",
"Quién accede a ellos",
"Para qué se utilizan"
],
"image":"https://images.unsplash.com/photo-1551288049-bebda4e38f71"
},

{
"title":"Consentimiento Informado",
"text":[
"Los agricultores deben comprender el uso de sus datos",
"Autorización clara y voluntaria",
"Derecho a retirar el consentimiento"
],
"image":"https://images.unsplash.com/photo-1554224155-8d04cb21cd6c"
},

{
"title":"Gobernanza de Datos",
"text":[
"Cooperativas de datos agrícolas",
"Data Trusts",
"Plataformas colaborativas"
],
"image":"https://images.unsplash.com/photo-1521737604893-d14cc237f11d"
},

{
"title":"Impactos Sociales",
"text":[
"Mayor productividad agrícola",
"Uso eficiente de recursos",
"Riesgo de exclusión de pequeños agricultores",
"Concentración económica"
],
"image":"https://images.unsplash.com/photo-1501004318641-b39e6451bec6"
},

{
"title":"Inclusión y Equidad",
"text":[
"Inclusión de mujeres rurales",
"Participación de jóvenes",
"Respeto a comunidades indígenas"
],
"image":"https://images.unsplash.com/photo-1464226184884-fa280b87c399"
},

{
"title":"Seguridad de Datos",
"text":[
"Encriptación de información",
"Anonimización de datos",
"Auditorías de seguridad"
],
"image":"https://images.unsplash.com/photo-1563986768494-4dee2763ff3f"
},

{
"title":"Conclusión",
"text":[
"Privacidad y protección de datos",
"Transparencia en el uso de información",
"Inclusión en la digitalización agrícola",
"Regulación ética del uso de datos"
],
"image":"https://images.unsplash.com/photo-1492496913980-501348b61469"
}

]

# ---------------- CONTROL DE DIAPOSITIVA ----------------

if "slide" not in st.session_state:
    st.session_state.slide = 0

slide = slides[st.session_state.slide]

# ---------------- CONTENIDO ----------------

st.markdown(f'<p class="title">{slide["title"]}</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:

    for t in slide["text"]:
        st.markdown(f'<p class="text">• {t}</p>', unsafe_allow_html=True)

with col2:
    st.image(slide["image"], use_container_width=True)

# ---------------- BOTONES ----------------

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ Anterior"):
        if st.session_state.slide > 0:
            st.session_state.slide -= 1

with col3:
    if st.button("Siguiente ➡️"):
        if st.session_state.slide < len(slides)-1:
            st.session_state.slide += 1

st.markdown(f'<p class="footer">Diapositiva {st.session_state.slide + 1} de {len(slides)}</p>', unsafe_allow_html=True)
