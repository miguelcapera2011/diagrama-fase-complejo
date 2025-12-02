import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import mpmath as mp

# ----------------------------------------------------------
# EXPLICACIÓN / EXPOSICIÓN (texto en primera persona)
# ----------------------------------------------------------
EXPOSICION = r'''
# Exposición: Cálculo de tamaño muestral para proporciones

En esta presentación explico, con mis propias palabras, cómo se comporta la varianza 
de una proporción y qué ajustes conviene hacer cuando la proporción esperada es muy 
pequeña (p < 0.1) o muy grande (p > 0.9). También presento alternativas que evitan 
la sobreestimación del tamaño muestral y muestro aplicaciones en estudios de eventos raros.

---

## **1. ¿Por qué la máxima varianza ocurre en p = 0.5?**

La varianza de una proporción muestral es:

\[
\text{Var}(\hat p) = \frac{p(1-p)}{n}
\]

La parte \(p(1-p)\) alcanza su máximo cuando \(p=0.5\).  
Esto significa que, si no conocemos p, usar \(p=0.5\) produce el tamaño muestral más grande (= más conservador).

---

## **2. Fórmula clásica del tamaño muestral**

\[
n = \frac{z^2 p(1-p)}{E^2}
\]

donde:

- \(E\): margen de error (mitad del ancho del IC)
- \(z\): cuantil normal según el nivel de confianza

Si no sabemos p → usamos **p = 0.5** (más conservador).

---

## **3. Ajustes cuando p < 0.1 o p > 0.9**

Cuando p es extrema:

- La aproximación normal puede fallar.
- El IC clásico puede ser demasiado optimista o demasiado ancho.

Alternativas:

### ✔ Wilson
Reduce el sesgo para p pequeñas.  
Permite obtener un n menor sin perder precisión.

### ✔ Transformaciones (arcsin o logit)
Estabilizan la varianza pero requieren más matemáticas.

### ✔ Aproximación Poisson (eventos raros)
Cuando p es muy pequeña:

\[
1 - (1-p)^n \ge 1 - \beta
\]

Se despeja:

\[
n \approx \frac{-\ln(\beta)}{p}
\]

Útil para situaciones donde queremos “ver al menos un caso”.

---

## **4. Aplicaciones: eventos raros**
- Calidad industrial (defectos muy raros).
- Epidemiología (enfermedades muy poco frecuentes).
- Riesgos de fallos (fallas críticas, errores poco comunes).

En estos casos la aproximación Poisson es ideal.

---
'''


# ----------------------------------------------------------
# FUNCIONES ESTADÍSTICAS
# ----------------------------------------------------------

def z_from_conf(conf_level):
    alpha = 1 - conf_level
    return float(mp.sqrt(2) * mp.erfinv(1 - alpha))


def n_standard(p, E, z):
    return math.ceil((z ** 2) * p * (1 - p) / (E ** 2))


def n_conservative(E, z):
    return n_standard(0.5, E, z)


def wilson_half_width(p, n, z):
    if n <= 0:
        return float("inf")

    z2 = z ** 2
    denom = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denom
    term = (p * (1 - p) / n) + (z2 / (4 * n * n))
    hw = (z * math.sqrt(term)) / denom
    return hw


def n_wilson_search(p, E, z, n_max=5_000_000):

    if p in [0, 1]:
        return None

    n = max(10, n_standard(p, E, z))

    if wilson_half_width(p, n, z) <= E:
        lo, hi = 2, n
        while lo < hi:
            mid = (lo + hi) // 2
            if wilson_half_width(p, mid, z) <= E:
                hi = mid
            else:
                lo = mid + 1
        return lo

    while wilson_half_width(p, n, z) > E and n < n_max:
        n *= 2

    lo, hi = n // 2, n
    while lo < hi:
        mid = (lo + hi) // 2
        if wilson_half_width(p, mid, z) <= E:
            hi = mid
        else:
            lo = mid + 1

    return lo if lo < n_max else None


def n_poisson(p, beta):
    if p <= 0:
        return None
    return math.ceil(-math.log(beta) / p)


# ----------------------------------------------------------
# INTERFAZ STREAMLIT
# ----------------------------------------------------------

st.set_page_config(page_title="Tamaño muestral para proporciones", layout="wide")

st.title("📊 Cálculo de tamaño muestral para proporciones")
st.markdown("App interactiva profesional — incluye Wilson, clásico y Poisson (eventos raros).")

with st.expander("📘 Ver exposición completa"):
    st.markdown(EXPOSICION)


# ---------------------------
# PARÁMETROS
# ---------------------------
st.sidebar.header("🔧 Parámetros de diseño")

conf = st.sidebar.selectbox("Nivel de confianza", [0.90, 0.95, 0.99], index=1)
E = st.sidebar.number_input("Margen de error E", min_value=0.001, max
