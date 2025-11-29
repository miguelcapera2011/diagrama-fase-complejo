# LIBRERÍAS
# =================================================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
import io
import plotly.graph_objects as go


# CONFIGURACIÓN DE PÁGINA
# =================================================================
st.set_page_config(
    page_title="Diagrama de fase",
    layout="wide",
)

st.title("Diagrama de fase de funciones complejas")

# ENTRADA DE FUNCIÓN
# =================================================================
entrada = st.text_input("Ingrese la función f(z):", "z**2 + 1")

# PARÁMETROS
# =================================================================
resolucion = st.slider("Resolución", 100, 600, 300)
color_map = st.selectbox("Mapa de color", ["plasma", "viridis", "inferno", "magma", "cividis"])
activar_3d = st.checkbox("Activar gráfica 3D interactiva", True)

# VARIABLES COMPLEJAS
# =================================================================
x = np.linspace(-3, 3, resolucion)
y = np.linspace(-3, 3, resolucion)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

z = sp.symbols('z')
try:
    f_expr = sp.sympify(entrada)
except:
    st.error("Error al interpretar la función.")
    st.stop()


def f(z_values, expression):
    f_lambd = sp.lambdify(z, expression, 'numpy')
    return f_lambd(z_values)


# CÁLCULO DEL DIAGRAMA DE FASE
# =================================================================
W = f(Z, f_expr)
phase = np.angle(W)

plt.figure(figsize=(7, 6))
plt.imshow(phase, extent=[-3, 3, -3, 3], cmap=color_map)
plt.title("Diagrama de fase", fontsize=20, color="#4A4A4A")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.colorbar(label="Fase")

buf = io.BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)

st.image(buf, caption="Diagrama de fase", use_container_width=True)
plt.close()


# CÁLCULO DE CEROS Y POLOS
# =================================================================
try:
    ceros = sp.nroots(f_expr)
except:
    ceros = []

try:
    numerador, denominador = sp.fraction(f_expr)
    polos = sp.nroots(denominador) if denominador != 1 else []
except:
    polos = []


# =================================================================
# 🔥 GRÁFICA 3D INTERACTIVA (ÚNICA 3D, SIN MATPLOTLIB)
# =================================================================

if activar_3d:

    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)

    LIM = 6 if entrada in ["sin(z)", "cos(z)", "tan(z)"] else 2

    x3 = np.linspace(-LIM, LIM, 150)
    y3 = np.linspace(-LIM, LIM, 150)
    X3, Y3 = np.meshgrid(x3, y3)
    Z3 = X3 + 1j * Y3

    W3 = f(Z3, f_expr)
    W3 = np.asarray(W3, dtype=np.complex128)
    W3 = np.where(np.isfinite(W3), W3, np.nan + 1j*np.nan)

    A3 = np.abs(W3)

    fig_int = go.Figure()

    # SUPERFICIE
    fig_int.add_trace(go.Surface(
        x=X3,
        y=Y3,
        z=A3,
        colorscale=color_map,
        opacity=0.96,
        showscale=False
    ))

    # CEROS AZULES
    for c in ceros:
        try:
            fig_int.add_trace(go.Scatter3d(
                x=[float(sp.re(c))],
                y=[float(sp.im(c))],
                z=[0],
                mode='markers',
                marker=dict(size=6, color='blue'),
                name="Cero"
            ))
        except:
            pass

    # POLOS ROJOS
    for p in polos:
        try:
            fig_int.add_trace(go.Scatter3d(
                x=[float(sp.re(p))],
                y=[float(sp.im(p))],
                z=[np.nanmax(A3)],
                mode='markers',
                marker=dict(size=7, color='red'),
                name="Polo"
            ))
        except:
            pass

    # -------------------------------------------------------------
    #TÍTULO ESTILO IDÉNTICO AL PRIMERO
    # -------------------------------------------------------------
    fig_int.update_layout(
        title=dict(
            text="Gráfica 3D Interactiva |f(z)|",
            font=dict(
                size=20,         # Igual al título del diagrama de fase
                color="#4A4A4A"  # Mismo color gris
            ),
            x=0.5
        ),
        autosize=True,
        height=800,
        scene=dict(
            xaxis_title="Re(z)",
            yaxis_title="Im(z)",
            zaxis_title="|f(z)|",
            camera=dict(eye=dict(x=2, y=2, z=1.5))
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig_int, use_container_width=True)
