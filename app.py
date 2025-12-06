# app.py
# Streamlit dashboard: Punto 6 - Tamaño muestral para proporciones extremas
# Ejecutar: streamlit run app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

st.set_page_config(
    page_title="Tamaño muestral — Proporciones extremas",
    layout="wide",
    page_icon="📈",
)

st.title("📈 Punto 6 — Tamaño muestral para proporciones extremas")
st.markdown(
    "Interfaz interactiva para explorar varianza, fórmulas de tamaño muestral y aplicaciones "
    "en eventos raros. Las fórmulas aparecen en notación matemática."
)
st.markdown("---")

# ------------------------
# Utilidades matemáticas
# ------------------------
def n_classic(p, Z, E):
    """Fórmula clásica n = Z^2 * p(1-p) / E^2"""
    return Z**2 * p * (1 - p) / E**2

def n_wilson_simple(Z, E):
    """Fórmula simplificada Wilson usada antes: n = Z^2 / (4 E^2)"""
    return Z**2 / (4 * E**2)

def n_poisson(p, Z, E):
    """Aproximación útil para eventos raros (poisson-like): n = Z^2 / (E^2 * p)"""
    # Evitar división por cero
    if p <= 0:
        return np.inf
    return Z**2 / (E**2 * p)

def finite_correction(n0, N):
    """Corrección por población finita"""
    if N is None or N <= 0:
        return n0
    return n0 / (1 + (n0 - 1) / N)

def required_normality_check(n, p):
    """Condición aproximada para la validez de aproximación normal"""
    return (n * p >= 5) and (n * (1 - p) >= 5)

# ------------------------
# Sidebar: parámetros globales
# ------------------------
st.sidebar.header("Parámetros globales")
confidence = st.sidebar.selectbox("Nivel de confianza", ["90%", "95%", "99%"])
conf_map = {"90%": 1.645, "95%": 1.96, "99%": 2.575}
Z = conf_map[confidence]
E = st.sidebar.slider("Error absoluto permitido (E)", 0.001, 0.20, 0.05, step=0.001)
N = st.sidebar.number_input("Tamaño de población (N) — 0 = infinito", min_value=0, value=0, step=1)

st.sidebar.markdown("---")
st.sidebar.write("Consejos:")
st.sidebar.write("- Si no conoces p, p=0.5 es conservador (mayor n).")
st.sidebar.write("- Para eventos raros usar aproximación Poisson o métodos exactos.")

# ------------------------
# Section 1: Varianza vs p
# ------------------------
st.header("1. Varianza de la proporción y por qué p = 0.5 es máximo")
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        "La varianza de una proporción muestral (para un solo muestreo) es:"
    )
    st.latex(r"\mathrm{Var}(\hat{p}) \approx \frac{p(1-p)}{n}")
    st.markdown(
        "El término \(p(1-p)\) es máximo cuando \(p = 0.5\). "
        "La curva es simétrica y produce la mayor incertidumbre en \(p=0.5\)."
    )

    p_slider = st.slider("Selecciona p para explorar (proporción esperada)", 0.0, 1.0, 0.1, 0.01)

    # Mostrar ejemplo de varianza y error estándar con n de ejemplo
    n_example = st.number_input("n de ejemplo para mostrar error estándar (ej: 100)", min_value=1, value=100, step=1)
    var_example = p_slider * (1 - p_slider)
    stderr_example = np.sqrt(var_example / n_example)
    st.write(f"Var(p) = p(1-p) = {var_example:.6f}")
    st.write(f"Error estándar (sqrt(var/n)) con n = {n_example}: {stderr_example:.6f}")

with col2:
    p_vals = np.linspace(0, 1, 400)
    var_vals = p_vals * (1 - p_vals)
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.plot(p_vals, var_vals)
    ax1.axvline(0.5, linestyle="--", linewidth=0.7)
    ax1.set_xlabel("p")
    ax1.set_ylabel("p(1-p)")
    ax1.set_title("Varianza p(1-p) vs p")
    st.pyplot(fig1)

st.markdown("---")

