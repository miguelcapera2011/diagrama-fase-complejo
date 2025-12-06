# ============================================================
# APP STREAMLIT – Punto 6: Cálculo de tamaño muestral en proporciones
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
st.set_page_config(
    page_title="Tamaño Muestral para Proporciones",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Punto 6: Cálculo de tamaño muestral para proporciones")
st.markdown("---")


# ============================================================
# SECCIÓN 1 — Varianza máxima en p = 0.5
# ============================================================
with st.container():
    st.header("1️⃣ ¿Por qué la máxima varianza ocurre en \( p = 0.5 \)?")

    st.markdown("""
    La varianza de una proporción está dada por:

    \[
    \text{Var}(p) = p(1-p)
    \]

    Esta expresión es máxima cuando:

    \[
    p = 0.5
    \]

    Esto sucede porque es el punto donde hay **mayor incertidumbre**:  
    no sabemos si el evento ocurre o no con la misma probabilidad.

    Cuando \( p \) es cercano a 0 o 1, la varianza es menor porque el evento es:
    - casi imposible, o
    - casi seguro.

    Por eso, cuando no se conoce la proporción, se usa por defecto \( p = 0.5 \).
    """)

    # Gráfica de la varianza
    p_vals = np.linspace(0, 1, 200)
    var_vals = p_vals * (1 - p_vals)

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(p_vals, var_vals)
    ax.set_xlabel("p")
    ax.set_ylabel("Var(p)")
    ax.set_title("Varianza de una proporción: p(1-p)")
    st.pyplot(fig)

st.markdown("---")


# ============================================================
# SECCIÓN 2 — Ajustes cuando p es muy pequeña o muy grande
# ============================================================
with st.container():
    st.header("2️⃣ Ajustes cuando \( p < 0.10 \) o \( p > 0.90 \)")

    st.markdown("""
    Cuando la proporción es muy baja o muy alta, la fórmula clásica del tamaño muestral:

    \[
    n = \frac{Z^2\,p(1-p)}{E^2}
    \]

    puede dar resultados incorrectos porque la aproximación normal falla.

    Para que la aproximación normal sea válida, debe cumplirse:

    \[
    np \ge 5 \quad\text{y}\quad n(1-p) \ge 5
    \]

    Cuando esto no se cumple, se aplican ajustes:

    ### ✔ Ajuste 1: Proporciones pequeñas
    Si \( p < 0.10 \):

    \[
    n = \frac{Z^2\,p}{E^2}
    \]

    porque \( 1 - p \approx 1 \).

    ### ✔ Ajuste 2: Uso de fórmulas alternativas
    Cuando el evento es muy raro (<5 %), la aproximación binomial no funciona bien.
    Por eso se usa la aproximación de Poisson o de Wilson.
    """)

st.markdown("---")


# ============================================================
# SECCIÓN 3 — Ecuaciones alternativas
# ============================================================
with st.container():
    st.header("3️⃣ Ecuaciones alternativas para evitar sobreestimación del tamaño muestral")

    st.markdown("""
    Cuando los eventos son extremadamente raros, usar \( p = 0.5 \) produce tamaños muestrales
    ridículamente grandes. Para evitar eso se recomiendan estas alternativas:

    ### ✔ Fórmula de Wilson
    \[
    n = \frac{Z^2}{4E^2}
    \]

    Esta fórmula es estable incluso cuando \( p \) es muy pequeña.

    ### ✔ Proporciones muy raras (modelo binomial ajustado)
    \[
    n = \frac{Z^2(1 - p)}{E^2\,p}
    \]

    Funciona bien cuando el evento ocurre en menos del 5% de los casos.

    ### ✔ Aproximación de Poisson (eventos muy raros)
    \[
    n = \frac{Z^2}{E^2\,\lambda}
    \]

    donde \( \lambda = p \) cuando el evento es muy raro.
    """)

st.markdown("---")


# ============================================================
# SECCIÓN 4 — Aplicaciones: eventos raros
# ============================================================
with st.container():
    st.header("4️⃣ Aplicaciones: estudios de eventos raros")

    st.subheader("🧪 Ejemplo 1: Reacciones adversas raras a un medicamento")
    st.markdown("""
    En estudios clínicos es importante detectar efectos secundarios graves,
    incluso si ocurren con muy poca frecuencia (por ejemplo, 1 en 10.000 personas).

    Aquí \( p \) es extremadamente pequeño:

    \[
    p \approx 0.0001
    \]

    Para estimar esta proporción con un error razonable, la fórmula clásica da:

    \[
    n \approx \frac{Z^2 p (1 - p)}{E^2} \approx \frac{Z^2 p}{E^2}
    \]

    Pero debido a que \( p \) es tan pequeño, se recomienda el **modelo de Poisson**:

    \[
    n = \frac{Z^2}{E^2 p}
    \]

    Esto evita subestimar o sobreestimar el tamaño muestral.
    """)

    st.subheader("🚑 Ejemplo 2: Accidentes graves en una población")
    st.markdown("""
    Supongamos que una ciudad quiere medir la tasa de accidentes graves
    en motocicletas, que ocurre aproximadamente en:

    \[
    p = 0.002
    \]

    Como el evento es muy raro, usar la fórmula clásica da valores poco fiables.
    Nuevamente, la aproximación de Poisson es más adecuada:

    \[
    n = \frac{Z^2}{E^2 p}
    \]

    Esto permite estimar correctamente la proporción de accidentes sin usar muestras imposibles de obtener.
    """)

st.markdown("---")

st.success("📘 Dashboard completo. Puedes subirlo directamente a Streamlit Cloud o GitHub Pages.")
