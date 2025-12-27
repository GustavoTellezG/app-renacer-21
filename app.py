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
st.title("🥗 Coach Renacer 21: Scanner")
st.markdown("""
    *Sube una foto de tu plato para ver si cumple con el protocolo.*
""")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔐 Llave de Acceso")
    api_key = st.text_input("Ingresa tu Google API Key", type="password")
    
    st.markdown("---")
    st.info("💡 **Tip:** Asegúrate de que la foto tenga buena luz.")

# --- FUNCIÓN DE ANÁLISIS ---
def analizar_imagen(imagen, prompt, key):
    try:
        genai.configure(api_key=key)
        
        # AQUÍ ESTÁ EL CAMBIO CLAVE: Usamos el modelo que SÍ tienes
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        response = model.generate_content([prompt, imagen])
        return response.text
    except Exception as e:
        return f"⚠️ Error técnico: {str(e)}"

# --- INTERFAZ PRINCIPAL ---
opcion = st.radio("Elige una opción:", ["Subir Foto 📂", "Usar Cámara 📸"], horizontal=True)

imagen_usuario = None

if opcion == "Subir Foto 📂":
    archivo = st.file_uploader("Carga tu imagen aquí", type=["jpg", "jpeg", "png"])
    if archivo:
        imagen_usuario = Image.open(archivo)

elif opcion == "Usar Cámara 📸":
    camera = st.camera_input("Toma la foto")
    if camera:
        imagen_usuario = Image.open(camera)

# --- BOTÓN DE ACCIÓN ---
if imagen_usuario is not None:
    st.image(imagen_usuario, caption="Tu plato", use_column_width=True)
    
    if api_key:
        if st.button("🔍 CONSULTAR AL COACH"):
            with st.spinner("El Coach está analizando tus macros..."):
                
                # EL PROMPT DEL COACH RENACER
                prompt_sistema = """
                Actúa como el Coach Experto del 'Reto Renacer 21'. Tu tono es motivador pero educativo.
                Analiza la imagen de comida y responde:
                
                1. 🥘 **¿Qué es esto?**: Identifica los alimentos.
                2. 🔥 **Calorías Aprox**: Estimación rápida.
                3. 🚦 **Semáforo Renacer**: 
                   - VERDE (Adelante, cumple protocolo).
                   - AMARILLO (Cuidado con porciones/combinaciones).
                   - ROJO (Evitar, procesados/azúcar).
                4. 💡 **Consejo Táctico**: Un tip breve sobre cómo comerlo (orden de ingesta, etc).
                
                Sé conciso y directo.
                """
                
                resultado = analizar_imagen(imagen_usuario, prompt_sistema, api_key)
                
                if "⚠️ Error" in resultado:
                    st.error(resultado)
                else:
                    st.success("¡Análisis Completado!")
                    st.markdown(resultado)
    else:
        st.warning("⚠️ Por favor ingresa tu API Key en la barra lateral.")
