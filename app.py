import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import log

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------
st.set_page_config(
    page_title="Tamaño Muestral para Proporciones Extremas",
    layout="wide"
)

st.title("Tamaño Muestral para Proporciones Muy Pequeñas o Muy Grandes")
st.write("""
""")

st.markdown("---")

# ----------------------------------------------------------
# SECCIÓN 1 — VARIANZA p(1-p)
# ----------------------------------------------------------
st.header("1️⃣ Varianza de una Proporción: ¿Por qué es máxima en p = 0.5?")

st.write("""
La fórmula de la varianza de una proporción muestral es:

\\[
Var(\\hat{p}) = p(1-p)
\\]

Esta expresión tiene un comportamiento **parabólico**:
- La varianza vale **0** cuando p = 0 y p = 1.
- Toma su **máximo valor** en p = 0.5.
- Disminuye cuando la proporción es muy baja o muy alta.

Esto significa que cuando p está cerca de 0 o de 1, la incertidumbre es menor.  
Por eso, usar p = 0.5 “por defecto” cuando el evento es raro **sobrestima enormemente** el tamaño muestral.
""")

p_var = st.slider("Selecciona un valor de p", 0.0, 1.0, 0.5, 0.01)
var_value = p_var * (1 - p_var)

st.latex(f"\\text{{Var}} = {var_value:.4f}")

# Gráfica
ps = np.linspace(0, 1, 200)
vars_ = ps * (1 - ps)

fig, ax = plt.subplots()
ax.plot(ps, vars_, label="Varianza p(1-p)", linewidth=2)
ax.scatter([p_var], [var_value], color='red', s=80)
ax.set_xlabel("p")
ax.set_ylabel("Varianza")
ax.set_title("Gráfica de la varianza de una proporción")
ax.grid(True)
st.pyplot(fig)

st.markdown("---")

# ----------------------------------------------------------
# SECCIÓN 2 — FÓRMULA CLÁSICA
# ----------------------------------------------------------
st.header("2️⃣ Tamaño Muestral con Fórmula Clásica")

st.write("""
La fórmula clásica para calcular el tamaño muestral es:

\\[
n = \\frac{Z^2 p (1-p)}{E^2}
\\]

Pero **solo funciona bien cuando p está entre 0.1 y 0.9**.  
Cuando p es extrema, la aproximación normal no es confiable.

Aquí puedes manipular los valores:
""")

col1, col2 = st.columns(2)

with col1:
    z = st.number_input("Valor Z (1.96 para 95%)", 1.0, 3.5, 1.96)
    p_est = st.number_input("Proporción estimada p", 0.0001, 0.9999, 0.5)
with col2:
    E = st.number_input("Error máximo E", 0.001, 0.5, 0.05)

n_classic = (z**2 * p_est * (1 - p_est)) / (E**2)
st.success(f"📌 Tamaño muestral recomendado con fórmula clásica: **n = {int(np.ceil(n_classic))}**")

st.markdown("---")

# ----------------------------------------------------------
# SECCIÓN 3 — PROBLEMAS CON P EXTREMAS
# ----------------------------------------------------------
st.header("3️⃣ ¿Qué pasa cuando la proporción es muy pequeña o muy grande?")

st.write("""
Cuando p se acerca a **0 o 1**:
- La varianza p(1−p) se vuelve muy pequeña.
- La fórmula clásica puede dar valores exagerados.
- La normal deja de ser una buena aproximación.
- Es mejor usar métodos especiales como Wilson, Agresti–Coull o Poisson.

A continuación veremos alternativas más robustas.
""")

st.markdown("---")

# ----------------------------------------------------------
# SECCIÓN 4 — MODELO POISSON PARA EVENTOS RAROS
# ----------------------------------------------------------
st.header("4️⃣ Cálculo del Tamaño Muestral para Eventos Raros (Modelo Poisson)")

st.write("""
Cuando la probabilidad de éxito es muy baja (**p < 0.05**), los eventos pueden modelarse con un proceso Poisson.

La fórmula para calcular el tamaño muestral necesario para observar **al menos un caso** con probabilidad C es:

\\[
n = \\frac{\\ln(1-C)}{\\ln(1-p)}
\\]

Esta herramienta es extremadamente útil en:
- epidemiología (detección de enfermedades raras)
- calidad industrial (defectos raros)
- farmacovigilancia (eventos adversos raros)
""")

col3, col4 = st.columns(2)

with col3:
    p_rare = st.number_input("Proporción rara p", 0.000001, 0.1, 0.01)
with col4:
    C = st.slider("Confianza de detectar ≥1 caso", 0.50, 0.999, 0.95, 0.01)

