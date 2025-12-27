import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Scanner Renacer 21",
    page_icon="🥗",
    layout="centered"
)

# --- CABECERA Y ESTILO ---
st.title("🥗 Coach Renacer 21: Scanner de Alimentos")
st.markdown("""
    *Bienvenido al Reto Renacer. Sube una foto de tu plato para analizar si cumple con nuestro protocolo.*
""")

# --- BARRA LATERAL (CONFIGURACIÓN) ---
with st.sidebar:
    st.header("🔐 Llave de Acceso")
    api_key = st.text_input("Ingresa tu Google API Key", type="password")
    st.warning("Tu llave no se guarda, solo se usa para esta sesión.")
    st.markdown("---")
    st.markdown("**Reglas de Oro Renacer:**")
    st.markdown("1. 🥬 Fibra primero")
    st.markdown("2. 🥩 Proteína y Grasas")
    st.markdown("3. 🍠 Carbohidratos al final")

# --- FUNCIÓN PARA CONSULTAR A GEMINI ---
def analizar_imagen(imagen, prompt, key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash') # Usamos Flash para respuesta rápida
        response = model.generate_content([prompt, imagen])
        return response.text
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- INTERFAZ PRINCIPAL ---
opcion = st.radio("¿Cómo quieres subir tu plato?", ["Subir Foto 📂", "Tomar Foto 📸"], horizontal=True)

imagen_usuario = None

if opcion == "Subir Foto 📂":
    archivo = st.file_uploader("Sube tu imagen aquí...", type=["jpg", "jpeg", "png"])
    if archivo:
        imagen_usuario = Image.open(archivo)

elif opcion == "Tomar Foto 📸":
    camera = st.camera_input("Toma una foto de tu comida")
    if camera:
        imagen_usuario = Image.open(camera)

# --- ANÁLISIS ---
if imagen_usuario is not None and api_key:
    st.image(imagen_usuario, caption="Tu plato", use_column_width=True)
    
    if st.button("🔍 ANALIZAR PLATO AHORA"):
        with st.spinner("El Coach está revisando tus ingredientes..."):
            
            # EL PROMPT MAESTRO (Aquí está la inteligencia del Coach)
            prompt_sistema = """
            Actúa como el Coach Experto en Nutrición y Salud del 'Reto Renacer 21'. 
            Tu tono es motivador pero firme con las reglas de salud metabólica.
            Analiza la imagen de comida adjunta y responde en este formato estructurado:

            1. 🥘 **Identificación:** ¿Qué alimentos ves en el plato? (Sé breve).
            2. 🔥 **Calorías Estimadas:** Un rango aproximado total.
            3. 🚦 **Semáforo Renacer:** - VERDE (Excelente, cumple protocolo anti-inflamatorio).
               - AMARILLO (Precaución, cuida las porciones o combinaciones).
               - ROJO (Evitar, contiene procesados, azúcar o harinas refinadas).
            4. 🧬 **Análisis Metabólico:** Explica brevemente el impacto en la insulina de este plato.
            5. 💡 **Consejo Táctico:** Dales un consejo accionable basado en las reglas del reto (ej. orden de ingesta, agregar vinagre, caminar después de comer).
            """
            
            resultado = analizar_imagen(imagen_usuario, prompt_sistema, api_key)
            st.markdown("---")
            st.markdown(resultado)
            st.success("¡Análisis completado! Sigue adelante con el Reto.")

elif imagen_usuario is not None and not api_key:
    st.warning("⚠️ Por favor ingresa tu API Key en la barra lateral para activar al Coach.")
