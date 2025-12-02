import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from math import ceil, log

# ----------------------
# Exposición (texto en primera persona)
# ----------------------
EXPOSICION = r'''
# Exposición: Cálculo de tamaño muestral para proporciones

En esta presentación explico, con mis propias palabras, cómo se comporta la varianza de una proporción y qué ajustes conviene hacer cuando la proporción esperada es muy pequeña (p < 0.1) o muy grande (p > 0.9). También presento alternativas que evitan la sobreestimación del tamaño muestral y muestro aplicaciones en estudios de eventos raros.

**1. ¿Por qué la máxima varianza ocurre en p = 0.5?**
La varianza de una proporción muestral se aproxima por \(\text{Var}(\hat p) = p(1-p)/n\). Para una n fija, la cantidad p(1-p) alcanza su máximo cuando p = 0.5 porque la función f(p)=p(1-p) = p - p^2 es un paraboloide con vértice en p=0.5 y valor máximo 0.25. Eso significa que, si no conocemos p, la elección conservadora p=0.5 produce el mayor tamaño muestral necesario para una precisión dada.

**2. Fórmula clásica (aproximación normal):**
Para un margen de error (medio ancho del intervalo) \(E\) y un nivel de confianza con cuantía \(z_{1-\alpha/2}\):

\[ n = \frac{z^2 \; p(1-p)}{E^2} .\]

Si p no se conoce y queremos ser conservadores usamos p = 0.5.

**3. Ajustes cuando p < 0.1 o p > 0.9**
Cuando p está muy cerca de 0 o de 1, la aproximación normal de la varianza puede ser pobre para tamaños moderados. Estrategias comunes:

- **Usar transformaciones** (por ejemplo la transformada arcsin o logit) para estabilizar la varianza antes de diseñar la muestra.
- **Usar intervalos tipo Wilson**: para proporciones pequeñas Wilson tiende a dar intervalos más precisos y menos extremos que el intervalo simétrico normal. Podemos hallar n resolviendo la condición del ancho del intervalo Wilson numéricamente.
- **Poisson/contaje para eventos raros**: si p es muy pequeño y n grande, el número de éxitos sigue aproximadamente una Poisson(\(\lambda = np\)). Para diseñar experimentos de detección (ej.: "queremos tener al menos una observación con probabilidad 1 - \beta"), se usa:

\[ 1 - (1-p)^n \ge 1 - \beta \quad\Rightarrow\quad n \ge \frac{\ln(\beta)}{\ln(1-p)} \approx \frac{-\ln(\beta)}{p} \quad (\text{si } p \ll 1).\]

Esto es muy útil en estudios de eventos raros: por ejemplo, para tener 95% de probabilidad de observar al menos un evento con p=0.001 necesitamos aproximadamente \(n \approx -\ln(0.05)/0.001 \approx 2995\).

**4. Ecuaciones alternativas para evitar sobreestimación**
- **Conservador**: usar p=0.5 en la fórmula clásica (genera la cota superior del n requerido).
- **Wilson (numérico)**: resolver numéricamente el mínimo n tal que el intervalo Wilson tiene medio ancho ≤ E.
- **Poisson para eventos raros**: usar la aproximación mostrada arriba cuando p muy pequeño y el objetivo es detectar al menos un suceso.

**5. Aplicaciones: estudios de eventos raros**
Ejemplos: detección de defectos muy inusuales en manufactura, prevalencia de una enfermedad muy rara, detección de ruido o fallos críticos. En estos casos la aproximación de Poisson y la planificación basada en la probabilidad de observar al menos un evento son muy útiles.

---

A continuación presento una app interactiva donde se pueden experimentar las fórmulas, comparar enfoques (clásico, conservador, Wilson y Poisson) y ver gráficas ilustrativas. He dejado campos para incluir imágenes o capturas vía URL.
'''

# ----------------------
# Funciones estadísticas
# ----------------------

def z_from_confidence(conf_level):
    # approximate z for common levels
    import mpmath as mp
    alpha = 1 - conf_level
    return abs(mp.sqrt(2) * mp.erfinv(1 - alpha))


