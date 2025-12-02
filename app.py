# app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# --------------------------------------------------------
# Configuración de la página
# --------------------------------------------------------
st.set_page_config(
    page_title="Dashboard: Tamaño Muestral para Proporciones (Eventos Raros)",
    layout="wide"
)

# Título general
st.title("Dashboard — Tamaño muestral para proporciones (eventos raros)")
st.write(
    "Calcula y compara tamaños muestrales cuando se espera una proporción muy pequeña o muy grande. "
    "Incluye métodos alternativos para evitar sobreestimación y dos ejemplos de la vida real."
)

# --------------------------------------------------------
# Funciones estadísticas: diferentes fórmulas
# --------------------------------------------------------
def n_classic(Z, p, d):
    """Fórmula clásica: n = Z^2 * p(1-p) / d^2"""
    p = float(p)
    return (Z**2) * p * (1 - p) / (d**2)

def n_conservative(Z, d):
    """Conservador: asume p=0.5 cuando p desconocida -> máximo varianza"""
    p = 0.5
    return (Z**2) * p * (1 - p) / (d**2)

def n_poisson_approx(Z, p, d):
    """
    Aproximación Poisson para eventos raros.
    Derivado de Var(X)=np -> tamaño n ≈ Z^2 / (d^2 * p)
    (útil cuando p muy pequeño, p < ~0.01)
    """
    p = max(p, 1e-12)
    return (Z**2) / (d**2 * p)

def n_relative_error(Z, p, rel_error):
    """
    Tamaño muestral usando margen de error relativo dr = d/p:
    n = Z^2 (1-p) / (p * dr^2)
    donde dr = rel_error (ej: 0.2 = 20% relativo)
    """
    p = float(p)
    dr = float(rel_error)
    return (Z**2) * (1 - p) / (p * (dr**2))

def agresti_coull_estimate(Z, p, d):
    """
    Fórmula informal que aplica corrección tipo Agresti-Coull.
    No es una fórmula estándar exacta para n, pero ajusta p hacia el centro.
    Implementaremos: p_adj = (p + z^2/(2*n_guess)) / (1 + z^2/n_guess)
    Para evitar dependencia circular, hacemos una iteración simple:
    1) n0 = classic
    2) p_adj = (x + z^2/2) / (n0 + z^2)  -- using x = p*n0
    3) recompute n with p_adj
    """
    # step 1: initial guess
    n0 = n_classic(Z, p, d)
    if n0 <= 0:
        return n0
    x0 = p * n0
    z2 = Z**2
    p_adj = (x0 + z2/2) / (n0 + z2)
    # second estimate
    n1 = n_classic(Z, p_adj, d)
    return n1

# --------------------------------------------------------
# Datos internos / ejemplos de la vida real
# --------------------------------------------------------
# Ejemplo 1: Prevalencia enfermedad rara (países)
df_disease = pd.DataFrame({
    "pais": ["Colombia", "México", "Perú"],
    "casos_reportados": [40, 120, 18],
    "poblacion": [50_000_000, 130_000_000, 33_000_000]
})
df_disease["prevalencia"] = df_disease["casos_reportados"] / df_disease["poblacion"]

# Ejemplo 2: Defectos en fábrica (microchips)
df_factory = pd.DataFrame({
    "lote": ["L1", "L2", "L3"],
    "produccion": [10000, 15000, 20000],
    "defectuosos": [3, 6, 5]
})
df_factory["proporcion"] = df_factory["defectuosos"] / df_factory["produccion"]

# --------------------------------------------------------
# Layout: dos columnas arriba para controles generales y explicaciones
# --------------------------------------------------------
st.markdown("---")
colA, colB = st.columns([2, 1])

with colA:
    st.header("Parámetros globales")
    Z_global = st.selectbox("Nivel de confianza Z (global)", [1.64, 1.96, 2.58], index=1, key="Z_global")
    method_help = st.selectbox(
        "Método recomendado por defecto para proporciones extremas",
        ["Clásico (p conocido)", "Conservador p=0.5", "Aproximación Poisson", "Error relativo", "Agresti–Coull (iterativo)"],
        index=2,
        key="method_global"
    )

with colB:
    st.header("Explicación breve")
    st.write(
        "• La varianza de una proporción es p(1-p). Es máxima en p=0.5.\n\n"
        "• Cuando p < 0.10 ó p > 0.90, la fórmula clásica puede dar tamaños sobreestimados.\n\n"
        "• Aquí puedes elegir distintos métodos y comparar resultados."
    )

st.markdown("---")

# --------------------------------------------------------
# TABS: ejemplo enfermedad, ejemplo fábrica, comparaciones
# --------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Enfermedad rara (países)", "Defectos fábrica (lotes)", "Comparador interactivo"])

