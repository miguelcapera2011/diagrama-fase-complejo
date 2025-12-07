import streamlit as st
import numpy as np

# ============================================
# 🎄 DECORACIÓN NAVIDEÑA (Luces animadas)
# ============================================

st.markdown("""
<style>
/* Contenedor superior */
.christmas-lights {
  position: relative;
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 15px;
}

/* Bombillos */
.bulb {
  width: 18px;
  height: 28px;
  border-radius: 50%;
  animation: blink 1.4s infinite alternate;
  box-shadow: 0 0 6px rgba(255, 255, 255, 0.6);
}

/* Colores */
.red { background: #ff4b4b; animation-delay: 0s; }
.green { background: #2ecc71; animation-delay: 0.3s; }
.blue { background: #3498db; animation-delay: 0.6s; }
.yellow { background: #f1c40f; animation-delay: 0.9s; }

/* Animación de encendido/apagado */
@keyframes blink {
  0% { opacity: 0.2; transform: scale(0.9); }
  100% { opacity: 1; transform: scale(1.2); }
}
</style>

<div class="christmas-lights">
  <div class="bulb red"></div>
  <div class="bulb green"></div>
  <div class="bulb blue"></div>
  <div class="bulb yellow"></div>
  <div class="bulb red"></div>
  <div class="bulb green"></div>
  <div class="bulb blue"></div>
  <div class="bulb yellow"></div>
</div>
""", unsafe_allow_html=True)



# ============================================================
#  APP
# ============================================================

st.header("🌟 Ejemplos completos — Eventos raros y tamaño muestral")

tab1, tab2 = st.tabs(["🌟 Ejemplo 1: Enfermedad rara", "🌟 Ejemplo 2: Falla química rara"])


# ============================================================
# =================== EJEMPLO 1 ==============================
# ============================================================

with tab1:
    st.subheader("🌟 EJEMPLO 1 — Prevalencia de una enfermedad rara (p = 0.008)")
    st.markdown("### 🔷 Contexto")
    st.write(r"""
Un hospital quiere estimar la proporción de pacientes que presentan **tuberculosis multirresistente (TB-MDR)**.

Estudios previos indican una prevalencia:

\[
p = 0.008 \quad (0.8\%)
\]

Este es un **evento raro**.

El investigador quiere:

- Error máximo: \(E = 0.01\)
- Confianza: \(Z = 1.96\)
""")

    st.markdown("### 1️⃣ Varianza máxima en p = 0.5 (problema que causa)")

    st.latex(r"n = \frac{1.96^2 (0.5)(0.5)}{0.01^2}")
    n1 = (1.96**2 * 0.25) / (0.01**2)
    st.latex(r"n = 9604")

    st.write("Interpretación:")
    st.latex(r"p(1-p) = 0.008(0.992) = 0.007936")

    st.info("La varianza real es **31 veces más pequeña**, así que 9604 es un enorme desperdicio de recursos.")

    st.markdown("### 2️⃣ Ajuste usando la proporción real (p < 0.10)")

    st.latex(r"n = \frac{1.96^2 (0.008)(0.992)}{0.01^2}")

    n2 = (1.96**2 * 0.008 * (1 - 0.008)) / (0.01**2)
    st.latex(r"n = 304")

    st.success("✔ **Conclusión del ajuste:** el tamaño muestral correcto es **304**, no **9604**.")

    st.markdown("### 3️⃣ Ecuación alternativa usando p(1−p) ≈ p")
    st.latex(r"p(1-p) \approx p")
    st.latex(r"n \approx \frac{1.96^2 (0.008)}{0.01^2}")
    st.latex(r"n \approx 307")

    st.markdown("### ✔ Conclusión del ejemplo 1")
    st.write("""
- Usar p = 0.5 habría requerido una muestra absurda (**9604**).  
- El ajuste correcto da **304**.  
- La aproximación da **307**, muy cercana.  

La técnica es **crucial en epidemiología de enfermedades poco frecuentes**.
""")


# ============================================================
# =================== EJEMPLO 2 ================================
# ============================================================

with tab2:
    st.subheader("🌟 EJEMPLO 2 — Estudio de falla muy rara en reactor químico (p = 0.002)")
    st.markdown("### 🔷 Contexto")
    st.write(r"""
Una empresa química quiere estimar la proporción de reacciones con aumento peligroso de temperatura.

Historial:

\[
p = 0.002 \quad (0.2\%)
\]

Evento extremadamente raro.

Se desea:

- Error \(E = 0.005\)
- Confianza \(Z = 1.96\)
""")

    st.markdown("### 1️⃣ Varianza máxima (uso incorrecto p=0.5)")
    st.latex(r"n = \frac{1.96^2 (0.25)}{0.005^2}")

    n1 = (1.96**2 * 0.25) / (0.005**2)
    st.latex(r"n = 38416")

    st.write("Varianza real del proceso:")
    st.latex(r"p(1-p) = 0.002(0.998) = 0.001996")

    st.info("La varianza real es **125 veces menor** que 0.25.")

    st.markdown("### 2️⃣ Ajuste usando la proporción real")
    st.latex(r"n = \frac{1.96^2 (0.002)(0.998)}{0.005^2}")
    st.latex(r"n = 307")

    st.success("✔ **Conclusión:** la muestra correcta es **307 observaciones**, no **38.416**.")

    st.markdown("### 3️⃣ Ecuación alternativa (p ≈ p(1−p))")
    st.latex(r"n \approx \frac{1.96^2 (0.002)}{0.005^2}")
    st.latex(r"n \approx 302")

    st.markdown("### ✔ Conclusión del ejemplo 2")
    st.write("""
- Usar p = 0.5 produjo una sobreestimación absurda (**38416**).  
- Usar p real da **307**.  
- La aproximación da **302**.  

Es esencial para **seguridad industrial y confiabilidad** en sistemas críticos.
""")
