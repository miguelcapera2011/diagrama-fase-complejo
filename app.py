import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="wide"
)

# Estilos CSS
st.markdown("""
<style>

body{
background-color:#f5f7f6;
}

.main-title{
text-align:center;
font-size:50px;
font-weight:bold;
color:#2e7d32;
}

.subtitle{
text-align:center;
font-size:25px;
color:#4e944f;
}

.section-title{
font-size:35px;
color:#1b5e20;
font-weight:bold;
margin-top:20px;
}

.text-box{
font-size:20px;
padding:15px;
background-color:#ffffff;
border-radius:10px;
box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITULO ----------------

st.markdown('<p class="main-title">Ética del Análisis de Datos Agrícolas</p>', unsafe_allow_html=True)

st.markdown('<p class="subtitle">Digitalización, privacidad y gobernanza de datos</p>', unsafe_allow_html=True)

st.image(
"https://images.unsplash.com/photo-1500382017468-9049fed747ef",
use_container_width=True
)

st.markdown("""
### Miguel Ángel Garatejo Capera  
**Universidad del Tolima**
""")

st.divider()

# ---------------- AGRICULTURA DIGITAL ----------------

st.markdown('<p class="section-title">Agricultura Digital</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

- Uso de sensores, drones e inteligencia artificial  
- Análisis de datos para mejorar producción  
- Optimización del uso de recursos  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1598514982841-6e3f8c6b3f4a",
use_container_width=True
)

st.divider()

# ---------------- PROBLEMAS ETICOS ----------------

st.markdown('<p class="section-title">Problemas Éticos</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

- Privacidad de los agricultores  
- Propiedad de los datos  
- Uso por empresas tecnológicas  
- Transparencia  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1555949963-aa79dcee981c",
use_container_width=True
)

st.divider()

# ---------------- PRIVACIDAD ----------------

st.markdown('<p class="section-title">Privacidad de los Agricultores</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

Los sistemas agrícolas recopilan:

- Ubicación de parcelas  
- Producción agrícola  
- Uso de insumos  
- Información personal  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1560493676-04071c5f467b",
use_container_width=True
)

st.divider()

# ---------------- EMPRESAS TECNOLOGICAS ----------------

st.markdown('<p class="section-title">Empresas Tecnológicas</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

- Plataformas digitales recopilan datos  
- Gran concentración de información  
- Riesgo de dependencia tecnológica  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1581091870627-3a5c9f7f6a1b",
use_container_width=True
)

st.divider()

# ---------------- TRANSPARENCIA ----------------

st.markdown('<p class="section-title">Transparencia</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

Los agricultores deben saber:

- Qué datos se recolectan  
- Cómo se usan  
- Quién accede a ellos  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1551288049-bebda4e38f71",
use_container_width=True
)

st.divider()

# ---------------- CONSENTIMIENTO ----------------

st.markdown('<p class="section-title">Consentimiento Informado</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

- Entender el uso de sus datos  
- Autorizar su uso  
- Poder retirar su consentimiento  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1554224155-8d04cb21cd6c",
use_container_width=True
)

st.divider()

# ---------------- GOBERNANZA ----------------

st.markdown('<p class="section-title">Gobernanza de Datos</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

Modelos de gestión:

- Cooperativas de datos  
- Data Trusts  
- Commons digitales  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1521737604893-d14cc237f11d",
use_container_width=True
)

st.divider()

# ---------------- IMPACTOS SOCIALES ----------------

st.markdown('<p class="section-title">Impactos Sociales</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

**Positivos**

- Mayor productividad  
- Mejor uso de recursos  

**Riesgos**

- Exclusión de pequeños agricultores  
- Concentración económica  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
use_container_width=True
)

st.divider()

# ---------------- INCLUSION ----------------

st.markdown('<p class="section-title">Inclusión y Equidad</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

Grupos vulnerables:

- Mujeres rurales  
- Jóvenes  
- Comunidades indígenas  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1464226184884-fa280b87c399",
use_container_width=True
)

st.divider()

# ---------------- SEGURIDAD ----------------

st.markdown('<p class="section-title">Seguridad de Datos</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

- Encriptación  
- Anonimización  
- Auditorías de seguridad  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1563986768494-4dee2763ff3f",
use_container_width=True
)

st.divider()

# ---------------- CONCLUSION ----------------

st.markdown('<p class="section-title">Conclusión</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="text-box">

La ética en datos agrícolas requiere:

- Privacidad  
- Transparencia  
- Inclusión  
- Regulación justa  

</div>
""", unsafe_allow_html=True)

with col2:
    st.image(
"https://images.unsplash.com/photo-1492496913980-501348b61469",
use_container_width=True
)
