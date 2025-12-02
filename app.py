# Guardar como app.py y ejecutar con: streamlit run app.py

import streamlit as st
import numpy as np
import plotly.express as px
import math

st.set_page_config(page_title="Tamaño Muestral en Eventos Raros", layout="wide")

# ------------------------------
# Título y explicación
# ------------------------------
st.title("📊 Tamaño Muestral para Proporciones en Eventos Raros")
st.markdown("""
Esta app permite entender **cómo calcular el tamaño muestral** para proporciones muy pequeñas o muy grandes, típicas de **eventos raros**.  

- La **varianza de una proporción** es \(Var(p) = p(1-p)\).  
- La **máxima varianza ocurre en \(p = 0.5\)**.  
- Para \(p<0.1\) o \(p>0.9\), se recomienda usar la **fórmula ajustada** para no sobredimensionar la muestra.  
- Puedes explorar interactivamente el efecto de la proporción esperada en el tamaño muestral.
""")

# ------------------------------
# Parámetros del usuario
# ------------------------------
st.sidebar.header("Parámetros del estudio")

# Error absoluto
E = st.sidebar.number_input("Error absoluto deseado (E)", min_value=0.0001, max_value=1.0, value=0.005, step=0.001)

# Nivel de confianza
confianza = st.sidebar.selectbox("Nivel de confianza (%)", [90, 95, 99])
Z_dict = {90:1.645, 95:1.96, 99:2.576}
Z = Z_dict[confianza]

# Slider para proporción interactiva
p_slider = st.sidebar.slider("Proporción esperada (p)", 0.001, 0.999, 0.01, 0.001)

# ------------------------------
# Fórmulas
# ------------------------------
def n_conservador(Z, E):
    """Tamaño muestral usando máxima varianza p=0.5"""
    return Z**2 * 0.25 / E**2

def n_ajustada(Z, p, E):
    """Tamaño muestral usando varianza real p(1-p)"""
    return Z**2 * p * (1-p) / E**2

# Tamaño muestral para proporción seleccionada
n_user = n_ajustada(Z, p_slider, E)
n_cons = n_conservador(Z, E)

st.subheader("📌 Resultados para la proporción seleccionada")
st.write(f"Proporción seleccionada: **{p_slider:.3f} ({p_slider*100:.2f}%)**")
st.write(f"Tamaño muestral ajustado: **{math.ceil(n_user)}**")
st.write(f"Tamaño muestral conservador (p=0.5): **{math.ceil(n_cons)}**")

# ------------------------------
# Gráfica interactiva del tamaño muestral vs p
# ------------------------------
p_vals = np.linspace(0.001,0.999,500)
n_vals_ajustada = n_ajustada(Z, p_vals, E)
n_vals_conservadora = np.full_like(p_vals, n_cons)

fig = px.line(x=p_vals, y=n_vals_ajustada, labels={"x":"Proporción esperada p", "y":"Tamaño muestral n"},
              title="Comparación: Tamaño muestral ajustado vs conservador", line_shape='spline')
fig.add_scatter(x=p_vals, y=n_vals_conservadora, mode='lines', name="Conservador (p=0.5)", line=dict(dash='dash', color='red'))
fig.add_scatter(x=[p_slider], y=[n_user], mode='markers+text', name="Proporción seleccionada",
                text=[f"n={math.ceil(n_user)}"], textposition="top right", marker=dict(size=10, color='green'))

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Ejemplos de eventos raros
# ------------------------------
st.header("🎯 Ejemplos de eventos raros")

# 1️⃣ Defectos graves en autos
p_auto = 0.005
E_auto = 0.002
n_auto = n_ajustada(Z, p_auto, E_auto)
st.subheader("1️⃣ Defectos graves en autos")
st.write(f"- Proporción esperada: {p_auto*100:.2f}%")
st.write(f"- Tamaño muestral ajustado: {math.ceil(n_auto)} autos")
st.write(f"- Tamaño muestral conservador: {math.ceil(n_conservador(Z,E_auto))} autos")

# 2️⃣ Reacciones graves a vacunas
p_vacuna = 0.001
E_vacuna = 0.0005
n_vacuna = n_ajustada(Z, p_vacuna, E_vacuna)
st.subheader("2️⃣ Reacciones graves a vacunas")
st.write(f"- Proporción esperada: {p_vacuna*100:.2f}%")
st.write(f"- Tamaño muestral ajustado: {math.ceil(n_vacuna)} personas")
st.write(f"- Tamaño muestral conservador: {math.ceil(n_conservador(Z,E_vacuna))} personas")

# ------------------------------
# Explicación final
# ------------------------------
st.markdown("""
---
✅ **Interpretación rápida para el usuario:**  
- La línea azul muestra el tamaño muestral usando la **proporción real** \(p\).  
- La línea roja discontinua muestra el tamaño muestral **conservador** usando p=0.5.  
- Para eventos raros (p muy pequeño), la línea azul está **muy por debajo** de la roja, evitando sobreestimación.  
- Puedes mover el slider para ver cómo cambia el tamaño muestral según la proporción esperada.
""")