# -----------------------
# TAB 1: Enfermedad rara
# -----------------------
with tab1:
    st.subheader("Ejemplo 1 — Prevalencia de enfermedad rara")
    st.write("Tabla de datos (internos). Puedes editar los valores si quieres simular otros escenarios.")

    # Mostrar y permitir edición rápida (editable copy)
    edit_df = st.checkbox("Editar tabla de prevalencias (editar en la cuadrícula)", key="edit_disease")
    if edit_df:
        df_disease_edit = st.experimental_data_editor(df_disease, key="disease_editor")
        df_disease = df_disease_edit.copy()
    st.dataframe(df_disease)

    st.markdown("**Cálculos automáticos por país**")
    st.write("Selecciona el país y el método para calcular el tamaño muestral.")

    col1, col2 = st.columns(2)
    with col1:
        pais_sel = st.selectbox("Selecciona país", df_disease["pais"].tolist(), key="pais_sel")
        row = df_disease[df_disease["pais"] == pais_sel].iloc[0]
        p_obs = float(row["prevalencia"])
        st.metric("Prevalencia observada (p̂)", f"{p_obs:.6f}")
    with col2:
        method1 = st.selectbox("Método (país)", ["Clásico", "Poisson", "Error relativo", "Agresti–Coull", "Conservador p=0.5"], index=1, key="method1")
        # parámetros
        if method1 == "Error relativo":
            rel_err = st.number_input("Error relativo deseado (ej: 0.2 = 20%)", min_value=0.01, max_value=2.0, value=0.2, step=0.01, key="rel_err1")
        else:
            rel_err = None
        d_abs = st.number_input("Margen de error absoluto d (ej: 0.001)", min_value=1e-6, max_value=0.5, value=0.001, key="d1")
        Z1 = st.selectbox("Nivel Z (país)", [1.64, 1.96, 2.58], index=1, key="Z1")

    # Compute sizes
    if method1 == "Clásico":
        n_calc = n_classic(Z1, p_obs, d_abs)
    elif method1 == "Poisson":
        n_calc = n_poisson_approx(Z1, p_obs, d_abs)
    elif method1 == "Error relativo":
        n_calc = n_relative_error(Z1, p_obs, rel_err)
    elif method1 == "Agresti–Coull":
        n_calc = agresti_coull_estimate(Z1, p_obs, d_abs)
    else:  # conservador
        n_calc = n_conservative(Z1, d_abs)

    st.markdown("### Resultado")
    st.write(f"Para {pais_sel}: proporción = {p_obs:.6f}")
    st.write(f"Usando método **{method1}**, Z={Z1}, d={d_abs}" )
    st.success(f"Tamaño muestral recomendado (aprox.):  {int(np.ceil(n_calc)):,}")

    # Visual: comparación entre métodos para ese p
    st.markdown("### Comparación de métodos (misma p)")
    methods = ["Clásico", "Poisson", "Error relativo", "Agresti–Coull", "Conservador"]
    results = []
    for m in methods:
        if m == "Clásico":
            results.append(n_classic(Z1, p_obs, d_abs))
        elif m == "Poisson":
            results.append(n_poisson_approx(Z1, p_obs, d_abs))
        elif m == "Error relativo":
            # usar rel_err por defecto 0.2 si no definido
            results.append(n_relative_error(Z1, p_obs, 0.2))
        elif m == "Agresti–Coull":
            results.append(agresti_coull_estimate(Z1, p_obs, d_abs))
        else:
            results.append(n_conservative(Z1, d_abs))

    fig, ax = plt.subplots(figsize=(6,3))
    ax.bar(methods, results)
    ax.set_ylabel("Tamaño muestral (n)")
    ax.set_title(f"Comparación de tamaños muestrales — p={p_obs:.6f}")
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    st.pyplot(fig)

