# ============================================================
# APP STREAMLIT PROFESIONAL – Punto 6: Proporciones extremas
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# CONFIGURACIÓN GENERAL
st.set_page_config(
    page_title="Tamaño muestral: Proporciones extremas",
    layout="wide"
)

st.title(" Tamaño muestral para proporciones extremas (Punto 6)")

# ============================================================
# MENÚ LATERAL
# ============================================================

menu = st.sidebar.radio(
    "INDICE",
    [
        "6.1 Varianza máxima (p = 0.5)",
        "6.2 Ajustes cuando p es extrema",
        "6.3 Alternativa Poisson",
        "6.4 Aplicaciones reales"
    ]
)

# ============================================================
# 6.1 VARIANZA MÁXIMA
# ============================================================

if menu == "6.1 Varianza máxima (p = 0.5)":
    st.header("6.1 ¿Por qué la máxima varianza ocurre en p = 0.5?")
    
    st.markdown(r"""
    La varianza de una proporción muestral es:

    \[
    \text{Var}(\hat p) = \frac{p(1-p)}{n}
    \]

    Como \(n\) es constante al planear la muestra, basta estudiar:

    \[
    f(p) = p(1-p)
    \]

    Esta función es una **parábola invertida**, y su máximo ocurre cuando:

    \[
    p = 0.5
    \]

    Esto significa que la incertidumbre es máxima cuando la mitad son éxitos y la mitad fracasos.
    Por eso, **si no se conoce p**, se utiliza **p = 0.5** para obtener el tamaño muestral más conservador.
    """)

    # Interacción gráfica
    st.subheader("📈 Interacción: gráfica de la varianza p(1−p)")
    p_point = st.slider("Seleccione un valor de p", 0.0, 1.0, 0.5, step=0.01)

    p_vals = np.linspace(0, 1, 300)
    var_vals = p_vals * (1 - p_vals)

    fig, ax = plt.subplots()
    ax.plot(p_vals, var_vals)
    ax.scatter([p_point], [p_point*(1-p_point)], s=100)
    ax.axvline(0.5, color="red", linestyle="--")
    ax.set_title("Varianza de la proporción")
    ax.set_xlabel("p")
    ax.set_ylabel("p(1−p)")
    st.pyplot(fig)

    st.success(f"Para p = {p_point}, la varianza es {round(p_point*(1-p_point),4)}")


# ============================================================
# 6.2 AJUSTES CUANDO p ES EXTREMA
# ============================================================

elif menu == "6.2 Ajustes cuando p es extrema":
    st.header("6.2 Ajustes cuando \(p\) es extrema")

    st.markdown(r"""
    La fórmula clásica del tamaño muestral para estimar una proporción es:

    \[
    n = \frac{z^2\; p(1-p)}{d^2}
    \]

    Cuando la proporción verdadera es muy pequeña:

    \[
    p < 0.05
    \]

    o muy grande:

    \[
    p > 0.95
    \]

    el término \(p(1-p)\) se vuelve demasiado pequeño, lo que hace que \(n\) salga exageradamente grande.

    Para evitarlo se usa el **ajuste de proporciones extremas**:

    \[
    p_{\text{ajustado}} =
    \begin{cases}
    0.05, & p < 0.05 \\
    0.95, & p > 0.95 \\
    p, & \text{en otro caso}
    \end{cases}
    \]
    """)

    st.subheader("🔧 Cálculo interactivo")

    col1, col2, col3 = st.columns(3)
    with col1:
        p = st.number_input("Proporción esperada p", 0.0001, 0.9999, 0.02)
    with col2:
        z = st.number_input("Valor z", value=1.96)
    with col3:
        d = st.number_input("Margen de error d", value=0.01)

    n_clasico = z**2 * p * (1 - p) / d**2
    p_adj = max(min(p, 0.95), 0.05)
    n_ajustado = z**2 * p_adj * (1 - p_adj) / d**2

    st.info(f"📘 Tamaño muestral clásico: **{round(n_clasico,2)}**")
    st.success(f" Tamaño muestral ajustado: **{round(n_ajustado,2)}**")
    st.write(f"Valor de p usado después del ajuste: **{p_adj}**")

    if p < 0.05 or p > 0.95:
        st.warning("Se aplicó el ajuste porque p es extrema.")


# ============================================================
# 6.3 MODELO POISSON
# ============================================================

elif menu == "6.3 Alternativa Poisson":
    st.header("6.3 Alternativa Poisson para eventos rarísimos")

    st.markdown(r"""
    Para proporciones muy pequeñas (\(p < 0.05\)), la distribución binomial se aproxima a Poisson.

    En Poisson:

    \[
    \lambda \approx p
    \]

    La fórmula del tamaño muestral queda:

    \[
    n = \frac{z^2 \lambda}{d^2}
    \]

    Esta fórmula **evita tamaños muestrales gigantes** provocados por el término \(p(1-p)\) cuando \(p\) es demasiado pequeña.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        lam = st.number_input("λ (≈ p si evento es raro)", 0.000001, 1.0, 0.01)
    with col2:
        z2 = st.number_input("Valor z", value=1.96)
    with col3:
        d2 = st.number_input("Margen de error d", value=0.005)

    n_poisson = z2**2 * lam / d2**2

    st.success(f"Tamaño muestral usando Poisson: **{round(n_poisson,2)}**")


# ============================================================
# 6.4 APLICACIONES REALES
# ============================================================

elif menu == "6.4 Aplicaciones reales":
    st.header("6.4 Aplicaciones reales: eventos rarísimos")

    st.write("""
    Aquí verás **dos casos reales** donde las proporciones son tan pequeñas  
    que se usan directamente los métodos de los incisos 6.1 — 6.3.
    """)

    ejemplo = st.selectbox(
        "Seleccione un caso real",
        ["Anafilaxia por vacunas", "Falla catastrófica de turbinas"]
    )

    # --------------------------- Ejemplo 1
    if ejemplo == "Anafilaxia por vacunas":
        st.subheader("Ejemplo 1 — Anafilaxia por vacunas (evento rarísimo)")

        st.markdown(r"""
        La anafilaxia tiene una frecuencia de:

        \[
        1 \text{ a } 5 \text{ casos por millón}
        \]

        Es decir:

        \[
        p \approx 10^{-6}
        \]

        Para estos valores, la binomial es inutilizable → se usa **Poisson**.
        """)

        lam2 = st.number_input("λ (casos por millón → dividir entre 1e6)", 
                               0.000001, 0.001, 0.000003)

        n_calc = (1.96**2) * lam2 / (0.0005**2)

        st.success(f"Tamaño muestral estimado: **{round(n_calc,2)} personas**")

    # --------------------------- Ejemplo 2
    else:
        st.subheader("Ejemplo 2 — Falla catastrófica en turbinas de avión")

        st.markdown(r"""
        Frecuencia real:

        \[
        p = \frac{1}{10\,000\,000} = 10^{-7}
        \]

        La varianza es tan extrema que solo Poisson permite estimaciones estables.
        """)

        lam3 = st.number_input("λ por hora de vuelo (≈ p)", 
                               0.00000001, 0.00001, 0.0000001)

        n_calc2 = (1.96**2) * lam3 / (0.0001**2)

        st.success(f"Tamaño muestral estimado: **{round(n_calc2,2)} horas de vuelo**")

st.divider()