# ------------------------
# Section 2: Calculadora interactiva
# ------------------------
st.header("2. Calculadora interactiva de tamaño muestral")
st.markdown("Compara resultados usando la fórmula clásica, Wilson (simple), y Poisson (para eventos raros).")

colA, colB = st.columns(2)

with colA:
    st.subheader("Parámetros del estudio")
    use_p50 = st.checkbox("Usar p = 0.5 (conservador)", value=False)
    if use_p50:
        p_used = 0.5
    else:
        p_used = st.number_input("Proporción esperada p* (si la conoces)", min_value=0.0, max_value=1.0, value=0.01, step=0.001)
    st.write("Nivel de confianza:", confidence, f"(Z = {Z})")
    st.write("Error absoluto E:", E)
    st.write("Población N (0 = infinito):", N)

with colB:
    st.subheader("Resultados (sin corrección poblacional)")
    n_c = n_classic(p_used, Z, E)
    n_w = n_wilson_simple(Z, E)
    n_p = n_poisson(p_used, Z, E)

    st.markdown("**Fórmula clásica**")
    st.latex(r"n = \frac{Z^2 \, p(1-p)}{E^2}")
    st.write("Resultado:", int(ceil(n_c)), "observaciones (número exacto:", n_c, ")")

    st.markdown("**Fórmula Wilson (simplificada)**")
    st.latex(r"n = \frac{Z^2}{4E^2}")
    st.write("Resultado:", int(ceil(n_w)), "observaciones (número exacto:", n_w, ")")

    st.markdown("**Aproximación Poisson (útil para eventos raros)**")
    st.latex(r"n = \frac{Z^2}{E^2 \, p}")
    if p_used <= 0:
        st.write("p debe ser > 0 para Poisson")
    else:
        st.write("Resultado:", int(ceil(n_p)), "observaciones (número exacto:", n_p, ")")

st.markdown("---")

# ------------------------
# Section 3: Corrección por población finita y chequeo de normalidad
# ------------------------
st.header("3. Corrección por población finita y validez de la aproximación normal")

n_classic_adj = finite_correction(n_c, N) if N > 0 else n_c
n_wilson_adj = finite_correction(n_w, N) if N > 0 else n_w
n_poisson_adj = finite_correction(n_p, N) if (N > 0 and p_used > 0) else n_p

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("n clásico (ajustado por N)", int(ceil(n_classic_adj)))
with col2:
    st.metric("n Wilson (ajustado por N)", int(ceil(n_wilson_adj)))
with col3:
    st.metric("n Poisson (ajustado por N)", int(ceil(n_poisson_adj)))

st.write("")
st.markdown("**Chequeo aproximado de normalidad (regla empírica)**")
valid_normal = required_normality_check(int(ceil(n_classic_adj)), p_used)
st.write(
    f"¿Se cumple n·p ≥ 5 y n·(1-p) ≥ 5 para n clásico ajustado? → "
    f"{'Sí' if valid_normal else 'No'}"
)
if not valid_normal:
    st.warning(
        "La aproximación normal **no** se cumple para la fórmula clásica. "
        "Considere métodos exactos (Clopper–Pearson) o la aproximación Poisson si el evento es raro."
    )

st.markdown("---")

# ------------------------
# Section 4: Dos aplicaciones completas (con calculadora propia)
# ------------------------
st.header("4. Aplicaciones: estudios de eventos raros (2 ejemplos)")

