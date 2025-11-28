# LIBRERÍAS
# =================================================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
import io


# CONFIGURACIÓN DE PÁGINA
# =================================================================
st.set_page_config(
    page_title="Diagrama de fase",
    layout="wide"
)


# FONDO TIPO GEOGEBRA + SIDEBAR ANCHO + ICONO HOME
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

    section[data-testid="stSidebar"] {
        width: 307px !important;
    }

    .home-icon {
        width: 22px;
        cursor: pointer;
        margin-bottom: 8px;
    }
    .home-icon:hover {
        transform: scale(1.15);
    }

    .welcome-text {
        font-size: 52px;
        color: #003366;
        font-weight: 900;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        margin-top: 51px;
        text-shadow: 2px 2px 4px #bcd2ff;
    }
    </style>
""", unsafe_allow_html=True)


# TÍTULO PRINCIPAL
# =================================================================
st.markdown("""
    <style>
        .title-container {
            text-align: center;
            margin-top: -60px;
            margin-bottom: 8px;
        }
        .main-title {
            font-size: 39px;
            font-weight: 800;
            color: #1a1a1a;
            font-family: 'Segoe UI', sans-serif;
        }
        .subtitle {
            font-size: 17px;
            font-weight: 300;
            color: #444444;
            margin-top: 7px;
            font-family: 'Segoe UI', sans-serif;
        }
        .logo-title {
            display:flex;
            align-items:center;
            justify-content:center;
            gap:6px;
            margin-bottom:10px;
        }
        .logo-title img {
            width:45px;
            height:45px;
        }
        .logo-title span {
            font-size:18px;
            font-weight:700;
            color:#003366;
            font-family:'Segoe UI', sans-serif;
        }
    </style>

    <div class="title-container">
        <div class="main-title">Diagrama De Fase</div>
        <div class="subtitle">Inspirado en <i>Visual Complex Functions</i> — Wegert (2012)</div>
    </div>
""", unsafe_allow_html=True)


# SIDEBAR
# =================================================================
st.sidebar.markdown("""
<a href="/" target="_self">
    <img class="home-icon" src="https://cdn-icons-png.flaticon.com/128/54/54759.png">
</a>

<div class="logo-title">
    <img src="https://content.gnoss.ws/imagenes/Usuarios/ImagenesCKEditor/c513da9b-6419-42be-82ef-3c448a0b5a79/a65dee0c-c70f-4ce1-b363-cfc36a980918.png">
    <span>VARIABLE COMPLEJA</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h4 style='font-size:16px;'>Configuración</h4>", unsafe_allow_html=True)

# SESSION STATE
# =================================================================
if "modo" not in st.session_state:
    st.session_state.modo = "manual"
if "ultima_funcion" not in st.session_state:
    st.session_state.ultima_funcion = ""
if "input_manual" not in st.session_state:
    st.session_state.input_manual = ""

def actualizar_manual():
    st.session_state.modo = "manual"
    st.session_state.ultima_funcion = st.session_state.input_manual

entrada_manual = st.sidebar.text_input(
    "Escribe una función de z",
    value=st.session_state.input_manual,
    key="input_manual",
    on_change=actualizar_manual,
    placeholder="ejemplo z**z"
)

# SELECTOR DE FUNCIONES
# =================================================================
st.sidebar.markdown("<br><b>Elegir función </b>", unsafe_allow_html=True)

funciones_libro = {
    "Selecciona una función": "",
    "z": "z",
    "z²": "z**2",
    "z³ - 1": "z**3 - 1",
    "(z+1)(z-2)": "(z+1)*(z-2)",
    "1/z": "1/z",
    "(z³-1)/(z²+1)": "(z**3 - 1)/(z**2 + 1)",
    "exp(z)": "exp(z)",
    "exp(-2π/z)": "exp(-2*pi/z)",
    "sin(z)": "sin(z)",
    "cos(z)": "cos(z)",
    "tan(z)": "tan(z)",
    "log(z)": "log(z)",
    "√z": "sqrt(z)",
    "z^(1/3)": "z**(1/3)",
    "(z - 1)/(z + 1)": "(z - 1)/(z + 1)",
    "(z⁵ - 1)/(z² - 1)": "(z**5 - 1)/(z**2 - 1)",
    "1/(z² + 1)": "1/(z**2 + 1)",
    "(z² + z + 1)/(z² - z + 1)": "(z**2 + z + 1)/(z**2 - z + 1)"  
}

