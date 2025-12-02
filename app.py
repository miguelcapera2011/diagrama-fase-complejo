# ============================================================
# APP STREAMLIT PROFESIONAL – Punto 6: Proporciones extremas
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------
st.set_page_config(
    page_title="Tamaño muestral: Proporciones extremas",
    layout="wide"
)

st.title("📊 Punto 6 – Tamaño muestral para proporciones extremas")
st.caption("Aplicación profesional para exposición: teoría + interacción + ejemplos reales.")

# ----------------------------------------------------------
# BARRA LATERAL – Navegación
# ----------------------------------------------------------
menu = st.sidebar.radio(
    "Secciones del Punto 6",
    [
        "6.1 Varianza máxima (p=0.5)",
        "6.2 Ajustes cuando p es extrema",
        "6.3 Alternativa (Poisson)",
        "6.4 Aplicaciones (eventos raros)"
    ]
)

# ----------------------------------------------------------
# SECCIÓN 6.1 – VARIANZA MÁXIMA
# ----------------------------------------------------------
if menu == "6.1 Varianza máxima (p=0.5)":
    st.header("6.1 ¿Por qué la máxima varianza ocurre en p = 0.5?")
    
    st.markdown("""
    La varianza de una proporción está dada por:
    
    \\[
    Var(\\hat p)=\\frac{p(1-p)}{n}
    \\]
    
    Ignorando **n**, la forma importante es:
    
    \\[
    p(1-p)
    \\]
    
    Esta expresión es una **parábola invertida**, y su valor máximo ocurre cuando la curva cambia de crecimiento a decrecimiento:  
    es decir, en **p = 0.5**.
    
    ### 🎯 Interpretación para la exposición
    - Cuando **p = 0.5**, existe máxima incertidumbre (mitad éxitos / mitad fracasos).  
    - Por eso, la **fórmula clásica del tamaño muestral usa p = 0.5** cuando no se conoce p.
    - Si p es muy extrema (muy pequeña o muy grande), la varianza disminuye drásticamente.
    """)

    # Interacción con la gráfica
    st.subheader("Gráfica interactiva de la varianza p(1-p)")

    p_point = st.slider("Seleccione un valor de p:", 0.0, 1.0, 0.5, 0.01)

    p_vals = np.linspace(0, 1, 300)
    var_vals = p_vals * (1 - p_vals)

    fig, ax = plt.subplots()
    ax.plot(p_vals, var_vals)
    ax.scatter([p_point], [p_point*(1-p_point)], s=100)

    ax.set_xlabel("p")
    ax.set_ylabel("Varianza p(1-p)")
    ax.axvline(0.5, color="red", linestyle="--")
    ax.set_title("Varianza según p")

    st.pyplot(fig)

    st.info(f"Con p = {p_point}, la varianza es: {round(p_point*(1-p_point),4)}")

# ----------------------------------------------------------
# SECCIÓN 6.2 – AJUSTES PARA p EXTREMA
# ----------------------------------------------------------
elif menu == "6.2 Ajustes cuando p es extrema":
    st.header("6.2 Ajustes cuando p < 0.10 o p > 0.90")
    
    st.markdown("""
    Cuando la proporción esperada es **muy pequeña** o **muy grande**, la fórmula clásica:
    
    \\[
    n = \\frac{z^2 p(1-p)}{d^2}
    \\]
    
    tiende a **sobreestimar** el tamaño muestral porque p(1-p) se vuelve demasiado pequeño.  
    Para corregir esto se usa un ajuste:
    
    - si p < 0.05 → usar p = 0.05  
    - si p > 0.95 → usar p = 0.95  
    
    🎯 Este ajuste estabiliza la varianza y evita muestras innecesariamente grandes.
    """)

    st.subheader("Cálculo interactivo")

    col1, col2, col3 = st.columns(3)

    with col1:
        p = st.number_input("Proporción esperada (p)", 0.0001, 0.9999, 0.02)
    with col2:
        z = st.number_input("Valor z", value=1.96)
    with col3:
        d = st.number_input("Margen de error", value=0.01)

    # Fórmula clásica
    n_clasico = z**2 * p * (1 - p) / d**2

    # Ajuste
    p_adj = max(min(p, 0.95), 0.05)
    n_ajustado = z**2 * p_adj * (1 - p_adj) / d**2

    st.write(f"🔵 **Tamaño muestral clásico:** {round(n_clasico,2)}")
    st.write(f"🟢 **Tamaño muestral ajustado:** {round(n_ajustado,2)}")
    st.write(f"⚙️ **Valor de p usado tras el ajuste:** {p_adj}")

    if p < 0.05 or p > 0.95:
        st.warning("p es extrema → Se aplicó ajuste.")
    else:
        st.info("p está en rango → No se aplicó ajuste.")

