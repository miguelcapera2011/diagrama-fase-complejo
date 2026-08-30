import io
import requests
import streamlit as st
from PyPDF2 import PdfReader

# Configuración inicial de la página
st.set_page_config(page_title="Visualizador de PDF desde GitHub", layout="wide")

st.title("📄 Lector de PDF desde GitHub")

# 1. Configuración del archivo en GitHub
# NOTA: Debes usar el enlace RAW (crudo) del archivo en GitHub.
# Ejemplo de formato RAW: "https://raw.githubusercontent.com/usuario/repositorio/main/documento.pdf"
PDF_URL = "https://raw.githubusercontent.com/pdf-association/pdf20standard/main/PDF20_ISO_32000-2_2020_with_comments.pdf"


@st.cache_data(show_spinner="Buscando y descargando PDF desde GitHub...")
def descargar_pdf_desde_github(url):
    """Descarga el PDF directamente desde el repositorio de GitHub."""
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            return respuesta.content
        else:
            st.error(
                f"No se pudo obtener el archivo. Código de estado: {respuesta.status_code}"
            )
            return None
    except Exception as e:
        st.error(f"Error al conectar con GitHub: {e}")
        return None


# 2. Búsqueda y descarga automática al cargar la app
pdf_bytes = descargar_pdf_desde_github(PDF_URL)

if pdf_bytes:
    st.success("✅ ¡PDF localizado y cargado con éxito!")

    # Pestañas para elegir el método de visualización
    tab1, tab2 = st.tabs(["Visor Integrado (Iframe)", "Lector de Texto"])

    # Opción A: Renderizar PDF directamente usando HTML/Iframe
    with tab1:
        st.subheader("Vista previa interactiva")
        # Mostramos el PDF codificado en el navegador
        st.download_button(
            label="⬇️ Descargar copia local",
            data=pdf_bytes,
            file_name="documento_github.pdf",
            mime="application/pdf",
        )
        pdf_display = f'<iframe src="data:application/pdf;base64,{io.BytesIO(pdf_bytes).read()}" width="100%" height="800" type="application/pdf"></iframe>'

        # Alternativa robusta con componentes nativos usando HTML embebido
        import base64

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Opción B: Extracción y lectura del texto del PDF
    with tab2:
        st.subheader("Extracción de Texto")
        reader = PdfReader(io.BytesIO(pdf_bytes))
        num_paginas = len(reader.pages)

        st.info(f"Total de páginas: {num_paginas}")

        pagina_num = st.slider("Selecciona una página", 1, num_paginas, 1)
        texto_pagina = reader.pages[pagina_num - 1].extract_text()

        st.markdown(f"**Página {pagina_num}:**")
        st.text_area("Contenido:", texto_pagina, height=400)
