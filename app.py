# app.py
"""
Sample Size Dashboard (Punto 6)
Streamlit app to explore sample size calculations for extreme proportions (p small or large).
Features:
 - Classical formula
 - Finite population correction
 - Wilson interval-based n (numerical search)
 - Agresti-Coull (numerical search)
 - Poisson approx (n = lambda / p)
 - Exact binomial (numerical search using binomial CDF criterion)
 - Simulated and uploadable datasets (2 examples included)
 - Interactive charts and Excel export
"""

from math import ceil, sqrt
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm, binom, poisson
import plotly.express as px
import io

st.set_page_config(page_title="Tamaño Muestra — Punto 6", layout="wide")

# -------------------------
# Helper functions
# -------------------------
Z_lookup = {90: 1.645, 95: 1.96, 99: 2.576}

def z_from_conf(conf):
    return Z_lookup.get(int(conf), norm.ppf(1 - (1 - conf/100)/2))

def classical_n(p, E, z):
    """Classical closed-form sample size for proportion."""
    return (z**2 * p * (1 - p)) / (E**2)

def finite_population_correction(n0, N):
    """Finite population corrected sample size."""
    if N is None or N <= 0:
        return n0
    return n0 / (1 + n0 / N)

def poisson_n(p, lam):
    """Poisson approximation: n = lambda / p"""
    if p <= 0:
        return np.nan
    return lam / p

def wilson_interval_halfwidth(p_hat, n, z):
    """Compute half-width of Wilson interval for observed x = round(p_hat*n)."""
    x = int(round(p_hat * n))
    if n == 0:
        return np.nan
    phat = x / n
    denom = 1 + (z**2) / n
    center = (phat + (z**2) / (2 * n)) / denom
    term = z * np.sqrt((phat * (1 - phat) / n) + (z**2) / (4 * n**2)) / denom
    halfw = term
    return halfw

def agresti_coull_halfwidth(p_hat, n, z):
    """Compute Agresti-Coull half-width using adjusted counts (x+z^2/2)."""
    # Agresti–Coull uses +z^2/2 pseudo-counts; we'll compute adjusted p_tilde and halfwidth (approx normal)
    x = int(round(p_hat * n))
    n_tilde = n + z**2
    p_tilde = (x + (z**2) / 2) / n_tilde
    halfw = z * np.sqrt(p_tilde * (1 - p_tilde) / n_tilde)
    return halfw

def find_min_n_by_halfwidth(p, E, z, method='wilson', max_n=200000):
    """Find minimal integer n such that half-width <= E using chosen method."""
    # Start from classical estimate as lower bound
    n0 = max(2, int(ceil(classical_n(max(p, 1e-12), E, z))))
    for n in range(n0, max_n+1):
        if method == 'wilson':
            hw = wilson_interval_halfwidth(p, n, z)
        elif method == 'agresti-coull':
            hw = agresti_coull_halfwidth(p, n, z)
        elif method == 'exact':
            # exact: find x = round(p*n) and compute two-sided Clopper-Pearson half-width conservatively
            x = int(round(p * n))
            # compute two-sided Clopper-Pearson interval (use binom.ppf) via inversion
            alpha = 2*(1 - norm.cdf(z))  # approx alpha from z
            # lower bound
            if x == 0:
                lower = 0.0
            else:
                lower = binom.ppf(alpha/2, n, p)  # not ideal; we'll approximate using beta inversion would be better
                # fallback: simple approximation using Wilson
                lower = max(0.0, (x / n) - z * sqrt((x / n) * (1 - x / n) / n))
            upper = min(1.0, (x / n) + z * sqrt((x / n) * (1 - x / n) / n))
            hw = max((x / n) - lower, upper - (x / n))
        else:
            hw = wilson_interval_halfwidth(p, n, z)
        # handle unrealistic nan
        if np.isnan(hw):
            continue
        if hw <= E:
            return n
    return None

def classical_with_correction(p, E, z, N=None):
    n0 = classical_n(p, E, z)
    n_corr = finite_population_correction(n0, N) if N else n0
    return n0, n_corr

