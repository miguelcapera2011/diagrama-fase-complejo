import streamlit as st
import numpy as np

# ============================================
# 🎄 DECORACIÓN NAVIDEÑA PROFESIONAL
# ============================================

st.markdown("""
<style>

/* --- CONTENEDOR GENERAL DE DECORACIÓN --- */
.navidad-header {
    position: relative;
    width: 100%;
    height: 140px;
    background: url('https://i.imgur.com/XM3aQ2X.png') no-repeat center top; /* 🌲 Rama navideña PNG */
    background-size: cover;
    margin-bottom: 20px;
}

/* --- NIEVE ANIMADA --- */
@keyframes nieve {
    0% { transform: translateY(-10px); opacity: 1; }
    100% { transform: translateY(140px); opacity: 0; }
}

.snowflake {
    position: absolute;
    top: 0;
    color: white;
    font-size: 10px;
    opacity: 0.9;
    animation: nieve linear infinite;
}

/* Crear muchos copos */
.snowflake:nth-child(1) { left: 10%; animation-duration: 3s; }
.snowflake:nth-child(2) { left: 20%; animation-duration: 4s; }
.snowflake:nth-child(3) { left: 30%; animation-duration: 2.5s; }
.snowflake:nth-child(4) { left: 40%; animation-duration: 3.7s; }
.snowflake:nth-child(5) { left: 50%; animation-duration: 4.2s; }
.snowflake:nth-child(6) { left: 60%; animation-duration: 3.1s; }
.snowflake:nth-child(7) { left: 70%; animation-duration: 3.8s; }
.snowflake:nth-child(8) { left: 80%; animation-duration: 2.9s; }
.snowflake:nth-child(9) { left: 90%; animation-duration: 3.5s; }

/* --- LUCES NAVIDEÑAS --- */
.luces {
    position: absolute;
    bottom: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    gap: 12px;
}

.bombillo {
    width: 18px;
    height: 28px;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(255,255,255,0.4);
    animation: prender 1.5s infinite alternate;
}

/* Colores + retardos */
.rojo { background: #ff4b4b; animation-delay: 0s; }
.verde { background: #2ecc71; animation-delay: 0.3s; }
.azul { background: #3498db; animation-delay: 0.6s; }
.amarillo { background: #f1c40f; animation-delay: 0.9s; }

/* Efecto prender/apagar */
@keyframes prender {
    0% { opacity: 0.3; transform: scale(0.9); }
    100% { opacity: 1; transform: scale(1.25); }
}

</style>

<div class="navidad-header">

  <!-- ❄️ NIEVE -->
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>
  <div class="snowflake">❄</div>

  <!-- 🎄 LUCES -->
  <div class="luces">
      <div class="bombillo rojo"></div>
      <div class="bombillo verde"></div>
      <div class="bombillo azul"></div>
      <div class="bombillo amarillo"></div>
      <div class="bombillo rojo"></div>
      <div class="bombillo verde"></div>
      <div class="bombillo azul"></div>
      <div class="bombillo amarillo"></div>
  </div>

</div>

""", unsafe_allow_html=True)
