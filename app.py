# app_tamanio_muestra_proporciones_streamlit.py
# Streamlit app para exponer "Punto 6: tamaño muestral para proporciones"
# Incluye explicación, fórmulas, gráficos interactivos y comparaciones.

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import log
from scipy.stats import norm

# Intento importar funciones para intervalos exactos (Clopper-Pearson) si están
# disponibles. Si no, mostraremos una nota y la funcionalidad opcional seguirá.
try:
    from statsmodels.stats.proportion import proportion_confint
    STATS_MODELS_AVAILABLE = True
except Exception:
    STATS_MODELS_AVAILABLE = False

st.set_page_config(
    page_title="Tamaño muestral para proporciones (Punto 6)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- UTILS -----------------

def z_from_alpha(alpha):
    return norm.ppf(1 - alpha / 2)


def n_classical(p, d, alpha):
    z = z_from_alpha(alpha)
    return (z ** 2) * p * (1 - p) / (d ** 2)


def n_conservative(d, alpha):
    # fórmula independiente de p (conservadora, basada en p=0.5): Z^2 * 0.25 / d^2
    z = z_from_alpha(alpha)
    return (z ** 2) * 0.25 / (d ** 2)


def n_wilson_approx(d, alpha):
    # Aproximación simple derivada de la cota máxima: Z^2/(4 d^2)
    z = z_from_alpha(alpha)
    return (z ** 2) / (4 * d ** 2)


def n_at_least_one(p, confidence):
    # n tal que P(al menos un caso) >= confidence
    # 1 - (1-p)^n >= confidence  -> (1-p)^n <= 1-confidence -> n >= log(1-confidence)/log(1-p)
    if p <= 0:
        return np.inf
    if p >= 1:
        return 1
    return np.log(1 - confidence) / np.log(1 - p)


# ----------------- APP LAYOUT -----------------

st.title("📊 Punto 6 — Tamaño muestral para proporciones (p muy pequeña / muy grande)")
st.markdown(
    """
    Esta app acompaña la exposición sobre **por qué la varianza de una proporción es máxima en p=0.5**,
    cómo evitar la **sobreestimación** del tamaño muestral cuando p es muy pequeña o muy grande,
    y qué ajustes prácticos se recomiendan (usar la proporción esperada, usar correcciones como Wilson/Agresti–Coull, o fórmulas especiales para eventos raros).
    """
)

st.sidebar.header("Parámetros globales")
alpha = st.sidebar.slider("Nivel de significación \(\alpha\)", min_value=0.005, max_value=0.10, value=0.05, step=0.005)
confidence_at_least_one = st.sidebar.slider("Confianza para 'al menos un caso'", min_value=0.80, max_value=0.999, value=0.95, step=0.01)

# -------------------------------------------
# Panel izquierdo: exposición + texto provisto
# -------------------------------------------

col1, col2 = st.columns([1.1, 1])

with col1:
    st.header("📚 Exposición (texto listo para leer)")

    exposicion_text = """
**En esta presentación veremos cómo calcular el tamaño muestral cuando se trabajan proporciones muy pequeñas o muy grandes.**

La varianza es máxima cuando **p = 0.5**. ¿Por qué? Porque **p(1−p)** forma una curva simétrica cuya cima está exactamente en **0.5**.

Si p es 0.5, entonces hay máxima incertidumbre: la mitad de la población tiene la característica y la otra mitad no. Esto hace que la variabilidad sea mayor.

En proporciones extremas, la varianza **p(1−p)** se hace muy pequeña. Si usamos p = 0.5 para ser ‘conservadores’, sobre estimamos mucho el tamaño de muestra, especialmente en estudios de eventos raros. Explicaremos por qué la varianza es máxima en p = 0.5 y qué ajustes deben hacerse cuando **p < 0.10** o **p > 0.90**.

Estos conceptos son esenciales para evitar sobreestimar el tamaño de muestra y para diseñar estudios de eventos raros o de alta prevalencia.

**Recomendaciones prácticas:**
- Usar la proporción real esperada en vez de usar 0.5.
- Aplicar correcciones que evitan sobredimensionar el tamaño muestral, por ejemplo: intervalos exactos tipo *Clopper–Pearson*, aproximaciones de *Wilson* o *Agresti–Coull*, o fórmulas específicas para eventos raros.

(El app permite comparar las fórmulas y visualizar cómo cambian los tamaños muestrales al modificar p, d y \alpha.)
"""

    st.markdown(exposicion_text)

    st.markdown("---")

    st.header("🔧 Controles del ejercicio (introduzca los valores)")
    p = st.number_input("Proporción esperada p (entre 0 y 1)", min_value=0.0, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    d = st.number_input("Error absoluto tolerado d (ej: 0.01 = ±1%)", min_value=0.0005, max_value=0.5, value=0.01, step=0.001, format="%.4f")

    st.write("- Si no conoce p, puede probar con p = 0.5 para obtener un tamaño conservador, pero la app mostrará la sobreestimación.")

    st.markdown("---")

    st.subheader("Métodos calculados")
    st.write("La app calcula:\n• Fórmula clásica con p\n• Fórmula conservadora (p=0.5)\n• Aproximación tipo Wilson (independiente de p)\n• Tamaño para ver al menos un caso con cierta confianza")

with col2:
    st.header("📈 Visualizaciones interactivas")
    
    # Plot 1: variance p(1-p) with highlight
    ps = np.linspace(0, 1, 501)
    variances = ps * (1 - ps)

    fig1, ax1 = plt.subplots(figsize=(6, 3.5))
    ax1.plot(ps, variances, lw=2)
    ax1.fill_between(ps, variances, alpha=0.08)
    ax1.axvline(0.5, color='k', lw=0.8, linestyle='--')
    ax1.scatter([p], [p * (1 - p)], color='red')
    ax1.annotate(f'p={p:.4f}\nvar={p*(1-p):.4f}', xy=(p, p*(1-p)), xytext=(p+0.05, p*(1-p)+0.02), arrowprops=dict(arrowstyle='->'))
    ax1.set_title('Varianza de la proporción: p(1-p)')
    ax1.set_xlabel('p')
    ax1.set_ylabel('Varianza')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 0.26)
    st.pyplot(fig1)

    # Plot 2: sample size vs p for classical and conservative
    p_values = np.linspace(0.0001, 0.9999, 200)
    n_classic_values = [n_classical(pp, d, alpha) for pp in p_values]
    n_conserv = n_conservative(d, alpha)
    n_wilson_val = n_wilson_approx(d, alpha)

    fig2, ax2 = plt.subplots(figsize=(6, 3.5))
    ax2.plot(p_values, n_classic_values, label='Clásica (p varía)')
    ax2.hlines(n_conserv, 0, 1, colors='orange', linestyles='--', label='Conservadora (p=0.5)')
    ax2.hlines(n_wilson_val, 0, 1, colors='green', linestyles=':', label='Aproximación Wilson')
    ax2.axvline(p, color='red', linestyle='--')
    ax2.set_yscale('log')
    ax2.set_xlabel('p')
    ax2.set_ylabel('Tamaño muestral estimado (escala log)')
    ax2.set_title(f'Tamaño muestral vs p (d={d}, \alpha={alpha})')
    ax2.legend()
    st.pyplot(fig2)

# ----------------- Results and comparisons -----------------

st.markdown("---")
st.header("🔢 Cálculos y comparaciones")

n_cl = n_classical(p, d, alpha)
n_cons = n_conservative(d, alpha)
n_wil = n_wilson_approx(d, alpha)
n_one = n_at_least_one(p, confidence_at_least_one)

colA, colB, colC, colD = st.columns(4)
colA.metric("Clásica (usando p)", f"{n_cl:.0f}")
colB.metric("Conservadora (p=0.5)", f"{n_cons:.0f}")
colC.metric("Wilson (aprox.)", f"{n_wil:.0f}")
colD.metric("Para ver ≥1 caso (conf={:.0f}%)".format(confidence_at_least_one*100), f"{np.ceil(n_one):.0f}")

st.markdown("**Interpretación:**")
st.write(
    f"• Si usas la proporción esperada p={p:.4f} la fórmula clásica da n≈{n_cl:.0f}.\n"
    f"• Si usas p=0.5 (conservador) obtienes n≈{n_cons:.0f}, que es {'mayor' if n_cons>n_cl else 'menor'} que la clásica por un factor ≈{(n_cons/n_cl):.2f}.\n"
    f"• La aproximación de Wilson produce n≈{n_wil:.0f} y es útil como cota independiente de p.\n"
)

# Show note about overestimation factor
st.write("**Factor de sobreestimación** (conservador / clásica):")
if n_cl > 0:
    st.write(factor := n_cons / max(1, n_cl))
else:
    st.write("Indeterminado (n clásico = 0)")

st.markdown("---")

# Optional: Clopper-Pearson example (requires statsmodels)
st.subheader("Intervalos exactos y Clopper–Pearson (opcional)")
if STATS_MODELS_AVAILABLE:
    st.write("Se detectó statsmodels. Puedes ver cómo cambia el intervalo exacto Clopper–Pearson para un número observado de éxitos x y tamaño n:")
    obs_n = st.number_input("n observado (ej. en un estudio piloto)", min_value=1, value=100, step=1)
    obs_x = st.number_input("x éxitos observados", min_value=0, max_value=obs_n, value=1, step=1)
    alpha_interval = st.slider("alpha para el intervalo de confianza", min_value=0.001, max_value=0.2, value=0.05, step=0.001)
    lower, upper = proportion_confint(count=obs_x, nobs=obs_n, alpha=alpha_interval, method='beta')
    st.write(f"Clopper–Pearson (exacto) para x={obs_x}, n={obs_n}, alpha={alpha_interval}: [{lower:.4f}, {upper:.4f}]")
else:
    st.info("La librería statsmodels no está disponible en este entorno. Para activar la sección de Clopper–Pearson instale statsmodels: pip install statsmodels")

st.markdown("---")

# ----------------- Examples / Scenarios -----------------

st.header("🧪 Ejemplos y escenarios recomendados para la exposición")

st.subheader("Ejemplo 1 — Evento raro")
st.write(
    "Suponga p=0.01 (1%) y que queremos d=0.01 (±1%). La fórmula clásica da un n moderado, y usar p=0.5 daría un n ridículamente grande."
)
st.write(f"Cálculo directo: n clásica = {n_classical(0.01, d, alpha):.0f}, n con p=0.5 = {n_conservative(d, alpha):.0f}")

st.subheader("Ejemplo 2 — Para observar al menos 1 caso")
st.write(
    "Si un evento tiene probabilidad p=0.005 (0.5%) y queremos 95% de probabilidad de detectar al menos un caso: "
)
st.write(f"n >= {np.ceil(n_at_least_one(0.005, 0.95)):.0f}")

st.markdown("---")

st.caption("App generada para apoyar una exposición en clase de Muestreo Estadístico — Punto 6 (proporciones extremas). Modifica los valores y muestra cómo cambia el tamaño muestral en las gráficas e indicadores.")

st.sidebar.markdown("---")
st.sidebar.header("Ayuda rápida")
st.sidebar.write("1) Ajusta p y d en el panel principal. 2) Observa las gráficas y los indicadores. 3) Usa la sección de Clopper–Pearson si instalas statsmodels.")

# Footer
st.markdown("---")
st.write("Si quieres, puedo exportar esta exposición a diapositivas PowerPoint o generar una versión PDF con las gráficas. Dime qué prefieres.")
