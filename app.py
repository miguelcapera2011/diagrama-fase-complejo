import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import io

# ===============================================================
# 1. Configuración de página
# ===============================================================
st.set_page_config(
    page_title="Variable Compleja | Miguel",
    layout="wide"
)

st.markdown("<h1 style='text-align:center;'>🧩 Variable Compleja – Diagramas y Arte</h1>", unsafe_allow_html=True)
st.write("Este programa calcula módulo, fase, derivadas, diagramas de flujo, fractales y arte basado en f(z).")


# ===============================================================
# 2. Entrada de la función
# ===============================================================
st.sidebar.header("Función")
entrada = st.sidebar.text_input("Ingresa la función f(z):", "z**2 + 1")


# ===============================================================
# 3. Definición segura de f(z)
# ===============================================================
def f(z, expr):
    try:
        return eval(expr, {"z": z, "np": np})
    except:
        return np.nan


# ===============================================================
# 4. Opciones de color
# ===============================================================
color_map = st.sidebar.selectbox(
    "Mapa de color:",
    ["viridis", "plasma", "inferno", "magma", "cividis", "turbo", "twilight"]
)


# ===============================================================
# 5. Área de trabajo (x,y)
# ===============================================================
x_min, x_max = st.sidebar.slider("Rango X:", -5.0, 5.0, (-2.0, 2.0))
y_min, y_max = st.sidebar.slider("Rango Y:", -5.0, 5.0, (-2.0, 2.0))
RES = st.sidebar.slider("Resolución:", 100, 800, 400)

x = np.linspace(x_min, x_max, RES)
y = np.linspace(y_min, y_max, RES)
X, Y = np.meshgrid(x, y)
Z = X + 1j*Y


# ===============================================================
# 6. Cálculo de f(z)
# ===============================================================
W = f(Z, entrada)
W = np.where(np.isfinite(W), W, np.nan + 1j*np.nan)


# ===============================================================
# 7. Magnitud |f(z)|
# ===============================================================
st.subheader("📌 Módulo |f(z)|")

fig1, ax1 = plt.subplots(figsize=(6, 6))
modulo = np.abs(W)
c = ax1.imshow(modulo, cmap=color_map, extent=[x_min,x_max,y_min,y_max])
plt.colorbar(c, ax=ax1)
ax1.set_title("|f(z)|")
st.pyplot(fig1)

buf1 = io.BytesIO()
fig1.savefig(buf1, format="png", dpi=300)
st.download_button("Descargar módulo", buf1.getvalue(), "modulo.png", "image/png")


# ===============================================================
# 8. Gráfica 3D
# ===============================================================
st.subheader("📌 Gráfica 3D de |f(z)|")

fig3d = plt.figure(figsize=(8, 6))
ax3d = fig3d.add_subplot(111, projection='3d')
ax3d.plot_surface(X, Y, modulo, cmap=color_map)
ax3d.set_title("Superficie 3D")
st.pyplot(fig3d)

buf3d = io.BytesIO()
fig3d.savefig(buf3d, format="png", dpi=300)
st.download_button("Descargar 3D", buf3d.getvalue(), "superficie3d.png", "image/png")


# ===============================================================
# 9. OPCIÓN DE ARTE / FRACTALES
# ===============================================================
activar_arte = st.sidebar.checkbox("🎨 Generar Arte / Fractal")

if activar_arte:
    st.subheader("🎨 Arte desde f(z)")
    tipo_arte = st.sidebar.selectbox("Tipo de Arte:", [
        "Fractal de Julia",
        "Fractal de Mandelbrot",
        "Estilo Van Gogh (fase)"
    ])

    # Malla usada para arte
    RESA = 600
    xA = np.linspace(-2, 2, RESA)
    yA = np.linspace(-2, 2, RESA)
    XA, YA = np.meshgrid(xA, yA)
    ZA = XA + 1j*YA

    # ===========================================================
    # FRACTAL DE JULIA
    # ===========================================================
    if tipo_arte == "Fractal de Julia":
        c = np.nanmean(f(ZA, entrada))
        Zj = ZA.copy()
        escape = np.zeros_like(Zj, dtype=int)
        max_iter = 180

        for i in range(max_iter):
            Zj = Zj*Zj + c
            mask = (escape == 0) & (np.abs(Zj) > 2.5)
            escape[mask] = i

        figA, axA = plt.subplots(figsize=(8, 8))
        axA.imshow(escape, cmap=color_map, extent=(-2,2,-2,2))
        axA.set_title("Fractal de Julia")
        axA.axis("off")
        st.pyplot(figA)

        bufA = io.BytesIO()
        figA.savefig(bufA, format="png", dpi=300)
        st.download_button("Descargar Julia", bufA.getvalue(), "julia.png", "image/png")

    # ===========================================================
    # MANDELBROT
    # ===========================================================
    elif tipo_arte == "Fractal de Mandelbrot":
        C = ZA
        Zm = np.zeros_like(C)
        escape = np.zeros_like(C, dtype=int)
        max_iter = 200

        for i in range(max_iter):
            Zm = Zm*Zm + C
            mask = (escape == 0) & (np.abs(Zm) > 2)
            escape[mask] = i

        figA, axA = plt.subplots(figsize=(8, 8))
        axA.imshow(escape, cmap=color_map, extent=(-2,2,-2,2))
        axA.set_title("Conjunto de Mandelbrot")
        axA.axis("off")
        st.pyplot(figA)

        bufA = io.BytesIO()
        figA.savefig(bufA, format="png", dpi=300)
        st.download_button("Descargar Mandelbrot", bufA.getvalue(), "mandelbrot.png", "image/png")

    # ===========================================================
    # ARTE VAN GOGH (SIN SCIPY)
    # ===========================================================
    elif tipo_arte == "Estilo Van Gogh (fase)":

        # Fase de f(z)
        W2 = f(ZA, entrada)
        W2 = np.where(np.isfinite(W2), W2, np.nan + 1j*np.nan)
        fase = np.angle(W2)

        # ---------------------------
        # Filtro Gaussiano CASERO
        # ---------------------------
        def gaussian_kernel(size=15, sigma=3):
            ax = np.linspace(-(size-1)/2., (size-1)/2., size)
            xx, yy = np.meshgrid(ax, ax)
            kernel = np.exp(-(xx**2 + yy**2) / (2.*sigma**2))
            return kernel / np.sum(kernel)

        kernel = gaussian_kernel(15, 3)

        def convolve(img, kernel):
            kh, kw = kernel.shape
            ih, iw = img.shape
            pad_h, pad_w = kh//2, kw//2
            img_pad = np.pad(img, ((pad_h, pad_h),(pad_w,pad_w)), mode='reflect')
            out = np.zeros_like(img)

            for i in range(ih):
                for j in range(iw):
                    region = img_pad[i:i+kh, j:j+kw]
                    out[i, j] = np.sum(region * kernel)
            return out

        suavizado = convolve(fase, kernel)

        # Turbulencia artística
        arte = suavizado + 0.4*np.sin(10*XA) + 0.4*np.cos(10*YA)

        figA, axA = plt.subplots(figsize=(8, 8))
        axA.imshow(arte, cmap="twilight", extent=(-2,2,-2,2))
        axA.set_title("Arte Estilo Van Gogh")
        axA.axis("off")
        st.pyplot(figA)

        bufA = io.BytesIO()
        figA.savefig(bufA, format="png", dpi=300)
        st.download_button("Descargar Van Gogh", bufA.getvalue(), "vangogh.png", "image/png")
