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
    # Intenta leer la clave desde los Secretos de Streamlit
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    # Si falla, muestra un mensaje amigable para ti (el administrador)
    st.error("⚠️ Error de Configuración: No se encontró la API Key en los 'Secrets' de Streamlit.")
    st.warning("Ve a 'Manage App' > 'Settings' > 'Secrets' y configura GOOGLE_API_KEY.")
    st.stop()

# --- FUNCIÓN DE ANÁLISIS (CEREBRO MEJORADO) ---
def analizar_imagen(imagen):
    # Usamos el modelo rápido y visual que ya validamos
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    # PROMPT DE ALTA PRECISIÓN
    prompt_sistema = """
    Actúa como el Coach Nutricional experto del 'Reto Renacer 21'.
    Analiza la imagen con visión de detalle "forense".
    
    🔍 **Instrucción de Diferenciación Visual:**
    - Fíjate en texturas internas, semillas y brillo.
    - Distingue bien entre Jitomate (rojo, pulpa húmeda, semillas visibles) vs Pimiento/Morrón (piel lisa, estructura hueca, sin pulpa líquida).
    
    Responde en este formato exacto:
    1. 🥘 **Identificación**: Lista los alimentos detectados con precisión.
    2. 🔥 **Calorías**: Estimación rápida del plato total.
    3. 🚦 **Semáforo**: 
       - VERDE (Adelante, alimentos naturales/fibra).
       - AMARILLO (Cuidado con porciones/combinaciones/frutas dulces).
       - ROJO (Evitar procesados/fritos/azúcares).
    4. 💡 **Consejo Renacer**: Un tip breve, empático y accionable basado en las reglas del reto (orden de ingesta, vinagre, hidratación).
    
    Sé conciso, motivador y directo.
    """
    
    # Generar respuesta
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
    # Convertir y mostrar imagen
    imagen = Image.open(img_file)
    st.image(imagen, caption="Tu Plato", use_column_width=True)
    
    if st.button("🔍 ANALIZAR MI PLATO"):
        with st.spinner("El Coach está analizando texturas e ingredientes..."):
            try:
                # Llamada a la IA
                respuesta = analizar_imagen(imagen)
                
                # Mostrar resultado
                st.success("¡Análisis Completado!")
                st.markdown(respuesta)
                st.balloons() # ¡Celebración!
                
            except Exception as e:
                st.error(f"Ocurrió un error técnico: {str(e)}")