def z_approx(conf_level):
    # fallback using scipy-less approximation via inverse of normal CDF (useer mpmath)
    import mpmath as mp
    alpha = 1 - conf_level
    return float(mp.sqrt(2) * mp.erfinv(1 - alpha))


def n_standard(p, E, z):
    # n = z^2 * p(1-p) / E^2
    return math.ceil((z**2) * p * (1 - p) / (E**2))


def n_conservative(E, z):
    # p = 0.5
    return n_standard(0.5, E, z)


def n_poisson_detect(p, beta):
    # n >= ln(beta) / ln(1-p). If p<<1, approx -ln(beta)/p
    if p <= 0:
        return math.inf
    try:
        n = math.log(beta) / math.log(1 - p)
        return math.ceil(n)
    except Exception:
        return math.ceil(-math.log(beta) / p)

# Wilson interval half-width computation and numeric search for n

def wilson_half_width(p, n, z):
    # Wilson interval half-width formula (exact) for a given n and p
    if n <= 0:
        return float('inf')
    z2 = z**2
    denom = 1 + z2 / n
    center = (p + z2/(2*n)) / denom
    term = (p*(1-p)/n + z2/(4*n*n))
    hw = (z * math.sqrt(term)) / denom
    return hw


def n_wilson_by_search(p, E, z, n_max=10_000_000):
    # Busca el n mínimo tal que wilson_half_width(p,n,z) <= E
    # Empieza en el estándar y sube exponencialmente
    if p == 0 or p == 1:
        # Wilson reduces to one-sided correction; treat specially
        return None
    n = max(10, n_standard(p, E, z))
    # if already ok, decrease
    if wilson_half_width(p, n, z) <= E:
        # intentar bajar n por búsqueda binaria hacia la izquierda
        lo, hi = 2, n
        while lo < hi:
            mid = (lo + hi) // 2
            if wilson_half_width(p, mid, z) <= E:
                hi = mid
            else:
                lo = mid + 1
        return lo
    # else aumentar exponencialmente
    while wilson_half_width(p, n, z) > E and n < n_max:
        n *= 2
    # binsearch between n/2 and n
    lo, hi = n//2, n
    while lo < hi:
        mid = (lo + hi)//2
        if wilson_half_width(p, mid, z) <= E:
            hi = mid
        else:
            lo = mid + 1
    return lo if lo < n_max else None

# ----------------------
# Interfaz Streamlit
# ----------------------

st.set_page_config(page_title='Tamaño muestral: proporciones (poco/mucho)', layout='wide')

st.title('Cálculo de tamaño muestral para proporciones — Exposición interactiva')

with st.expander('Ver exposición (texto)'):
    st.markdown(EXPOSICION)

# Sidebar inputs
st.sidebar.header('Parámetros de diseño')
conf = st.sidebar.selectbox('Nivel de confianza', [0.90, 0.95, 0.99], index=1)
E = st.sidebar.number_input('Margen de error (E) — medio ancho del IC', min_value=0.001, max_value=0.5, value=0.03, step=0.001, format="%.3f")
p = st.sidebar.slider('Proporción esperada p', min_value=0.0, max_value=1.0, value=0.05, step=0.001)

# For poisson detection
beta = st.sidebar.number_input('Beta (prob. de NO detectar al menos 1 evento)', min_value=1e-6, max_value=0.5, value=0.05, format='%.5f')

z = z_approx(conf)
st.sidebar.markdown(f'Cuantil z (aprox) = **{z:.3f}**')

st.markdown('---')

# Image placeholders via URL
st.subheader('Imágenes / capturas (opcional)')
img1 = st.text_input('URL imagen 1 (ej.: esquema explicación)', '')
img2 = st.text_input('URL imagen 2 (ej.: captura tabla o diagrama)', '')

col1, col2 = st.columns(2)
with col1:
    if img1:
        try:
            st.image(img1, use_column_width=True)
        except Exception as e:
            st.error('No se pudo cargar la imagen 1. Verifique la URL.')
with col2:
    if img2:
        try:
            st.image(img2, use_column_width=True)
        except Exception as e:
            st.error('No se pudo cargar la imagen 2. Verifique la URL.')

