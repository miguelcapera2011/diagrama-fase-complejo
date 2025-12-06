# ============================================================
# APP STREAMLIT – Proporciones extremas y tamaño muestral
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ----------------- CONFIG GENERAL -----------------
st.set_page_config(
    page_title="Proporciones extremas y tamaño muestral",
    page_icon="📊",
    layout="centered",
)

# Fondo bonito con CSS
st.markdown("""
<style>
body {
    background-color: #e8f0ff;
}
.block-container {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 0 15px rgba(0,0,0,0.15);
}
h1, h2, h3, p, label, span {
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ----------------- TÍTULO BONITO -----------------
st.markdown("""
# 📘 Proporciones con p muy pequeñas o muy grandes  
### **Tamaño muestral, varianza y eventos raros**
""")


# ----------------- INTRODUCCIÓN -----------------
st.write("""
Esta app te permite entender de forma clara:

- Cómo cambia la **varianza** de una proporción.  
- Por qué la varianza es mayor cuando **p = 0.5**.  
- Qué pasa cuando la proporción esperada es **muy pequeña (< 0.10)** o muy grande **(> 0.90)**.  
- Cómo ajustar la **fórmula del tamaño muestral** en eventos raros para evitar sobreestimar la muestra.

Todo explicado sin derivadas, de forma intuitiva.
""")


# ----------------- SLIDER PARA p -----------------
st.subheader("🔧 Ajusta el valor de p (proporción esperada)")

p = st.slider(
    "Selecciona un valor para p",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01
)

var_p = p * (1 - p)
st.write(f"### 📌 Varianza: **{var_p:.4f}**")


# ----------------- GRÁFICA VARIANZA -----------------
st.subheader("📈 Varianza de la proporción: p(1-p)")

p_vals = np.linspace(0, 1, 200)
var_vals = p_vals * (1 - p_vals)

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(p_vals, var_vals, linewidth=2)
ax.scatter([p], [var_p], s=120)
ax.set_xlabel("p")
ax.set_ylabel("Varianza: p(1-p)")
ax.set_title("Curva de la varianza según p")
ax.grid(True)

st.pyplot(fig)


# ----------------- SECCIÓN: EXPLICACIÓN SIMPLE -----------------
st.markdown("""
---

## 🌟 ¿Por qué la varianza es máxima en p = 0.5? (explicación sin derivadas)

La varianza de una proporción es:

\\[
Var(\hat{p}) = p(1-p)
\\]

Esta expresión mide la **incertidumbre**.  

- Cuando p está muy cerca de **0**, casi nadie tiene la característica → poca variabilidad.  
- Cuando p está muy cerca de **1**, casi todos la tienen → poca variabilidad.  
- Cuando p = 0.5, hay **máxima mezcla**, máxima incertidumbre, máximo “desorden”.

Por eso la varianza es más alta en **0.5**, el punto donde hay más posibilidad de ver resultados muy distintos.

---
""")


# ----------------- SECCIÓN: TAMAÑO MUESTRAL -----------------
st.markdown("## 🧮 Cálculo del tamaño muestral para proporciones")

Z = st.number_input("Valor de Z (ej: 1.96 para 95%)", value=1.96)
E = st.number_input("Error máximo permitido (E)", value=0.05)

n_standard = (Z**2 * p * (1 - p)) / (E**2)

st.write(f"### 📌 Tamaño muestral estándar: **n = {n_standard:.2f}**")


# ----------------- AJUSTES PARA EVENTOS RAROS -----------------
st.markdown("""
---

## ⚠ Ajustes cuando p es muy pequeña (< 0.10) o muy grande (> 0.90)

Cuando p es muy pequeña, por ejemplo:

- Enfermedades raras  
- Accidentes poco frecuentes  
- Defectos de fabricación muy bajos  

El producto \\(p(1-p)\\) se hace **tan pequeño** que:

- La fórmula estándar **subestima la incertidumbre real**.  
- Y puede **necesitarse más muestra** de la que la fórmula normal predice.

### ✔ Fórmula alternativa recomendada (para eventos raros):

Cuando p < 0.10, se recomienda usar:

\\[
n = \frac{Z^2 \, p}{E^2}
\\]

porque cuando p es muy pequeña, 1–p ≈ 1, y la fórmula se simplifica.

### ✔ Otra alternativa para evitar sobreestimar:

Usamos el ajuste:

\\[
p_{adj} = p + \frac{1}{2n}
\\]

(Esto evita que p=0 cause errores.)

---
""")


# ----------------- CÁLCULO AJUSTADO -----------------
st.subheader("🔧 Tamaño muestral ajustado para eventos raros")

if p < 0.10 or p > 0.90:
    n_rare = (Z**2 * p) / (E**2)
    st.write(f"### 📌 Tamaño muestral para eventos raros: **n = {n_rare:.2f}**")
else:
    st.write("### ✔ p no es extremo (no requiere ajuste especial).")


# ----------------- APLICACIONES -----------------
st.markdown("""
---

## 🌍 Aplicaciones reales: estudios de eventos raros

### ✔ Epidemiología
- Detección de cáncer poco frecuente  
- Incidencia de enfermedades infecciosas raras  

### ✔ Ingeniería y calidad
- Defectos de un producto que ocurren menos del 1%  
- Fallas críticas en sistemas de seguridad  

### ✔ Medio ambiente
- Niveles de contaminación por debajo del 5%  
- Presencia rara de un contaminante en agua

En todos estos casos, **p es muy pequeña**, la varianza también,  
y se necesitan **muestras más grandes** para detectar algo raro con precisión.

---

## ✨ Gracias por explorar esta herramienta interactiva
Ajusta los valores y observa cómo cambia todo.  
Así se entiende de forma visual y clara la teoría del muestreo con proporciones.
""")