def actualizar_lista():
    st.session_state.modo = "lista"
    seleccion = funciones_libro[st.session_state.select_libro]
    if seleccion != "":
        st.session_state.ultima_funcion = seleccion
        st.session_state.input_manual = ""

st.sidebar.selectbox(
    "Seleccionar función del libro",
    list(funciones_libro.keys()),
    index=0,
    key="select_libro",
    label_visibility="collapsed",
    on_change=actualizar_lista
)

# Convertir a minúsculas
entrada = st.session_state.ultima_funcion.lower()


# OPCIONES
# =================================================================
color_map = st.sidebar.selectbox("Paleta de color", ["hsv", "twilight", "rainbow", "turbo"])
resolucion = st.sidebar.slider("Resolución del gráfico", 300, 800, 500)
activar_3d = st.sidebar.checkbox("Mostrar Gráfica 3D")


# FUNCIÓN PRINCIPAL f(z)
# =================================================================
def f(z, expr):
    try:
        z_sym = sp.Symbol('z')
        f_sym = sp.sympify(expr)
        f_lamb = sp.lambdify(z_sym, f_sym, modules=['numpy'])
        return f_lamb(z)
    except Exception as e:
        raise ValueError(f"Error al interpretar la función: {e}")


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
        tipo = f"polinómica de grado {sp.degree(f_expr)}"
    elif sp.denom(f_expr) != 1:
        tipo = "racional"
    elif "exp" in str(f_expr):
        tipo = "exponencial"
    elif "sin" in str(f_expr) or "cos" in str(f_expr):
        tipo = "trigonométrica"
    elif "log" in str(f_expr):
        tipo = "logarítmica"

    try:
        ceros = sp.solve(sp.Eq(f_expr, 0), z)
    except:
        ceros = []

    try:
        polos = sp.solve(sp.Eq(sp.denom(f_expr), 0), z)
    except:
        polos = []

    return tipo, ceros, polos


# PANTALLA INICIAL
# =================================================================
if entrada.strip() == "":
    col1, col2 = st.columns([1, 1])
    
    st.markdown("<div style='margin-top:40px'></div>", unsafe_allow_html=True)
    with col1:
        st.image(
            "https://www.software-shop.com/images/productos/maple/img2023-1.png",
            width=430 , 
        )

    with col2:
        st.markdown("<div class='welcome-text'>¡Bienvenidos!</div>", unsafe_allow_html=True)

    st.stop()

tipo, ceros, polos = analizar_funcion(entrada)

st.markdown(f"""
<div style='display:flex; gap:25px; font-size:17px; margin-top:10px;'>
    <div><b>Tipo:</b> {tipo}</div>
    <div><b>Ceros:</b> {ceros}</div>
    <div><b>Polos:</b> {polos}</div>
</div>
""", unsafe_allow_html=True)


# ===========================================================
# NUEVA SECCIÓN — EVALUAR UN PUNTO z₀
# ===========================================================
st.sidebar.markdown("<br><b>Evaluar un punto z₀</b>", unsafe_allow_html=True)

z0_input = st.sidebar.text_input("Escribe un número complejo", placeholder="Ejemplo: 1+2i")

def convertir_z(texto):
    texto = texto.replace(" ", "")
    texto = texto.replace("i", "j")
    try:
        return complex(texto)
    except:
        return None

z0 = convertir_z(z0_input)
w0 = None
color_z0 = None
arg_z0 = None

if z0 is not None:
    try:
        w0 = f(z0, entrada)
        modulo = abs(w0)
        arg_z0 = np.angle(w0)

        st.sidebar.write(f"**|f(z₀)| = {modulo:.4f}**")
        st.sidebar.write(f"**arg(f(z₀)) = {arg_z0:.4f} rad**")

        # COLOR CORRESPONDIENTE
        cmap = plt.get_cmap(color_map)
        color_z0 = cmap((arg_z0 + np.pi) / (2*np.pi))

        st.sidebar.color_picker(
            "Color correspondiente",
            value="#%02x%02x%02x" % tuple(int(c*255) for c in color_z0[:3])
        )

    except:
        st.sidebar.write("Error al evaluar f(z₀).")


