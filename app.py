import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ========================================
# CONFIGURACIÓN
# ========================================
st.title("📊 Ejemplos de Tamaño Muestral para Eventos Raros")
st.write("Interactúa con los valores para ver cómo cambian las fórmulas, los ajustes y la gráfica en tiempo real.")

st.sidebar.header("🔧 Parámetros interactivos")

# Parámetros globales
Z = st.sidebar.number_input("Valor Z (confianza)", value=1.96, min_value=1.0, max_value=3.0, step=0.01)
E = st.sidebar.number_input("Error permitido (E)", value=0.01, min_value=0.0001, max_value=0.20, step=0.001)

# Elegir ejemplo
ejemplo = st.sidebar.selectbox(
    "Selecciona el ejemplo",
    ("Ejemplo 1: Enfermedad Rara (p = 0.008)", "Ejemplo 2: Falla Química Extrema (p = 0.002)")
)

# Asignar p según ejemplo
if ejemplo == "Ejemplo 1: Enfermedad Rara (p = 0.008)":
    p_default = 0.008
else:
    p_default = 0.002

p = st.sidebar.number_input("Proporción esperada (p)", value=p_default, min_value=0.0001, max_value=0.9999, step=0.0001)

# ========================================
# FUNCIONES
# ========================================
def n_clasico(E, Z):
    return (Z**2 * 0.25) / (E**2)

def n_ajustado(p, E, Z):
    return (Z**2 * p * (1 - p)) / (E**2)

def n_aprox(p, E, Z):
    return (Z**2 * p) / (E**2)

# Cálculos
n1 = n_clasico(E, Z)
n2 = n_ajustado(p, E, Z)
n3 = n_aprox(p, E, Z)

# ========================================
# MOSTRAR RESULTADOS
# ========================================

st.header("📌 Resultados del Cálculo")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tamaño clásico (p=0.5)", f"{n1:,.0f}")

with col2:
    st.metric("Ajuste usando p real", f"{n2:,.0f}")

with col3:
    st.metric("Ecuación alternativa (p≈p(1-p))", f"{n3:,.0f}")

# Mensajes dinámicos según relación
st.subheader("📢 Interpretación dinámica")

if p < 0.10:
    st.info("✔ Detectado evento raro (p < 0.10). Se requieren ajustes especiales para evitar sobreestimar la muestra.")
else:
    st.warning("⚠ p no es muy pequeña. El ajuste es menor y el método clásico puede ser suficiente.")

if n1 > n2 * 10:
    st.success("🎉 Con el ajuste se redujo la muestra más de 10 veces. ¡Gran ahorro de recursos!")
elif n1 > n2 * 3:
    st.success("✔ El ajuste reduce la muestra entre 3 y 10 veces.")
else:
    st.info("El ajuste reduce ligeramente la muestra.")

# ========================================
# GRAFICA QUE CAMBIA EN TIEMPO REAL
# ========================================
st.header("📉 Varianza vs Proporción (p)")

p_vals = np.linspace(0.0001, 0.9999, 300)
variance_vals = p_vals * (1 - p_vals)

fig, ax = plt.subplots()
ax.plot(p_vals, variance_vals)
ax.axvline(p, color='red')
ax.set_title("Varianza de p(1-p) según el valor de p")
ax.set_xlabel("p")
ax.set_ylabel("Varianza p(1-p)")

st.pyplot(fig)

# ========================================
# EXPLICACIÓN DEL EJEMPLO ELEGIDO
# ========================================
st.header("📘 Explicación del Ejemplo Seleccionado")

if ejemplo == "Ejemplo 1: Enfermedad Rara (p = 0.008)":
    st.write("""
### 🦠 Ejemplo 1 — Enfermedad Rara (TB-MDR)

- Proporción real del evento: **0.008 (0.8%)**  
- Este es un evento raro y la varianza es muy baja.  
- Usar p = 0.5 daría una muestra exageradamente grande.  

**Lo que se observa arriba en tiempo real:**

- El tamaño muestral clásico siempre será muy grande, porque la varianza máxima ocurre en **p = 0.5**.  
- El ajuste usando la p real reduce drásticamente la muestra.  
- La ecuación alternativa p≈p(1–p) produce un valor muy cercano al ajuste real.  
""")

else:
    st.write("""
### ⚗️ Ejemplo 2 — Falla Química Extrema (0.2%)

- Proporción real del evento: **0.002 (0.2%)**
- Es un evento extremadamente raro.  
- Usar p = 0.5 produciría una muestra imposible de recolectar.  

**Lo que se observa arriba en tiempo real:**

- El tamaño muestral clásico crece muchísimo porque asume varianza máxima.  
- Con el ajuste, la muestra se reduce más de 100 veces.  
- La aproximación p≈p(1–p) funciona muy bien para eventos raros.  
""")

st.success("La aplicación te muestra cómo los ajustes evitan sobreestimar la muestra y por qué es esencial usar la p real en eventos raros.")
