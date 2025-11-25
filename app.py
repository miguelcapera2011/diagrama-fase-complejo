# =================================================================
# APP: Diagrama de fase avanzado (fase + módulo + contours + animación)
# =================================================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import io
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# =================================================================
# CONFIG
# =================================================================
st.set_page_config(page_title="Diagrama de fase avanzado", layout="wide")

# =================================================================
# CSS básico
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
    .welcome-text { font-size:48px; color:#003366; text-align:center; margin-top:80px; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# SIDEBAR: entradas y opciones
# =================================================================
st.sidebar.title("Configuración")

if "ultima_funcion" not in st.session_state:
    st.session_state.ultima_funcion = ""

def actualizar_manual():
    st.session_state.ultima_funcion = st.session_state.input_manual

entrada_manual = st.sidebar.text_input(
    "Escribe una función de z",
    st.session_state.ultima_funcion,
    key="input_manual",
    on_change=actualizar_manual,
    placeholder="ejemplo: (z**3 - 1)/(z**2 + 1)"
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
    "sqrt(z)": "sqrt(z)"
}

def actualizar_lista():
    sel = funciones_libro.get(st.session_state.select_libro, "")
    if sel != "":
        st.session_state.ultima_funcion = sel
        st.session_state.input_manual = ""

st.sidebar.selectbox("Función del libro", list(funciones_libro.keys()),
                     key="select_libro", on_change=actualizar_lista)

entrada = st.session_state.ultima_funcion

st.sidebar.markdown("---")
LIM = st.sidebar.slider("Tamaño del plano (LIM)", 1.0, 10.0, 3.0, 0.5)
resolucion = st.sidebar.slider("Resolución (N)", 200, 900, 500)
color_map = st.sidebar.selectbox("Paleta de color", ["hsv", "turbo", "twilight", "rainbow"])
modo_3D = st.sidebar.checkbox("Mostrar 3D (|f(z)|)", value=False)
mostrar_contours = st.sidebar.checkbox("Mostrar líneas de nivel (contours) sobre |f(z)|", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### Animación (rotación)")
enable_animation = st.sidebar.checkbox("Usar control de animación (phi)", value=False)
phi = 0.0
if enable_animation:
    # slider para controlar la rotación (animación manual)
    phi = st.sidebar.slider("phi (radianes)", 0.0, 2*np.pi, 0.0, step=0.01)

# =================================================================
# UTIL: evaluar función segura
# =================================================================
def safe_sympy_sympify(expr_text):
    try:
        z = sp.Symbol('z')
        f_expr = sp.sympify(expr_text)
        return f_expr
    except Exception:
        return None

def f_eval(Z, expr_text, phi=0.0):
    """Evalúa f en el array Z. Aplica rotación z -> z*exp(i phi) si phi != 0"""
    try:
        z_sym = sp.Symbol('z')
        f_sym = sp.sympify(expr_text)
        f_lamb = sp.lambdify(z_sym, f_sym, modules=['numpy'])
    except Exception:
        # error: devolver NaN array del mismo shape
        return np.full_like(Z, np.nan, dtype=np.complex128)

    if phi != 0.0:
        Z = Z * np.exp(1j * phi)
    # ejecutar
    try:
        W = f_lamb(Z)
        W = np.asarray(W, dtype=np.complex128)
        W = np.where(np.isfinite(W), W, np.nan + 1j*np.nan)
        return W
    except Exception:
        return np.full_like(Z, np.nan, dtype=np.complex128)

# =================================================================
# DETECCIÓN DE CEROS Y POLOS (con multiplicidad aproximada)
# =================================================================
def detect_zeros_poles(expr_text):
    """
    Devuelve listas de (root, multiplicidad) aproximadas para ceros y polos.
    Intentamos usar nroots y agrupar raíces repetidas.
    """
    z = sp.Symbol('z')
    try:
        f_sym = sp.sympify(expr_text)
    except Exception:
        return [], []

    # obtener numerador y denominador simbólicos
    try:
        f_simpl = sp.together(f_sym)  # poner en forma num/den
        num, den = sp.together(f_simpl).as_numer_denom()
    except Exception:
        num, den = f_sym, sp.Integer(1)

    zeros = []
    poles = []
    # funciones para obtener raíces numéricas y agrupar con tolerancia
    def group_roots(nroots_list, tol=1e-6):
        grouped = []
        used = [False]*len(nroots_list)
        for i, r in enumerate(nroots_list):
            if used[i]:
                continue
            count = 1
            ri = complex(r)
            used[i] = True
            for j in range(i+1, len(nroots_list)):
                if used[j]:
                    continue
                rj = complex(nroots_list[j])
                if abs(ri - rj) < tol:
                    count += 1
                    used[j] = True
            grouped.append((ri, count))
        return grouped

    # num roots
    try:
        nroots_num = sp.nroots(num)
        zeros = group_roots(nroots_num, tol=1e-7)
    except Exception:
        zeros = []

    # den roots
    try:
        nroots_den = sp.nroots(den)
        poles = group_roots(nroots_den, tol=1e-7)
    except Exception:
        poles = []

    # convertir a forma de sympy (aprox)
    zeros_sym = [(complex(r), int(m)) for r, m in zeros]
    poles_sym = [(complex(r), int(m)) for r, m in poles]

    return zeros_sym, poles_sym

# =================================================================
# FUNCIONES DE GRAFIADO
# =================================================================
def plot_phase_ax(ax, phase, LIM, cmap):
    ax.imshow(phase, extent=(-LIM, LIM, -LIM, LIM), cmap=cmap, origin='lower', aspect='equal')
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")

def plot_magnitude_ax(ax, M, X, Y, LIM, show_contours):
    im = ax.imshow(M, extent=(-LIM, LIM, -LIM, LIM), origin='lower', aspect='equal')
    if show_contours:
        # contours sobre la malla (usamos 8 niveles automáticos)
        try:
            cs = ax.contour(X, Y, M, levels=8, linewidths=0.7)
            ax.clabel(cs, inline=True, fontsize=8)
        except Exception:
            pass
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    return im

def plot_phase_and_magnitude(expr_text, N, LIM, cmap, phi, show_contours, zeros, poles):
    x = np.linspace(-LIM, LIM, N)
    y = np.linspace(-LIM, LIM, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j*Y

    W = f_eval(Z, expr_text, phi=phi)
    phase = np.angle(W)
    M = np.abs(W)

    # crear figura con 2 columnas
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
    ax1, ax2 = axes

    plot_phase_ax(ax1, phase, LIM, cmap)
    im = plot_magnitude_ax(ax2, M, X, Y, LIM, show_contours)

    # marcar ceros y polos (con multiplicidad)
    for (r_complex, mult) in zeros:
        try:
            rx, ry = r_complex.real, r_complex.imag
            ax1.scatter(rx, ry, s=50, marker='o', facecolors='none', edgecolors='blue', linewidths=1.5)
            ax2.scatter(rx, ry, s=50, marker='o', facecolors='none', edgecolors='blue', linewidths=1.5)
            ax1.text(rx+0.08*LIM, ry+0.06*LIM, f"0 (m={mult})", color='blue', fontsize=9)
            ax2.text(rx+0.08*LIM, ry+0.06*LIM, f"0 (m={mult})", color='blue', fontsize=9)
        except Exception:
            pass

    for (r_complex, mult) in poles:
        try:
            rx, ry = r_complex.real, r_complex.imag
            ax1.scatter(rx, ry, s=50, marker='x', color='red', linewidths=1.5)
            ax2.scatter(rx, ry, s=50, marker='x', color='red', linewidths=1.5)
            ax1.text(rx+0.08*LIM, ry+0.06*LIM, f"p (m={mult})", color='red', fontsize=9)
            ax2.text(rx+0.08*LIM, ry+0.06*LIM, f"p (m={mult})", color='red', fontsize=9)
        except Exception:
            pass

    return fig, im

def plot_3D_surface(expr_text, N, LIM, phi):
    x = np.linspace(-LIM, LIM, N)
    y = np.linspace(-LIM, LIM, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j*Y
    W = f_eval(Z, expr_text, phi=phi)
    M = np.abs(W)
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    # Para no saturar y tener buena visual, limitamos valores extremos al percentil 99
    # (esto evita picos infinitos que rompan la visual)
    vmax = np.nanpercentile(M[np.isfinite(M)], 99) if np.isfinite(M).any() else np.nan
    ax.plot_surface(X, Y, np.nan_to_num(M, nan=0.0), rstride=1, cstride=1, cmap='viridis', linewidth=0, antialiased=True)
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    ax.set_zlabel("|f(z)|")
    return fig

# =================================================================
# MAIN: Validación y salida
# =================================================================
st.title("Diagrama de fase — avanzado")

if entrada.strip() == "":
    st.markdown("<div class='welcome-text'>¡Bienvenido! Inserta una función en la barra lateral.</div>", unsafe_allow_html=True)
    st.stop()

# analizar y detectar ceros/polos
tipo = "desconocida"
f_sym = safe_sympy_sympify(entrada)
if f_sym is not None:
    if f_sym.is_polynomial():
        try:
            grado = sp.degree(f_sym)
            tipo = f"polinómica grado {grado}"
        except Exception:
            tipo = "polinómica"
    else:
        # heurística simple
        s = str(f_sym)
        if "exp" in s:
            tipo = "exponencial"
        elif "sin" in s or "cos" in s or "tan" in s:
            tipo = "trigonométrica"
        elif "log" in s:
            tipo = "logarítmica"
        else:
            tipo = "racional/otra"

zeros, poles = detect_zeros_poles(entrada)

# mostrar información
st.markdown(f"**Función:** `{entrada}`  \n**Tipo estimado:** {tipo}")
if zeros:
    st.markdown(f"**Ceros detectados (aprox):** {[(complex(r).real, complex(r).imag, m) for r, m in zeros]}")
else:
    st.markdown("**Ceros detectados (aprox):** ninguno")
if poles:
    st.markdown(f"**Polos detectados (aprox):** {[(complex(r).real, complex(r).imag, m) for r, m in poles]}")
else:
    st.markdown("**Polos detectados (aprox):** ninguno")

# Graficar fase + magnitud lado a lado
fig, im = plot_phase_and_magnitude(entrada, resolucion, LIM, color_map, phi if enable_animation else 0.0, mostrar_contours, zeros, poles)
st.pyplot(fig, use_container_width=True)

# opcion 3D
if modo_3D:
    st.markdown("### Vista 3D — |f(z)|")
    fig3d = plot_3D_surface(entrada, min(300, resolucion//2), LIM, phi if enable_animation else 0.0)
    st.pyplot(fig3d, use_container_width=True)

# descarga de imagen (fase+módulo)
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=200)
buf.seek(0)
st.download_button("Descargar imagen (fase + módulo)", buf.getvalue(), file_name="fase_modulo.png", mime="image/png")

# nota final
st.caption("La detección de ceros/polos es numérica (aproximada). Para funciones complicadas o ramificadas, los resultados pueden necesitar verificación simbólica adicional.")
