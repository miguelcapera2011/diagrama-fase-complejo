# =================================================================
# LIBRERIAS INSTALADAS
# =================================================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import io
import mpmath  # Para la función zeta de Riemann

# =================================================================
# CONFIGURACIÓN DE PÁGINA
# =================================================================
st.set_page_config(
    page_title="Diagrama de fase",
    layout="wide"
)

# =================================================================
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
        font-size: 55px;
        color: #003366;
        font-weight: 900;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        margin-top: 110px;
        text-shadow: 2px 2px 4px #bcd2ff;
    }
    input::placeholder {
        color: #cccccc;
        opacity: 0.4;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# TÍTULO PRINCIPAL
# =================================================================
st.markdown("""
    <style>
        .title-container {text-align: center; margin-top: -60px; margin-bottom: 8px;}
        .main-title {font-size: 38px; font-weight: 800; color: #1a1a1a; font-family: 'Segoe UI', sans-serif;}
        .subtitle {font-size: 20px; font-weight: 300; color: #444444; margin-top: 10px; font-family: 'Segoe UI', sans-serif;}
        .logo-title {display:flex; align-items:center; justify-content:center; gap:6px; margin-bottom:10px;}
        .logo-title img {width:45px; height:45px;}
        .logo-title span {font-size:18px; font-weight:700; color:#003366; font-family:'Segoe UI', sans-serif;}
    </style>
    <div class="title-container">
        <div class="main-title">Diagrama De Fase</div>
        <div class="subtitle">Inspirado en <i>Visual Complex Functions</i> — Wegert (2012)</div>
    </div>
""", unsafe_allow_html=True)

# =================================================================
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
<h4 style='font-size:16px;'>Configuración</h4>
""", unsafe_allow_html=True)

# Estado inicial
if "modo" not in st.session_state:
    st.session_state.modo = "manual"
if "ultima_funcion" not in st.session_state:
    st.session_state.ultima_funcion = ""

def actualizar_manual():
    st.session_state.modo = "manual"
    st.session_state.ultima_funcion = st.session_state.input_manual

entrada_manual = st.sidebar.text_input(
    "Escribe una función de z",
    st.session_state.ultima_funcion,
    key="input_manual",
    on_change=actualizar_manual,
    placeholder="ejemplo z**z"
)

# =================================================================
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
    "zeta de Riemann": "zeta(z)"  # <-- Función de Riemann
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

entrada = st.session_state.ultima_funcion

# =================================================================
# OPCIONES
# =================================================================
color_map = st.sidebar.selectbox("Paleta de color", ["hsv", "twilight", "rainbow", "turbo"])
resolucion = st.sidebar.slider("Resolución del gráfico", 300, 800, 500)

# =================================================================
# FIRMA
# =================================================================
st.sidebar.markdown("""
<style>
.autor-sidebar {font-size: 14px; color: #003366; font-weight: 600; font-family: 'Segoe UI', sans-serif; margin-top: 15px; padding-top: 10px; border-top: 1px solid #cccccc; opacity: 0.85;}
.autor-sidebar:hover {opacity: 1;}
</style>
<div class="autor-sidebar">Autor: Miguel Ángel Capera</div>
""", unsafe_allow_html=True)

# =================================================================
# FUNCIÓN PRINCIPAL
# =================================================================
def f(z, expr):
    z_sym = sp.Symbol('z')
    f_sym = sp.sympify(expr)
    if "zeta" in str(f_sym):
        f_lamb = sp.lambdify(z_sym, f_sym, modules=[{"zeta": mpmath.zeta}, "numpy"])
    else:
        f_lamb = sp.lambdify(z_sym, f_sym, modules=['numpy'])
    return f_lamb(z)

# =================================================================
# PLOTEAR FASE + CEROS Y POLOS
# =================================================================
def plot_phase(expr, N, ceros, polos):
    LIM = 6 if expr in ["sin(z)", "cos(z)", "tan(z)"] else 2
    x = np.linspace(-LIM, LIM, N)
    y = np.linspace(-LIM, LIM, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j*Y

    W = f(Z, expr)
    W = np.asarray(W, dtype=np.complex128)
    W = np.where(np.isfinite(W), W, np.nan + 1j*np.nan)
    phase = np.angle(W)

    fig, ax = plt.subplots(figsize=(8, 8))
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
            ax.text(float(sp.re(c))+0.15, float(sp.im(c))+0.1, f"{sp.pretty(c)}", color="blue", fontsize=10)
        except: pass

    for p in polos:
        try:
            ax.scatter(float(sp.re(p)), float(sp.im(p)), color="red", s=40)
            ax.text(float(sp.re(p))+0.15, float(sp.im(p))+0.1, f"{sp.pretty(p)}", color="red", fontsize=10)
        except: pass

    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    st.download_button("Descargar imagen", buf.getvalue(), file_name="fase.png", mime="image/png")

# =================================================================
# ANALIZAR
# =================================================================
def analizar_funcion(expr):
    if expr.strip() == "": return "sin función", [], []
    z = sp.Symbol('z')
    try:
        f_expr = sp.sympify(expr)
    except:
        return "inválida", [], []

    tipo = "desconocida"
    if f_expr.is_polynomial(): tipo = f"polinómica de grado {sp.degree(f_expr)}"
    elif sp.denom(f_expr) != 1: tipo = "racional"
    elif "exp" in str(f_expr): tipo = "exponencial"
    elif "sin" in str(f_expr) or "cos" in str(f_expr): tipo = "trigonométrica"
    elif "log" in str(f_expr): tipo = "logarítmica"

    try: ceros = sp.solve(sp.Eq(f_expr, 0), z)
    except: ceros = []
    try: polos = sp.solve(sp.Eq(sp.denom(f_expr), 0), z)
    except: polos = []

    return tipo, ceros, polos

# =================================================================
# MOSTRAR WELCOME
# =================================================================
if entrada.strip() == "":
    col1, col2 = st.columns([1,1])
    with col1:
        st.image("https://www.software-shop.com/images/productos/maple/img2023-1.png", width=430)
    with col2:
        st.markdown("<div class='welcome-text'>¡Bienvenidos!</div>", unsafe_allow_html=True)
    st.stop()

tipo, ceros, polos = analizar_funcion(entrada)

# Mostrar tipo, ceros y polos en notación matemática horizontal
st.markdown(f"""
<div style='display:flex; gap:25px; font-size:17px; margin-top:10px;'>
    <div><b>Tipo:</b> {tipo}</div>
    <div><b>Ceros:</b> {" , ".join([sp.pretty(c) for c in ceros])}</div>
    <div><b>Polos:</b> {" , ".join([sp.pretty(p) for p in polos])}</div>
</div>
""", unsafe_allow_html=True)

plot_phase(entrada, resolucion, ceros, polos)
