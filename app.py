import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------
# CONFIGURACIÓN GLOBAL
# -----------------------------------------
st.set_page_config(
    page_title="Tamaño Muestral para Proporciones Extremas",
    layout="wide"
)

# Tamaño global para todas las figuras (más pequeñas)
plt.rcParams["figure.figsize"] = (3.5, 2.5)
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10

st.title("📊 Tamaño Muestral para Proporciones Muy Pequeñas o Muy Grandes")
st.write("""
Bienvenido. Este documento está optimizado **como una presentación**, con:

- fórmulas matemáticas claras usando \\(\\LaTeX\\)
- gráficas pequeñas para no romper el diseño
- explicaciones limpias y listas para exponer
""")

st.markdown("---")

# ===============================================================
# SLIDE 1 — VARIANZA
# ===============================================================
st.header("1️⃣ Varianza de una Proporción")

st.write("### Fórmula fundamental:")

st.latex(r"""
\text{Var}(\hat{p}) = p(1 - p)
""")

st.write("""
La varianza es máxima cuando \\(p = 0.5\\), y disminuye cuando la proporción
se acerca a 0 o a 1.
""")

# Interacción
p_var = st.slider("Selecciona un valor de p:", 0.0, 1.0, 0.5, 0.01)
var_value = p_var * (1 - p_var)

st.write("### Valor calculado:")
st.latex(fr"\text{{Var}}(\hat p) = {var_value:.4f}")

# Gráfica
ps = np.linspace(0, 1, 200)
vars_ = ps * (1 - ps)
fig, ax = plt.subplots()
ax.plot(ps, vars_, linewidth=2)
ax.scatter([p_var], [var_value], color="red", s=50)
ax.set_title("Varianza de una proporción")
ax.set_xlabel("p")
ax.set_ylabel("Varianza")
ax.grid(True)
st.pyplot(fig)

st.markdown("---")

# ===============================================================
# SLIDE 2 — FÓRMULA CLÁSICA
# ===============================================================
st.header("2️⃣ Fórmula Clásica del Tamaño Muestral")

st.write("### Ecuación principal:")

st.latex(r"""
n = \frac{Z^2 \, p(1-p)}{E^2}
""")

st.write("""
Esta fórmula funciona bien cuando **0.10 < p < 0.90**.  
Para proporciones extremas deja de ser confiable.
""")

# Inputs
col1, col2 = st.columns(2)
with col1:
    z = st.number_input("Valor Z:", 1.0, 3.5, 1.96)
    p_est = st.number_input("Proporción estimada p:", 0.0001, 0.999, 0.5)

with col2:
    E = st.number_input("Error máximo E:", 0.001, 0.5, 0.05)

n_classic = (z**2 * p_est * (1 - p_est)) / (E**2)
st.success(f"📌 Tamaño muestral estimado: **n = {int(np.ceil(n_classic))}**")

st.markdown("---")

# ===============================================================
# SLIDE 3 — PROBLEMAS P EXTREMAS
# ===============================================================
st.header("3️⃣ Problemas Cuando p es Muy Pequeña o Muy Grande")

st.write("""
Cuando **p < 0.10** o **p > 0.90**, ocurre:

- La varianza es muy baja → mala aproximación normal  
- La fórmula clásica tiende a sobreestimar  
- La incertidumbre es asimétrica  
""")

st.markdown("---")

# ===============================================================
# SLIDE 4 — POISSON
# ===============================================================
st.header("4️⃣ Tamaño Muestral para Eventos Raros (Poisson)")

st.write("### Fórmula:")

st.latex(r"""
n = \frac{\ln(1 - C)}{\ln(1 - p)}
""")

col3, col4 = st.columns(2)
with col3:
    p_raro = st.number_input("Proporción rara p:", 0.000001, 0.1, 0.01)
with col4:
    C = st.slider("Probabilidad de observar ≥1 caso:", 0.50, 0.999, 0.95)

n_poisson = np.log(1 - C) / np.log(1 - p_raro)
st.success(f"📌 Tamaño muestral necesario: **n = {int(np.ceil(n_poisson))}**")