# ===========================================================
# DIAGRAMA DE FASE
# ===========================================================
def plot_phase(expr, N, ceros, polos, z0=None, color_z0=None):

    LIM = 6 if expr in ["sin(z)", "cos(z)", "tan(z)"] else 2

    x = np.linspace(-LIM, LIM, N)
    y = np.linspace(-LIM, LIM, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    W = f(Z, expr)
    W = np.asarray(W, dtype=np.complex128)
    W = np.where(np.isfinite(W), W, np.nan + 1j*np.nan)
    phase = np.angle(W)

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.imshow(phase, extent=(-LIM, LIM, -LIM, LIM), cmap=color_map, alpha=0.96)

    ax.set_title(f" f(z) = {expr}", fontsize=14, pad=12)

    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")

    # Ceros
    for c in ceros:
        try:
            ax.scatter(float(sp.re(c)), float(sp.im(c)), color="blue", s=40)
            ax.text(float(sp.re(c))+0.12, float(sp.im(c))+0.08, "Cero", color="blue", fontsize=10)
        except:
            pass

    # Polos
    for p in polos:
        try:
            ax.scatter(float(sp.re(p)), float(sp.im(p)), color="red", s=40)
            ax.text(float(sp.re(p))+0.12, float(sp.im(p))+0.08, "Polo", color="red", fontsize=10)
        except:
            pass

    # ================================
    # DIBUJAR z₀ SI EXISTE
    # ================================
    if z0 is not None and color_z0 is not None:
        ax.scatter(z0.real, z0.imag, color=color_z0, s=80, edgecolor="black")
        ax.text(z0.real + 0.1, z0.imag + 0.1, "z₀", fontsize=10, color="black")

    return fig


fig_phase = plot_phase(entrada, resolucion, ceros, polos, z0=z0, color_z0=color_z0)
st.pyplot(fig_phase)

buf1 = io.BytesIO()
fig_phase.savefig(buf1, format="png", dpi=300)
st.download_button("Descargar Diagrama de Fase", buf1.getvalue(), "diagrama_fase.png", "image/png")


# ===========================================================
# GRÁFICA 3D
# ===========================================================
if activar_3d:

    LIM = 6 if entrada in ["sin(z)", "cos(z)", "tan(z)"] else 2

    x3 = np.linspace(-LIM, LIM, 150)
    y3 = np.linspace(-LIM, LIM, 150)
    X3, Y3 = np.meshgrid(x3, y3)
    Z3 = X3 + 1j * Y3

    W3 = f(Z3, entrada)
    W3 = np.asarray(W3, dtype=np.complex128)
    W3 = np.where(np.isfinite(W3), W3, np.nan + 1j*np.nan)

    A3 = np.abs(W3)

    fig3 = plt.figure(figsize=(8, 7))
    ax3 = fig3.add_subplot(111, projection="3d")

    ax3.plot_surface(X3, Y3, A3, cmap=color_map, rstride=1, cstride=1, antialiased=True, alpha=0.95)

    # Ceros
    for c in ceros:
        try:
            ax3.scatter(float(sp.re(c)), float(sp.im(c)), 0, color="blue", s=50)
        except:
            pass

    # Polos
    for p in polos:
        try:
            ax3.scatter(float(sp.re(p)), float(sp.im(p)), np.nanmax(A3), color="red", s=60)
        except:
            pass

    # ================================
    # PUNTO z₀ EN 3D
    # ================================
    if z0 is not None and w0 is not None:
        ax3.scatter(z0.real, z0.imag, abs(w0), color=color_z0, s=80, edgecolor="black")

    ax3.set_xlabel("Re(z)")
    ax3.set_ylabel("Im(z)")
    ax3.set_zlabel("|f(z)|")

    ax3.set_title("Gráfica 3D de |f(z)|")

    st.pyplot(fig3)

    buf2 = io.BytesIO()
    fig3.savefig(buf2, format="png", dpi=300)
    st.download_button("Descargar Gráfica 3D", buf2.getvalue(), "grafica_3d.png", "image/png")
