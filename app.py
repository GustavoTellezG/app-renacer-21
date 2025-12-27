import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Scanner Renacer 21", page_icon="🥗")

st.title("🥗 Coach Renacer 21: Scanner")

# --- SIDEBAR ---
with st.sidebar:
    api_key = st.text_input("Tu API Key", type="password")

# --- FUNCIÓN INTELIGENTE ---
def analizar_imagen(imagen, prompt, key):
    genai.configure(api_key=key)
    
    # INTENTO 1: Usamos el modelo Flash estándar
    nombre_modelo = 'gemini-1.5-flash'
    
    try:
        model = genai.GenerativeModel(nombre_modelo)
        response = model.generate_content([prompt, imagen])
        return response.text
    except Exception as e:
        # SI FALLA: Iniciamos Protocolo de Diagnóstico
        error_msg = f"⚠️ Error con {nombre_modelo}: {str(e)}"
        
        # Consultamos qué modelos SÍ están disponibles
        lista_modelos = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    lista_modelos.append(m.name)
            debug_info = f"\n\n📋 **MODELOS DISPONIBLES EN TU CUENTA:**\n" + "\n".join(lista_modelos)
        except Exception as e2:
            debug_info = f"\n\nNo se pudo listar modelos: {str(e2)}"
            
        return error_msg + debug_info

# --- INTERFAZ ---
opcion = st.radio("Opción:", ["Subir Foto 📂", "Cámara 📸"], horizontal=True)
imagen_usuario = None

if opcion == "Subir Foto 📂":
    archivo = st.file_uploader("Imagen", type=["jpg", "png", "jpeg"])
    if archivo: imagen_usuario = Image.open(archivo)
elif opcion == "Cámara 📸":
    camera = st.camera_input("Foto")
    if camera: imagen_usuario = Image.open(camera)

if imagen_usuario and api_key:
    st.image(imagen_usuario, width=300)
    if st.button("🔍 ANALIZAR AHORA"):
        with st.spinner("Analizando..."):
            prompt = "Eres un nutricionista experto. Analiza este plato, estima calorías y di si es saludable. Sé breve."
            resultado = analizar_imagen(imagen_usuario, prompt, api_key)
            st.warning(resultado) # Usamos warning para que resalte si es error o texto
