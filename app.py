import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Eventos Raros – Tamaño Muestral", layout="wide")

st.title("📊 Tamaño Muestral en Proporciones Extremas (Eventos Raros)")

st.markdown("""
Esta app explica cómo calcular el tamaño muestral cuando la proporción esperada es **muy pequeña** o **muy grande**.
Incluye:

- Efecto de la varianza y por qué es máxima en **p = 0.5**.  
- Ajustes cuando **p < 0.10 o p > 0.90**.  
- Fórmula alternativa para evitar **sobreestimación** del tamaño muestral.  
- Dos **ejemplos reales** de estudios de eventos raros con gráficas y cálculos interactivos.  
""")


# ============================================================
# 1. VARIANZA Y FÓRMULA GENERAL
# ============================================================

st.header("1️⃣ Varianza y fórmula clásica del tamaño muestral")

st.markdown("""
La fórmula clásica para estimar el tamaño muestral en proporciones es:

\[
n = \frac{Z^2 \, p(1-p)}{E^2}
\]

La varianza de una proporción es:

\[
Var(p) = p(1-p)
\]

📌 **Punto clave:** la varianza es máxima cuando **p = 0.5**, lo que genera el **mayor tamaño muestral posible**.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Parámetros interactivos")
    p = st.slider("Proporción esperada p", 0.0, 1.0, 0.05, 0.01)
    Z = st.slider("Valor Z", 1.0, 3.0, 1.96, 0.01)
    E = st.slider("Margen de error E", 0.001, 0.2, 0.05, 0.001)

with col2:
    st.subheader("Resultado")
    n = (Z**2 * p * (1 - p)) / (E**2)
    st.metric("Tamaño muestral clásico n", int(np.ceil(n)))

    if p == 0.5:
        st.success("La varianza es MÁXIMA en p = 0.5 → mayor tamaño muestral.")
    elif p < 0.10:
        st.warning("p < 0.10: evento raro → varianza baja → menor tamaño muestral.")
    elif p > 0.90:
        st.warning("p > 0.90: evento casi seguro → varianza baja → menor tamaño muestral.")
    else:
        st.info("Varianza moderada.")


# ---------- GRAFICA DE VARIANZA ----------
st.subheader("📈 Comportamiento de la varianza p(1−p)")

p_vals = np.linspace(0, 1, 300)
var_vals = p_vals * (1 - p_vals)

fig, ax = plt.subplots()
ax.plot(p_vals, var_vals)
ax.axvline(p, color="red", linestyle="--")
ax.set_title("Varianza de la Proporción")
ax.set_xlabel("p")
ax.set_ylabel("p(1-p)")
st.pyplot(fig)



# ============================================================
# 2. AJUSTE PARA p EXTREMAS Y FÓRMULA ALTERNATIVA
# ============================================================

st.header("2️⃣ Ajuste para proporciones extremas y fórmula alternativa")

st.markdown("""
Cuando **p < 0.10 o p > 0.90**, la fórmula clásica sobreestima el tamaño muestral.  
Para corregir esto se usa un ajuste:

\[
n_{ajustado} = \frac{Z^2 p(1-p)}{E^2 + \frac{Z^2}{N}}
\]

La ecuación alternativa reduce el sesgo cuando el evento es muy raro o muy común.
""")

N = st.number_input("Tamaño poblacional N", 100, 10000000, 50000)

n_adj = (Z**2 * p * (1 - p)) / (E**2 + (Z**2 / N))

st.metric("Tamaño muestral ajustado", int(np.ceil(n_adj)))

if p < 0.10:
    st.success("Como p es muy pequeño, este ajuste evita una sobreestimación grande.")
elif p > 0.90:
    st.success("Como p es muy grande, el ajuste corrige la reducción de varianza.")
else:
    st.info("El ajuste es menos crítico cuando p está entre 0.10 y 0.90.")

# ---------- GRAFICA DEL AJUSTE ----------
st.subheader("📉 Comparación: fórmula clásica vs ajustada")

n_classic_vals = (Z**2 * p_vals * (1 - p_vals)) / (E**2)
n_adj_vals = (Z**2 * p_vals * (1 - p_vals)) / (E**2 + (Z**2 / N))

fig2, ax2 = plt.subplots()
ax2.plot(p_vals, n_classic_vals, label="Clásica")
ax2.plot(p_vals, n_adj_vals, label="Ajustada")
ax2.set_xlabel("p")
ax2.set_ylabel("Tamaño muestral")
ax2.legend()
ax2.axvline(p, linestyle="--")
st.pyplot(fig2)



# ============================================================
# 3. EJEMPLO REAL 1 — ENFERMEDAD RARA
# ============================================================

st.header("3️⃣ Ejemplo real 1 — Prevalencia de una enfermedad rara")

st.markdown("""
Supongamos que queremos estimar la prevalencia de una enfermedad que afecta al **0.3%** de la población.

- Evento extremadamente raro  
- Relevante para salud pública  
- Necesitamos evitar sobreestimar el tamaño muestral  
""")

p1 = st.slider("Proporción esperada p1 (enfermedad rara)", 0.001, 0.02, 0.003, 0.001)
Z1 = 1.96
E1 = st.slider("Margen E1", 0.005, 0.05, 0.01, 0.005)

n1 = (Z1**2 * p1 * (1 - p1)) / (E1**2)
n1_adj = (Z1**2 * p1 * (1 - p1)) / (E1**2 + (Z1**2 / N))

colA, colB = st.columns(2)
with colA:
    st.metric("n clásico", int(np.ceil(n1)))
with colB:
    st.metric("n ajustado", int(np.ceil(n1_adj)))

if n1 - n1_adj > 1000:
    st.warning("⚠ La fórmula clásica sobreestima enormemente el tamaño muestral.")
else:
    st.success("Ajuste adecuado para eventos rarísimos.")

# ----- Grafica -----
st.subheader("📊 Comportamiento para enfermedad rara")

fig3, ax3 = plt.subplots()
ax3.plot(p_vals, (Z1**2 * p_vals * (1 - p_vals)) / (E1**2))
ax3.axvline(p1, color="red", linestyle="--")
ax3.set_title("Tamaño muestral clásico vs p")
ax3.set_xlabel("p")
ax3.set_ylabel("n")
st.pyplot(fig3)



# ============================================================
# 4. EJEMPLO REAL 2 — EVENTO MUY FRECUENTE
# ============================================================

st.header("4️⃣ Ejemplo real 2 — Adopción casi universal de una vacuna")

st.markdown("""
Imaginemos medir la proporción de personas vacunadas cuando se espera un valor muy alto  
(por ejemplo, **p = 0.97**).  
""")

p2 = st.slider("Proporción p2 (vacunación alta)", 0.90, 1.0, 0.97, 0.01)
Z2 = 1.96
E2 = st.slider("Margen E2", 0.005, 0.05, 0.01, 0.005)

n2 = (Z2**2 * p2 * (1 - p2)) / (E2**2)
n2_adj = (Z2**2 * p2 * (1 - p2)) / (E2**2 + (Z2**2 / N))

colC, colD = st.columns(2)
with colC:
    st.metric("n clásico", int(np.ceil(n2)))
with colD:
    st.metric("n ajustado", int(np.ceil(n2_adj)))

if p2 > 0.95:
    st.info("Como p está cerca de 1, la varianza es pequeña → n disminuye.")

# ----- Grafica -----
st.subheader("📊 Comportamiento para evento muy frecuente")

fig4, ax4 = plt.subplots()
ax4.plot(p_vals, (Z2**2 * p_vals * (1 - p_vals)) / (E2**2))
ax4.axvline(p2, color="green", linestyle="--")
ax4.set_title("Tamaño muestral clásico vs p")
ax4.set_xlabel("p")
ax4.set_ylabel("n")
st.pyplot(fig4)
