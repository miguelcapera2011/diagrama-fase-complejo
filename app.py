# Guardar como app.py y ejecutar: streamlit run app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Tamaño Muestral en Eventos Raros", layout="wide")

st.title("📊 Tamaño Muestral para Proporciones en Eventos Raros")

st.markdown("""
Esta app permite entender **cómo calcular el tamaño muestral** para proporciones muy pequeñas o muy grandes.  
Se enfoca en **eventos raros**, donde usar la varianza máxima sobreestima la muestra.  
Puedes interactuar con los ejemplos reales para ver **cómo se calcula paso a paso**.
""")

# ------------------------------
# Parámetros globales
# ------------------------------
st.sidebar.header("Parámetros generales")
confianza = st.sidebar.selectbox("Nivel de confianza (%)", [90, 95, 99])
Z_dict = {90:1.645, 95:1.96, 99:2.576}
Z = Z_dict[confianza]

# Funciones para tamaño muestral
def n_conservador(Z, E):
    return Z**2 * 0.25 / E**2

def n_ajustada(Z, p, E):
    return Z**2 * p * (1-p) / E**2

# ------------------------------
# Ejemplo 1: Defectos graves en autos
# ------------------------------
st.header("1️⃣ Ejemplo: Defectos graves en autos")
st.markdown("""
**Introducción:** Se estima que un pequeño porcentaje de autos nuevos presenta defectos graves que requieren reparación inmediata.  
Se desea determinar cuántos autos se deben inspeccionar para estimar la proporción con un margen de error aceptable.
""")

p_auto = st.slider("Proporción esperada de defectos en autos (p)", 0.001, 0.05, 0.005, 0.001, key="auto")
E_auto = st.number_input("Error absoluto deseado (E)", min_value=0.0005, max_value=0.01, value=0.002, step=0.0005, key="auto_e")

n_auto = n_ajustada(Z, p_auto, E_auto)
n_auto_cons = n_conservador(Z, E_auto)

st.markdown(f"""
**Cálculo paso a paso:**  
- Fórmula ajustada: n = Z² * p * (1-p) / E²  
- Sustituyendo valores: n = {Z}² * {p_auto} * (1-{p_auto}) / {E_auto}²  
- Resultado: n ≈ **{math.ceil(n_auto)} autos**
""")

st.markdown(f"- Tamaño muestral conservador (p=0.5): {math.ceil(n_auto_cons)} autos")

# ------------------------------
# Ejemplo 2: Reacciones graves a vacunas
# ------------------------------
st.header("2️⃣ Ejemplo: Reacciones graves a vacunas")
st.markdown("""
**Introducción:** En estudios de seguridad de vacunas, se quiere estimar la proporción de personas que podrían presentar reacciones graves, aunque sean muy raras.
""")

p_vacuna = st.slider("Proporción esperada de reacciones graves (p)", 0.0001, 0.01, 0.001, 0.0001, key="vacuna")
E_vacuna = st.number_input("Error absoluto deseado (E)", min_value=0.0001, max_value=0.005, value=0.0005, step=0.0001, key="vac_e")

n_vacuna = n_ajustada(Z, p_vacuna, E_vacuna)
n_vacuna_cons = n_conservador(Z, E_vacuna)

st.markdown(f"""
**Cálculo paso a paso:**  
- Fórmula ajustada: n = Z² * p * (1-p) / E²  
- Sustituyendo valores: n = {Z}² * {p_vacuna} * (1-{p_vacuna}) / {E_vacuna}²  
- Resultado: n ≈ **{math.ceil(n_vacuna)} personas**
""")

st.markdown(f"- Tamaño muestral conservador (p=0.5): {math.ceil(n_vacuna_cons)} personas")

# ------------------------------
# Gráfica comparativa general
# ------------------------------
st.header("📈 Gráfica comparativa de tamaño muestral")

p_vals = np.linspace(0.001,0.999,500)
n_vals_ajustada = n_ajustada(Z, p_vals, 0.002)  # ejemplo con E=0.002
n_vals_conservadora = np.full_like(p_vals, n_conservador(Z, 0.002))

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(p_vals, n_vals_ajustada, label="Ajustado p", color='blue')
ax.axhline(y=n_conservador(Z, 0.002), color='red', linestyle='--', label="Conservador p=0.5")
ax.scatter([p_auto, p_vacuna], [n_auto, n_vacuna], color=['green','orange'], s=100, zorder=5,
           label="Eventos raros")
ax.set_xlabel("Proporción esperada p")
ax.set_ylabel("Tamaño muestral n")
ax.set_title("Comparación: Tamaño muestral ajustado vs conservador")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.markdown("""
✅ **Interpretación:**  
- La línea azul muestra el tamaño muestral usando la proporción real \(p\).  
- La línea roja discontinua muestra el tamaño muestral conservador usando p=0.5.  
- Los puntos verdes y naranjas representan los dos eventos raros interactivos, mostrando cómo cambian los tamaños muestrales según las proporciones y errores que el usuario selecciona.
""")
