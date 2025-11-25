import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io

# -------------------------------------------------------------
# Funciones matemáticas complejas
# -------------------------------------------------------------
z = sp.symbols("z")
color_map = "hsv"

def f(Z, expr):
    if expr == "sin(z)":
        return np.sin(Z)
    elif expr == "cos(z)":
        return np.cos(Z)
    elif expr == "tan(z)":
        return np.tan(Z)
    else:
        # Interpretar como expresión compleja
        try:
            sym_f = sp.lambdify(z, sp.sympify(expr), "numpy")
            return sym_f(Z)
        except:
            return np.nan + 1j*np.nan


# -------------------------------------------------------------
# Obtener ceros y polos
# -------------------------------------------------------------
def obtener_ceros_polos(expr):
    try:
        expr_sym = sp.sympify(expr)
        num, den = sp.fraction(expr_sym)

        ceros = sp.solve(sp.Eq(num, 0), z)
        polos = sp.solve(sp.Eq(den, 0), z)

        return ceros, polos
    except:
        return [], []


# -------------------------------------------------------------
# Gráfico fase
# -------------------------------------------------------------
def plot_phase(expr, N, ceros, polos):

    LIM = 6 if expr in ["sin(z)", "cos(z)", "tan(z)"] else 2

    x = np.linspace(-LIM, LIM, N)
    y = np.linspace(-LIM, LIM, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    W = f(Z, expr)
    W = np.asarray(W, dtype=np.complex128)
    W = np.where(np.isfinite(W), W, np.nan + 1j*np.nan)
    phase = np.angle(W)

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.set_dpi(100)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.imshow(phase, extent=(-LIM, LIM, -LIM, LIM), cmap=color_map, alpha=0.96)

    ax.set_xticks(np.arange(-LIM, LIM+0.01, LIM/5), minor=True)
    ax.set_yticks(np.arange(-LIM, LIM+0.01, LIM/5), minor=True)
    ax.grid(which='minor', color='#ffffff', linewidth=0.03)

    ax.set_xticks(np.arange(-LIM, LIM+0.01, LIM/2))
    ax.set_yticks(np.arange(-LIM, LIM+0.01, LIM/2))
    ax.grid(which='major', color='#f8f8f8', linewidth=0.08)

    ax.axhline(0, color='#bfbfbf', linewidth=0.6)
    ax.axvline(0, color='#bfbfbf', linewidth=0.6)

    ax.set_xlabel("Re(z)", fontsize=12)
    ax.set_ylabel("Im(z)", fontsize=12)

    for c in ceros:
        try:
            ax.scatter(float(sp.re(c)), float(sp.im(c)), color="blue", s=40)
            ax.text(float(sp.re(c))+0.15, float(sp.im(c))+0.1, "Cero", color="blue", fontsize=10)
        except:
            pass

    for p in polos:
        try:
            ax.scatter(float(sp.re(p)), float(sp.im(p)), color="red", s=40)
            ax.text(float(sp.re(p))+0.15, float(sp.im(p))+0.1, "Polo", color="red", fontsize=10)
        except:
            pass

    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    st.download_button("Descargar imagen", buf.getvalue(),
                       file_name="fase.png", mime="image/png")


# -------------------------------------------------------------
# Interfaz principal
# -------------------------------------------------------------
st.title("Graficador de Funciones Complejas")

expr = st.text_input("Función f(z):", "sin(z)")
N = st.slider("Resolución de la gráfica:", 200, 800, 400)

ceros, polos = obtener_ceros_polos(expr)

st.write("### Diagrama de Fase")
plot_phase(expr, N, ceros, polos)

# -------------------------------------------------------------
# -----------   SECCIÓN 3D COMPLETAMENTE NUEVA   --------------
# -------------------------------------------------------------
st.sidebar.write("### Opciones de gráfico 3D")
enable_3d = st.sidebar.checkbox("Mostrar gráfico 3D (|f(z)|)")

lim3d = st.sidebar.slider("Límite del plano para el 3D", 1, 10, 4)

if enable_3d:

    x3 = np.linspace(-lim3d, lim3d, 150)
    y3 = np.linspace(-lim3d, lim3d, 150)
    X3, Y3 = np.meshgrid(x3, y3)
    Z3 = X3 + 1j * Y3

    W3 = f(Z3, expr)
    W3 = np.asarray(W3, dtype=np.complex128)
    W3 = np.where(np.isfinite(W3), W3, np.nan + 1j*np.nan)
    M3 = np.abs(W3)

    fig3 = plt.figure(figsize=(7, 6))
    ax3 = fig3.add_subplot(111, projection='3d')

    surf = ax3.plot_surface(
        X3, Y3, M3,
        cmap="viridis",
        linewidth=0,
        antialiased=True,
        alpha=0.95
    )

    ax3.set_title("|f(z)| en 3D", fontsize=14)
    ax3.set_xlabel("Re(z)")
    ax3.set_ylabel("Im(z)")
    ax3.set_zlabel("|f(z)|")

    ax3.view_init(elev=30, azim=45)

    fig3.colorbar(surf, shrink=0.6)

    st.pyplot(fig3, use_container_width=True)
