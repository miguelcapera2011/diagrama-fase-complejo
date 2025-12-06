import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import log, sqrt

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------
st.set_page_config(
    page_title="Tamaño Muestral para Proporciones Extremas",
    layout="wide"
)

# ⬇️ Nuevo: tamaño global para todas las gráficas
plt.rcParams["figure.figsize"] = (4, 3)

st.title("📊 Tamaño Muestral para Proporciones Muy Pequeñas o Muy Grandes")
st.write("""
Esta aplicación está diseñada para **presentación y exposición**, con explicaciones completas,
fórmulas claras y herramientas interactivas.
""")

st.markdown("---")

# ===============================================================
# 1. VARIANZA p(1-p)
# ===============================================================
st.header("1️⃣ Varianza de una Proporción y su Comportamiento")

st.write("""
La varianza de una proporción está dada por la fórmula fundamental:

🔹 **Fórmula de la varianza de una proporción:**

\\[
Var(\\hat{p}) = p(1-p)
\\]

Esta fórmula se deriva de la distribución binomial y nos dice cómo cambia la variabilidad del estimador \\(\\hat{p}\\).
La varianza depende directamente de p.
""")

with st.expander("📘 ¿Por qué la varianza es máxima en p = 0.5? (Ver explicación y gráfico)"):
    st.write("""
La función:

\\[
f(p) = p(1-p)
\\]

es una parábola invertida.  
El máximo ocurre cuando la derivada se hace cero:

\\[
f'(p) = 1 - 2p = 0 \Rightarrow p = 0.5
\\]

Por lo tanto:

- La varianza ES MÁXIMA en p = 0.5.  
- Disminuye cuando p se acerca a 0 o 1.  
- Esto explica por qué usar p = 0.5 cuando el evento es raro **sobrestima muchísimo el tamaño muestral**.
""")

p_var = st.slider("Selecciona un valor de p:", 0.0, 1.0, 0.5, 0.01)
var_value = p_var * (1 - p_var)

st.latex(f"Var(\\hat p) = {var_value:.4f}")

# Gráfica
ps = np.linspace(0, 1, 200)
vars_ = ps * (1 - ps)
fig, ax = plt.subplots()
ax.plot(ps, vars_, linewidth=2)
ax.scatter([p_var], [var_value], color="red", s=80)
ax.set_title("Varianza de una proporción")
ax.set_xlabel("p")
ax.set_ylabel("Varianza")
ax.grid(True)
st.pyplot(fig)

st.markdown("---")


# ===============================================================
# 2. FÓRMULA CLÁSICA
# ===============================================================
st.header("2️⃣ Fórmula Clásica para el Tamaño Muestral")

st.write("""
La fórmula clásica para estimar una proporción con precisión E y nivel de confianza Z es:

\\[
n = \\frac{ Z^2 \\, p(1-p) }{ E^2 }
\\]

⚠ **Advertencia:**  
Esta fórmula solo es adecuada cuando 0.10 < p < 0.90.  
Para proporciones extremas, la aproximación normal falla.

""")

with st.expander("📘 Derivación de la fórmula clásica (opcional)"):
    st.write("""
La fórmula proviene de:

\\[
E = Z \\sqrt{\\frac{p(1-p)}{n}}
\\]

Despejando n:

\\[
n = \\frac{ Z^2 p(1-p) }{E^2}
\\]
""")

col1, col2 = st.columns(2)

with col1:
    z = st.number_input("Valor Z:", 1.0, 3.5, 1.96)
    p_est = st.number_input("Proporción estimada p:", 0.0001, 0.999, 0.5)

with col2:
    E = st.number_input("Error máximo E:", 0.001, 0.5, 0.05)

n_classic = (z**2 * p_est * (1 - p_est)) / (E**2)
st.success(f"📌 Tamaño muestral (fórmula clásica): **n = {int(np.ceil(n_classic))}**")

st.markdown("---")


# ===============================================================
# 3. PROBLEMAS CON p EXTREMAS
# ===============================================================
st.header("3️⃣ Problemas Cuando la Proporción es Muy Pequeña o Muy Grande")

st.write("""
Cuando **p es muy pequeña (< 0.1)** o **muy grande (> 0.9)**:

### ❌ Problema 1 — La varianza es muy pequeña  
Esto hace que la normal no sea una buena aproximación.

### ❌ Problema 2 — La fórmula clásica puede explotar  
El tamaño muestral puede estimarse muy alto sin necesidad.

### ❌ Problema 3 — Incertidumbre asimétrica  
Los intervalos dejan de ser simétricos.

Por esta razón pasamos a métodos más robustos como Poisson, Wilson y Agresti-Coull.
""")

st.markdown("---")


# ===============================================================
# 4. MODELO POISSON — EVENTOS RAROS
# ===============================================================
st.header("4️⃣ Tamaño Muestral para Eventos Raros (Modelo Poisson)")

st.write("""
Cuando p < 0.05, los eventos pueden modelarse como una distribución Poisson.

### 📌 Fórmula para el tamaño muestral necesario para observar ≥1 caso

\\[
n = \\frac{ \\ln(1-C) }{ \\ln(1-p) }
\\]

donde:

- \\(p\\) = proporción del evento raro  
- \\(C\\) = probabilidad deseada de observar al menos un caso  
""")

