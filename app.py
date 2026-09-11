import streamlit as st
import urllib.parse

# Configuración de la página (Ancho amplio para lucir el diseño)
st.set_page_config(page_title="Barbería Gods Time", page_icon="✂️", layout="wide")

# -------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (FONDO OSCURO, ESTILO DORADO Y TARJETAS)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo general oscuro de la aplicación */
    .stApp {
        background-color: #111111;
        color: #f0f0f0;
        background-image: radial-gradient(circle at center, #222222 0%, #0a0a0a 100%);
    }
    
    /* Contenedor principal de login / bienvenida */
    .main-container {
        background: rgba(20, 20, 20, 0.85);
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #333333;
        box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.7);
        max-width: 600px;
        margin: auto;
    }

    /* Título principal con estilo elegante */
    .brand-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        margin-bottom: 0px;
    }

    /* Subtítulo */
    .brand-subtitle {
        color: #b0b0b0;
        font-size: 1rem;
        font-style: italic;
        margin-bottom: 25px;
    }

    /* Estilo de botones personalizados */
    .stButton > button {
        background-color: #d4af37;
        color: #111111;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #f3c653;
        color: #000000;
    }

    /* Ocultar elementos predeterminados molestos de streamlit si se desea */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# INICIALIZAR ESTADOS EN LA SESIÓN
# -------------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "ventas" not in st.session_state:
    st.session_state.ventas = []

if "tasa_dolar" not in st.session_state:
    st.session_state.tasa_dolar = 36.50  # Tasa de referencia

if "citas" not in st.session_state:
    st.session_state.citas = []

# Precios base en dólares
SERVICIOS_PRECIOS = {
    "Corte Clásico": 8.0,
    "Corte + Barba": 12.0,
    "Corte Fade / Moderno": 10.0,
    "Barba sola": 5.0,
    "Corte Niño": 7.0
}

# -------------------------------------------------------------
# BARRA LATERAL (CONTROL Y TASA)
# -------------------------------------------------------------
st.sidebar.markdown("<h3 style='color: #d4af37; text-align: center;'>✂️ Gods Time Admin</h3>", unsafe_allow_html=True)
st.sidebar.info(f"💱 Tasa del Día: **{st.session_state.tasa_dolar:.2f} Bs/$**")

if st.session_state.autenticado:
    st.sidebar.divider()
    st.sidebar.success("Modo Administrador Activo")
    nueva_tasa = st.sidebar.number_input("Actualizar Tasa (Bs)", min_value=1.0, value=st.session_state.tasa_dolar, step=0.1)
    if nueva_tasa != st.session_state.tasa_dolar:
        st.session_state.tasa_dolar = nueva_tasa
        
    opcion_admin = st.sidebar.radio("Menú Admin:", [
        "📊 Panel de Control", 
        "💰 Registrar Venta", 
        "📋 Citas Guardadas", 
        "🚪 Cerrar Sesión"
    ])

# -------------------------------------------------------------
# FLUJO PRINCIPAL DE LA APLICACIÓN
# -------------------------------------------------------------

# SI NO ESTÁ AUTENTICADO: VEMOS LA PANTALLA EXACTA DE LA FOTO
if not st.session_state.autenticado:
    
    # Botón superior destacado para clientes (igual al de tu video)
    col_top1, col_top2, col_top3 = st.columns([1, 2, 1])
    with col_top2:
        modo_cliente = st.button("📅 ¡AGENDAR CITA AQUÍ!", use_container_width=True)

    if "ver_cliente" not in st.session_state:
        st.session_state.ver_cliente = False

    if modo_cliente:
        st.session_state.ver_cliente = not st.session_state.ver_cliente

    # SI EL CLIENTE HIZO CLIC EN AGENDAR, SE ABRE LA VISTA DE CITAS Y PRECIOS
    if st.session_state.ver_cliente:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #d4af37;'>Panel de Clientes - Barbería Gods Time</h2>", unsafe_allow_html=True)
        
        tab_cita, tab_precios = st.tabs(["📅 Agendar Cita", "💵 Lista de Precios"])
        
        with tab_cita:
            st.subheader("Reserva tu espacio")
            with st.form("form_cita_publica", clear_on_submit=True):
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    cliente_cita = st.text_input("Tu Nombre y Apellido")
                with col_c2:
                    telefono_cita = st.text_input("Número de Teléfono (Ej: 4121234567)")
                
                servicio_cita = st.selectbox("Selecciona el Servicio", list(SERVICIOS_PRECIOS.keys()))
                precio_usd = SERVICIOS_PRECIOS[servicio_cita]
                precio_bs = precio_usd * st.session_state.tasa_dolar
                
                st.info(f"💵 Precio estimado: **${precio_usd:.2f}** | 🇻🇪 **Bs {precio_bs:,.2f}**")
                
                col_f, col_h, col_b = st.columns(3)
                with col_f:
                    fecha_cita = st.date_input("Fecha de Cita")
                with col_h:
                    hora_cita = st.time_input("Hora de Cita")
                with col_b:
                    barbero_cita = st.selectbox("Barbero", ["Francisco", "Jonder"])
                
                submit_cita = st.form_submit_button("Agendar y Enviar a WhatsApp", use_container_width=True)
                
                if submit_cita:
                    if cliente_cita and telefono_cita:
                        mensaje = (
                            f"¡Hola! 👋 Quiero confirmar una cita en *Barbería Gods Time* ✂️.\n\n"
                            f"👤 Cliente: {cliente_cita}\n"
                            f"📅 Fecha: {fecha_cita}\n"
                            f"⏰ Hora: {hora_cita}\n"
                            f"💈 Servicio: {servicio_cita}\n"
                            f"👨‍🦱 Barbero: {barbero_cita}\n"
                            f"💰 Total: ${precio_usd:.2f} (Bs {precio_bs:,.2f
