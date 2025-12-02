import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURACIÓN
st.set_page_config(page_title="Tamaño Muestral - Proporciones Extremas", layout="wide")
st.title("📊 Tamaño Muestral para Proporciones Muy Pequeñas o Muy Grandes")
st.write("""
Esta aplicación explica y demuestra de forma interactiva el **punto 6**:

- Por qué la **varianza p(1−p)** es máxima en **p = 0.5**
- Qué ocurre cuando **p < 0.10** (eventos raros) o **p > 0.90**
- Cómo aplicar **ajustes** para evitar sobreestimar tamaño de muestra
- Aplicado en **2 ejemplos reales** que reaccionan a tus parámetros
""")

st.divider()

# =======================================================
# 1. VARIANZA INTERACTIVA
# =======================================================

st.header("1️⃣ Varianza de la proporción y su máximo en p = 0.5")

p_slider = st.slider("Selecciona un valor de p", 0.0, 1.0, 0.5, 0.01)

st.write(f"""
Para p = **{p_slider}**, la varianza es:

\\[
Var(p) = p(1-p) = {round(p_slider*(1-p_slider), 4)}
\\]
""")

# Gráfica de varianza
p_vals = np.linspace(0, 1, 300)
var_vals = p_vals * (1 - p_vals)

fig1, ax1 = plt.subplots(figsize=(6,4))
ax1.plot(p_vals, var_vals)
ax1.scatter([p_slider], [p_slider*(1-p_slider)], color="red")
ax1.axvline(0.5, color="orange", linestyle="--")
ax1.set_title("Varianza de p según p(1-p)")
ax1.set_xlabel("p")
ax1.set_ylabel("Varianza")
st.pyplot(fig1)

st.info("""
✔ La incertidumbre máxima ocurre en p = 0.5  
✔ Cuando p es muy pequeño o muy grande, la varianza baja → la fórmula estándar deja de funcionar bien.
""")

st.divider()



# =======================================================
# 2. CÁLCULO INTERACTIVO DEL TAMAÑO MUESTRAL
# =======================================================

st.header("2️⃣ Cálculo interactivo del tamaño muestral")

col1, col2 = st.columns(2)

with col1:
    p = st.slider("Proporción esperada p", 0.0, 1.0, 0.05)
    E = st.slider("Margen de error E", 0.005, 0.2, 0.02)

with col2:
    Z = st.selectbox("Nivel de confianza", [1.64, 1.96, 2.58], index=1)
    metodo = st.radio(
        "Método",
        ["Estándar", "Ajustado para extremos", "Wilson (recomendado)"]
    )

# funciones
def n_estandar(p, E, Z):
    return (Z**2 * p*(1-p)) / E**2

def n_ajuste(p, E, Z):
    p_adj = max(min(p, 0.95), 0.05)
    return (Z**2 * p_adj*(1-p_adj)) / E**2

def n_wilson(p, E, Z):
    return (Z**2 * p*(1-p) + Z**2 * (E**2)/4 ) / (E**2)

# cálculo
if metodo == "Estándar":
    n = n_estandar(p, E, Z)
elif metodo == "Ajustado para extremos":
    n = n_ajuste(p, E, Z)
else:
    n = n_wilson(p, E, Z)

st.success(f"📌 Tamaño muestral: **{int(np.ceil(n))} personas**")

# gráfica dinámica
fig4, ax4 = plt.subplots(figsize=(6,4))
ax4.plot(p_vals, n_estandar(p_vals, E, Z), label="Estándar")
ax4.plot(p_vals, n_ajuste(p_vals, E, Z), label="Ajustado extremo")
ax4.plot(p_vals, n_wilson(p_vals, E, Z), label="Wilson")
ax4.scatter([p], [n], color="red")
ax4.set_title("Tamaño muestral según p y método")
ax4.set_xlabel("p")
ax4.set_ylabel("n")
ax4.legend()
st.pyplot(fig4)

st.info("""
La diferencia entre métodos aumenta muchísimo cuando p es muy pequeña o muy grande.
""")

st.divider()


# =======================================================
# 3. EJEMPLOS REALES — INTERACTIVOS
# =======================================================

st.header("3️⃣ Ejemplos reales (interactivos con tus parámetros)")

tab1, tab2 = st.tabs(["🧪 Enfermedad rara", "⚙️ Fallas de productos"])

# --- EJEMPLO 1 ---
with tab1:
    st.subheader("Enfermedad con prevalencia cercana a 1%")

    datos = pd.DataFrame({
        "Año": [2021, 2022, 2023, 2024],
        "Población": [5000, 5200, 5100, 5300],
        "Casos": [52, 45, 60, 55]
    })
    datos["Proporción"] = datos["Casos"] / datos["Población"]

    st.write(datos)

    p_real = datos["Proporción"].mean()
    n_enf = n_wilson(p_real, E, Z)

    st.success(f"📌 Tamaño muestral según tus parámetros: **{int(n_enf)} personas**")

    fig5, ax5 = plt.subplots(figsize=(6,4))
    ax5.plot(datos["Año"], datos["Proporción"], marker="o")
    ax5.set_title("Prevalencia histórica")
    st.pyplot(fig5)

# --- EJEMPLO 2 ---
with tab2:
    st.subheader("Fallas raras en dispositivos electrónicos")

    df2 = pd.DataFrame({
        "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
        "Producidos": [6000, 5900, 6100, 6200, 5800, 6050],
        "Fallas": [20, 18, 22, 21, 19, 23]
    })

    df2["Proporción"] = df2["Fallas"] / df2["Producidos"]

    st.write(df2)

    p_falla = df2["Proporción"].mean()
    n_falla = n_wilson(p_falla, E, Z)

    st.success(f"📌 Tamaño muestral según tus parámetros: **{int(n_falla)} productos**")

    fig6, ax6 = plt.subplots(figsize=(6,4))
    ax6.bar(df2["Mes"], df2["Proporción"])
    ax6.set_title("Tasa mensual de fallas")
    st.pyplot(fig6)
