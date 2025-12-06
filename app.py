# STREAMLIT APP: Cálculo tamaño muestral para proporciones (Punto inicial)
# Miguel Angel Garatejo · Daniela Angulo
# Programa: Matemáticas con Estadística — Asignatura: Muestreo
# Esta app implementa la portada, introducción y la primera sección del enunciado:
# "Cálculo de tamaño muestral para proporciones cuando se espera una proporción
# muy pequeña o muy grande (efectos en la varianza)."

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

st.set_page_config(page_title="Muestreo - Proporciones (Punto 1)", layout="wide")

# -----------------------------
# Portada bonita
# -----------------------------
st.markdown("""
<style>
.header-card{
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  padding: 24px;
  border-radius: 12px;
}
.names{
  font-size:26px;
  font-weight:700;
}
.subtitle{
  font-size:16px;
  color: #cbd5e1;
}
</style>
<div class='header-card'>
  <div class='names'>Miguel Angel Garatejo · Daniela Angulo</div>
  <div class='subtitle'>Programa: Matemáticas con Estadística — Asignatura: Muestreo</div>
</div>
""", unsafe_allow_html=True)

st.write("\n")

# -----------------------------
# Introducción
# -----------------------------
with st.expander("Introducción al punto (mostrar) ", expanded=True):
    st.markdown(
        """
        En este primer bloque trabajaremos la estimación del tamaño muestral para proporciones cuando
        **se espera una proporción muy pequeña o muy grande** (casos de eventos raros o muy frecuentes).

        Los objetivos son:
        - Mostrar la fórmula clásica de tamaño muestral para proporciones y por qué la varianza máxima ocurre en \(p=0.5\).
        - Permitir interactuar con la proporción \(p\) mediante un *slider* y ver en tiempo real la varianza y el tamaño muestral.
        - Mostrar ajustes y alternativas (p.ej. aproximación de Poisson para eventos raros, y la estrategia conservadora \(p=0.5\)).
        """
    )

st.markdown("---")