col3, col4 = st.columns(2)
with col3:
    p_raro = st.number_input("Proporción rara p:", 0.000001, 0.1, 0.01)
with col4:
    C = st.slider("Confianza de observar ≥1 caso:", 0.50, 0.999, 0.95)

n_poisson = np.log(1 - C) / np.log(1 - p_raro)

st.success(f"📌 Tamaño muestral necesario: **n = {int(np.ceil(n_poisson))}**")

# Gráfica
ps_small = np.linspace(0.0001, 0.05, 200)
ns_small = np.log(1 - C) / np.log(1 - ps_small)
fig2, ax2 = plt.subplots()
ax2.plot(ps_small, ns_small)
ax2.set_xlabel("p")
ax2.set_ylabel("n requerido")
ax2.set_title("Tamaño muestral para detectar ≥1 evento raro")
ax2.grid(True)
st.pyplot(fig2)

st.markdown("---")

# ===============================================================
# 5. MÉTODOS ROBUSTOS (WILSON Y AGREESTI)
# ===============================================================
st.header("5️⃣ Métodos Alternativos Robustos")

st.write("""
Existen intervalos más robustos que la normal para proporciones extremas:

---

## 🔷 Intervalo de Wilson

\\[
\\tilde{p} = 
\\frac{ p + \\frac{Z^2}{2n} }{1 + \\frac{Z^2}{n}}
\\]

---

## 🔷 Intervalo Agresti–Coull

\\[
\\tilde{p} = \\frac{x + Z^2/2}{n + Z^2}
\\]

Ambos corrigen sesgos cuando p está cerca de 0 o 1.  
(En versiones futuras agregaremos calculadora interactiva aquí.)
""")

st.markdown("---")

# ===============================================================
# 6. EJEMPLOS APLICADOS
# ===============================================================
st.header("6️⃣ Ejemplos Aplicados con Fórmulas y Cálculo Interactivo")

st.write("A continuación se presentan dos casos reales y completos.")


# ===============================================================
# EJEMPLO 1
# ===============================================================
st.subheader("🧪 Ejemplo 1: Enfermedad Rara — p = 0.005")

st.write("""
### 📌 Introducción del problema:
Un laboratorio quiere estudiar una enfermedad cuya prevalencia es **0.5% (p = 0.005)**.  
Desea tener al menos **95% de probabilidad** de detectar un caso.

### Usamos la fórmula Poisson:
\\[
n = \\frac{\\ln(1-C)}{\\ln(1-p)}
\\]
""")

colA, colB = st.columns(2)
with colA:
    p_e1 = st.number_input("Proporción (p):", 0.0001, 0.01, 0.005)
with colB:
    C_e1 = st.slider("Confianza:", 0.80, 0.999, 0.95)

n_e1 = np.log(1 - C_e1) / np.log(1 - p_e1)
st.success(f"✔ Tamaño muestral requerido: **{int(np.ceil(n_e1))}**")

# gráfica
ps_e1 = np.linspace(0.0001, 0.01, 200)
ns_e1 = np.log(1 - C_e1) / np.log(1 - ps_e1)
fig3, ax3 = plt.subplots()
ax3.plot(ps_e1, ns_e1)
ax3.set_xlabel("p")
ax3.set_ylabel("n requerido")
ax3.set_title("Tamaño muestral vs prevalencia")
ax3.grid(True)
st.pyplot(fig3)

st.markdown("---")


# ===============================================================
# EJEMPLO 2
# ===============================================================
st.subheader("🏭 Ejemplo 2: Control de Calidad — p = 0.02")

st.write("""
### 📌 Introducción del problema:
Una fábrica tiene una tasa de defectos de **2%**.  
Desea estimarla con un error máximo **E = 0.01** y confianza **95%**.

### Fórmula usada:

\\[
n = \\frac{ Z^2 \\, p(1-p) }{ E^2 }
\\]
""")

colC, colD, colE = st.columns(3)
with colC:
    p_e2 = st.number_input("Proporción (p):", 0.001, 0.2, 0.02)
with colD:
    E_e2 = st.number_input("Error E:", 0.001, 0.1, 0.01)
with colE:
    z_e2 = st.number_input("Valor Z:", 1.0, 3.5, 1.96)

n_e2 = (z_e2**2 * p_e2 * (1 - p_e2)) / (E_e2**2)
st.success(f"✔ Tamaño muestral requerido: **{int(np.ceil(n_e2))}**")

# gráfica
ps_e2 = np.linspace(0.005, 0.1, 200)
ns_e2 = (z_e2**2 * ps_e2 * (1 - ps_e2)) / (E_e2**2)
fig4, ax4 = plt.subplots()
ax4.plot(ps_e2, ns_e2)
ax4.set_xlabel("p")
ax4.set_ylabel("n requerido")
ax4.set_title("Tamaño muestral vs tasa de defectos")
ax4.grid(True)
st.pyplot(fig4)

st.markdown("---")

st.header("🎯 Conclusión")

st.write("""
Esta aplicación muestra que:

✔ La varianza es máxima en p = 0.5  
✔ La fórmula clásica falla cuando p está cerca de 0 o 1  
✔ Cuando los eventos son raros, el modelo Poisson es el correcto  
✔ Para proporciones extremas, los métodos de Wilson y Agresti-Coull son más robustos  

Gracias por utilizar esta herramienta educativa optimizada para exposición.
""")
