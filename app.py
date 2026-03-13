import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Ética del Análisis de Datos Agrícolas",
    page_icon="🌱",
    layout="wide"
)

# Estilo visual
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#2E7D32;
}

.section-title{
    font-size:35px;
    color:#1B5E20;
    font-weight:bold;
}

.text-box{
    font-size:20px;
    padding:10px;
}
</style>
""", unsafe_allow_html=True)


# ----- DIAPOSITIVA 1 -----

st.markdown('<p class="main-title">Ética del Análisis de Datos Agrícolas</p>', unsafe_allow_html=True)

st.image(
"https://images.unsplash.com/photo-1500382017468-9049fed747ef",
use_container_width=True
)

st.markdown("""
### Digitalización, privacidad y gobernanza de datos

**Miguel Ángel Garatejo Capera**  
Universidad del Tolima
""")

st.divider()

# ----- DIAPOSITIVA 2 -----

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
    "https://images.unsplash.com/photo-1598514982841-6e3f8c6b3f4a"
    )

st.divider()

# ----- DIAPOSITIVA 3 -----

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
    "https://images.unsplash.com/photo-1555949963-aa79dcee981c"
    )

st.divider()

# ----- DIAPOSITIVA 4 -----

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
    "https://images.unsplash.com/photo-1560493676-04071c5f467b"
    )

st.divider()

# ----- DIAPOSITIVA 5 -----

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
    "https://images.unsplash.com/photo-1581091870627-3a5c9f7f6a1b"
    )

st.divider()

# ----- DIAPOSITIVA 6 -----

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
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
    )

st.divider()

# ----- DIAPOSITIVA 7 -----

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
    "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c"
    )

st.divider()

# ----- DIAPOSITIVA 8 -----

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
    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"
    )

st.divider()

# ----- DIAPOSITIVA 9 -----

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
    "https://images.unsplash.com/photo-1501004318641-b39e6451bec6"
    )

st.divider()

# ----- DIAPOSITIVA 10 -----

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
    "https://images.unsplash.com/photo-1464226184884-fa280b87c399"
    )

st.divider()

# ----- DIAPOSITIVA 11 -----

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
    "https://images.unsplash.com/photo-1563986768494-4dee2763ff3f"
    )

st.divider()

# ----- DIAPOSITIVA 12 -----

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
    "https://images.unsplash.com/photo-1492496913980-501348b61469"
    )