# -----------------------------
# Controls (sidebar)
# -----------------------------
st.sidebar.header("Controles")
p = st.sidebar.slider("Proporción esperada (p)", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.3f")
E = st.sidebar.slider("Margen de error (E) (error absoluto)", min_value=0.005, max_value=0.20, value=0.03, step=0.001, format="%.3f")
conf_level = st.sidebar.selectbox("Nivel de confianza", options=[90, 95, 99], index=1)

# z-scores for common confidence levels
z_map = {90:1.644853, 95:1.959964, 99:2.575829}
z = z_map[conf_level]

# -----------------------------
# Theory + Formula (left column) and Interactive Plot (right column)
# -----------------------------
col1, col2 = st.columns([1,1])

with col1:
    st.subheader("Teoría y fórmulas")
    st.markdown("""
    **Fórmula estándar (aproximación normal)**

    Para una proporción poblacional \(p\) y margen de error absoluto \(E\), el tamaño muestral aproximado (para muestras grandes) es:

    \[
      n \approx \frac{z^2 \; p (1-p)}{E^2}
    \]

    donde \(z\) es el cuantil de la distribución normal estándar correspondiente al nivel de confianza.

    **Varianza de una proporción:**

    \[
      \mathrm{Var}(\hat p) = \frac{p(1-p)}{n}
    \]

    Observa que la **varianza** (en términos de \(p\)) es \(p(1-p)\) — ésta alcanza su valor máximo en \(p=0.5\).

    *Prueba rápida*: derivando \(f(p)=p(1-p)=p-p^2\), \(f'(p)=1-2p\) se anula en \(p=0.5\) y es un máximo.
    """, unsafe_allow_html=False)

    st.markdown("**Ajustes y alternativas para proporciones extremas**")
    st.markdown("""
    - **Estrategia conservadora:** si no se conoce \(p\), usar \(p=0.5\) garantiza la máxima varianza y por tanto el tamaño muestral más seguro:
      \(n_{cons} = \dfrac{z^2(0.5)(0.5)}{E^2} = \dfrac{z^2}{4E^2}\).

    - **Eventos raros (p < 0.10):** para proporciones muy pequeñas la distribución binomial puede aproximarse por una Poisson con media \(\lambda = np\). En ese contexto la varianza se aproxima por \(p\) (cuando \(1-p\approx 1\)), y una fórmula práctica es:
      \(n \approx \dfrac{z^2\, p}{E^2}\) (esta es una aproximación — usarla con cuidado y validar con simulación o métodos exactos).

    - **Formas más robustas (evitar sobreestimación):** usar fórmulas tipo Agresti–Coull o el intervalo de Wilson para estimar el tamaño requiere iteración (ya que esas fórmulas usan el tamaño final para calcular el ajuste). Una aproximación práctica es calcular iterativamente hasta converger en \(n\).
    """)

    st.markdown("**Resumen de recomendaciones rápidas:**")
    st.write("- Si no tiene idea de p: usar p=0.5 (conservador).")
    st.write("- Si espera eventos raros (p<0.1): evaluar la aproximación Poisson y/o usar métodos exactos o simulación.")

with col2:
    st.subheader("Gráfica interactiva (varianza y n)")

    ps = np.linspace(0,1,501)
    var_curve = ps*(1-ps)

    # compute sample sizes for the chosen E and z
    def n_standard(p_val):
        # avoid p exactly 0 or 1 causing n=0
        p_val = max(min(p_val, 1-1e-12), 1e-12)
        return (z**2 * p_val * (1-p_val)) / (E**2)

    n_p = n_standard(p)
    n_conservative = (z**2) / (4 * E**2)
    n_poisson = (z**2 * p) / (E**2)  # approx for rare events

    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(ps, var_curve, linewidth=2)
    ax.set_xlabel('p')
    ax.set_ylabel('Varianza (p(1-p))')
    ax.set_title('Varianza de la proporción en función de p')
    ax.grid(True, linestyle=':', linewidth=0.6)

    # marker for selected p
    ax.scatter([p], [p*(1-p)], s=70)
    ax.annotate(f'p={p:.3f}\nvar={p*(1-p):.4f}', xy=(p, p*(1-p)), xytext=(p+0.05, p*(1-p)+0.02), fontsize=9)

    st.pyplot(fig)

    # display numeric results in a small card
    st.markdown("""
    **Cálculos (resultado en tiempo real)**
    """)
    st.metric(label="Tamaño muestral (fórmula estándar)", value=f"n ≈ {ceil(n_p):,}")
    st.caption(f"n (no redondeado) = {n_p:.2f}")

    st.metric(label="Tamaño conservador (p=0.5)", value=f"n_cons ≈ {ceil(n_conservative):,}")
    st.caption(f"n_cons (no redondeado) = {n_conservative:.2f}")

    st.metric(label="Aproximación Poisson (p pequeño)", value=f"n_poisson ≈ {ceil(n_poisson):,}")
    st.caption(f"n_poisson (no redondeado) = {n_poisson:.2f}")

# -----------------------------
# Notas finales y siguiente paso
# -----------------------------
st.markdown('---')
st.subheader('Notas')
st.write(
    'Este panel cubre la teoría principal y una visualización interactiva.\n'
    'Siguientes pasos que podemos implementar: mostrar la iteración Agresti–Coull/Wilson para tamaño muestral, ' 
    'un ejemplo práctico con datos reales (simulación) y exportar los resultados a un Excel bonito con dos ejemplos de la vida real.'
)

st.info('Si estás de acuerdo, procedo a agregar: (1) el cálculo iterativo Agresti–Coull, (2) dos ejemplos reales con exportación a Excel, y (3) una sección de interpretación para tu exposición.')

# FIN DEL ARCHIVO
