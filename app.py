import streamlit as st
import numpy as np

# ===========================================
#     🎄 SUPER DECORACIÓN NAVIDEÑA PREMIUM
# ===========================================

navidad_css = """
<style>

/* ---------------------------------------------------- */
/* 🎄 1. FONDO DEGRADADO NAVIDEÑO                       */
/* ---------------------------------------------------- */
.stApp {
    background: linear-gradient(135deg, #e8f7ff, #fff8f8, #e8fff3);
    background-attachment: fixed;
}

/* Bloque central translúcido */
.block-container {
    background: rgba(255, 255, 255, 0.80);
    padding: 2rem;
    border-radius: 18px;
    box-shadow: 0 0 25px rgba(0,0,0,0.20);
}

/* ---------------------------------------------------- */
/* 🎄 2. NIEVE ANIMADA                                   */
/* ---------------------------------------------------- */
@keyframes snow_fall {
    0% {background-position: 0px 0px;}
    100% {background-position: 0px 1000px;}
}
body::before {
    content: "";
    position: fixed;
    width: 100%; height: 100%;
    background-image: url('https://i.imgur.com/7eM7ZpP.png');
    background-size: contain;
    opacity: 0.22;
    pointer-events: none;
    animation: snow_fall 20s linear infinite;
    z-index: -1;
}

/* ---------------------------------------------------- */
/* 🎄 3. LUCES NAVIDEÑAS ANIMADAS EN LA PARTE SUPERIOR   */
/* ---------------------------------------------------- */
@keyframes blink {
    0%, 100% {opacity: 1;}
    50% {opacity: 0.3;}
}

.luces {
    width: 100%;
    text-align: center;
    margin-bottom: 10px;
}

.luces span {
    height: 14px;
    width: 14px;
    margin: 0 6px;
    display: inline-block;
    border-radius: 50%;
    animation: blink 1.2s infinite;
}

.l1 { background:#ff1a1a; animation-delay:0s; }
.l2 { background:#ffd700; animation-delay:0.2s; }
.l3 { background:#00e676; animation-delay:0.4s; }
.l4 { background:#29b6f6; animation-delay:0.6s; }
.l5 { background:#ff80ab; animation-delay:0.8s; }

/* ---------------------------------------------------- */
/* 🎄 4. RAMAS NAVIDEÑAS DECORATIVAS                    */
/* ---------------------------------------------------- */
.ramas {
    background-image: url('https://i.imgur.com/Y9M0Cqf.png');
    background-repeat: repeat-x;
    height: 90px;
    background-size: contain;
    margin-bottom: 15px;
}

/* ---------------------------------------------------- */
/* 🎄 5. ÁRBOL NAVIDEÑO EN LA ESQUINA                    */
/* ---------------------------------------------------- */
.arbol {
    position: fixed;
    bottom: 10px;
    right: 10px;
    width: 130px;
    opacity: 0.90;
    z-index: 10;
}

/* ---------------------------------------------------- */
/* 🎄 6. ESTRELLAS BRILLANDO                             */
/* ---------------------------------------------------- */
@keyframes starGlow {
    0%,100% {opacity: 0.7;}
    50% {opacity: 1;}
}
.star {
    position: fixed;
    width: 25px;
    animation: starGlow 2.5s ease-in-out infinite;
    z-index: 5;
}
.star1 { top: 40px; left: 40px; }
.star2 { top: 60px; right: 50px; }
.star3 { top: 160px; left: 120px; }

/* ---------------------------------------------------- */
/* 🎄 7. TABS NAVIDEÑOS PREMIUM                          */
/* ---------------------------------------------------- */
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.6);
    border-radius: 12px;
    margin-right: 8px;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background-color: #004d40 !important;
    color: white !important;
    box-shadow: 0 0 10px #004d40;
}

/* Títulos */
h1, h2, h3 {
    color: #004d40 !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.15);
}
</style>

<!-- LUCES ANIMADAS -->
<div class="ramas"></div>
<div class="luces">
    <span class="l1"></span><span class="l2"></span><span class="l3"></span>
    <span class="l4"></span><span class="l5"></span><span class="l1"></span>
    <span class="l2"></span><span class="l3"></span><span class="l4"></span>
</div>

<!-- ESTRELLAS -->
<img class="star star1" src="https://i.imgur.com/2nCt3Sbl.png">
<img class="star star2" src="https://i.imgur.com/2nCt3Sbl.png">
<img class="star star3" src="https://i.imgur.com/2nCt3Sbl.png">

<!-- ÁRBOL NAVIDEÑO -->
<img class="arbol" src="https://i.imgur.com/LxWwQYP.png">

"""