# -----------------------
# TAB 2: Defectos fábrica
# -----------------------
with tab2:
    st.subheader("Ejemplo 2 — Defectos en microchips (lotes)")
    st.write("Tabla de producción por lote. Selecciona un lote y calcula tamaños con distintos métodos.")

    edit_df2 = st.checkbox("Editar tabla de la fábrica (cuadrícula)", key="edit_factory")
    if edit_df2:
        df_factory_edit = st.experimental_data_editor(df_factory, key="factory_editor")
        df_factory = df_factory_edit.copy()
    st.dataframe(df_factory)

    col1, col2 = st.columns(2)
    with col1:
        lote_sel = st.selectbox("Selecciona lote", df_factory["lote"].tolist(), key="lote_sel")
        rowf = df_factory[df_factory["lote"] == lote_sel].iloc[0]
        p_lote = float(rowf["proporcion"])
        st.metric("Proporción observada (p̂)", f"{p_lote:.6f}")
    with col2:
        method2 = st.selectbox("Método (lote)", ["Clásico", "Poisson", "Error relativo", "Agresti–Coull", "Conservador p=0.5"], index=1, key="method2")
        if method2 == "Error relativo":
            rel_err2 = st.number_input("Error relativo deseado (ej: 0.25 = 25%)", min_value=0.01, max_value=2.0, value=0.25, step=0.01, key="rel_err2")
        else:
            rel_err2 = None
        d2 = st.number_input("Margen de error absoluto d (ej: 0.0005)", min_value=1e-6, max_value=0.5, value=0.001, key="d2")
        Z2 = st.selectbox("Nivel Z (lote)", [1.64, 1.96, 2.58], index=1, key="Z2")

    # compute
    if method2 == "Clásico":
        n2 = n_classic(Z2, p_lote, d2)
    elif method2 == "Poisson":
        n2 = n_poisson_approx(Z2, p_lote, d2)
    elif method2 == "Error relativo":
        n2 = n_relative_error(Z2, p_lote, rel_err2)
    elif method2 == "Agresti–Coull":
        n2 = agresti_coull_estimate(Z2, p_lote, d2)
    else:
        n2 = n_conservative(Z2, d2)

    st.markdown("### Resultado")
    st.write(f"Lote {lote_sel}: proporción = {p_lote:.6f}")
    st.write(f"Método **{method2}**, Z={Z2}, d={d2}")
    st.success(f"Tamaño muestral recomendado (aprox.):  {int(np.ceil(n2)):,}")

    # Visual: evolución n según p pequeña
    st.markdown("### Cómo varía n si p cambia (rango pequeño)")
    p_vals = np.linspace(max(1e-6, p_lote*0.1), max(1e-6, p_lote*5 + 1e-6), 200)
    n_vals_classic = [n_classic(Z2, pv, d2) for pv in p_vals]
    n_vals_poisson = [n_poisson_approx(Z2, pv, d2) for pv in p_vals]

    fig2, ax2 = plt.subplots(figsize=(6,3))
    ax2.plot(p_vals, n_vals_classic, label="Clásico")
    ax2.plot(p_vals, n_vals_poisson, label="Poisson approx", linestyle="--")
    ax2.set_xlabel("p (proporción)")
    ax2.set_ylabel("n requerido")
    ax2.set_title("n vs p (rango pequeño)")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)

# -----------------------
# TAB 3: Comparador interactivo
# -----------------------
with tab3:
    st.subheader("Comparador interactivo — Explora distintos p y métodos")
    st.write("Selecciona p manualmente (o toma una p observada de los ejemplos) y compara las fórmulas.")

    col1, col2 = st.columns(2)
    with col1:
        p_manual = st.number_input("Proporción p manual", min_value=1e-8, max_value=0.999999, value=0.001, step=1e-4, key="p_manual")
        Z3 = st.selectbox("Nivel Z (comparador)", [1.64, 1.96, 2.58], index=1, key="Z3")
        d3 = st.number_input("Margen de error absoluto d", min_value=1e-6, max_value=0.5, value=0.001, key="d3")
        rel_err3 = st.number_input("Error relativo (si usa)", min_value=0.01, max_value=2.0, value=0.25, step=0.01, key="rel_err3")
    with col2:
        st.markdown("Métodos disponibles:")
        st.write("- Clásico (p conocido)\n- Poisson (eventos raros)\n- Error relativo\n- Agresti–Coull\n- Conservador p=0.5")
        st.markdown("Resultado dinámico:")

    # compute all
    results = {
        "Clásico": n_classic(Z3, p_manual, d3),
        "Poisson": n_poisson_approx(Z3, p_manual, d3),
        "Error relativo": n_relative_error(Z3, p_manual, rel_err3),
        "Agresti–Coull": agresti_coull_estimate(Z3, p_manual, d3),
        "Conservador p=0.5": n_conservative(Z3, d3)
    }

    df_results = pd.DataFrame.from_dict(results, orient='index', columns=['n'])
    df_results['n_ceil'] = np.ceil(df_results['n']).astype(int)
    st.dataframe(df_results)

    fig3, ax3 = plt.subplots(figsize=(6,3))
    ax3.bar(df_results.index, df_results['n'])
    ax3.set_ylabel("n requerido")
    ax3.set_title(f"Comparación de métodos para p={p_manual:.6f}")
    ax3.grid(axis='y', linestyle='--', alpha=0.4)
    st.pyplot(fig3)

st.markdown("---")
st.info("Consejo práctico: cuando trabajes con proporciones muy pequeñas, revisa siempre el 'error relativo' y considera usar la aproximación de Poisson o métodos iterativos (Agresti–Coull) para evitar diseños sobredimensionados o muestras que produzcan 0 casos.")