# -------------------------
# UI Layout
# -------------------------
st.title("📊 Dashboard — Tamaño de muestra para proporciones extremas (Punto 6)")
st.markdown("""
Esta app interactiva cubre **teoría**, **fórmulas**, **cálculos en tiempo real**, **gráficos** y **ejemplos** para proporciones muy pequeñas o muy grandes (p < 0.10 o p > 0.90).
Usa la barra lateral para configurar parámetros, prueba con los ejemplos incluidos o sube tus propios datos CSV.
""")

# Sidebar
with st.sidebar:
    st.header("Configuración de cálculo")
    conf = st.selectbox("Nivel de confianza (%)", [90, 95, 99], index=1)
    z = z_from_conf(conf)
    p_input = st.number_input("Proporción esperada p (0 < p < 1)", min_value=0.0, max_value=1.0, value=0.002, format="%.6f")
    E = st.number_input("Margen de error E (valor absoluto)", min_value=0.0001, max_value=0.5, value=0.001, step=0.0001, format="%.6f")
    N = st.number_input("Población finita N (0 = desconocida)", min_value=0, value=0, step=1)
    use_population = N > 0
    method = st.selectbox("Método para búsqueda de n (cuando aplique)", ["clásica", "wilson", "agresti-coull", "poisson", "exact"])
    lam_for_poisson = st.number_input("λ para Poisson (usado si método Poisson)", min_value=1.0, value=3.0, step=0.5)
    st.markdown("---")
    st.header("Datos / Ejemplos")
    st.write("La app incluye 2 ejemplos simulados: enfermedad rara y encuesta con p alto. Puedes subir tus propios CSV.")
    upload1 = st.file_uploader("Subir CSV para ejemplo 1 (opcional)", type=["csv"], key="up1")
    upload2 = st.file_uploader("Subir CSV para ejemplo 2 (opcional)", type=["csv"], key="up2")
    st.markdown("---")
    if st.button("Generar informe y Excel con resultados"):
        st.session_state.generate_report = True

# -------------------------
# Example datasets (simulados) OR cargar los tuyos
# -------------------------
@st.cache_data
def generate_simulated_datasets():
    rng = np.random.default_rng(seed=12345)
    # Example 1: rare event, p=0.002, n=10000
    n1 = 10000
    p1 = 0.002
    data1 = rng.binomial(1, p1, n1)
    df1 = pd.DataFrame({"event": data1})
    df1["id"] = np.arange(1, n1+1)
    # Example 2: high prop p=0.92, n=1000
    n2 = 1000
    p2 = 0.92
    data2 = rng.binomial(1, p2, n2)
    df2 = pd.DataFrame({"event": data2})
    df2["id"] = np.arange(1, n2+1)
    return df1, df2

df1_sim, df2_sim = generate_simulated_datasets()

# Replace if uploaded
if upload1:
    try:
        df1 = pd.read_csv(upload1)
        st.sidebar.success("Ejemplo 1: CSV cargado correctamente.")
    except Exception as e:
        st.sidebar.error(f"Error leyendo CSV 1: {e}")
        df1 = df1_sim.copy()
else:
    df1 = df1_sim.copy()

if upload2:
    try:
        df2 = pd.read_csv(upload2)
        st.sidebar.success("Ejemplo 2: CSV cargado correctamente.")
    except Exception as e:
        st.sidebar.error(f"Error leyendo CSV 2: {e}")
        df2 = df2_sim.copy()
else:
    df2 = df2_sim.copy()

# Assume columns: either 'event' (0/1) or a single column
def ensure_event_col(df):
    if "event" in df.columns:
        return df[["id","event"]] if "id" in df.columns else df[["event"]]
    # try first numeric column
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            return pd.DataFrame({"event": df[c].astype(int)})
    # fallback: create zeros
    return pd.DataFrame({"event": np.zeros(len(df), dtype=int)})

df1_clean = ensure_event_col(df1)
df2_clean = ensure_event_col(df2)

