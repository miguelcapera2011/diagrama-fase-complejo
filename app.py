import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# CONFIG
st.set_page_config(page_title="Tamaño Muestral y Eventos Raros", layout="centered")

st.title("📊 Análisis de Proporciones y Eventos Raros")
st.write("Esta aplicación contiene dos módulos: cálculo de tamaño muestral y estudio de eventos raros.")

tabs = st.tabs(["📐 Tamaño Muestral", "🧪 Eventos Raros"])

# ============================================================
# =====================  TAB 1 ===============================
# ============================================================

with tabs[0]:
    st.header("📐 Cálculo de Tamaño Muestral para Proporciones Extremas")

    with st.expander("📘 ¿Por qué la varianza es máxima en p = 0.5?"):
        st.write("""
La varianza de una proporción es:
\[
Var(\hat{p}) = p(1-p)
\]
Es máxima en **p = 0.5** porque ahí el producto es mayor.
Cuando **p < 0.10** o **p > 0.90**, la varianza disminuye y el tamaño muestral real necesario también baja.
""")

    # Base de datos interna
    csv_data = """evento,ocurrencias,total
A,3,10000
B,1,8000
C,5,15000
"""

    df = pd.read_csv(StringIO(csv_data))
    st.subheader("📁 Base interna de eventos raros")
    st.dataframe(df)

    # Parámetros
    st.subheader("🔧 Parámetros")

    p = st.slider("Proporción esperada (p)", 0.001, 0.999, 0.05)
    Z = st.selectbox("Nivel de confianza (Z)", [1.64, 1.96, 2.58], index=1)
    E = st.number_input("Margen de error (E)", min_value=0.0001, max_value=0.2, value=0.02)

    # Cálculo estándar
    n_standard = (Z**2 * p * (1 - p)) / (E**2)

    # Ajuste
    if p < 0.1:
        p_adj = p + 0.5 * p
    elif p > 0.9:
        p_adj = p - 0.5 * (1 - p)
    else:
        p_adj = p

    n_adjusted = (Z**2 * p_adj * (1 - p_adj)) / (E**2)

    st.subheader("📐 Resultados")
    st.write(f"🔸 Tamaño muestral estándar: **{int(np.ceil(n_standard))}**")
    st.write(f"🔹 Tamaño muestral ajustado: **{int(np.ceil(n_adjusted))}**")

    # Gráfica varianza
    st.subheader("📉 Varianza p(1−p)")
    fig1, ax1 = plt.subplots()
    px = np.linspace(0, 1, 300)
    ax1.plot(px, px * (1 - px), linewidth=2)
    ax1.scatter([p], [p * (1 - p)], color="red", s=80)
    ax1.set_title("Varianza de una proporción")
    ax1.set_xlabel("p")
    ax1.set_ylabel("Var(p̂)=p(1−p)")
    st.pyplot(fig1)


# ============================================================
# =====================  TAB 2 ===============================
# ============================================================

with tabs[1]:
    st.header("🧪 Estudio de Eventos Raros y Tamaño Muestral")

    csv_data = """id,eventos,total
1,2,12000
2,1,15000
3,0,18000
4,4,25000
"""
    df2 = pd.read_csv(StringIO(csv_data))

    st.subheader("📁 Base de datos interna")
    st.dataframe(df2)

    df2["p_hat"] = df2["eventos"] / df2["total"]
    p_est = df2["p_hat"].mean()

    st.write(f"Estimación promedio de p = **{p_est:.6f}**")

    with st.expander("📘 ¿Qué hace esta app?"):
        st.write("""
1. Lee una base con eventos raros.
2. Calcula la proporción estimada \( \hat{p} \).
3. Usa esa estimación para calcular tamaño muestral.
4. Grafica la relación entre p y el tamaño muestral.
""")

    Z2 = st.selectbox("Nivel de confianza (Z)", [1.64, 1.96, 2.58], index=1)
    E2 = st.number_input("Margen de error (E)", 0.00001, 0.01, 0.001)

    n2 = (Z2**2 * p_est * (1 - p_est)) / (E2**2)

    st.subheader("📐 Tamaño muestral requerido")
    st.write(f"🔸 Tamaño muestral estimado: **{int(np.ceil(n2))}**")

    # Gráfica
    fig2, ax2 = plt.subplots()
    p_values = np.linspace(0.00001, 0.05, 200)
    n_values = (Z2**2 * p_values * (1 - p_values)) / (E2**2)

    ax2.plot(p_values, n_values, linewidth=2)
    ax2.scatter([p_est], [n2], color="red", s=80)
    ax2.set_title("Tamaño muestral vs proporción")
    ax2.set_xlabel("p")
    ax2.set_ylabel("n requerido")
    st.pyplot(fig2)
