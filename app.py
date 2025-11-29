import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
from cmath import phase

# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================
st.set_page_config(page_title="Diagrama de Fase Complejo", layout="wide")

st.title("📈 Diagrama de fase y superficie 3D de funciones complejas")

st.markdown("""
Esta herramienta permite graficar:

- **Diagrama de fase** en el plano complejo  
- **Superficie 3D interactiva** de |f(z)|  
- **Ceros y polos** automáticamente detectados  
""")

# ============================================================
# ENTRADA DEL USUARIO
# ============================================================

entrada = st.text_input("Ingresa la función f(z):", "z**2 + 1")
activar_3d = st.checkbox("Mostrar gráfica 3D interactiva", True)

color_map = st.selectbox("Mapa de color:", ["viridis", "plasma", "inferno", "magma", "cividis"])

# ============================================================
# PROCESAMIENTO DE LA FUNCIÓN
# ============================================================

z = sp.symbols("z")
try:
    f_expr = sp.sympify(entrada)
except:
    st.error("❌ Error al interpretar la función.")
    st.stop()

# Convertir a función numérica
f = sp.lambdify(z, f_expr, "numpy")

# Detectar ceros y polos
ceros = []
polos = []

try:
    ceros = sp.solve(sp.Eq(f_expr, 0), z)
except:
    ceros = []

try:
    polos = sp.solve(sp.Eq(sp.denom(f_expr), 0), z)
except:
    polos = []

# ============================================================
# DIAGRAMA DE FASE
# ============================================================

st.subheader("🎨 Diagrama de fase")

X = np.linspace(-3, 3, 600)
Y = np.linspace(-3, 3, 600)
X, Y = np.meshgrid(X, Y)
Z = X + 1j*Y

try:
    W = f(Z)
except Exception:
    W = np.zeros_like(Z)

A = np.angle(W)

fig_phase = go.Figure(data=go.Heatmap(
    z=A,
    x=np.linspace(-3, 3, 600),
    y=np.linspace(-3, 3, 600),
    colorscale="HSV",
    colorbar=dict(title="Fase")
))

fig_phase.update_layout(
    title="Diagrama de Fase de f(z)",
    xaxis_title="Re(z)",
    yaxis_title="Im(z)",
)

st.plotly_chart(fig_phase, use_container_width=True)

# ============================================================
# ❌ SE ELIMINÓ COMPLETAMENTE LA GRÁFICA 3D DE MATPLOTLIB
# ============================================================

# **NO EXISTE MÁS ESE BLOQUE**

# ============================================================
# GRÁFICA 3D INTERACTIVA (PLOTLY)
# ============================================================

if activar_3d:
    st.subheader("🌐 Superficie 3D Interactiva de |f(z)|")

    x3 = np.linspace(-3, 3, 150)
    y3 = np.linspace(-3, 3, 150)
    X3, Y3 = np.meshgrid(x3, y3)
    Z3 = X3 + 1j * Y3

    try:
        W3 = f(Z3)
    except:
        W3 = np.zeros_like(Z3)

    A3 = np.abs(W3)

    fig3d = go.Figure(data=[go.Surface(
        x=X3,
        y=Y3,
        z=A3,
        colorscale=color_map
    )])

    fig3d.update_layout(
        title="Superficie 3D Interactiva de |f(z)|",
        scene=dict(
            xaxis_title="Re(z)",
            yaxis_title="Im(z)",
            zaxis_title="|f(z)|",
        ),
        height=700,
    )

    st.plotly_chart(fig3d, use_container_width=True)
