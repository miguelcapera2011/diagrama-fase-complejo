import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Eventos Raros – Tamaño Muestral", layout="wide")

st.title("📊 Cálculo de Tamaño Muestral para Proporciones Extremas (Eventos Raros)")

st.markdown("""
Esta app permite analizar cómo cambia el tamaño muestral cuando la proporción esperada es muy pequeña o muy grande.
Incluye:

- Por qué la varianza es máxima en **p = 0.5**.
- Ajustes cuando **p < 0.10** o **p > 0.90**.
- Fórmula alternativa para evitar sobreestimación.
- Dos ejemplos de **eventos raros** totalmente interactivos.
""")

# ========================
# SECCIÓN: FÓRMULA GENERAL
# ========================

st.header("1️⃣ Fórmula general e interacción en tiempo real")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Valores de entrada")
    p = st.slider("Proporción esperada (p)", 0.0, 1.0, 0.05, 0.01)
    Z = st.slider("Valor Z", 1.0, 3.0, 1.96, 0.01)
    E = st.slider("Margen de error (E)", 0.001, 0.2, 0.05, 0.001)

with col2:
    st.subheader("Resultado del tamaño muestral")

    n = (Z**2 * p * (1 - p)) / (E**2)
    st.metric("Tamaño muestral (n)", f"{int(np.ceil(n))}")

    # Mensaje dinámico
    if p == 0.5:
        st.success("🟦 La varianza es MÁXIMA cuando p = 0.5. Esto produce el mayor tamaño muestral posible.")
    elif p < 0.10:
        st.warning("🟨 p es muy pequeño (< 0.10). Esto reduce la varianza y el tamaño muestral.")
    elif p > 0.90:
        st.warning("🟪 p es muy grande (> 0.90). También reduce la varianza y el tamaño muestral.")
    else:
        st.info("ℹ La varianza está en un nivel intermedio.")

# ========================
# GRÁFICA DINÁMICA varianza
# ========================

st.subheader("📈 Cómo cambia la varianza p(1 - p)")

p_vals = np.linspace(0, 1, 200)
var_vals = p_vals * (1 - p_vals)

fig, ax = plt.subplots()
ax.plot(p_vals, var_vals)
ax.axvline(p, linestyle="--")
ax.set_xlabel("p")
ax.set_ylabel("Varianza: p(1-p)")
st.pyplot(fig)



# ============================================================
# SECCIÓN 2 — AJUSTE PARA EVENTOS RAROS
# ============================================================

st.header("2️⃣ Ajuste cuando p < 0.10 o p > 0.90")

st.markdown("""
Cuando **p es extrema**, la fórmula tradicional suele sobreestimar el tamaño muestral.  
Se usa un ajuste recomendado:

\[
n_{ajustado} = \frac{Z^2 \cdot p(1-p)}{E^2 + \frac{Z^2}{N}}
\]

*(Usado cuando el evento es muy raro o muy frecuente.)*
""")

colA, colB = st.columns(2)

with colA:
    N = st.number_input("Población total (N)", 100, 10_000_000, 50000)
    n_adj = (Z**2 * p * (1 - p)) / (E**2 + (Z**2 / N))

with colB:
    st.metric("n ajustado", f"{int(np.ceil(n_adj))}")

    if p < 0.10:
        st.success("✔ Como p es muy pequeño, el ajuste evita **sobreestimar** el tamaño muestral.")
    elif p > 0.90:
        st.success("✔ Como p es muy grande, el ajuste también reduce la sobreestimación.")
    else:
        st.info("El ajuste es útil, pero menos relevante cuando p está entre 0.10 y 0.90.")


# ========================
# GRÁFICA DINÁMICA DEL AJUSTE
# ========================

st.subheader("📉 Comparación: fórmula clásica vs. fórmula ajustada")

n_classic_vals = (Z**2 * p_vals * (1 - p_vals)) / (E**2)
n_adj_vals = (Z**2 * p_vals * (1 - p_vals)) / (E**2 + (Z**2 / N))

fig2, ax2 = plt.subplots()
ax2.plot(p_vals, n_classic_vals, label="Clásica")
ax2.plot(p_vals, n_adj_vals, label="Ajustada")
ax2.axvline(p, linestyle="--")
ax2.legend()
st.pyplot(fig2)



# ============================================================
# SECCIÓN 3 — EJEMPLO 1 (EVENTO RARO)
# ============================================================

st.header("3️⃣ Ejemplo 1 — Enfermedad rara (p = 0.003)")

p1 = st.slider("p1 (eventos raros — enfermedad)", 0.001, 0.02, 0.003, 0.001)
Z1 = 1.96
E1 = 0.01

n1 = (Z1**2 * p1 * (1 - p1)) / (E1**2)
n1_adj = (Z1**2 * p1 * (1 - p1)) / (E1**2 + (Z1**2 / 1000000))

st.metric("n clásico", int(np.ceil(n1)))
st.metric("n ajustado", int(np.ceil(n1_adj)))

if n1 - n1_adj > 2000:
    st.warning("⚠ La fórmula clásica **sobreestima muchísimo** el tamaño muestral para eventos raros.")
else:
    st.success("Ajuste apropiado para eventos raros.")



# ============================================================
# SECCIÓN 4 — EJEMPLO 2 (EVENTO MUY FRECUENTE)
# ============================================================

st.header("4️⃣ Ejemplo 2 — Adopción casi universal de una vacuna (p = 0.97)")

p2 = st.slider("p2 (evento casi seguro)", 0.90, 1.0, 0.97, 0.01)
Z2 = 1.96
E2 = 0.01

n2 = (Z2**2 * p2 * (1 - p2)) / (E2**2)
n2_adj = (Z2**2 * p2 * (1 - p2)) / (E2**2 + (Z2**2 / 500000))

st.metric("n clásico", int(np.ceil(n2)))
st.metric("n ajustado", int(np.ceil(n2_adj)))

if p2 > 0.95:
    st.info("Cuando p es muy alto, la varianza es pequeña → se necesita **menos muestra**.")