# Compute sizes
n_std = n_standard(p, E, z)
n_cons = n_conservative(E, z)
n_wilson = n_wilson_by_search(p, E, z)
n_poisson = n_poisson_detect(p, beta)

st.subheader('Cálculos principales')
st.markdown(f'- Fórmula clásica (normal): **n = z^2 p(1-p) / E^2**')
st.markdown(f'- Resultado (usando p = {p:.3f}): **n = {n_std:,d}**')
st.markdown(f'- Conservador (p = 0.5): **n = {n_cons:,d}**')
if n_wilson is not None:
    st.markdown(f'- Wilson (n mínimo numérico): **n = {n_wilson:,d}**')
else:
    st.markdown(f'- Wilson: no aplicable (p=0 o 1) o fuera de rango.')
st.markdown(f'- Método Poisson (diseño para detectar al menos 1 evento con prob. 1 - beta, beta={beta}): **n ≈ {n_poisson:,d}**')

# Table summary
summary = pd.DataFrame({
    'Método': ['Clásico (p elegido)', 'Conservador (p=0.5)', 'Wilson (numérico)', 'Poisson (detección)'],
    'n_estimado': [n_std, n_cons, n_wilson if n_wilson else np.nan, n_poisson]
})

st.dataframe(summary.style.format({'n_estimado':'{:,}'}))

# Plots
st.subheader('Gráficas ilustrativas')

# 1) Varianza p(1-p) vs p
ps = np.linspace(0,1,501)
vars_ = ps * (1-ps)
fig1, ax1 = plt.subplots(figsize=(6,3))
ax1.plot(ps, vars_)
ax1.axvline(0.5, color='k', linestyle='--')
ax1.set_xlabel('p')
ax1.set_ylabel('p(1-p) (varianza relativa)')
ax1.set_title('Varianza relativa p(1-p) — máximo en p = 0.5')
st.pyplot(fig1)

# 2) n required as function of p (for fixed E and z)
ps2 = np.linspace(0.001,0.999,199)
ns_std = [n_standard(pi, E, z) for pi in ps2]
ns_wilson = [n_wilson_by_search(pi, E, z) for pi in ps2]

fig2, ax2 = plt.subplots(figsize=(6,3))
ax2.plot(ps2, ns_std, label='Clásico')
ax2.plot(ps2, ns_wilson, label='Wilson (numérico)', linestyle='--')
ax2.set_ylim(0, max(filter(lambda v: np.isfinite(v), ns_std)) * 1.2)
ax2.set_xlabel('p')
ax2.set_ylabel('Tamaño muestral n')
ax2.set_title('n requerido en función de p (E y nivel de confianza fijos)')
ax2.legend()
st.pyplot(fig2)

# 3) For rare p show poisson approx
st.subheader('Ejemplo: diseño para eventos raros (Poisson)')
if p < 0.05:
    st.markdown(f'Con p = {p:.4f} y beta = {beta}, se requiere aproximadamente n = {n_poisson:,d} para tener probabilidad {1-beta:.3f} de observar al menos un evento.')
else:
    st.markdown('La aproximación Poisson es recomendable cuando p es pequeño (por ejemplo p < 0.01 ó p < 0.05).')

# Downloadable report (CSV)
report = summary.copy()
report['p_usado'] = p
report['E'] = E
report['confianza'] = conf

csv = report.to_csv(index=False).encode('utf-8')
st.download_button('Descargar resumen (CSV)', csv, file_name='resumen_tamanomuestra.csv', mime='text/csv')

st.markdown('---')
st.markdown('**Notas finales / Recomendaciones (como si yo lo presentara):**')
st.markdown('- Si no conocemos p, usar p=0.5 para garantizar una estimación conservadora del tamaño muestral.')
st.markdown('- Para p muy pequeñas usar la aproximación Poisson o diseñar con la probabilidad de detectar al menos un evento.')
st.markdown('- Para niveles de confianza altos y p extremos, prefiera intervalos tipo Wilson o procedimientos exactos en lugar de la aproximación normal simples.')

st.caption('App creada como entrega tipo 'exposición'; edítela libremente para incorporar imágenes reales y adaptarla a su informe.')
