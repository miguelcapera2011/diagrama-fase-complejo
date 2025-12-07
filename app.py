import streamlit as st
import numpy as np

# ===========================================================
# 🎄 DECORACIÓN NAVIDEÑA ELEGANTE Y PROFESIONAL
# ===========================================================

st.markdown("""
<style>

body {
    margin: 0;
    padding: 0;
}

/* --- CONTENEDOR PRINCIPAL CON RAMAS --- */
.navidad-banner {
    position: relative;
    width: 100%;
    height: 170px;
    background: url('https://i.imgur.com/l2s8MnP.png') no-repeat center top;
    background-size: cover;
    overflow: hidden;
    border-bottom: 2px solid #d8d8d8;
    margin-bottom: 18px;
}

/* --- NIEVE ELEGANTE --- */
@keyframes nieve-caer {
    0% { transform: translateY(-20px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(200px) rotate(360deg); opacity: 0; }
}

.snowflake {
    position: absolute;
    top: -10px;
    font-size: 12px;
    color: #ffffff;
    opacity: 0.9;
    animation: nieve-caer linear infinite;
}

/* Distribución y tiempos diferentes */
.snowflake:nth-child(1) { left: 10%; animation-duration: 4s; }
.snowflake:nth-child(2) { left: 25%; animation-duration: 5s; }
.snowflake:nth-child(3) { left: 40%; animation-duration: 3.5s; }
.snowflake:nth-child(4) { left: 55%; animation-duration: 4.2s; }
.snowflake:nth-child(5) { left: 70%; animation-duration: 5.1s; }
.snowflake:nth-child(6) { left: 85%; animation-duration: 3.8s; }

/* --- LUCES FAIRY LIGHTS ELEGANTES --- */
.fairy-lights {
    position: absolute;
    bottom: 10px;
    width: 100%;
    display: flex;
    justify-content: center;
    gap: 14px;
}

.light {
    width: 10px;
    height: 10px;
    background: radial-gradient(circle, rgba(255,255,255,1), rgba(255,255,255,0));
    border-radius: 50%;
    animation: brillar 1.8s infinite alternate;
}

/* Animación de brillo suave */
@keyframes brillar {
    0% { opacity: 0.25; transform: scale(0.8); }
    100% { opacity: 1; transform: scale(1.3); }
}

/* Colores pastel elegantes */
.light:nth-child(1) { background: #ffe5e5; animation-delay: 0s; }
.light:nth-child(2) { background: #e5ffd9; animation-delay: 0.3s; }
.light:nth-child(3) { background: #d9e9ff; animation-delay: 0.6s; }
.light:nth-child(4) { background: #fff7d9; animation-delay: 0.9s; }
.light:nth-child(5) { background: #ffd9f7; animation-delay: 0.4s; }

</style>

<div class="navidad-banner">

    <!-- ❄️ NIEVE -->
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>

    <!-- ✨ LUCES SUAVES -->
    <div class="fairy-lights">
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
    </div>

</div>
""", unsafe_allow_html=True)
