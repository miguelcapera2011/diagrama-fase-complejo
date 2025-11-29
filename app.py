# =====================================================================================
# LIBRERÍAS
# =====================================================================================
import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go

# =====================================================================================
# CONFIGURACIÓN DE PÁGINA
# =====================================================================================
st.set_page_config(
    page_title="Diagrama de fase",
    layout="wide"
)

# =====================================================================================
# FUNCIÓN PARA PARSEAR f(z)
# =====================================================================================
def parse_function(expr_text):
    z = sp.symbols("z")
    try:
        expr = sp.sympify(expr_text)
        f = sp.lambdify(z, expr, "numpy")
        return f, expr
    except:
        return None, None

# =====================================================================================
# BUSCAR CEROS Y POLOS (APROXIMADOS)
# =====================================================================================
def get_zeros_poles(expr):
    z = sp.symbols("z")

    zeros_x, zeros_y = [], []
    poles_x, poles_y = [], []

    try:
        # Ceros simbólicos
        sol = sp.solve(expr, z)

        for s in sol:
            if s.is_real:
                zeros_x.append(float(s))
                zeros_y.append(0.0)
            else:
                zeros_x.append(float(sp.re(s)))
                zeros_y.append(float(sp.im(s)))

        # Polos: calcular denominador si existe
        if expr.is_fraction:
            denom = sp.denom(expr)
            poles = sp.solve(denom, z)

            for p in poles:
                if p.is_real:
                    poles_x.append(float(p))
                    poles_y.append(0.0)
                else:
                    poles_x.append(float(sp.re(p)))
                    poles_y.append(float(sp.im(p)))

    except:
        pass

    return zeros_x, zeros_y, poles_x, poles_y

# =====================================================================================
# INTERFAZ
# =====================================================================================
st.title("📌 Diagrama de Fase Complejo – Gráfica 3D Interactiva")

func_input = st.text_input("Ingresa f(z):", "z**2 - 1")

# =====================================================================================
# PROCESO
# =====================================================================================
f, expr = parse_function(func_input)

if f is None:
    st.error("Error al procesar la función.")
    st.stop()

# ZONA DEL PLANO COMPLEJO
re_vals = np.linspace(-3, 3, 180)
im_vals = np.linspace(-3, 3, 180)
X, Y = np.meshgrid(re_vals, im_vals)
Z = X + 1j * Y

try:
    W = f(Z)
    Zabs = np.abs(W)
except:
    st.error("No se pudo evaluar la función.")
    st.stop()

# =====================================================================================
# CEROS Y POLOS
# =====================================================================================
zeros_x, zeros_y, poles_x, poles_y = get_zeros_poles(expr)

# =====================================================================================
# GRÁFICA 3D INTERACTIVA — MÁS GRANDE, SIN BARRA LATERAL
# =====================================================================================
fig = go.Figure()

# Superficie principal
fig.add_trace(go.Surface(
    x=X,
    y=Y,
    z=Zabs,
    colorscale="Turbo",
    showscale=False,
    opacity=0.97
))

# ------------------------------
# Ceros (rojo)
# ------------------------------
if len(zeros_x) > 0:
    fig.add_trace(go.Scatter3d(
        x=zeros_x,
        y=zeros_y,
        z=[0] * len(zeros_x),
        mode="markers",
        marker=dict(size=8, color="red", symbol="circle"),
        name="Ceros"
    ))

# ------------------------------
# Polos (azul)
# ------------------------------
if len(poles_x) > 0:
    height = np.max(Zabs) * 0.9
    fig.add_trace(go.Scatter3d(
        x=poles_x,
        y=poles_y,
        z=[height] * len(poles_x),
        mode="markers",
        marker=dict(size=8, color="blue", symbol="x"),
        name="Polos"
    ))

# Layout grande
fig.update_layout(
    title="Superficie |f(z)| con Ceros y Polos",
    width=1400,
    height=850,
    scene=dict(
        xaxis_title="Re(z)",
        yaxis_title="Im(z)",
        zaxis_title="|f(z)|",
        camera=dict(eye=dict(x=1.8, y=1.8, z=1.3))
    ),
    margin=dict(l=0, r=0, t=40, b=0)
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
