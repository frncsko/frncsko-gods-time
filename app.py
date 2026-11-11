import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Fran ADS - Gestor de Publicidad",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estados en sesión
if "saldo" not in st.session_state:
    st.session_state.saldo = 350.00

if "bono_reclamado" not in st.session_state:
    st.session_state.bono_reclamado = False

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
            "presupuesto": 5.0,
            "audiencia": "Intereses: Moda & Estilo"
        },
        {
            "id": 4,
            "nombre": "Branding Apertura de Semana",
            "plataforma": "Display Red",
            "estado": "Activo",
            "clics": "890 clics",
            "presupuesto": 8.0,
            "audiencia": "Remarketing"
        }
    ]

# ----------------- DETECCIÓN DE ENLACE DE REGISTRO CON BONO -----------------
# Lee el parámetro de URL ?ref=... (ejemplo: https://tu-app.streamlit.app/?ref=FRAN10)
query_params = st.query_params
codigo_ref = query_params.get("ref", None)

if codigo_ref and not st.session_state.bono_reclamado:
    st.session_state.saldo += 10.00
    st.session_state.bono_reclamado = True
    st.toast