n_poisson = np.log(1 - C) / np.log(1 - p_rare)
st.success(f"📌 Tamaño muestral necesario: **{int(np.ceil(n_poisson))}**")

# gráfica
fig2, ax2 = plt.subplots()
ps_small = np.linspace(0.0001, 0.05, 200)
ns_small = np.log(1 - C) / np.log(1 - ps_small)
ax2.plot(ps_small, ns_small)
ax2.set_xlabel("p")
ax2.set_ylabel("n requerido")
ax2.set_title("Tamaño muestral para detectar ≥1 evento raro")
ax2.grid(True)
st.pyplot(fig2)

st.markdown("---")

# ----------------------------------------------------------
# SECCIÓN 5 — EJEMPLOS APLICADOS
# ----------------------------------------------------------
st.header("5️⃣ Ejemplos Aplicados (Interactividad + Explicación)")

st.write("""
A continuación presentamos **dos casos reales** donde se requieren tamaños muestrales especializados.
Cada caso tiene una breve introducción del problema, conceptos relevantes y controles para que el usuario experimente.
""")

# ---------------- EXAMPLE 1 ----------------
st.subheader("🧪 Ejemplo 1: Detección de una Enfermedad Rara (p ≈ 0.005)")

st.write("""
Supongamos que un laboratorio quiere estimar la prevalencia de una enfermedad rara.  
La literatura indica que su prevalencia es de **0.5% (p = 0.005)**.  
El laboratorio quiere tener **95% de probabilidad** de detectar al menos un caso.

Usamos el modelo Poisson para eventos raros.
""")

colA, colB = st.columns(2)

with colA:
    p_e1 = st.number_input("Proporción esperada (p)", 0.0001, 0.05, 0.005)
with colB:
    C_e1 = st.slider("Confianza deseada", 0.80, 0.999, 0.95)

n_e1 = np.log(1 - C_e1) / np.log(1 - p_e1)

st.info(f"📌 Para detectar ≥1 caso con {int(C_e1*100)}% de confianza, se requiere: **n = {int(np.ceil(n_e1))} muestras**.")

# graph
ps_e1 = np.linspace(0.0001, 0.01, 200)
ns_e1 = np.log(1 - C_e1) / np.log(1 - ps_e1)

fig3, ax3 = plt.subplots()
ax3.plot(ps_e1, ns_e1)
ax3.set_xlabel("p esperada")
ax3.set_ylabel("n requerido")
ax3.set_title("Sensibilidad del tamaño muestral a la prevalencia")
ax3.grid(True)
st.pyplot(fig3)

st.markdown("---")

# ---------------- EXAMPLE 2 ----------------
st.subheader("🏭 Ejemplo 2: Control de Calidad en una Fábrica (p ≈ 0.02)")

st.write("""
Una fábrica produce 100,000 piezas al mes.  
La gerencia quiere estimar la tasa de defectos, históricamente alrededor de **2% (p = 0.02)**,  
con un error máximo de **E = 0.01** y un nivel de confianza del **95% (Z = 1.96)**.

Aquí sí podemos usar la fórmula clásica porque p no es extremadamente baja (<0.01).
""")

colC, colD, colE = st.columns(3)

with colC:
    p_e2 = st.number_input("Tasa estimada de defectos p", 0.001, 0.2, 0.02)
with colD:
    E_e2 = st.number_input("Error máximo permitido E", 0.001, 0.1, 0.01)
with colE:
    z_e2 = st.number_input("Valor Z (95% = 1.96)", 1.0, 3.5, 1.96)

n_e2 = (z_e2**2 * p_e2 * (1 - p_e2)) / (E_e2**2)

st.success(f"📌 Tamaño muestral recomendado: **n = {int(np.ceil(n_e2))} piezas**.")

# gráfica
ps_e2 = np.linspace(0.005, 0.1, 200)
ns_e2 = (z_e2**2 * ps_e2 * (1 - ps_e2)) / (E_e2**2)

fig4, ax4 = plt.subplots()
ax4.plot(ps_e2, ns_e2)
ax4.set_xlabel("p esperada")
ax4.set_ylabel("n requerido")
ax4.set_title("Tamaño muestral en función de la tasa de defectos")
ax4.grid(True)
st.pyplot(fig4)

st.markdown("---")

# ----------------------------------------------------------
# CIERRE
# ----------------------------------------------------------
st.header("🎯 Conclusión")

st.write("""
Esta aplicación demuestra que:
- La varianza de una proporción es máxima en p=0.5.
- Para proporciones extremas, la fórmula normal falla.
- Para eventos raros, el **modelo Poisson** es la herramienta adecuada.
- Cada caso debe analizarse con el método correcto.

Gracias por usar esta aplicación educativa.  
¡Ahora estás listo para exponer este tema como un profesional!
""")

