import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración básica de la página
st.set_page_config(
    page_title="Tamaño Muestral para Proporciones Extremas - Sección 6",
    layout="wide"
)

# -----------------------------
# SECCIÓN 6: Tamaño muestral para proporciones muy pequeñas o muy grandes
# -----------------------------

st.header("6️⃣ Cálculo de Tamaño Muestral para Proporciones Muy Pequeñas o Muy Grandes")

st.write("""
El cálculo del tamaño de muestra para proporciones se vuelve **especialmente delicado** 
cuando la proporción real del fenómeno es muy **pequeña (p < 0.10)** o muy **grande (p > 0.90)**.
Esto ocurre, por ejemplo, en estudios epidemiológicos de enfermedades raras o en procesos industriales
con tasas de error extremadamente bajas.
""")

# ----------- BOTÓN TEORÍA COMPLETA  ---------------------
with st.expander("📘 Mostrar teoría completa del punto 6"):
    st.markdown("""
    # 🧠 **Fundamentos Teóricos del Punto 6**

    ## 🔹 1. ¿Por qué la máxima varianza ocurre en p = 0.5?

    La varianza de una proporción está dada por:

    \[
    Var(\hat p) = p(1-p)
    \]

    Esta función es una parábola invertida cuyo máximo ocurre cuando:

    \[
    \frac{d}{dp}[\,p(1-p)\,] = 0 \quad \Rightarrow \quad p = 0.5
    \]

    En ese punto:

    \[
    Var_{\max} = 0.25
    \]

    ✔ Esto significa que **la incertidumbre máxima ocurre cuando la proporción está en 50%**.  
    ✔ Cuando p se acerca a 0 o 1, **la varianza cae drásticamente**, volviendo ineficiente el uso de aproximaciones normales.

    ---

    ## 🔹 2. Problema cuando p < 0.10 o p > 0.90

    La fórmula clásica del tamaño muestral:

    \[
    n = \frac{Z^2\, p(1-p)}{E^2}
    \]

    **funciona solo cuando** la distribución muestral de \(\hat p\) es aproximadamente normal.

    Pero cuando p es muy pequeña o grande:

    - La distribución es **muy asimétrica**
    - La normal **sobrestima** la variabilidad
    - El tamaño muestral puede inflarse sin necesidad
    - Los intervalos de confianza dejan de ser simétricos

    ⚠️ Por eso se requieren *correcciones especiales*.

    ---

    ## 🔹 3. Ajustes a la fórmula clásica

    ### ✔ Caso p pequeña:
    \[
    p < 0.10 \quad \Rightarrow \quad \text{usar aproximación Poisson}
    \]

    En eventos raros:

    \[
    n = \frac{\ln(1-C)}{\ln(1-p)}
    \]

    ### ✔ Caso p grande:
    Como \( p \to 1 \), basta trabajar con:

    \[
    q = 1-p
    \]

    y tratar el modelo igual que eventos raros.

    ---

    ## 🔹 4. Ecuaciones alternativas para evitar sobreestimación

    - Intervalo de Wilson
    - Intervalo de Agresti–Coull
    - Modelos basados en Poisson

    Estos métodos producen estimaciones **realistas** y evitan tamaños muestrales inflados.

    ---

    ## 🔹 5. Aplicaciones reales (eventos raros)

    - Enfermedades con prevalencia < 1%
    - Defectos industriales menores al 0.5%
    - Accidentes muy poco frecuentes
    - Mutaciones genéticas raras

    """)

# ===============================================================
# GRÁFICA: VARIANZA (TEXTO IZQ – GRÁFICA DER)
# ===============================================================

col6a, col6b = st.columns([1.3, 1])

with col6a:
    st.subheader("📈 Varianza de una proporción")
    st.write("""
    La varianza disminuye cuando p se acerca a 0 o 1.  
    Una varianza pequeña implica que la distribución ya **no es simétrica**, lo cual invalida
    la aproximación normal.
    """)

with col6b:
    ps = np.linspace(0, 1, 200)
    vars_ = ps * (1 - ps)
    fig6_1, ax6_1 = plt.subplots(figsize=(2.2, 1.6))
    ax6_1.plot(ps, vars_, linewidth=2)
    ax6_1.set_title("Varianza p(1-p)")
    ax6_1.grid(True)
    st.pyplot(fig6_1)

# ===============================================================
# GRÁFICA: POISSON PARA EVENTOS RAROS
# ===============================================================
col6c, col6d = st.columns([1.3, 1])

with col6c:
    st.subheader("📉 Tamaño muestral para detectar ≥1 evento raro")
    st.write("""
    Para eventos raros (p < 0.05), la probabilidad de observar al menos un caso en n individuos es:

    \[
    P(X\ge1) = 1-(1-p)^n
    \]

    Despejando n tenemos:

    \[
    n = \frac{\ln(1-C)}{\ln(1-p)}
    \]
    """)

with col6d:
    p_small = st.number_input("Proporción rara p:", 0.00001, 0.05, 0.01, key="p_small_6")
    C_small = st.slider("Confianza C:", 0.50, 0.999, 0.95, key="C_small_6")
    n_required = np.log(1 - C_small) / np.log(1 - p_small)

    ps2 = np.linspace(0.0001, 0.05, 200)
    ns2 = np.log(1 - C_small) / np.log(1 - ps2)

    fig6_2, ax6_2 = plt.subplots(figsize=(2.2, 1.6))
    ax6_2.plot(ps2, ns2)
    ax6_2.set_title("Modelo Poisson")
    ax6_2.grid(True)
    st.pyplot(fig6_2)

st.success(f"📌 Tamaño muestral necesario: **n = {int(np.ceil(n_required))}**")

# ===============================================================
# IMAGEN TEMÁTICA (OPCIONAL)
# ===============================================================

st.markdown("### 🖼 Imagen ilustrativa")

st.info("Puedes colocar una imagen aquí (por ejemplo: distribución Poisson, curva p(1-p), o un esquema conceptual).")

try:
    st.image("imagenes/eventos_raros.png", width=350)
except:
    st.warning("⚠️ No se encontró la imagen: coloca un archivo llamado **eventos_raros.png** en la carpeta /imagenes.")

st.markdown("---")