st.markdown(navidad_css, unsafe_allow_html=True)

# ============================================================
# 🎄 TU APP (SIN CAMBIAR LÓGICA)
# ============================================================

st.header("Eventos raros y tamaño muestral")

tab1, tab2 = st.tabs(["🌟 Aplicación #1: Enfermedad rara", "🌟 Aplicación #2: Falla química rara"])

# ===================================================================
# EJEMPLO 1
# ===================================================================
with tab1:
    st.subheader("Prevalencia de una enfermedad rara (p = 0.008)")
    st.markdown("Contexto")
    st.write("""
Un hospital quiere estimar la proporción de pacientes que presentan **tuberculosis multirresistente (TB-MDR)**.
""")

    p = st.number_input("Valor de p (proporción esperada)", min_value=0.0001, max_value=1.0,
                        value=0.008, step=0.0005, format="%.4f")
    Z = st.number_input("Valor Z", min_value=1.0, max_value=3.0, value=1.96, step=0.01)
    E = st.number_input("Error máximo E", min_value=0.001, max_value=0.2,
                        value=0.01, step=0.001, format="%.3f")

    st.latex(rf"p = {p} \quad ({p*100:.2f}\%)")

    if p < 0.10:
        st.info("🔵 **Evento raro** (p < 0.10): la varianza real es muy baja.")
    elif p > 0.90:
        st.warning("🟠 p > 0.90: evento casi seguro.")
    else:
        st.error("🔴 p no es extremo.")

    st.markdown("### 1️⃣ Varianza máxima p = 0.5")
    st.latex(rf"n = \frac{{{Z}^2 (0.25)}}{{{E}^2}}")
    n1 = (Z**2 * 0.25) / (E**2)
    st.latex(rf"n = {int(n1)}")

    st.markdown("### 2️⃣ Ajuste con p real")
    st.latex(rf"n = \frac{{{Z}^2 ({p})({1-p})}}{{{E}^2}}")
    n2 = (Z**2 * p * (1 - p)) / (E**2)
    st.latex(rf"n = {int(n2)}")

    st.success(f"✔ Tamaño correcto: {int(n2)}")

    st.markdown("### 3️⃣ Aproximación p(1-p) ≈ p")
    naprox = (Z**2 * p) / (E**2)
    st.latex(rf"n \approx {int(naprox)}")


# ===================================================================
# EJEMPLO 2
# ===================================================================
with tab2:
    st.subheader("Estudio de falla muy rara en reactor químico (p = 0.002)")

    p2 = st.number_input("Valor de p (proporción esperada) - Ejemplo 2", min_value=0.0001,
                         max_value=1.0, value=0.002, step=0.0005, format="%.4f")
    Z2 = st.number_input("Valor Z - Ejemplo 2", min_value=1.0, max_value=3.0,
                         value=1.96, step=0.01)
    E2 = st.number_input("Error máximo E - Ejemplo 2", min_value=0.001, max_value=0.2,
                         value=0.005, step=0.001, format="%.3f")

    st.latex(rf"p = {p2} \quad ({p2*100:.2f}\%)")

    if p2 < 0.10:
        st.info("🔵 Evento extremadamente raro.")
    elif p2 > 0.90:
        st.warning("🟠 p > 0.90: varianza casi cero.")
    else:
        st.error("🔴 p no es extremo.")

    st.markdown("### 1️⃣ Varianza máxima")
    n1_2 = (Z2**2 * 0.25) / (E2**2)
    st.latex(rf"n = {int(n1_2)}")

    st.markdown("### 2️⃣ Ajuste usando p real")
    n2_2 = (Z2**2 * p2 * (1 - p2)) / (E2**2)
    st.latex(rf"n = {int(n2_2)}")

    st.success(f"✔ Tamaño correcto: {int(n2_2)}")

    st.markdown("### 3️⃣ Aproximación")
    naprox2 = (Z2**2 * p2) / (E2**2)
    st.latex(rf"n \approx {int(naprox2)}")

