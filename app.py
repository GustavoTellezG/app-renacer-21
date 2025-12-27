import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Scanner Renacer 21", page_icon="🥗", layout="centered")

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🥗 Coach Renacer: Scanner IA")
st.markdown("---")

# --- CONEXIÓN SECRETA (Sin pedirle nada al usuario) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Error: No se detectó la API Key del sistema.")
    st.stop()

# --- FUNCIÓN DE ANÁLISIS ---
def analizar_imagen(imagen):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    prompt = """
    Actúa como el Coach del 'Reto Renacer 21'. Analiza la imagen:
    1. 🥘 **Identifica**: ¿Qué es?
    2. 🔥 **Calorías**: Estimación rápida.
    3. 🚦 **Semáforo**: VERDE (Adelante), AMARILLO (Cuidado), ROJO (Evitar).
    4. 💡 **Consejo**: Tip corto y motivador.
    """
    return model.generate_content([prompt, imagen]).text

# --- INTERFAZ ---
opcion = st.radio("", ["📸 Tomar Foto", "📂 Subir desde Galería"], horizontal=True)

img_file = None

if opcion == "📸 Tomar Foto":
    img_file = st.camera_input("Captura tu plato")
elif opcion == "📂 Subir desde Galería":
    img_file = st.file_uploader("Elige tu imagen", type=["jpg", "png", "jpeg"])

if img_file:
    # Mostrar imagen
    imagen = Image.open(img_file)
    st.image(imagen, caption="Tu Plato", use_column_width=True)
    
    # Botón de acción
    if st.button("🔍 ANALIZAR MI PLATO"):
        with st.spinner("El Coach está revisando tus ingredientes..."):
            try:
                respuesta = analizar_imagen(imagen)
                st.markdown("### 📋 Veredicto del Coach:")
                st.info(respuesta)
                st.balloons() # ¡Efecto de celebración!
            except Exception as e:
                st.error(f"Error de conexión: {e}")