# Gráfica
ps_small = np.linspace(0.0001, 0.05, 200)
ns_small = np.log(1 - C) / np.log(1 - ps_small)
fig2, ax2 = plt.subplots()
ax2.plot(ps_small, ns_small)
ax2.set_xlabel("p")
ax2.set_ylabel("n requerido")
ax2.set_title("Tamaño muestral para eventos raros")
ax2.grid(True)
st.pyplot(fig2)

st.markdown("---")

# ===============================================================
# SLIDE 5 — MÉTODOS ROBUSTOS
# ===============================================================
st.header("5️⃣ Intervalos Robustos (Wilson & Agresti–Coull)")

st.write("### Intervalo de Wilson:")

st.latex(r"""
\tilde{p} = 
\frac{p + \frac{Z^2}{2n}}{1 + \frac{Z^2}{n}}
""")

st.write("### Intervalo Agresti–Coull:")

st.latex(r"""
\tilde{p} = \frac{x + \frac{Z^2}{2}}{n + Z^2}
""")

st.write("""
Ambos métodos funcionan mucho mejor para proporciones cercanas a 0 o 1.
""")

st.markdown("---")

# ===============================================================
# SLIDE 6 — EJEMPLO 1
# ===============================================================
st.header("🧪 Ejemplo 1 — Enfermedad Rara (p = 0.005)")

st.write("### Fórmula usada:")

st.latex(r"""
n = \frac{\ln(1 - C)}{\ln(1 - p)}
""")

colA, colB = st.columns(2)
with colA:
    p_e1 = st.number_input("Proporción:", 0.0001, 0.01, 0.005)
with colB:
    C_e1 = st.slider("Confianza:", 0.80, 0.999, 0.95)

n_e1 = np.log(1 - C_e1) / np.log(1 - p_e1)
st.success(f"✔ Tamaño muestral requerido: **{int(np.ceil(n_e1))}**")

# Gráfica
ps_e1 = np.linspace(0.0001, 0.01, 200)
ns_e1 = np.log(1 - C_e1) / np.log(1 - ps_e1)
fig3, ax3 = plt.subplots()
ax3.plot(ps_e1, ns_e1)
ax3.set_xlabel("p")
ax3.set_ylabel("n requerido")
ax3.set_title("Eventos raros — Ejemplo")
ax3.grid(True)
st.pyplot(fig3)

st.markdown("---")

# ===============================================================
# SLIDE 7 — EJEMPLO 2
# ===============================================================
st.header("🏭 Ejemplo 2 — Control de Calidad (p = 0.02)")

st.write("### Usamos la fórmula clásica:")

st.latex(r"""
n = \frac{Z^2 \, p(1-p)}{E^2}
""")

colC, colD, colE = st.columns(3)
with colC:
    p_e2 = st.number_input("Proporción:", 0.001, 0.2, 0.02)
with colD:
    E_e2 = st.number_input("Error E:", 0.001, 0.1, 0.01)
with colE:
    z_e2 = st.number_input("Valor Z:", 1.0, 3.5, 1.96)

n_e2 = (z_e2**2 * p_e2 * (1 - p_e2)) / (E_e2**2)
st.success(f"✔ Tamaño muestral requerido: **{int(np.ceil(n_e2))}**")

# Gráfica
ps_e2 = np.linspace(0.005, 0.1, 200)
ns_e2 = (z_e2**2 * ps_e2 * (1 - ps_e2)) / (E_e2**2)
fig4, ax4 = plt.subplots()
ax4.plot(ps_e2, ns_e2)
ax4.set_xlabel("p")
ax4.set_ylabel("n requerido")
ax4.set_title("Control de calidad — Ejemplo")
ax4.grid(True)
st.pyplot(fig4)

st.markdown("---")

# ===============================================================
# FINAL
# ===============================================================
st.header("🎯 Conclusión")

st.write("""
✔ Las fórmulas funcionan correctamente para rangos específicos  
✔ La aproximación normal falla en proporciones extremas  
✔ Poisson y Wilson–Agresti son alternativas robustas  
✔ Todas las gráficas aquí fueron reducidas para presentación  
✔ La notación matemática se muestra ahora con \\(\\LaTeX\\) claro  
""")
