import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sustentación Anteproyecto | STATIS Colombia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        background-color: #0E1117;
    }
    /* Caja estilo Documento Oficial (Izquierda) */
    .doc-box {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-top: 4px solid #8B949E;
        border-radius: 10px;
        padding: 20px;
        height: 100%;
        animation: fadeIn 0.5s ease-out;
    }
    .doc-header {
        color: #8B949E;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        margin-bottom: 10px;
        border-bottom: 1px solid #30363D;
        padding-bottom: 6px;
    }
    .doc-text {
        color: #C9D1D9;
        font-size: 0.95rem;
        line-height: 1.65;
        text-align: justify;
    }
    /* Tarjeta Interactiva de Exposición (Derecha) */
    .card {
        background: linear-gradient(135deg, #1E2530 0%, #161B22 100%);
        padding: 20px;
        border-radius: 14px;
        border-left: 5px solid #00D4FF;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        margin-bottom: 16px;
        animation: fadeIn 0.6s ease-out;
    }
    .card-title {
        color: #00D4FF;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .highlight-text {
        color: #F8FAFC;
        font-size: 1.0rem;
        line-height: 1.55;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL DE NAVEGACIÓN
# ---------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/320px-Flag_of_Colombia.svg.png", width=55)
st.sidebar.title("🎓 Sustentación en Vivo")
st.sidebar.caption("Universidad del Tolima | GINVAE-UT")
st.sidebar.markdown("---")

seccion = st.sidebar.radio(
    "📑 Secciones del Anteproyecto:",
    [
        "1. Título, Autores y Resumen",
        "2. Justificación",
        "3. Planteamiento del Problema",
        "4. Marco Referencial",
        "5. Objetivos",
        "6. Diseño Metodológico (STATIS)",
        "7. Aspectos Bioéticos y Cronograma",
        "8. Resultados Esperados"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("👈 **Izquierda:** Texto oficial del documento.\n\n👉 **Derecha:** Apoyo visual y explicación interactiva.")

# =========================================================
# SECCIÓN 1: TÍTULO, AUTORES Y RESUMEN
# =========================================================
if seccion == "1. Título, Autores y Resumen":
    st.title("1️⃣ Identificación y Resumen del Anteproyecto")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítems 1 al 6</div>
            <p class="doc-text">
                <b>1. TÍTULO:</b><br>
                Análisis Departamental de indicadores de delitos y afectación a la fuerza pública en Colombia: Un estudio mediante técnicas multivía.<br><br>
                <b>2. AUTORES:</b><br>
                • Miguel Ángel Garatejo Capera (Estudiante)<br>
                • Edith Johana Medina Hernández (Profesora / Directora)<br><br>
                <b>3. GRUPO Y LÍNEA:</b><br>
                GINVAE-UT — Línea de Análisis Multivariado.<br><br>
                <b>5. RESUMEN:</b><br>
                En este trabajo de grado se busca analizar de forma conjunta la evolución de indicadores de delitos y de afectaciones a la fuerza pública en los departamentos de Colombia, mediante la exploración de indicadores publicados por el Observatorio de Derechos Humanos y Defensa Nacional del Ministerio de Defensa. Se propone modelar los datos en tres vías (departamentos, años e indicadores), a través de técnicas de la familia STATIS (particularmente X-STATIS y STATICO), buscando identificar trayectorias territoriales similares, evaluar la estabilidad de estos patrones a lo largo del tiempo, y determinar cuáles variables delictivas ejercen mayor peso en las desigualdades regionales observadas.<br><br>
                <b>6. DURACIÓN:</b> 6 meses.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("🚀 Explicación Visual")
        m1, m2, m3 = st.columns(3)
        m1.metric("Unidades (n)", "32 Dptos.", "Cobertura Nacional")
        m2.metric("Tiempo (k)", "13 Años", "2012 – 2024")
        m3.metric("Duración", "6 Meses", "Trabajo de Grado")

        st.markdown("""
        <div class="card">
            <div class="card-title">💡 ¿Cuál es la idea central?</div>
            <p class="highlight-text">
                En lugar de estudiar un solo delito o un solo año, vamos a cruzar <b>3 dimensiones simultáneamente</b> 
                (Territorio × Tiempo × Indicadores) usando estadística multivía (<b>X-STATIS y STATICO</b>) para 
                descubrir qué departamentos se comportan parecido y cómo cambiaron sus dinámicas de seguridad.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.success("🎯 **Producto final:** Una caracterización multidimensional que sirva de insumo técnico para políticas públicas de seguridad focalizadas.")

# =========================================================
# SECCIÓN 2: JUSTIFICACIÓN
# =========================================================
elif seccion == "2. Justificación":
    st.title("2️⃣ Justificación del Estudio")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítem 7</div>
            <p class="doc-text">
                El conflicto armado colombiano es el de mayor duración del hemisferio occidental, y desde más de seis décadas se relaciona con economías ilegales. Ortiz-Riomalo y Rettberg (2018) muestran que los grupos armados han financiado sus actividades sobre todo con el narcotráfico y más recientemente con la minería de oro, señalando que esa relación no es uniforme, cambia con las características de cada zona.<br><br>
                Varias investigaciones han estudiado el conflicto y sus consecuencias. Por ejemplo, Rodríguez Takeuchi (2009) y Fiandrino et al. (2023) analizaron factores asociados al conflicto; sin embargo, es común que se usen datos de un solo año (2005 y 2018), quedando por explorar cómo se comportan al mismo tiempo y a lo largo de varios años los distintos delitos y las afectaciones a la fuerza pública.<br><br>
                Por ello, este estudio es pertinente a escala nacional y regional, porque identificar cómo se parecen y diferencian los departamentos puede ayudar a que las políticas de seguridad reconozcan las particularidades de cada región, en lugar de aplicar el mismo esquema a todo el país.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("💡 ¿Por qué es necesario este estudio?")
        
        pilar = st.selectbox(
            "Selecciona el argumento clave para explicar:",
            [
                "1. Heterogeneidad Territorial (Economías Ilegales)",
                "2. Vacío Metodológico (De cortes estáticos a series multivía)",
                "3. Pertinencia en Políticas Públicas"
            ]
        )

        if "1." in pilar:
            st.markdown("""
            <div class="card">
                <div class="card-title">🗺️ El conflicto no es uniforme en Colombia</div>
                <p class="highlight-text">
                    • Las economías ilícitas (narcotráfico y minería ilegal de oro) cambian según la capacidad institucional y geográfica de cada departamento (Ortiz-Riomalo y Rettberg, 2018).<br>
                    • Medir promedios nacionales oculta las realidades críticas de ciertas regiones.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif "2." in pilar:
            st.markdown("""
            <div class="card">
                <div class="card-title">⏳ Superar la "foto" de un solo año</div>
                <p class="highlight-text">
                    • Estudios previos (Rodríguez Takeuchi, 2009; Fiandrino et al., 2023) analizan cortes transversales (un único año).<br>
                    • Nuestro estudio analiza <b>13 años continuos de forma simultánea</b>, capturando la evolución real.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <div class="card-title">🏛️ Políticas diferenciales vs. esquemas únicos</div>
                <p class="highlight-text">
                    • Agrupar departamentos con perfiles similares permite focalizar estrategias de seguridad según el tipo de amenaza dominante en cada territorio.
                </p>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# SECCIÓN 3: PLANTEAMIENTO DEL PROBLEMA
# =========================================================
elif seccion == "3. Planteamiento del Problema":
    st.title("3️⃣ Planteamiento del Problema")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítem 8</div>
            <p class="doc-text">
                Los grupos armados organizados al margen de la ley (GAO) han financiado sus actividades mediante terrorismo, secuestro, narcotráfico y minería ilegal, afectando a la población civil, el ambiente y a la Fuerza Pública.<br><br>
                <b>Cifras oficiales (MinDefensa, 2012–2024):</b><br>
                • <b>Fuerza Pública:</b> 18.630 afectados (16.476 heridos y 2.154 asesinados). Pasó de 2.848 en 2012 a 600 en 2024.<br>
                • <b>Terrorismo:</b> 9.164 casos (subió de 666 en 2012 a 1.126 en 2024).<br>
                • <b>Secuestro:</b> 3.042 casos (mínimo de 160 en 2021, repuntó a 313 en 2024).<br>
                • <b>Minería ilegal:</b> 22.720 capturas (pico de 2.560 en 2016; bajó a 1.148 en 2024).<br><br>
                <b>Pregunta Central:</b> ¿Cómo analizar, mediante técnicas multivía, los indicadores de delitos y afectación a la fuerza pública en Colombia, a partir de información del Ministerio de Defensa Nacional, para describir las similitudes y diferencias entre los departamentos y su evolución durante el periodo de estudio?
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("📊 Contraste de Cifras y Preguntas")
        c1, c2 = st.columns(2)
        c1.metric("Fuerza Pública (2012 → 2024)", "18.630 total", "-78.9% (2.848 → 600)", delta_color="normal")
        c2.metric("Terrorismo (2012 → 2024)", "9.164 total", "+69.1% (666 → 1.126)", delta_color="inverse")

        df_hitos = pd.DataFrame({
            "Fenómeno": ["Fuerza Pública", "Fuerza Pública", "Terrorismo", "Terrorismo", "Minería Ilegal", "Minería Ilegal"],
            "Momento": ["2012", "2024", "2012", "2024", "2016 (Pico)", "2024"],
            "Registros": [2848, 600, 666, 1126, 2560, 1148]
        })
        fig = px.bar(
            df_hitos, x="Fenómeno", y="Registros", color="Momento", barmode="group",
            title="Comportamientos opuestos en el tiempo (MinDefensa)",
            template="plotly_dark", color_discrete_sequence=["#00D4FF", "#FF4B4B", "#00E676"],
            height=290
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("❓ Ver las 3 Preguntas Articuladoras", expanded=True):
            st.write("1. **Trayectorias:** ¿Qué departamentos siguen trayectorias similares?")
            st.write("2. **Acuerdo de Paz (2016):** ¿Las similitudes se mantienen o cambian tras 2016?")
            st.write("3. **Variables clave:** ¿Qué indicadores explican más las diferencias territoriales?")

# =========================================================
# SECCIÓN 4: MARCO REFERENCIAL
# =========================================================
elif seccion == "4. Marco Referencial":
    st.title("4️⃣ Marco Referencial")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítem 9</div>
            <p class="doc-text">
                <b>9.1 Estudios sobre criminalidad y seguridad en Colombia:</b><br>
                • <b>Holmes et al. (2006):</b> Compararon departamentos y hallaron que los factores económicos y la erradicación pesan más que la sola producción de coca.<br>
                • <b>Idrobo et al. (2014):</b> Relación entre minería ilegal de oro y violencia tras el auge de 2008.<br>
                • <b>González et al. (2022):</b> Secuestros, robos y homicidios (2000–2013); Bolívar, Caquetá, Cesar, Meta y Tolima entre los más afectados.<br>
                • <b>Fajardo-Steinhäuser (2024):</b> Efectos del cese al fuego y Acuerdo de Paz de 2016 en municipios con presencia de FARC vs. ELN.<br><br>
                <b>9.2 Técnicas de análisis multivía (Familia STATIS):</b><br>
                • Propuestas por <b>L’Hermier des Plantes (1976)</b> y desarrolladas por <b>Thioulouse (2011)</b> para comparar secuencias de tablas en el tiempo.<br>
                • <b>Medina Hernández (2022):</b> Aplicó STATICO a indicadores de equidad de género y ODS en 115 países.<br>
                • <b>Rodríguez-Martínez et al. (2023):</b> Aplicaron X-STATIS a trayectorias de países (2008–2016).
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("📚 Síntesis de Antecedentes")
        tab_ctx, tab_met = st.tabs(["🇨🇴 Línea Temática (Seguridad)", "📐 Línea Estadística (STATIS)"])

        with tab_ctx:
            df_aut = pd.DataFrame({
                "Autor(es)": ["Holmes et al. (2006)", "Idrobo et al. (2014)", "González et al. (2022)", "Fajardo-Steinhäuser (2024)"],
                "Enfoque": ["Coca vs. violencia", "Minería ilegal de oro", "Secuestro e inversión", "Posacuerdo de Paz 2016"],
                "¿Incluye Fuerza Pública?": ["No", "No", "No", "No"]
            })
            st.dataframe(df_aut, use_container_width=True, hide_index=True)
            st.warning("💡 **Vacío detectado:** Ninguno de estos antecedentes integra longitudinalmente las bajas/heridos de la Fuerza Pública con los delitos ambientales y terrorismo.")

        with tab_met:
            st.markdown("""
            <div class="card">
                <div class="card-title">Respaldo Metodológico Probado</div>
                <p class="highlight-text">
                    • <b>L’Hermier des Plantes (1976) & Thioulouse (2011):</b> Fundamentos teóricos de STATIS y STATICO.<br>
                    • <b>Medina Hernández (2022) & Rodríguez-Martínez et al. (2023):</b> Demuestran la eficacia de STATICO y X-STATIS para resumir trayectorias territoriales e indicadores socioeconómicos en el tiempo.
                </p>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# SECCIÓN 5: OBJETIVOS
# =========================================================
elif seccion == "5. Objetivos":
    st.title("5️⃣ Objetivos de la Investigación")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítem 10</div>
            <p class="doc-text">
                <b>10.1 OBJETIVO GENERAL:</b><br>
                Analizar mediante técnicas multivía indicadores de delitos y afectación a la fuerza pública en Colombia, desde información del Ministerio de Defensa Nacional, describiendo las similitudes y diferencias observadas entre departamentos y su evolución en el tiempo.<br><br>
                <b>10.2 OBJETIVOS ESPECÍFICOS:</b><br>
                <b>1.</b> Identificar los departamentos que presentan trayectorias similares en la ocurrencia de delitos y en los indicadores de afectación a la fuerza pública.<br><br>
                <b>2.</b> Explorar si las similitudes entre departamentos se mantienen durante el periodo de estudio o cambian en años concretos, en especial después de la firma del Acuerdo de Paz.<br><br>
                <b>3.</b> Examinar las relaciones existentes entre los indicadores estudiados caracterizando los patrones territoriales observados.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("🎯 Desglose Operativo (¿Qué producto da cada objetivo?)")
        st.markdown("""
        <div class="card">
            <div class="card-title">Objetivo General → Visión Integral</div>
            <p class="highlight-text">Unificar en un solo modelo multivía (2012–2024) el comportamiento territorial de seguridad y defensa en los 32 departamentos.</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("**OE 1 (Espacio):** Plano *Compromiso* y trayectorias para agrupar departamentos con perfiles similares.")
        st.warning("**OE 2 (Tiempo):** *Interestructura* para detectar quiebres estructurales entre años (ej. pre y post Acuerdo de Paz 2016).")
        st.success("**OE 3 (Variables):** *Intraestructura* y correlaciones entre delitos (Bloque Y) y afectación a la Fuerza Pública (Bloque X).")

# =========================================================
# SECCIÓN 6: DISEÑO METODOLÓGICO (STATIS)
# =========================================================
elif seccion == "6. Diseño Metodológico (STATIS)":
    st.title("6️⃣ Diseño Metodológico y Cubo Multivía")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítem 11</div>
            <p class="doc-text">
                <b>11.1 Enfoque:</b> Cuantitativo, longitudinal, descriptivo y exploratorio (13 años: 2012–2024).<br>
                <b>11.2 Fuentes:</b> Ministerio de Defensa Nacional (registros de hechos), DANE (proyecciones poblacionales para tasas) y TerriData-DNP (variables contextuales).<br>
                <b>11.4 Bloques de Indicadores:</b><br>
                • <i>Delitos y Criminalidad:</i> Terrorismo, secuestro, capturas por minería ilegal, delitos contra el medio ambiente e incautación de insumos (oro y mercurio).<br>
                • <i>Afectación a la Fuerza Pública:</i> Integrantes de FF.MM. y Policía heridos y asesinados.<br><br>
                <b>11.5 Estructura Multivía (X-STATIS / STATICO):</b><br>
                Cubos de tres vías: <b>n = 32</b> departamentos × <b>k = 13</b> años × <b>(p, q)</b> variables. Se evaluará una sola K-tabla (X-STATIS) o dos K-tablas pareadas X vs. Y (STATICO).<br><br>
                <b>11.6 Procesamiento (R / Python):</b> Revisión de calidad, armonización territorial/temporal y cálculo de interestructura, compromiso e intraestructura.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("🧊 Estructura Tridimensional de los Datos")
        
        # Gráfico 3D interactivo
        x, y, z = np.meshgrid(np.arange(1, 6), np.arange(1, 9), np.arange(2012, 2025, 3))
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=x.flatten(), y=y.flatten(), z=z.flatten(),
            mode='markers',
            marker=dict(size=6, color=z.flatten(), colorscale='Viridis', opacity=0.9)
        )])
        fig_3d.update_layout(
            title="Cubo de Datos STATIS (Rota con el mouse)",
            scene=dict(
                xaxis_title="Variables (Bloques X, Y)",
                yaxis_title="Departamentos (n=32)",
                zaxis_title="Años (k=13)"
            ),
            template="plotly_dark",
            height=330,
            margin=dict(l=0, r=0, b=0, t=35)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

        eleccion = st.radio(
            "Alternativas metodológicas a contrastar en R/Python:",
            ["X-STATIS (1 K-tabla conjunta)", "STATICO (2 K-tablas pareadas: X vs Y)"],
            horizontal=True
        )
        if "X-STATIS" in eleccion:
            st.info("**X-STATIS:** Analiza todas las variables juntas en una única secuencia de matrices para obtener el compromiso territorial global.")
        else:
            st.success("**STATICO:** Cruza directamente la tabla de **Afectación a la Fuerza Pública (X)** contra la tabla de **Delitos (Y)** año tras año.")

# =========================================================
# SECCIÓN 7: ASPECTOS BIOÉTICOS Y CRONOGRAMA
# =========================================================
elif seccion == "7. Aspectos Bioéticos y Cronograma":
    st.title("7️⃣ Aspectos Bioéticos y Cronograma")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítems 12 y 14</div>
            <p class="doc-text">
                <b>12. ASPECTOS BIOÉTICOS:</b><br>
                Este estudio no recoge información directamente de personas ni usa datos que identifiquen a individuos. La información proviene de registros administrativos públicos del Ministerio de Defensa Nacional, procesados agregadamente por departamento y año. Por ello se clasifica como <b>investigación sin riesgo</b>.<br><br>
                Los resultados se presentarán con rigor técnico y sin estigmatizar territorios, documentando el código en R/Python para garantizar la reproducibilidad científica.<br><br>
                <b>14. CRONOGRAMA (6 MESES):</b><br>
                • <b>Mes 1–2:</b> Revisión bibliográfica y marco referencial.<br>
                • <b>Mes 2:</b> Verificación de bases e implementación STATIS en Python/R.<br>
                • <b>Mes 3:</b> Análisis e interpretación por departamento, año e indicador.<br>
                • <b>Mes 4–5:</b> Redacción del documento final de tesis.<br>
                • <b>Mes 6:</b> Revisión, ajustes finales y entrega.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("📅 Plan de Trabajo Semestral")
        df_crono = pd.DataFrame([
            dict(Actividad="1. Revisión bibliográfica", Inicio=1, Fin=2),
            dict(Actividad="2. Verificación base de datos", Inicio=2, Fin=2.9),
            dict(Actividad="3. Implementación STATIS (R/Python)", Inicio=2, Fin=2.9),
            dict(Actividad="4. Análisis e interpretación", Inicio=3, Fin=3.9),
            dict(Actividad="5. Contraste y conclusiones", Inicio=3, Fin=3.9),
            dict(Actividad="6. Redacción documento final", Inicio=4, Fin=5.9),
            dict(Actividad="7. Ajustes finales y entrega", Inicio=6, Fin=6.9),
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
            xaxis=dict(title="Mes", tickvals=[1, 2, 3, 4, 5, 6], ticktext=["M1", "M2", "M3", "M4", "M5", "M6"]),
            yaxis=dict(autorange="reversed"),
            template="plotly_dark",
            height=300,
            margin=dict(l=0, r=10, b=20, t=20)
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

        st.info("🛡️ **Compromiso Ético:** Investigación **sin riesgo** (datos públicos agregados), enfoque no estigmatizante y código 100% reproducible.")

# =========================================================
# SECCIÓN 8: RESULTADOS ESPERADOS
# =========================================================
elif seccion == "8. Resultados Esperados":
    st.title("8️⃣ Resultados Esperados y Cierre")
    col_doc, col_app = st.columns([1, 1.15], gap="large")

    with col_doc:
        st.markdown("""
        <div class="doc-box">
            <div class="doc-header">📄 Documento Oficial — Ítems 16 y 17</div>
            <p class="doc-text">
                <b>16. RESULTADOS ESPERADOS:</b><br>
                Se espera identificar los departamentos que siguen trayectorias similares en los indicadores de delitos y de afectación a la fuerza pública y los que se apartan del patrón general (estructura compromiso). También se busca describir si esas similitudes se mantienen o cambian alrededor de acontecimientos como la firma del Acuerdo de Paz.<br><br>
                Asimismo, se caracterizarán las relaciones entre los indicadores y se documentará todo el procesamiento para que el análisis sea replicable. Se entregará el documento de trabajo de grado y se socializarán los hallazgos como insumo técnico para políticas públicas focalizadas.<br><br>
                <b>17. EVALUADORES SUGERIDOS (UT):</b><br>
                • Julie Kimberly Ramírez Brinez (Depto. Matemáticas y Estadística)<br>
                • Gisou Díaz Rojo (Depto. Matemáticas y Estadística)
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_app:
        st.subheader("🏆 Entregables e Impacto")
        st.markdown("""
        <div class="card">
            <div class="card-title">1. Tipologías Territoriales (Estructura Compromiso)</div>
            <p class="highlight-text">Clasificación de los 32 departamentos según su trayectoria conjunta de delitos y afectación a la Fuerza Pública.</p>
        </div>
        <div class="card">
            <div class="card-title">2. Flujo Reproducible en R / Python</div>
            <p class="highlight-text">Scripts documentados para replicar el análisis multivía en futuros periodos o con nuevos indicadores.</p>
        </div>
        <div class="card">
            <div class="card-title">3. Insumo para Políticas Públicas</div>
            <p class="highlight-text">Evidencia estadística para diseñar estrategias de seguridad diferenciadas por región.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎉 Finalizar Socialización del Anteproyecto", type="primary", use_container_width=True):
            st.balloons()
            st.success("¡Muchas gracias por su atención! Quedo atento a las observaciones de la profesora y los evaluadores.")
