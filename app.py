import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Scanner Renacer 21",
    page_icon="🥗",
    layout="centered"
)

# --- ESTILOS VISUALES (CSS) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.title("🥗 Coach Renacer: Scanner IA")
st.markdown("---")

# --- CONEXIÓN SEGURA (Secretos) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Error de Configuración: No se encontró la API Key.")
    st.stop()

# --- FUNCIÓN DE ANÁLISIS (CEREBRO AJUSTADO) ---
def analizar_imagen(imagen):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    # PROMPT CON RESTRICCIONES DE MARCA
    prompt_sistema = """
    Actúa como el Coach Nutricional experto del 'Reto Renacer 21'.
    Analiza la imagen con visión de detalle "forense" (texturas, semillas, brillo).
    
    🔍 **Instrucciones de Personalidad:**
    - Tono: Profesional, empático y basado en ciencia.
    - ⛔ **RESTRICCIÓN ABSOLUTA:** NUNCA recomiendes "vinagre de manzana" ni remedios caseros.
    - Enfócate solo en: Composición del plato, macronutrientes, orden de ingesta (vegetales primero) e hidratación.
    
    Responde en este formato exacto:
    1. 🥘 **Identificación**: Lista los alimentos detectados (distingue bien jitomate vs pimiento).
    2. 🔥 **Calorías**: Estimación rápida del plato total.
    3. 🚦 **Semáforo**: 
       - VERDE (Adelante, alimentos naturales/fibra).
       - AMARILLO (Cuidado con porciones/combinaciones/frutas dulces).
       - ROJO (Evitar procesados/fritos/azúcares).
    4. 💡 **Consejo Renacer**: Un tip breve y accionable (Ej: "Mastica despacio", "Bebe agua antes", "Empieza por la fibra").
    """
    
    response = model.generate_content([prompt_sistema, imagen])
    return response.text

# --- INTERFAZ DE USUARIO ---
opcion = st.radio("Elige una opción:", ["📸 Tomar Foto", "📂 Subir desde Galería"], horizontal=True)

img_file = None

if opcion == "📸 Tomar Foto":
    img_file = st.camera_input("Captura tu plato")
elif opcion == "📂 Subir desde Galería":
    img_file = st.file_uploader("Elige tu imagen", type=["jpg", "png", "jpeg"])

# --- LÓGICA DEL BOTÓN ---
if img_file:
    imagen = Image.open(img_file)
    st.image(imagen, caption="Tu Plato", use_column_width=True)
    
    if st.button("🔍 ANALIZAR MI PLATO"):
        with st.spinner("El Coach está analizando tus nutrientes..."):
            try:
                respuesta = analizar_imagen(imagen)
                st.success("¡Análisis Completado!")
                st.markdown(respuesta)
                st.balloons()
            except Exception as e:
                st.error(f"Error técnico: {str(e)}")