# -------------------------
# Show datasets and quick stats
# -------------------------
st.header("💾 Bases de datos (Ejemplos)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Ejemplo 1 — Evento raro (simulado o cargado)")
    st.dataframe(df1_clean.head(100))
    c1_count = df1_clean["event"].sum()
    st.markdown(f"- Observaciones: **{len(df1_clean)}**  \n- Eventos (sum): **{c1_count}**  \n- Proporción empírica: **{c1_count/len(df1_clean):.6f}**")
with col2:
    st.subheader("Ejemplo 2 — Proporción muy alta (simulado o cargado)")
    st.dataframe(df2_clean.head(100))
    c2_count = df2_clean["event"].sum()
    st.markdown(f"- Observaciones: **{len(df2_clean)}**  \n- Eventos (sum): **{c2_count}**  \n- Proporción empírica: **{c2_count/len(df2_clean):.6f}**")

# -------------------------
# Interactive charts
# -------------------------
st.header("📈 Visualizaciones")

colA, colB = st.columns(2)
with colA:
    st.subheader("Histograma — Ejemplo 1")
    fig1 = px.histogram(df1_clean, x="event", title="Distribución de eventos (Ejemplo 1)", labels={"event":"Evento (0/1)"})
    st.plotly_chart(fig1, use_container_width=True)
with colB:
    st.subheader("Histograma — Ejemplo 2")
    fig2 = px.histogram(df2_clean, x="event", title="Distribución de eventos (Ejemplo 2)", labels={"event":"Evento (0/1)"})
    st.plotly_chart(fig2, use_container_width=True)

# Varianza vs p plot
st.subheader("Varianza teórica p(1-p) vs p")
p_values = np.linspace(0,1,201)
var_values = p_values*(1-p_values)
fig_var = px.line(x=p_values, y=var_values, title="Varianza teórica de una proporción", labels={"x":"p","y":"p(1-p)"})
st.plotly_chart(fig_var, use_container_width=True)

# -------------------------
# Calculations
# -------------------------
st.header("🧮 Cálculos de tamaño de muestra (en tiempo real)")

colL, colR = st.columns([1,1])
with colL:
    st.subheader("Parámetros")
    st.write(f"- Nivel de confianza: **{conf}%** (Z = {z:.4f})")
    st.write(f"- Proporción esperada p: **{p_input:.6f}**")
    st.write(f"- Margen de error E: **{E:.6f}**")
    st.write(f"- Población total N: **{int(N) if use_population else 'Desconocida'}**")
    st.write(f"- Método seleccionado: **{method}**")

with colR:
    st.subheader("Resultados rápidos")
    # Classical
    n0 = classical_n(p_input, E, z)
    n0_ceil = ceil(n0)
    n_corr = finite_population_correction(n0, N) if use_population else n0
    n_corr_ceil = ceil(n_corr)
    st.write(f"Fórmula clásica (n0): **{n0:.2f}** → redondeo **{n0_ceil}**")
    if use_population:
        st.write(f"Con corrección por población finita: **{n_corr:.2f}** → redondeo **{n_corr_ceil}**")
    # Other methods
    if method == 'poisson':
        n_poisson = poisson_n(p_input, lam_for_poisson)
        st.write(f"Poisson (n = λ / p) con λ={lam_for_poisson}: **{n_poisson:.2f}** → redondeo **{ceil(n_poisson)}**")
    elif method in ['wilson','agresti-coull','exact']:
        st.write("Buscando n mínimo (proceso iterativo). Esto puede tardar unos segundos...")
        n_found = find_min_n_by_halfwidth(p_input, E, z, method=method, max_n=200000)
        if n_found:
            st.write(f"n mínimo encontrado ({method}): **{n_found}**")
        else:
            st.write("No se encontró n hasta el límite (200000). Ajusta parámetros.")

# Show formulas and step-by-step
st.header("📐 Fórmulas y explicación paso a paso")
st.markdown("**Fórmula clásica** (usada como referencia):")
st.latex(r"n_0 = \frac{Z^2 \, p (1-p)}{E^2}")
if use_population:
    st.markdown("**Corrección por población finita**:")
    st.latex(r"n = \frac{n_0}{1 + \frac{n_0}{N}}")

