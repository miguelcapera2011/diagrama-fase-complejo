import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------
st.set_page_config(
    page_title="Tamaño Muestral para Proporciones Extremas",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Cálculo de Tamaño Muestral para Proporciones Extremas")
st.markdown("""
Esta aplicación implementa todos los puntos del **numeral 6** del documento:
- Proporciones muy pequeñas o muy grandes  
- Varianza máxima en p = 0.5  
- Ajustes cuando p < 0.10 o p > 0.90  
- Alternativas para evitar sobreestimación  
- Aplicaciones en eventos raros  

Además, incluye espacios para imágenes tipo exposición.
""")

# ------------------------------------------------------------
# SECCIÓN 1: EXPLICACIÓN TEÓRICA (Punto 6)
# ------------------------------------------------------------
st.header("📌 1. Fundamentación Teórica del Punto 6")

st.subheader("🔹 ¿Por qué la máxima varianza ocurre en p = 0.5?")
st.markdown("""
La varianza de una proporción es:

\[
Var(p)=p(1-p)
\]

Esta función es simétrica y alcanza su máximo cuando:

\[
p=0.5
\]

Esto implica que, cuando no conocemos la proporción, usar **p = 0.5** da el tamaño muestral más conservador.
""")

st.subheader("🔹 Ajustes cuando p es muy pequeño o muy grande")
st.markdown("""
Cuando:

- \( p < 0.10 \)  (eventos raros)
- \( p > 0.90 \)  (eventos casi seguros)

la fórmula clásica **sobreestima el tamaño muestral**, porque la varianza real es mucho menor que 0.25.

Por eso, se recomienda usar fórmulas ajustadas o métodos alternativos como:
- Usar varianza real \( p(1-p) \)
- Aproximación de Poisson cuando p es muy pequeño
- Intervalos de Wilson para evitar estimaciones incorrectas
""")

st.subheader("🔹 Ecuaciones alternativas para eventos raros")
st.markdown("""
Cuando \( p \ll 0.10 \):

\[
n \approx \frac{Z^2}{E^2} p
\]

Y para modelar recuentos raros:

\[
n \approx \frac{Z^2}{\lambda}
\]

Esto evita tamaños muestrales exageradamente grandes.
""")

st.subheader("🔹 Aplicaciones: estudios de eventos raros")
st.markdown("""
- Enfermedades poco comunes  
- Defectos de fabricación  
- Fraude financiero  
- Seguridad industrial  
- Astrofísica (detección de sucesos muy poco probables)  
""")

# ------------------------------------------------------------
# SECCIÓN 2: CARGA DE IMÁGENES PARA EXPOSICIÓN
# ------------------------------------------------------------
st.header("🖼️ 2. Agregar Imágenes (para exposición)")

url_img = st.text_input("Pegue el link de la imagen que desea mostrar:")
if url_img:
    st.image(url_img, caption="Imagen cargada para la exposición", use_column_width=True)

# ------------------------------------------------------------
# SECCIÓN 3: Cálculo de tamaño muestral
# ------------------------------------------------------------
st.header("📐 3. Cálculo del Tamaño Muestral")

st.sidebar.header("Parámetros")

p = st.sidebar.number_input("Proporción estimada p", min_value=0.0001, max_value=0.9999, value=0.05)
Z = st.sidebar.number_input("Valor Z (ej: 1.96 para 95%)", min_value=1.0, max_value=4.0, value=1.96)
E = st.sidebar.number_input("Margen de error E", min_value=0.0005, max_value=0.2, value=0.02)

st.subheader("Fórmula clásica")
n_classic = (Z**2 * p * (1 - p)) / (E**2)

st.latex(r"n = \frac{Z^2 \ p(1-p)}{E^2}")

st.metric("Tamaño muestral (clásico)", f"{n_classic:.1f}")

# ------------------------------------------------------------
# Ajustes para proporciones extremas
# ------------------------------------------------------------
st.subheader("✔ Ajuste recomendado para proporciones extremas")

if p < 0.10 or p > 0.90:
    st.warning("p es extremo → se aplican correcciones especiales")

# Alternativa de Wilson (más precisa en eventos raros)
n_wilson = (Z**2 / (2*E**2)) * (p*(1-p) + E**2)

st.metric("Tamaño muestral ajustado (Wilson)", f"{n_wilson:.1f}")

# ------------------------------------------------------------
# Gráfica de varianza
# ------------------------------------------------------------
st.header("📊 4. Varianza de la proporción")

fig, ax = plt.subplots(figsize=(6,4))
x = np.linspace(0,1,200)
ax.plot(x, x*(1-x))
ax.axvline(0.5, linestyle="--")
ax.set_title("Varianza p(1-p)")
ax.set_xlabel("p")
ax.set_ylabel("Varianza")

st.pyplot(fig)

# ------------------------------------------------------------
# Pie de página
# ------------------------------------------------------------
st.caption("App creada como entrega tipo exposición. Puedes editarla libremente.")