# App: Example 1 - Reacciones adversas raras
with st.expander("Ejemplo 1 — Reacciones adversas raras (medicamento)", expanded=True):
    st.subheader("Introducción al evento")
    st.write(
        "Queremos estimar la proporción de pacientes que presentan una reacción adversa grave "
        "a un medicamento nuevo. Estudios preliminares sugieren una proporción muy baja."
    )
    st.markdown("**Parámetros recomendados**")
    col1, col2, col3 = st.columns(3)
    with col1:
        p1 = st.number_input("p* estimada (Reacción adversa)", min_value=0.0001, max_value=0.1, value=0.005, step=0.0001, key="p1")
    with col2:
        E1 = st.number_input("Error E (absoluto) ejemplo", min_value=0.0005, max_value=0.05, value=0.0025, step=0.0005, key="E1")
    with col3:
        conf1 = st.selectbox("Confianza", ["95%","99%"], key="conf1")
    Z1 = 1.96 if conf1 == "95%" else 2.575

    n1_classic = n_classic(p1, Z1, E1)
    n1_poisson = n_poisson(p1, Z1, E1)
    st.markdown("**Resultados para Reacciones adversas**")
    st.write(f"Fórmula clásica → n = {int(ceil(n1_classic))} (valor exacto: {n1_classic:.2f})")
    st.write(f"Aproximación Poisson → n = {int(ceil(n1_poisson))} (valor exacto: {n1_poisson:.2f})")
    if not required_normality_check(int(ceil(n1_classic)), p1):
        st.info("Nota: la aproximación normal no es válida aquí; prefiera Poisson o métodos exactos.")

# App: Example 2 - Accidentes graves en ciudad
with st.expander("Ejemplo 2 — Accidentes graves (vigilancia en población)", expanded=False):
    st.subheader("Introducción al evento")
    st.write(
        "Una ciudad quiere estimar la proporción de accidentes graves por año entre motociclistas. "
        "Se espera una proporción baja (por ejemplo, 0.2% - 0.5%)."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        p2 = st.number_input("p* estimada (Accidentes graves)", min_value=0.0001, max_value=0.02, value=0.002, step=0.0001, key="p2")
    with col2:
        E2 = st.number_input("Error E (absoluto) ejemplo", min_value=0.0005, max_value=0.02, value=0.001, step=0.0005, key="E2")
    with col3:
        conf2 = st.selectbox("Confianza", ["95%","99%"], key="conf2")
    Z2 = 1.96 if conf2 == "95%" else 2.575

    n2_classic = n_classic(p2, Z2, E2)
    n2_poisson = n_poisson(p2, Z2, E2)
    st.markdown("**Resultados para Accidentes graves**")
    st.write(f"Fórmula clásica → n = {int(ceil(n2_classic))} (valor exacto: {n2_classic:.2f})")
    st.write(f"Aproximación Poisson → n = {int(ceil(n2_poisson))} (valor exacto: {n2_poisson:.2f})")
    if not required_normality_check(int(ceil(n2_classic)), p2):
        st.info("Nota: la aproximación normal no es válida aquí; prefiera Poisson o métodos exactos.")

st.markdown("---")

# ------------------------
# Section 5: Visual comparativa de n según p
# ------------------------
st.header("5. Visual comparativa: Tamaño muestral requerido vs p")

st.markdown("Muestra cómo cambia el tamaño muestral (fórmula clásica) según p en el rango 0–0.5 (en eventos raros).")

p_range = np.linspace(0.0005, 0.5, 300)
n_vals = [n_classic(p, Z, E) for p in p_range]
n_vals_wilson = [n_wilson_simple(Z, E)] * len(p_range)
n_vals_poisson = [n_poisson(p, Z, E) for p in p_range]

fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.plot(p_range, n_vals, label="Clásica (p*(1-p))")
ax2.plot(p_range, n_vals_poisson, label="Poisson", linestyle="--")
ax2.plot(p_range, n_vals_wilson, label="Wilson simple", linestyle=":")
ax2.set_xlabel("p (proporción esperada)")
ax2.set_ylabel("n requerido")
ax2.set_ylim(bottom=0)
ax2.set_title("Comparativa: n requerido vs p (E y Z fijos)")
ax2.legend()
st.pyplot(fig2)

st.markdown(
    "Interpretación: observa cómo para valores pequeños de p la fórmula clásica baja, "
    "pero la aproximación Poisson puede diverger y Wilson se mantiene constante (no depende de p)."
)

st.markdown("---")
st.info("Este dashboard puede exportarse o adaptarse para generar diapositivas. "
        "Si quieres, agrego: (1) cálculo exacto Clopper–Pearson (requiere scipy/statsmodels), "
        "(2) exportar resultados a CSV, (3) mensajes automáticos para la exposición oral.")
