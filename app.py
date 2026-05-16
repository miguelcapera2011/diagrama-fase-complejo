# =====================================================
# TIEMPO DE EJECUCIÓN POR CANTIDAD DE CLUSTERS
# =====================================================

st.header("⏱ Comparación de Tiempo de Ejecución por Clusters")

st.markdown("""
Este análisis permite comparar cuánto tarda el algoritmo K-Means
para diferentes cantidades de clusters (k).

Así podemos observar:

- Rendimiento del algoritmo
- Coste computacional
- Relación entre tiempo y cantidad de clusters
""")

# Lista para guardar tiempos
tiempos_kmeans = []

# Lista para guardar inercias
inercias_kmeans = []

# Rango de clusters a evaluar
rangos_k = range(2, 11)

# Barra de progreso
progress_bar = st.progress(0)

# Texto de estado
status_text = st.empty()

# =====================================================
# CÁLCULO DE TIEMPOS
# =====================================================

for idx, k_test in enumerate(rangos_k):

    status_text.text(f"Calculando K-Means con k = {k_test}...")

    # Tiempo inicio
    inicio_k = time.time()

    # Modelo KMeans
    modelo_k = KMeans(
        n_clusters=k_test,
        n_init=50,
        random_state=42
    )

    # Entrenamiento
    modelo_k.fit(datos.drop(columns=['State']))

    # Tiempo final
    fin_k = time.time()

    # Tiempo en milisegundos
    tiempo_ms = (fin_k - inicio_k) * 1000

    # Guardar resultados
    tiempos_kmeans.append(tiempo_ms)
    inercias_kmeans.append(modelo_k.inertia_)

    # Actualizar barra progreso
    progreso = (idx + 1) / len(rangos_k)
    progress_bar.progress(progreso)

# Limpiar texto
status_text.empty()

# =====================================================
# DATAFRAME RESULTADOS
# =====================================================

tiempos_df = pd.DataFrame({
    'Clusters': list(rangos_k),
    'Tiempo_ms': tiempos_kmeans,
    'Inercia': inercias_kmeans
})

# =====================================================
# MÉTRICAS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⚡ Tiempo mínimo",
        f"{tiempos_df['Tiempo_ms'].min():.2f} ms"
    )

with col2:
    mejor_k = tiempos_df.loc[
        tiempos_df['Tiempo_ms'].idxmin(),
        'Clusters'
    ]

    st.metric(
        "🏆 Mejor rendimiento",
        f"k = {mejor_k}"
    )

with col3:
    st.metric(
        "📈 Tiempo promedio",
        f"{tiempos_df['Tiempo_ms'].mean():.2f} ms"
    )

# =====================================================
# TABLA INTERACTIVA
# =====================================================

st.subheader("📋 Tabla de tiempos")

st.dataframe(
    tiempos_df.style.format({
        'Tiempo_ms': '{:.2f}',
        'Inercia': '{:.2f}'
    }),
    use_container_width=True
)

# =====================================================
# GRÁFICO TIEMPOS
# =====================================================

fig_tiempos = px.line(
    tiempos_df,
    x='Clusters',
    y='Tiempo_ms',
    markers=True,
    title='Tiempo de ejecución vs Número de Clusters',
    text='Tiempo_ms'
)

fig_tiempos.update_traces(
    line=dict(width=4),
    marker=dict(size=12),
    texttemplate='%{text:.2f} ms',
    textposition='top center'
)

fig_tiempos.update_layout(
    height=650,
    xaxis_title='Número de Clusters (k)',
    yaxis_title='Tiempo de ejecución (ms)',
    template='plotly_dark'
)

st.plotly_chart(fig_tiempos, use_container_width=True)

# =====================================================
# GRÁFICO INERCIA
# =====================================================

fig_inercia = px.bar(
    tiempos_df,
    x='Clusters',
    y='Inercia',
    color='Clusters',
    title='Inercia por número de clusters'
)

fig_inercia.update_layout(
    height=650,
    template='plotly_dark'
)

st.plotly_chart(fig_inercia, use_container_width=True)

# =====================================================
# COMPARACIÓN TIEMPO VS INERCIA
# =====================================================

fig_compare = px.scatter(
    tiempos_df,
    x='Tiempo_ms',
    y='Inercia',
    size='Clusters',
    color='Clusters',
    hover_data=['Clusters'],
    title='Relación entre Tiempo e Inercia'
)

fig_compare.update_layout(
    height=650,
    template='plotly_dark'
)

st.plotly_chart(fig_compare, use_container_width=True)

# =====================================================
# EXPORTAR RESULTADOS
# =====================================================

csv_tiempos = tiempos_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Descargar resultados tiempos KMeans",
    data=csv_tiempos,
    file_name='tiempos_kmeans.csv',
    mime='text/csv'
)

# =====================================================
# EXPLICACIÓN
# =====================================================

with st.expander("📘 Interpretación del análisis de tiempos"):

    st.markdown("""
    ### ¿Qué significa este análisis?

    El algoritmo K-Means debe:

    1. Calcular distancias
    2. Asignar puntos a clusters
    3. Recalcular centroides
    4. Repetir hasta converger

    Cuando aumenta el número de clusters:

    - aumentan los cálculos,
    - aumenta el movimiento de centroides,
    - puede aumentar el tiempo computacional.

    ### Inercia

    La inercia mide qué tan compactos son los clusters.

    Menor inercia:
    - clusters más compactos,
    - mejor agrupamiento.

    ### Objetivo

    Encontrar un equilibrio entre:

    - bajo tiempo,
    - baja inercia,
    - buena separación de clusters.
    """)
