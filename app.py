# Guardar como app.py y ejecutar con `streamlit run app.py`

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import norm

st.title("Tamaño Muestral para Proporciones Raras con Gráfica")

# ------------------------------
# Parámetros del estudio
# ------------------------------
st.header("Parámetros del estudio")
E = st.number_input("Error absoluto deseado (E)", min_value=0.0001, max_value=1.0, value=0.005, step=0.001)
confianza = st.selectbox("Nivel de confianza (%)", [90, 95, 99])
Z = norm.ppf(1 - (1-confianza/100)/2)

# ------------------------------
# Rango de proporciones
# ------------------------------
p_vals = np.linspace(0.001, 0.999, 500)  # evita 0 y 1 exactos para no dividir entre cero

# Tamaño muestral conservador (varianza máxima)
n_max_var = (Z**2 * 0.25) / (E**2)

# Tamaño muestral ajustado (varianza real)
n_ajustada = (Z**2 * p_vals * (1 - p_vals)) / (E**2)

# ------------------------------
# Gráfica comparativa
# ------------------------------
st.subheader("Comparación del tamaño muestral")
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(p_vals, n_ajustada, label="Ajustado para p", color='blue')
ax.axhline(y=n_max_var, color='red', linestyle='--', label="Conservador (máx. varianza)")
ax.set_xlabel("Proporción esperada p")
ax.set_ylabel("Tamaño muestral n")
ax.set_title("Tamaño muestral vs proporción esperada")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ------------------------------
# Ejemplos de eventos raros
# ------------------------------
st.header("Ejemplos de eventos raros")

# 1️⃣ Defectos graves en autos
st.subheader("1️⃣ Defectos graves en autos")
p_auto = 0.005
E_auto = 0.002
n_auto = (Z**2 * p_auto * (1-p_auto)) / (E_auto**2)
st.write(f"Proporción esperada: {p_auto*100}%")
st.write(f"Tamaño muestral ajustado: {math.ceil(n_auto)} autos")

# 2️⃣ Reacciones graves a vacuna
st.subheader("2️⃣ Reacciones graves a vacuna")
p_vacuna = 0.001
E_vacuna = 0.0005
n_vacuna = (Z**2 * p_vacuna * (1-p_vacuna)) / (E_vacuna**2)
st.write(f"Proporción esperada: {p_vacuna*100}%")
st.write(f"Tamaño muestral ajustado: {math.ceil(n_vacuna)} personas")
