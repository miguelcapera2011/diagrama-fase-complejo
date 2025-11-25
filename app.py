# =================================================================
# LIBRERIAS
# =================================================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import io
from mpl_toolkits.mplot3d import Axes3D

# =================================================================
# CONFIGURACIÓN DE PÁGINA
# =================================================================
st.set_page_config(
    page_title="Diagrama de fase",
    layout="wide"
)

# =================================================================
# FONDO TIPO GEOGEBRA + SIDEBAR + ESTILOS
# =================================================================
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        background-image:
            linear-gradient(#e5e5e5 1px, transparent 1px),
            linear-gradient(90deg, #e5e5e5 1px, transparent 1px);
        background-size: 25px 25px;
    }

    .welcome-text {
        font-size: 52px;
        color: #003366;
        font-weight: 900;
        text-align: center;
        margin-top: 110px;
        text-shadow: 2px 2px 4px #bcd2ff;
    }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# TÍTULO
# =================================================================
st.markdown("""
<div style='text-align:center; margin-top:-40px;'>
    <h1 style='font-size:38px; font-weight:800;'>Diagrama De Fase</h1>
    <p style='font-size:20px;'>Inspirado en <i>Visual Complex Functions</i> — Wegert (2012)</p>
</div>
""", unsafe_allow_html=True)

# =================================================================
# SIDEBAR — INGRESO DE FUNCIÓN
# =================================================================
st.sidebar.markdown("### Configuración de función")

if "ultima_funcion" not in st.session_state:
    st.session_state.ultima_funcion = ""

def actualizar_manual():
    st.session_state.ultima_funcion = st.session_state.input_manual

entrada_manual = st.sidebar.text_input(
    "Escribe una función de z",
    st.session_state.ultima_funcion,
    key="input_manual",
    on_change=actualizar_manual,
    placeholder="ejemplo z**3 - 1"
)

funciones_libro = {
    "Selecciona una función": "",
    "z": "z",
    "z²": "z**2",
    "z³ - 1": "z**3 - 1",
    "1/z": "1/z",
    "(z³-1)/(z²+1)": "(z**3 - 1)/(z**2 + 1)",
    "exp(z)": "exp(z)",
    "sin(z)": "sin(z)",
    "cos(z)": "cos(z)",
    "tan(z)": "tan(z)",
    "log(z)": "log(z)",
    "√z": "sqrt(z)"
}

def actualizar_lista():
    seleccion = funciones_libro[st.session_state.select_libro]
    if seleccion != "":
        st.session_state.ultima_funcion = seleccion
        st.session_state.input_manual = ""

st.sidebar.selectbox(
    "Función del libro",
    list(funciones_libro.keys()),
    key="select_libro",
    on_change=actualizar_lista
)

entrada = st.session_state.ultima_funcion

# =================================================================
# OPCIONES AVANZADAS — ZOOM + LIM + 3D
# =================================================================
st.sidebar.markdown("### Opciones del plano complejo")

LIM = st.sidebar.slider("Tamaño del plano (Zoom)", 1.0, 10.0, 3.0, 0.5)
resolucion = st.sidebar.slider("Resolución del gráfico", 200, 900, 500)
color_map = st.sidebar.selectbox("Paleta de color", ["hsv", "turbo", "twilight", "rainbow"])

modo_3D = st.sidebar.checkbox("Mostrar gráfico 3D de |f(z)|")

# =================================================================
# FUNCIÓN PRINCIPAL
# =================================================================
def f(z, expr):
    z_sym = sp.Symbol('z')
    try:
        f_expr = sp.sympify(expr)
        f_lamb = sp.lambdify(z_sym, f_expr, 'numpy')
        return f_lamb(z)
    except:
        return np.nan

# =================================================================
# ANALIZAR FUNCIÓN
# =================================================================
def analizar_funcion(expr):
    if expr.strip() == "":
        return "sin función", [], []
    z = sp.Symbol('z')
    try:
        f_expr = sp.sympify(expr)
    except:
        return "inválida", [], []

    tipo = "desconocida"
    if f_expr.is_polynomial():
        tipo = f"polinómica grado {sp.degree(f_expr)}"
    elif sp.denom(f_expr) != 1:
        tipo = "racional"
    elif "exp" in str(f_expr):
        tipo = "exponencial"

    try:
        ceros = sp.solve(sp.Eq(f_expr, 0), z)
    except:
        ceros = []

    try:
        polos = sp.solve(sp.Eq(sp.denom(f_expr), 0), z)
    except:
        polos = []

    return tipo, ceros, polos

# =================================================================
# GRAFICAR FASE (2D)
# =================================================================
def plot_phase(expr, N, ceros, polos, LIM):

    x = np.linspace(-LIM, LIM, N)
    y = np.linspace(-LIM, LIM, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j*Y

    W = f(Z, expr)
    W = np.where(np.isfinite(W), W, np.nan)
    phase = np.angle(W)

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.set_dpi(100)

    ax.imshow(phase, extent=(-LIM, LIM, -LIM, LIM), cmap=color_map)

    ax.set_xlabel("Re(z)", fontsize=12)
    ax.set_ylabel("Im(z)", fontsize=12)

    for c in ceros:
        ax.scatter(float(sp.re(c)), float(sp.im(c)), color="blue", s=40)

    for p in polos:
        ax.scatter(float(sp.re(p)), float(sp.im(p)), color="red", s=40)

    st.pyplot(fig, use_container_width=True)

# =================================================================
# GRAFICAR MODO 3D |f(z)|
# =================================================================
def plot_3D(expr, N, LIM):

    x = np.linspace(-LIM, LIM, N)
    y = np.linspace(-LIM, LIM, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j*Y

    W = f(Z, expr)
    M = np.abs(W)

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, M, rstride=1, cstride=1, cmap='viridis', linewidth=0)

    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    ax.set_zlabel("|f(z)|")

    st.pyplot(fig, use_container_width=True)

# =================================================================
# SI NO HAY FUNCIÓN MOSTRAR MENSAJE
# =================================================================
if entrada.strip() == "":
    st.markdown("<div class='welcome-text'>¡Bienvenido!</div>", unsafe_allow_html=True)
    st.stop()

# =================================================================
# MOSTRAR TIPO, CEROS, POLOS
# =================================================================
tipo, ceros, polos = analizar_funcion(entrada)

st.markdown(f"""
### Detalles de la función  
**Tipo:** {tipo}  
**Ceros:** {ceros}  
**Polos:** {polos}
""")

# =================================================================
# GRAFICAR
# =================================================================
plot_phase(entrada, resolucion, ceros, polos, LIM)

if modo_3D:
    st.markdown("### Gráfico 3D de |f(z)|")
    plot_3D(entrada, 200, LIM)
