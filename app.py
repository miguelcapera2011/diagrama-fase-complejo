import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from mpl_toolkits.mplot3d import Axes3D
import io

st.set_page_config(layout="wide", page_title="Analizador Complejo")

# ------------------------------
# Función general para evaluar
# ------------------------------
def f(z, expresion):
    try:
        z_sym = sp.symbols("z")
        expr = sp.sympify(expresion)
        f_lamb = sp.lambdify(z_sym, expr, "numpy")
        return f_lamb(z)
    except:
        return np.nan


# ------------------------------
# Analizar ceros, polos, tipo
# ------------------------------
def analizar_funcion(expr):
    z = sp.symbols("z")
    try:
        expr_sym = sp.sympify(expr)
        num, den = sp.fraction(expr_sym)
        ceros = sp.solve(num, z)
        polos = sp.solve(den, z)
        tipo = "Racional" if den != 1 else "Polinómica"
        return tipo, ceros, polos
    except:
        return "Desconocido", [], []


# ------------------------------
# Fase
# ------------------------------
def plot_phase(expr, resolucion, ceros, polos):
    x = np.linspace(-5, 5, resolucion)
    y = np.linspace(-5, 5, resolucion)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    W = f(Z, expr)
    W = np.asarray(W, dtype=np.complex128)
    W = np.where(np.isfinite(W), W, np.nan + 1j*np.nan)

    phase = np.angle(W)

    fig, ax = plt.subplots(figsize=(6, 6))
    c = ax.imshow(phase, extent=[-5, 5, -5, 5], origin="lower", cmap="twilight")
    fig.colorbar(c)
    ax.set_title("Mapa de Fase Arg(f(z))")

    # Marcar ceros y polos
    for c0 in ceros:
        if c0.is_real:
            ax.plot(float(c0), 0, "go", markersize=8)
        else:
            ax.plot(float(sp.re(c0)), float(sp.im(c0)), "go", markersize=8)

    for p0 in polos:
        if p0.is_real:
            ax.plot(float(p0), 0, "rx", markersize=8)
        else:
            ax.plot(float(sp.re(p0)), float(sp.im(p0)), "rx", markersize=8)

    return fig


# ------------------------------
# Interfaz
# ------------------------------
st.markdown("<h2 style='text-align:center;'>Analizador de Funciones Complejas</h2>", unsafe_allow_html=True)

entrada = st.text_input("Ingresa f(z):", "z**2 + 1")
resolucion = st.slider("Resolución del Mapa de Fase", 50, 500, 250)

tipo, ceros, polos = analizar_funcion(entrada)

st.write("**Tipo:**", tipo)
st.write("**Ceros:**", ceros)
st.write("**Polos:**", polos)

# ------------------------------
# Mostrar diagrama de fase
# ------------------------------
fig_fase = plot_phase(entrada, resolucion, ceros, polos)
st.pyplot(fig_fase)

# ------------------------------
# Botón DESCARGAR
# ------------------------------
buffer = io.BytesIO()
canvas = FigureCanvasAgg(fig_fase)
canvas.print_png(buffer)

st.download_button(
    label="Descargar diagrama",
    data=buffer.getvalue(),
    file_name="diagrama_fase.png",
    mime="image/png"
)

# ------------------------------
# GRÁFICO 3D
# ------------------------------
st.markdown("---")
st.markdown("### Gráfico 3D de |f(z)|")

activar_3d = st.checkbox("Mostrar gráfica 3D")
lim3d = st.slider("Límite del plano 3D", 2, 12, 5)

if activar_3d:
    x3 = np.linspace(-lim3d, lim3d, 120)
    y3 = np.linspace(-lim3d, lim3d, 120)
    X3, Y3 = np.meshgrid(x3, y3)
    Z3 = X3 + 1j * Y3

    W3 = f(Z3, entrada)
    W3 = np.asarray(W3, dtype=np.complex128)
    W3 = np.where(np.isfinite(W3), W3, np.nan + 1j*np.nan)

    A3 = np.abs(W3)

    fig3 = plt.figure(figsize=(7, 6))
    ax3 = fig3.add_subplot(111, projection="3d")

    superficie = ax3.plot_surface(
        X3, Y3, A3,
        cmap="viridis",
        rstride=1,
        cstride=1,
        linewidth=0,
        antialiased=True,
        alpha=0.95
    )

    ax3.set_title("|f(z)| en 3D (movible)")
    ax3.set_xlabel("Re(z)")
    ax3.set_ylabel("Im(z)")
    ax3.set_zlabel("|f(z)|")
    fig3.colorbar(superficie, shrink=0.6)

    st.pyplot(fig3)