st.markdown("**Wilson interval half-width (se usa para buscar n con método 'wilson'):**")
st.latex(r"\text{halfwidth} \approx z \frac{\sqrt{\hat p(1-\hat p)/n + z^2/(4n^2)}}{1 + z^2/n}")

st.markdown("**Agresti–Coull (ajuste):**")
st.latex(r"\tilde p = \frac{x + z^2/2}{n + z^2} \quad ; \quad \text{halfwidth} \approx z\sqrt{\frac{\tilde p(1-\tilde p)}{n + z^2}}")

st.markdown("**Poisson (eventos raros):**")
st.latex(r"n \approx \frac{\lambda}{p} \quad (\lambda \text{ elegido, e.g. } 3 \text{ para confianza alta})")

# -------------------------
# Excel export (create in-memory)
# -------------------------
def create_excel_bytes(df1, df2, results_summary, figs=None):
    import pandas as pd
    from io import BytesIO
    import xlsxwriter
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name="Example1_Data", index=False)
        df2.to_excel(writer, sheet_name="Example2_Data", index=False)
        pd.DataFrame(results_summary).to_excel(writer, sheet_name="Results_Summary", index=False)
        workbook = writer.book
        # Insert images if provided
        if figs:
            for name, fig_bytes in figs.items():
                worksheet = workbook.add_worksheet(name[:30])
                workbook.add_worksheet  # no-op to keep writer happy
                # Write image from bytes
                worksheet.insert_image('B2', name + ".png", {'image_data': fig_bytes})
    return output.getvalue()

if st.session_state.get("generate_report", False):
    # Prepare summary
    results_summary = {
        "method": [method],
        "p": [p_input],
        "E": [E],
        "confidence": [conf],
        "classical_n0": [n0_ceil],
        "corrected_n": [n_corr_ceil if use_population else None],
    }
    # create simple plots bytes
    figs = {}
    # example plots as bytes
    import matplotlib.pyplot as plt
    from io import BytesIO
    buf = BytesIO()
    fig, ax = plt.subplots()
    ax.hist(df1_clean["event"], bins=2)
    ax.set_title("Ejemplo1_hist")
    fig.savefig(buf, format='png')
    buf.seek(0)
    figs["example1_hist"] = buf
    buf2 = BytesIO()
    fig2, ax2 = plt.subplots()
    ax2.hist(df2_clean["event"], bins=2)
    ax2.set_title("Ejemplo2_hist")
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    figs["example2_hist"] = buf2

    excel_bytes = create_excel_bytes(df1_clean, df2_clean, results_summary, figs)
    st.success("Informe preparado. Descarga el Excel con datos y resumen.")
    st.download_button("Descargar Excel (dashboard)", excel_bytes, file_name="sample_size_dashboard.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# -------------------------
# Presentation notes and script
# -------------------------
st.header("📝 Guion para tu exposición (lista para leer)")
st.markdown("""
**Introducción breve (30s):** explicar qué es una proporción poblacional y por qué p muy pequeña/ grande es un caso especial.

**Problema central:** la fórmula clásica se basa en aproximación normal; cuando p<0.10 o p>0.90 se rompen las condiciones np>=5 y n(1-p)>=5.

**Métodos revisados:**
- Fórmula clásica (mostrar)
- Corrección población finita (mostrar)
- Wilson y Agresti-Coull (explicar idea)
- Poisson para eventos raros
- Método exacto binomial (cuando hay pocos éxitos observados)

**Ejemplos reales:** describir los ejemplos (se muestran en el panel).
**Interpretación de resultados:** mostrar que la clásica subestima en casos extremos y que Wilson/Agresti corrigen.
**Conclusión:** resumir recomendaciones prácticas.

Puedes copiar y pegar esto en tus diapositivas.
""")
st.markdown("---")
st.caption("App creada para fines educativos. Revisa parámetros y usa datos reales para decisiones de muestreo en investigación.")
