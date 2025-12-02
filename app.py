# ============================================================
# APP STREAMLIT COMPLETA – Cálculo de tamaño muestral para proporciones extremas
# Incluye los 4 incisos del punto 6 en una sola aplicación
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    page_title="Tamaño muestral para proporciones extremas",
    layout="wide"
)

st.title("📊 Cálculo de tamaño muestral para proporciones muy pequeñas o muy grandes")
st.write("Aplicación completa del **Punto 6**: teoría + interactividad + ejemplos reales.")

# ==========================================
# SECCIÓN 6.1 — Varianza máxima en p = 0.5
# ==========================================

st.header("6.1 ¿Por qué la máxima varianza ocurre en p = 0.5?")

st.write("""
La varianza de una proporción es:

\\[
Var(\\hat p)=\\frac{p(1-p)}{n}
\\]

Si ignoramos momentáneamente a n, la expresión importante es:

\\[
p(1-p)
\\]

Esta es una parábola invertida cuya **máxima varianza ocurre en p = 0.5**.
""")

# Gráfica
p_vals = np.linspace(0, 1, 300)
var_vals = p_vals * (1 - p_vals)

fig1, ax1 = plt.subplots()
ax1.plot(p_vals, var_vals)
ax1.set_xlabel("p")
ax1.set_ylabel("Varianza p(1-p)")
ax1.set_title("Varianza máxima en p = 0.5")

st.pyplot(fig1)

st.info("Cuando p = 0.5 hay máxima incertidumbre: mitad éxitos / mitad fracasos → mayor variabilidad.")

st.divider()

# ==========================================
# SECCIÓN 6.2 — Ajustes cuando p es extrema
# ==========================================

st.header("6.2 Ajustes cuando p < 0.10 o p > 0.90")

st.write("""
Cuando p es muy pequeña o muy grande, la fórmula clásica:

\\[
n = \\frac{z^2 p(1-p)}{d^2}
\\]

puede **sobreestimar** el tamaño muestral.  
Aquí aplicamos un ajuste usando límites razonables:  
- si p < 0.05 → usar p = 0.05  
- si p > 0.95 → usar p = 0.95  
""")

# Inputs
col1, col2, col3 = st.columns(3)

with col1:
    p = st.number_input("Proporción esperada (p)", min_value=0.0001, max_value=0.9999, value=0.02)
with col2:
    z = st.number_input("Valor z (1.96 para 95%)", value=1.96)
with col3:
    d = st.number_input("Margen de error (d)", value=0.01)

# Cálculo clásico
n_clasico = z**2 * p * (1 - p) / d**2

# Ajuste
p_adj = max(min(p, 0.95), 0.05)
n_ajustado = z**2 * p_adj * (1 - p_adj) / d**2

st.subheader("Resultados")

st.write(f"📌 **Tamaño muestral clásico:** {round(n_clasico,2)}")
st.write(f"📌 **Tamaño muestral ajustado:** {round(n_ajustado,2)}")

if p < 0.05 or p > 0.95:
    st.warning("p es extrema. Se aplicó un ajuste para evitar sobreestimación.")
else:
    st.info("p está en rango aceptable. No se necesitó ajuste.")

st.divider()

# ==========================================
# SECCIÓN 6.3 — Ecuación alternativa (Poisson)
# ==========================================

st.header("6.3 Alternativa para evitar sobreestimación: modelo de Poisson")

st.write("""
Para eventos muy raros, la binomial se aproxima por una **Poisson**, lo cual da un tamaño muestral más estable:

\\[
n = \\frac{Z_{\\alpha/2}^2 \\, \\lambda}{d^2}
\\]

Donde **λ ≈ p** cuando p es muy pequeño.
""")

# Inputs Poisson
col4, col5, col6 = st.columns(3)

with col4:
    lam = st.number_input("Tasa λ (≈ p si p es muy pequeño)", value=0.01)
with col5:
    z2 = st.number_input("Valor z", value=1.96)
with col6:
    d2 = st.number_input("Margen de error", value=0.005)

# Cálculo Poisson
n_poisson = z2**2 * lam / d2**2

st.write(f"📌 **Tamaño muestral usando Poisson:** {round(n_poisson,2)}")

st.info("Este método es ideal cuando p < 0.05.")

st.divider()

# ==========================================
# SECCIÓN 6.4 — Aplicaciones reales
# ==========================================

st.header("6.4 Aplicaciones reales: estudios de eventos raros")

st.write("Seleccione uno para ver su explicación:")

ejemplo = st.selectbox(
    "Ejemplos reales",
    ["Anafilaxia por vacunas", "Falla catastrófica en turbinas de aviones"]
)

if ejemplo == "Anafilaxia por vacunas":
    st.subheader("Anafilaxia posterior a vacunación")
    st.write("""
- Evento extremadamente raro: **1 a 5 casos por millón**  
- Se estudia con modelos tipo **Poisson**  
- Se usa en sistemas como **VAERS** (EE.UU.)
    """)
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Vaccine_types_diagram.svg/640px-Vaccine_types_diagram.svg.png")

else:
    st.subheader("Falla catastrófica en turbinas de aviones")
    st.write("""
- Probabilidad aproximada: **1 evento por cada 10 millones de horas de vuelo**  
- Industria aeronáutica usa modelos Poisson y análisis de riesgo extremo  
    """)
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Jet_engine_diagram.svg/640px-Jet_engine_diagram.svg.png")

st.success("La app cubre los 4 incisos del punto 6: teoría, gráficas, interactividad y aplicaciones reales.")
