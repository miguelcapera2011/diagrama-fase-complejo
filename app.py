import streamlit as st
from pypdf import PdfReader

# Configuración de la página
st.set_page_config(page_title="Lector de PDF", page_icon="📄", layout="wide")

st.title("📄 Lector y Visualizador de PDF")
st.write("Sube un archivo PDF para extraer y explorar su contenido.")

# Cargador de archivos
uploaded_file = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        # Leer el archivo PDF subido
        reader = PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        
        # Mostrar métricas del documento
        st.success(f"¡PDF cargado con éxito! Total de páginas: **{num_pages}**")
        
        st.divider()

        # Opciones de visualización
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("⚙️ Opciones")
            page_number = st.number_input(
                "Selecciona el número de página:",
                min_value=1,
                max_value=num_pages,
                value=1,
                step=1
            )
            
            # Botón para descargar el texto extraído
            full_text = "\n\n".join([page.extract_text() or "" for page in reader.pages])
            st.download_button(
                label="📥 Descargar todo el texto (.txt)",
                data=full_text,
                file_name=f"{uploaded_file.name}_texto.txt",
                mime="text/plain"
            )

        with col2:
            st.subheader(f"📖 Contenido de la Página {page_number}")
            
            # Extraer el texto de la página seleccionada (pypdf usa índices base 0)
            selected_page = reader.pages[page_number - 1]
            extracted_text = selected_page.extract_text()
            
            if extracted_text.strip():
                st.text_area(
                    label="Texto extraído:",
                    value=extracted_text,
                    height=400
                )
            else:
                st.warning("Esta página no contiene texto extraíble (puede ser una imagen o escaneo).")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo PDF para comenzar.")
