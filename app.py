import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA (Dashboard limpio)
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Muestreo Estadístico",
    layout="wide"
)

st.title(" Muestreo Estadístico")
st.markdown("Este dashboard incluye **dos módulos**: tamaño muestral para proporciones y eventos raros.")


# ---------------------------------------------------------------
# FUNCIONES
# ---------------------------------------------------------------

def tamaño_muestral_proporciones(Z, p, d):
    """n = Z² * p(1-p) / d²"""
    return (Z**2) * p * (1 - p) / (d**2)


def tamaño_muestral_eventos_raros(Z, p, d):
    """Ajuste más fuerte cuando p es muy pequeño"""
    p = max(p, 0.000001)
    return (Z**2) * p * (1 - p) / (d**2)


def grafica_varianza():
    p_vals = np.linspace(0, 1, 300)
    var = p_vals * (1 - p_vals)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(p_vals, var, linewidth=2)
    ax.set_xlabel("p")
    ax.set_ylabel("Varianza = p(1-p)")
    ax.set_title("Curva de la varianza de una proporción")
    ax.grid(True)
    return fig


def grafica_muestra_eventos(p_vals, Z, d):
    n_vals = [(Z**2) * p * (1 - p) / (d**2) for p in p_vals]

    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(p_vals, n_vals, linewidth=2)
    ax.set_xlabel("Proporción estimada p")
    ax.set_ylabel("Tamaño muestral requerido")
    ax.set_title("Tamaño muestral vs proporción (eventos raros)")
    ax.grid(True)
    return fig


# ---------------------------------------------------------------
# TABS DE DASHBOARD
# ---------------------------------------------------------------
tab1, tab2 = st.tabs([" Tamaño Muestral", "🧪 Eventos Raros"])


# ---------------------------------------------------------------
# MÓDULO 1: TAMAÑO MUESTRAL
# ---------------------------------------------------------------
with tab1:
    st.header(" Cálculo del tamaño muestral para proporciones")

    col1, col2 = st.columns(2)

    with col1:
        Z = st.selectbox(
            "Nivel de confianza (Z)", 
            [1.64, 1.96, 2.58], 
            index=1, 
            key="Z1"
        )

        p = st.slider("Proporción esperada p", 0.01, 0.99, 0.5, 0.01)
        d = st.number_input("Margen de error d", min_value=0.001, max_value=0.2, value=0.05)

    with col2:
        n = tamaño_muestral_proporciones(Z, p, d)
        st.metric("Tamaño muestral requerido", f"{int(np.ceil(n))}")

        st.markdown("### Curva de varianza p(1-p)")
        st.pyplot(grafica_varianza())

    with st.expander("¿Por qué la varianza es máxima en p = 0.5?"):
        st.write("""
La varianza de una proporción es:

\[
Var(p) = p(1 - p)
\]

Es una parábola simétrica que alcanza su máximo cuando:

\[
\frac{d}{dp}p(1-p) = 0 \Rightarrow p = 0.5
\]

Esto significa que **la incertidumbre es máxima cuando hay la misma probabilidad de éxito y fracaso**.
        """)


# ---------------------------------------------------------------
# MÓDULO 2: EVENTOS RAROS

with tab2:
    st.header("Estudio de eventos raros")

    st.write("Usamos una base interna simulada con eventos de baja frecuencia.")

    # Base interna
    data = pd.DataFrame({
        "evento": ["sí"] * 3 + ["no"] * 197
    })

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Base interna")
        st.dataframe(data.head())

        total = len(data)
        eventos = sum(data["evento"] == "sí")
        p_hat = eventos / total

        st.metric("Proporción observada p̂", f"{p_hat:.4f}")

        Z2 = st.selectbox(
            "Nivel de confianza (Z)", 
            [1.64, 1.96, 2.58], 
            index=1, 
            key="Z2"
        )

        d2 = st.number_input("Margen de error d", min_value=0.0001, max_value=0.2, value=0.01)

    with col2:
        n2 = tamaño_muestral_eventos_raros(Z2, p_hat, d2)
        st.metric("Tamaño muestral recomendado", f"{int(np.ceil(n2))}")

        st.markdown("### Relación entre p y n")
        p_vals_small = np.linspace(0.0001, 0.05, 100)
        st.pyplot(grafica_muestra_eventos(p_vals_small, Z2, d2))

    with st.expander("Explicación"):
        st.write("""
Cuando **p es muy pequeño**, la varianza se aplana pero el error relativo aumenta, por eso:

\[
n = \frac{Z^2 p(1-p)}{d^2}
\]

puede generar tamaños muestrales muy grandes.  
Aquí se aplica un **ajuste para evitar subestimar el tamaño** cuando los eventos son raros.
        """)
