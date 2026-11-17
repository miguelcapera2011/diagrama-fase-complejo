import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS ANIMADOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sustentación Anteproyecto | STATIS Colombia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Animación suave de entrada */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        background-color: #0E1117;
    }
    .card {
        background: linear-gradient(135deg, #1E2530 0%, #161B22 100%);
        padding: 22px;
        border-radius: 14px;
        border-left: 5px solid #00D4FF;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 18px;
        animation: fadeIn 0.6s ease-out;
    }
    .card-accent {
        background: linear-gradient(135deg, #1A2A3A 0%, #111927 100%);
        padding: 22px;
        border-radius: 14px;
        border-left: 5px solid #FF4B4B;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 18px;
        animation: fadeIn 0.8s ease-out;
    }
    .card-title {
        color: #00D4FF;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .highlight-text {
        color: #F8FAFC;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background-color: rgba(0, 212, 255, 0.15);
        color: #00D4FF;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL DE NAVEGACIÓN
# ---------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/320px-Flag_of_Colombia.svg.png", width=60)
st.sidebar.title("🎓 Socialización Anteproyecto")
st.sidebar.caption("Universidad del Tolima | GINVAE-UT")
st.sidebar.markdown("---")

seccion = st.sidebar.radio(
    "📌 Selecciona una sección para desplegar:",
    [
        "1. Título e Identificación",
        "2. Planteamiento del Problema",
        "3. Justificación y Vacío Científico",
        "4. Objetivos",
        "5. Diseño Metodológico (STATIS)",
        "6. Cronograma y Resultados Esperados"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip de exposición:** Haz clic en las pestañas y desplegables de cada vista para ir revelando la explicación paso a paso.")

# ---------------------------------------------------------
# SECCIÓN 1: TÍTULO E IDENTIFICACIÓN
# ---------------------------------------------------------
if seccion == "1. Título e Identificación":
    st.markdown('<span class="badge">Trabajo de Grado</span> <span class="badge">Análisis Multivariado</span> <span class="badge">Duración: 6 Meses</span>', unsafe_allow_html=True)
    st.title("📊 Análisis Departamental de Indicadores de Delitos y Afectación a la Fuerza Pública en Colombia")
    st.subheader("Un estudio mediante técnicas multivía (2012 – 2024)")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🧭 Síntesis del Proyecto</div>
            <p class="highlight-text">
                Esta investigación modela de forma conjunta la evolución espacio-temporal de <b>delitos estratégicos</b> 
                y <b>afectaciones a la Fuerza Pública</b> en los <b>32 departamentos de Colombia</b> durante 13 años (2012–2024).
                <br><br>
                Mediante técnicas multivía de la familia <b>STATIS (X-STATIS y STATICO)</b>, se busca descubrir trayectorias 
                territoriales comunes, evaluar qué ocurrió tras el <b>Acuerdo de Paz de 2016</b> e identificar qué variables 
                explican las desigualdades regionales.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">👥 Equipo Investigador</div>
            <p class="highlight-text">
                <b>Autor:</b><br>Miguel Ángel Garatejo Capera<br><br>
                <b>Directora:</b><br>Dra. Edith Johana Medina Hernández<br><br>
                <b>Grupo de Investigación:</b><br>GINVAE-UT (Análisis Estadístico)<br><br>
                <b>Línea:</b> Análisis Multivariado
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Métricas clave del alcance
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Territorios (n)", "32 Dptos.", "Cobertura Nacional")
    m2.metric("Ventana Temporal (k)", "13 Años", "2012 – 2024")
    m3.metric("Fuente Principal", "MinDefensa", "Obs. DD.HH.")
    m4.metric("Enfoque Técnico", "STATIS", "X-STATIS / STATICO")

# ---------------------------------------------------------
# SECCIÓN 2: PLANTEAMIENTO DEL PROBLEMA
# ---------------------------------------------------------
elif seccion == "2. Planteamiento del Problema":
    st.title("🔍 Planteamiento del Problema")
    st.write("Las economías ilegales (narcotráfico, minería de oro) y las acciones de los GAO impactan de forma heterogénea al territorio y a la Fuerza Pública.")

    # Tarjetas de cifras reales del documento (2012-2024)
    st.subheader("📈 Dimensión del Fenómeno en Colombia (Acumulado 2012–2024)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fuerza Pública Afectada", "18.630", "16.476 heridos | 2.154 asesinados", delta_color="inverse")
    c2.metric("Capturas Minería Ilegal", "22.720", "Pico en 2016 (2.560)", delta_color="off")
    c3.metric("Casos de Terrorismo", "9.164", "Subió de 666 (2012) a 1.126 (2024)", delta_color="inverse")
    c4.metric("Secuestros Registrados", "3.042", "Repunte: 160 (2021) → 313 (2024)", delta_color="inverse")

    # Gráfico comparativo interactivo de los hitos mencionados en el documento
    df_hitos = pd.DataFrame({
        "Indicador": ["Afectación Fuerza Pública", "Afectación Fuerza Pública", "Terrorismo", "Terrorismo", "Minería Ilegal (Capturas)", "Minería Ilegal (Capturas)"],
        "Año": ["2012", "2024", "2012", "2024", "2016 (Pico)", "2024"],
        "Casos": [2848, 600, 666, 1126, 2560, 1148]
    })
    fig = px.bar(
        df_hitos, x="Indicador", y="Casos", color="Año", barmode="group",
        title="Contraste de Cifras Oficiales Reportadas en el Planteamiento (MinDefensa)",
        template="plotly_dark", color_discrete_sequence=["#00D4FF", "#FF4B4B", "#00E676"]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Pregunta problema interactiva
    with st.expander("❓ VER PREGUNTA CENTRAL Y PREGUNTAS ARTICULADORAS", expanded=True):
        st.markdown("""
        <div class="card-accent">
            <div class="card-title" style="color:#FF4B4B;">Pregunta Central de Investigación</div>
            <p class="highlight-text">
                ¿Cómo analizar, mediante técnicas multivía, los indicadores de delitos y afectación a la fuerza pública en Colombia, 
                a partir de información del Ministerio de Defensa Nacional, para describir las similitudes y diferencias entre 
                los departamentos y su evolución durante el periodo de estudio?
            </p>
        </div>
        """, unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.info("**1. Trayectorias:** ¿Qué departamentos siguen trayectorias similares en delitos y afectaciones?")
        col_p2.warning("**2. Punto de Quiebre:** ¿Se mantienen esas similitudes o cambian tras el Acuerdo de Paz de 2016?")
        col_p3.success("**3. Peso de Variables:** ¿Qué indicadores explican mejor las diferencias territoriales?")

# ---------------------------------------------------------
# SECCIÓN 3: JUSTIFICACIÓN Y VACÍO CIENTÍFICO
# ---------------------------------------------------------
elif seccion == "3. Justificación y Vacío Científico":
    st.title("💡 Justificación y Vacío en la Literatura")

    tab1, tab2, tab3 = st.tabs(["🧩 El Problema del Análisis Tradicional", "📚 Vacío en Estudios Previos", "🏛️ Aporte a Políticas Públicas"])

    with tab1:
        st.markdown("""
        <div class="card">
            <div class="card-title">¿Por qué no basta con mirar tablas por separado?</div>
            <p class="highlight-text">
                Analizar totales nacionales o un solo año oculta la dinámica real del conflicto:
                <ul>
                    <li>Un departamento puede bajar en afectaciones a la Fuerza Pública pero dispararse en <b>minería ilegal o terrorismo</b>.</li>
                    <li>Las dinámicas cambian antes y después de hitos como el <b>Acuerdo de Paz de 2016</b>.</li>
                    <li>Se requiere una herramienta que cruce <b>Espacio × Tiempo × Variables</b> al mismo tiempo.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="card">
            <div class="card-title">¿Qué han hecho otros autores y qué falta por hacer?</div>
            <p class="highlight-text">
                • <b>Cortes transversales (1 solo año):</b> Estudios como Rodríguez Takeuchi (2005) o Fiandrino et al. (2023) analizan un único año.<br>
                • <b>Variables aisladas:</b> Holmes et al. (2006), Idrobo et al. (2014) y González et al. (2022) relacionan violencia con coca, oro o inversión.<br>
                • <b>Nuestro diferencial:</b> Ninguno integra de forma multivía y longitudinal la <b>afectación física a la Fuerza Pública (heridos y asesinados)</b> junto con delitos ambientales, terrorismo y secuestro.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.success("🎯 **Impacto Práctico:** Identificar grupos de departamentos con perfiles delictivos similares permite diseñar **políticas de seguridad focalizadas** según la realidad de cada región, evitando aplicar un mismo esquema uniforme a todo el país.")

# ---------------------------------------------------------
# SECCIÓN 4: OBJETIVOS
# ---------------------------------------------------------
elif seccion == "4. Objetivos":
    st.title("🎯 Objetivos de la Investigación")

    st.markdown("""
    <div class="card">
        <div class="card-title">🏆 Objetivo General</div>
        <p class="highlight-text">
            Analizar mediante técnicas multivía indicadores de delitos y afectación a la fuerza pública en Colombia, 
            desde información del Ministerio de Defensa Nacional, describiendo las similitudes y diferencias observadas 
            entre departamentos y su evolución en el tiempo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📌 Objetivos Específicos (Haz clic en cada fase)")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("1️⃣ Trayectorias Territoriales", use_container_width=True):
            st.info("**OE1:** Identificar los departamentos que presentan trayectorias similares en la ocurrencia de delitos y en los indicadores de afectación a la fuerza pública.")
    with col2:
        if st.button("2️⃣ Estabilidad y Acuerdo de Paz", use_container_width=True):
            st.warning("**OE2:** Explorar si las similitudes entre departamentos se mantienen durante el periodo de estudio o cambian en años concretos, en especial después de la firma del Acuerdo de Paz.")
    with col3:
        if st.button("3️⃣ Caracterización de Indicadores", use_container_width=True):
            st.success("**OE3:** Examinar las relaciones existentes entre los indicadores estudiados caracterizando los patrones territoriales observados.")

# ---------------------------------------------------------
# SECCIÓN 5: DISEÑO METODOLÓGICO (STATIS)
# ---------------------------------------------------------
elif seccion == "5. Diseño Metodológico (STATIS)":
    st.title("⚙️ Diseño Metodológico y Estructura Multivía")

    col_izq, col_der = st.columns([1.2, 1])

    with col_izq:
        st.markdown("""
        <div class="card">
            <div class="card-title">📐 Arquitectura del Cubo de Datos (3 Vías)</div>
            <p class="highlight-text">
                • <b>Enfoque:</b> Cuantitativo, longitudinal, descriptivo y exploratorio.<br>
                • <b>Filas (n = 32):</b> Los 32 departamentos de Colombia.<br>
                • <b>Estudios (k = 13):</b> Serie anual continua 2012–2024.<br>
                • <b>Bloque X (Fuerza Pública):</b> Integrantes heridos y asesinados.<br>
                • <b>Bloque Y (Delitos):</b> Terrorismo, secuestro, capturas por minería ilegal, delitos ambientales e incautaciones (oro/mercurio).
            </p>
        </div>
        """, unsafe_allow_html=True)

        metodo = st.radio(
            "Selecciona la técnica multivía a explorar:",
            ["X-STATIS (Una sola K-tabla conjunta)", "STATICO (Dos K-tablas pareadas X vs Y)"]
        )
        if "X-STATIS" in metodo:
            st.info("**X-STATIS:** Analiza todos los indicadores (delitos + fuerza pública) en una única estructura tridimensional para extraer el *Compromiso* (estructura común) y las trayectorias departamentales.")
        else:
            st.success("**STATICO:** Analiza la covariación entre dos secuencias de tablas pareadas: cómo la estructura de **Delitos (Y)** se relaciona con la **Afectación a la Fuerza Pública (X)** a lo largo de los 13 años.")

    with col_der:
        # Visualización 3D interactiva del cubo de datos STATIS
        import numpy as np
        x, y, z = np.meshgrid(np.arange(1, 6), np.arange(1, 9), np.arange(2012, 2025, 3))
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=x.flatten(), y=y.flatten(), z=z.flatten(),
            mode='markers',
            marker=dict(size=6, color=z.flatten(), colorscale='Viridis', opacity=0.85)
        )])
        fig_3d.update_layout(
            title="Representación del Cubo Multivía (Dptos × Variables × Años)",
            scene=dict(
                xaxis_title="Indicadores (p, q)",
                yaxis_title="Departamentos (n=32)",
                zaxis_title="Años (k=13)"
            ),
            template="plotly_dark",
            height=420,
            margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    # Flujo de procesamiento
    st.subheader("🔄 Etapas del Procesamiento (R / Python)")
    p1, p2, p3, p4 = st.columns(4)
    p1.markdown("**1. Revisión:** Calidad y completitud (2012–2024) + tasas DANE.")
    p2.markdown("**2. Armonización:** Estandarización territorial y anual.")
    p3.markdown("**3. STATIS:** Interestructura → Compromiso → Intraestructura.")
    p4.markdown("**4. Ética:** Investigación sin riesgo (datos agregados públicos).")

# ---------------------------------------------------------
# SECCIÓN 6: CRONOGRAMA Y RESULTADOS ESPERADOS
# ---------------------------------------------------------
elif seccion == "6. Cronograma y Resultados Esperados":
    st.title("📅 Cronograma (6 Meses) y Resultados Esperados")

    # Diagrama de Gantt interactivo del cronograma del documento
    df_crono = pd.DataFrame([
        dict(Actividad="1. Revisión bibliográfica y marco referencial", Inicio=1, Fin=2),
        dict(Actividad="2. Verificación y documentación base de indicadores", Inicio=2, Fin=2.9),
        dict(Actividad="3. Implementación STATIS en Python / R", Inicio=2, Fin=2.9),
        dict(Actividad="4. Análisis e interpretación (Dpto-Año-Indicador)", Inicio=3, Fin=3.9),
        dict(Actividad="5. Contraste con marco referencial y conclusiones", Inicio=3, Fin=3.9),
        dict(Actividad="6. Redacción del documento final de tesis", Inicio=4, Fin=5.9),
        dict(Actividad="7. Revisión, ajustes finales y entrega", Inicio=6, Fin=6.9),
    ])

    fig_gantt = go.Figure()
    for _, row in df_crono.iterrows():
        fig_gantt.add_trace(go.Bar(
            y=[row["Actividad"]],
            x=[row["Fin"] - row["Inicio"] + 0.9],
            base=row["Inicio"],
            orientation='h',
            marker_color='#00D4FF',
            showlegend=False
        ))
    fig_gantt.update_layout(
        title="Plan de Ejecución Semestral (Mes 1 a Mes 6)",
        xaxis=dict(title="Meses", tickvals=[1, 2, 3, 4, 5, 6], ticktext=["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"]),
        yaxis=dict(autorange="reversed"),
        template="plotly_dark",
        height=350
    )
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.subheader("🚀 Productos y Resultados Esperados")
    r1, r2, r3 = st.columns(3)
    r1.success("**Mapas y Tipologías:** Agrupación de departamentos según trayectorias de violencia y afectación institucional.")
    r2.info("**Reproducibilidad:** Código documentado en R/Python para replicar el análisis multivía en otros periodos.")
    r3.warning("**Insumo Técnico:** Documento de grado y socialización para focalización de políticas públicas de seguridad.")

    st.markdown("---")
    if st.button("🎉 Finalizar Socialización", type="primary"):
        st.balloons()
        st.success("¡Muchas gracias! Quedo atento a sus preguntas y observaciones.")
