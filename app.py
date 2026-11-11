import streamlit as st

# 1. Configuración de página (debe ser la primera orden de Streamlit)
st.set_page_config(
    page_title="Fran ADS - Gestor de Publicidad",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialización segura de variables en session_state
if "saldo" not in st.session_state:
    st.session_state.saldo = 350.00

if "bono_reclamado" not in st.session_state:
    st.session_state.bono_reclamado = False

if "mensaje_bono" not in st.session_state:
    st.session_state.mensaje_bono = False

if "campanas" not in st.session_state:
    st.session_state.campanas = [
        {
            "id": 1,
            "nombre": "Campaña Conversión Promo VIP",
            "plataforma": "TikTok Reels",
            "estado": "Activo",
            "clics": "3,120 clics",
            "presupuesto": 15.0,
            "audiencia": "Radio Local (10 km)"
        },
        {
            "id": 2,
            "nombre": "Re-engagement Audiencia Local",
            "plataforma": "Instagram Feed",
            "estado": "Activo",
            "clics": "1,240 clics",
            "presupuesto": 10.0,
            "audiencia": "Público General 18-35"
        },
        {
            "id": 3,
            "nombre": "Lanzamiento Edición Especial",
            "plataforma": "Historias / Shorts",
            "estado": "Pausado",
            "clics": "470 clics",
            "presupuesto": 5.
