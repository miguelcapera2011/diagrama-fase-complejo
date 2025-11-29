import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ===========================
# CONFIGURACIÓN DE LA PÁGINA
# ===========================
st.set_page_config(page_title="Diagrama de Fase Complejo", layout="wide")

st.title("🎨 Diagrama de Fase de Funciones Complejas")
st.write("Visualización del plano complejo y gráfica 3D interactiva de |f(z)|.")

# ==============
# ENTRADA USUARIO
# ==============
funcion_str = st.text_input("Ingresa la función f(z)", "z**2 + 1")

# Rango del plano complejo
col1, col2 = st.columns(2)
with col1:
    min_val = st.number_input("Mínimo (Re/Im)", value=-2.0)
with col2:
    max_val = st.number_input("Máximo (Re/Im)", value=2.0)

densidad = st.slider("Densidad de puntos", 100, 600, 300)

# Elegir mapa de color
color_map = st.selectbox("Mapa de colores", ["turbo", "viridis", "plasma", "magma", "inferno", "hsv"])

# Activar gráfica 3D
activar_3d = st.checkbox("Mostrar gráfica 3D interactiva |f(z)|", True)

# ==========================
# CONSTRUIR EL PLANO COMPLEJO
# ==========================
x = np.linspace(min_val, max_val, densidad)
y = np.linspace(min_val, max_val, densidad)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# =======================
# CALCULAR LA FUNCIÓN f(z)
# =======================
try:
    f = eval(funcion_str, {"z": Z, "np": np})
except Exception as e:
    st.error(f"Error en la función: {e}")
    st.stop()

# ==============================
# DIAGRAMA DE FASE (ARGUMENTO)
# ==============================
fig, ax = plt.subplots(figsize=(6, 6))
fase = np.angle(f)

img = ax.imshow(fase, extent=[min_val, max_val, min_val, max_val],
                 origin="lower", cmap=color_map)

ax.set_title("Diagrama de Fase (arg(f(z)))")
ax.set_xlabel("Re(z)")
ax.set_ylabel("Im(z)")
plt.colorbar(img, ax=ax)

st.pyplot(fig)

# =====================================
# GRÁFICA 3D INTERACTIVA |f(z)| (PLOTLY)
# =====================================
if activar_3d:
    st.subheader("🌋 Gráfica 3D interactiva de |f(z)|")

    X3 = X
    Y3 = Y
    Z3 = np.abs(f)

    fig_int = go.Figure(
        data=[
            go.Surface(
                x=X3,
                y=Y3,
                z=Z3,
                colorscale=color_map,
                opacity=0.96
            )
        ]
    )

    fig_int.update_layout(
        title="Gráfica 3D Interactiva |f(z)|",
        autosize=True,
        scene=dict(
            xaxis_title="Re(z)",
            yaxis_title="Im(z)",
            zaxis_title="|f(z)|",
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.2)
            )
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig_int, use_container_width=True)

st.success("Visualización completada correctamente.")
