import streamlit as st
import numpy as np

st.header("🌟 Ejemplos completos — Eventos raros y tamaño muestral")

tab1, tab2 = st.tabs(["🌟 Ejemplo 1: Enfermedad rara", "🌟 Ejemplo 2: Falla química rara"])


# ============================================================
# =================== EJEMPLO 1 ================================
# ============================================================

with tab1:
    st.subheader("🌟 EJEMPLO 1 — Prevalencia de una enfermedad rara (p = 0.008)")
    st.markdown("### 🔷 Contexto")
    st.write("""
Un hospital quiere estimar la proporción de pacientes que presentan **tuberculosis multirresistente (TB-MDR)**.

Estudios previos indican una prevalencia:
""")

    # -----------------------------
    # VALORES INTERACTIVOS (Z, E, p)
    # -----------------------------

    p = st.number_input("Valor de p (proporción esperada)", min_value=0.0001, max_value=1.0,
                        value=0.008, step=0.0005, format="%.4f")
    Z = st.number_input("Valor Z", min_value=1.0, max_value=3.0, value=1.96, step=0.01)
    E = st.number_input("Error máximo E", min_value=0.001, max_value=0.2,
                        value=0.01, step=0.001, format="%.3f")

    st.latex(rf"p = {p} \quad ({p*100:.2f}\%)")

    # -----------------------------
    # ALERTA según p
    # -----------------------------
    if p < 0.10:
        st.info("🔵 **p es muy pequeño:** es un evento raro, la varianza es muy baja y NO se debe usar p=0.5.")
    elif p > 0.90:
        st.warning("🟠 **p está por encima de 0.9:** evento casi seguro, también la varianza es muy pequeña.")
    else:
        st.error("🔴 **p no es extremo:** usar esta fórmula con p=0.5 puede ser correcto para máxima varianza.")

    st.write("""
Este es un **evento raro**.

El investigador quiere:
- Error máximo: **E = 0.01**
- Confianza: **Z = 1.96**
""")

    st.markdown("### 1️⃣ Varianza máxima en p = 0.5 (problema que causa)")

    st.latex(rf"n = \frac{{{Z}^2 (0.5)(0.5)}}{{{E}^2}}")
    n1 = (Z**2 * 0.25) / (E**2)
    st.latex(rf"n = {int(n1)}")

    st.write("Interpretación:")
    st.latex(rf"p(1-p) = {p}({1-p}) = {p*(1-p):.6f}")

    st.info(f"La varianza real es **{0.25/(p*(1-p)):.1f} veces más pequeña**, así que {int(n1)} sería un enorme desperdicio.")

    st.markdown("### 2️⃣ Ajuste usando la proporción real (p < 0.10)")

    st.latex(rf"n = \frac{{{Z}^2 ({p})({1-p})}}{{{E}^2}}")

    n2 = (Z**2 * p * (1 - p)) / (E**2)
    st.latex(rf"n = {int(n2)}")

    st.success(f"✔ **Conclusión del ajuste:** el tamaño muestral correcto es **{int(n2)}**, no **{int(n1)}**.")

    st.markdown("### 3️⃣ Ecuación alternativa usando p(1−p) ≈ p")
    st.latex(r"p(1-p) \approx p")
    st.latex(rf"n \approx \frac{{{Z}^2 ({p})}}{{{E}^2}}")

    naprox = (Z**2 * p) / (E**2)
    st.latex(rf"n \approx {int(naprox)}")

    st.markdown("### ✔ Conclusión del ejemplo 1")
    st.write(f"""
- Usar p = 0.5 habría requerido una muestra absurda (**{int(n1)}**).  
- El ajuste correcto da **{int(n2)}**.  
- La aproximación da **{int(naprox)}**, muy cercana.  

La técnica es **crucial en epidemiología de enfermedades poco frecuentes**.
""")


# ============================================================
# =================== EJEMPLO 2 ================================
# ============================================================

with tab2:
    st.subheader("🌟 EJEMPLO 2 — Estudio de falla muy rara en reactor químico (p = 0.002)")
    st.markdown("### 🔷 Contexto")
    st.write("""
Una empresa química quiere estimar la proporción de reacciones con aumento peligroso de temperatura.

Historial:
""")

    # -----------------------------
    # VALORES INTERACTIVOS
    # -----------------------------
    p2 = st.number_input("Valor de p (proporción esperada) - Ejemplo 2", min_value=0.0001, max_value=1.0,
                         value=0.002, step=0.0005, format="%.4f")
    Z2 = st.number_input("Valor Z - Ejemplo 2", min_value=1.0, max_value=3.0,
                         value=1.96, step=0.01)
    E2 = st.number_input("Error máximo E - Ejemplo 2", min_value=0.001, max_value=0.2,
                         value=0.005, step=0.001, format="%.3f")

    st.latex(rf"p = {p2} \quad ({p2*100:.2f}\%)")

    # Alertas inteligentes
    if p2 < 0.10:
        st.info("🔵 **Evento extremadamente raro:** p < 0.10 → varianza muy pequeña.")
    elif p2 > 0.90:
        st.warning("🟠 **Evento casi seguro:** p > 0.90 → varianza casi cero.")
    else:
        st.error("🔴 p no es extremo → p=0.5 podría ser apropiado para máxima varianza.")

    st.write("""
Evento extremadamente raro.

Se desea:
- Error **E = 0.005**
- Confianza **Z = 1.96**
""")

    st.markdown("### 1️⃣ Varianza máxima (uso incorrecto p=0.5)")
    st.latex(rf"n = \frac{{{Z2}^2 (0.25)}}{{{E2}^2}}")

    n1_2 = (Z2**2 * 0.25) / (E2**2)
    st.latex(rf"n = {int(n1_2)}")

    st.write("Varianza real del proceso:")
    st.latex(rf"p(1-p) = {p2}({1-p2}) = {p2*(1-p2):.6f}")

    st.info(f"La varianza real es **{0.25/(p2*(1-p2)):.1f} veces menor** que 0.25.")

    st.markdown("### 2️⃣ Ajuste usando la proporción real")
    st.latex(rf"n = \frac{{{Z2}^2 ({p2})({1-p2})}}{{{E2}^2}}")
    n2_2 = (Z2**2 * p2 * (1 - p2)) / (E2**2)
    st.latex(rf"n = {int(n2_2)}")

    st.success(f"✔ **Conclusión:** la muestra correcta es **{int(n2_2)}**, no **{int(n1_2)}**.")

    st.markdown("### 3️⃣ Ecuación alternativa (p ≈ p(1−p))")
    st.latex(rf"n \approx \frac{{{Z2}^2 ({p2})}}{{{E2}^2}}")

    naprox2 = (Z2**2 * p2) / (E2**2)
    st.latex(rf"n \approx {int(naprox2)}")

    st.markdown("### ✔ Conclusión del ejemplo 2")
    st.write(f"""
- Usar p = 0.5 produjo una sobreestimación absurda (**{int(n1_2)}**).  
- Usar p real da **{int(n2_2)}**.  
- La aproximación da **{int(naprox2)}**.  

Es esencial para **seguridad industrial y confiabilidad** en sistemas críticos.
""")