# ----------------------------------------------------------
# SECCIÓN 6.3 – MODELO POISSON
# ----------------------------------------------------------
elif menu == "6.3 Alternativa (Poisson)":
    st.header("6.3 Alternativa para evitar sobreestimación: Poisson")

    st.markdown("""
    Para eventos muy raros (p < 0.05), la distribución binomial se aproxima a una **Poisson**, lo cual permite un cálculo más estable:
    
    \\[
    n = \\frac{z^2 \\, \\lambda}{d^2}
    \\]
    
    Donde:
    - \\( \\lambda ≈ p \\) cuando los eventos son muy raros  
    - La varianza es igual a la media → más estable para muestras pequeñas
    
    ### 🎯 Ventaja para la exposición:
    - Este método evita tamaños muestrales exagerados cuando p es muy baja.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        lam = st.number_input("λ (≈ p si evento es raro)", 0.000001, 1.0, 0.01)
    with col2:
        z2 = st.number_input("Valor z", value=1.96)
    with col3:
        d2 = st.number_input("Margen de error", value=0.005)

    n_poisson = z2**2 * lam / d2**2

    st.write(f"🟣 **Tamaño muestral usando Poisson:** {round(n_poisson,2)}")

    st.info("Este método es ideal cuando p < 0.05 (eventos muy poco frecuentes).")

# ----------------------------------------------------------
# SECCIÓN 6.4 – APLICACIONES REALES (EVENTOS RAROS)
# ----------------------------------------------------------
elif menu == "6.4 Aplicaciones (eventos raros)":
    st.header("6.4 Aplicaciones reales de eventos raros")
    st.write("""
    A continuación se presentan **dos estudios reales** donde los eventos son extremadamente raros  
    y por eso se utilizan los métodos de los incisos 6.1, 6.2 y 6.3.
    
    Cada ejemplo aplica directamente las fórmulas calculadas en las secciones anteriores.
    """)

    ejemplo = st.selectbox(
        "Seleccione un caso real:",
        ["Anafilaxia por vacunas", "Falla catastrófica de turbinas de avión"]
    )

    if ejemplo == "Anafilaxia por vacunas":
        st.subheader("Ejemplo 1 — Anafilaxia por vacunas (muy raro)")
        
        st.markdown("""
        La anafilaxia post-vacuna ocurre en **1 a 5 casos por millón**.  
        Esto corresponde a **p ≈ 0.000001 – 0.000005** → evento rarísimo.
        
        ⭐ **Modelo recomendado:** Poisson (inciso 6.3).  
        ⭐ **Problema:** la fórmula clásica daría tamaños monstruosamente grandes.
        """)

        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Vaccine_types_diagram.svg/640px-Vaccine_types_diagram.svg.png")

        # Interacción
        lam2 = st.number_input("λ realista (casos por millón → divida entre 1e6)", 0.000001, 0.001, 0.000003)

        n_calc = (1.96**2) * lam2 / (0.0005**2)

        st.success(f"Tamaño muestral estimado (Poisson): {round(n_calc,2)} personas")
    
    else:
        st.subheader("Ejemplo 2 — Falla catastrófica en turbinas")
        st.markdown("""
        Frecuencia real: **1 evento por cada 10 millones de horas de vuelo.**
        
        Esto equivale a:
        
        \\[
        p = 0.0000001
        \\]
        
        ⭐ Su varianza es tan extrema que se utiliza **Poisson** para estimaciones de riesgo.  
        """)
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Jet_engine_diagram.svg/640px-Jet_engine_diagram.svg.png")

        lam3 = st.number_input("λ por hora de vuelo (≈ p)", 0.00000001, 0.00001, 0.0000001)

        n_calc2 = (1.96**2) * lam3 / (0.0001**2)

        st.success(f"Tamaño muestral estimado (Poisson): {round(n_calc2,2)} horas de vuelo")

st.divider()

st.caption("App profesional — diseñada para exposición académica sobre muestreo.")
