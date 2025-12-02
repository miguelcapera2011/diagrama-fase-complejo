import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ================================================================
# CONFIGURACIÓN GENERAL
# ================================================================
st.set_page_config(
    page_title="Tamaño Muestral para Proporciones Extremas",
    layout="wide"
)

st.title("📊 Cálculo de Tamaño Muestral para Proporciones Muy Pequeñas o Muy Grandes")
st.write("""
Esta aplicación explica de forma clara el **punto 6** solicitado:

- Por qué la **varianza es máxima en p = 0.5**.  
- Cómo ajustar el cálculo cuando **p < 0.10** o **p > 0.90**.  
- Ecuaciones alternativas para evitar **sobreestimación del tamaño muestral**.  
- Aplicaciones reales a **eventos raros**.
""")

st.divider()

# ================================================================
# SECCIÓN 1 — VARIANZA Y POR QUÉ ES MÁXIMA EN P = 0.5
# ================================================================
st.header("1️⃣ ¿Por qué la varianza es máxima en p = 0.5?")

st.write("""
La varianza de una proporción es:

\\[
Var(p) = p(1-p)
\\]

Esta expresión forma una parábola simétrica que alcanza su máximo en **p = 0.5**, porque es cuando existe la mayor incertidumbre:  
ni es muy probable (p ≈ 1) ni muy improbable (p ≈ 0).  
""")

# Gráfica de varianza
p_vals = np.linspace(0, 1, 200)
var_vals = p_vals * (1 - p_vals)

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(p_vals, var_vals)
ax.axvline(0.5, color="red")
ax.set_xlabel("p")
ax.set_ylabel("Var(p)")
ax.set_title("Varianza de una proporción")
st.pyplot(fig)

st.info("👉 Observa que la curva alcanza su punto más alto en **p = 0.5**.")

st.divider()

# ================================================================
# SECCIÓN 2 — CÁLCULO GENERAL DE TAMAÑO MUESTRAL
# ================================================================
st.header("2️⃣ Cálculo de tamaño muestral para proporciones")

st.write("""
La fórmula clásica es:

\\[
n = \\, \\frac{Z^2 \\, p(1-p)}{E^2}
\\]

Esta fórmula funciona bien cuando **p está entre 0.1 y 0.9**.  
Pero cuando **p < 0.10** o **p > 0.90**, la varianza es tan pequeña que la fórmula produce tamaños de muestra exagerados.
""")

col1, col2 = st.columns(2)

with col1:
    p = st.slider("Proporción esperada (p)", 0.0, 1.0, 0.05)
    E = st.slider("Margen de error permitido (E)", 0.005, 0.2, 0.02)
with col2:
    Z = st.selectbox("Nivel de confianza (Z)", [1.64, 1.96, 2.58], index=1)
    metodo = st.radio(
        "Método de cálculo",
        ["Fórmula estándar", "Ajuste para proporciones extremas", "Wilson"],
    )

# ----------------------------------------------------
# FUNCIONES
# ----------------------------------------------------
def n_estandar(p, E, Z):
    return (Z**2 * p * (1-p)) / (E**2)

def n_ajustada(p, E, Z):
    # Ajuste recomendado para proporciones muy pequeñas
    p_adj = max(p, 0.05) if p < 0.10 else (min(p, 0.95) if p > 0.90 else p)
    return (Z**2 * p_adj * (1-p_adj)) / (E**2)

def n_wilson(p, E, Z):
    # Intervalo de Wilson → más estable
    return (Z**2 * p*(1-p) + Z**2 * E**2 / 4) / (E**2)

# ----------------------------------------------------
# Cálculo
# ----------------------------------------------------
if metodo == "Fórmula estándar":
    n = n_estandar(p, E, Z)
elif metodo == "Ajuste para proporciones extremas":
    n = n_ajustada(p, E, Z)
elif metodo == "Wilson":
    n = n_wilson(p, E, Z)

st.success(f"📌 Tamaño muestral requerido: **{int(np.ceil(n))} personas**")

st.info("""
✔ El método **ajustado** o **Wilson** es más estable cuando p es muy pequeña (<0.10).  
✔ Evita que la fórmula estándar produzca valores absurdos (como miles o millones).
""")

st.divider()

# ================================================================
# SECCIÓN 3 — EJEMPLO REAL 1: EVENTO RARO EN SALUD
# ================================================================
st.header("3️⃣ Ejemplo real: enfermedad rara (p = 0.008)")

st.write("""
Una enfermedad afecta a menos del 1% de la población.  
Tenemos datos históricos y queremos diseñar un nuevo estudio.
""")

df = pd.DataFrame({
    "Año": [2021, 2022, 2023, 2024],
    "Casos_totales": [10000, 11000, 10500, 12000],
    "Casos_enfermedad": [80, 85, 75, 96]
})
df["Proporción"] = df["Casos_enfermedad"] / df["Casos_totales"]

st.dataframe(df)

st.write("### Tendencia de la proporción")

fig2, ax2 = plt.subplots(figsize=(6,4))
ax2.plot(df["Año"], df["Proporción"], marker="o")
ax2.set_title("Proporción histórica de enfermedad rara")
ax2.set_ylabel("Proporción")
st.pyplot(fig2)

p_real = df["Proporción"].mean()
n_real = n_ajustada(p_real, 0.01, 1.96)

st.success(f"📌 Tamaño muestral recomendado para nuevo estudio: **{int(n_real)} personas**")

st.divider()

# ================================================================
# SECCIÓN 4 — EJEMPLO REAL 2: FALLAS RARAS EN DISPOSITIVOS
# ================================================================
st.header("4️⃣ Ejemplo real: tasa de fallas de un dispositivo electrónico")

st.write("""
Una empresa quiere estimar la tasa de fallas. Las fallas son muy raras (<0.5%).
""")

df2 = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
    "Producción": [6000, 6100, 5800, 5900, 6200, 6150],
    "Fallas": [18, 21, 17, 19, 23, 22]
})

df2["Proporción"] = df2["Fallas"] / df2["Producción"]

st.dataframe(df2)

fig3, ax3 = plt.subplots(figsize=(6,4))
ax3.bar(df2["Mes"], df2["Proporción"])
ax3.set_title("Tasa mensual de fallas")
ax3.set_ylabel("Proporción")
st.pyplot(fig3)

p_falla = df2["Proporción"].mean()
n_falla = n_ajustada(p_falla, 0.01, 1.96)

st.success(f"📌 Tamaño muestral sugerido para monitoreo: **{int(n_falla)} productos**")

st.info("""
Este ejemplo muestra cómo los eventos raros requieren muestras grandes para estimarse con precisión.
""")
