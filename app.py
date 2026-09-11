import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Barberia God's Time", page_icon="✂️", layout="wide")

# -------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (TEMA OSCURO + EFECTO DORADO BRILLANTE)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Estilo general de la app (Modo Oscuro Elegante) */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Efecto de letras doradas con brillo de espejo animado */
    @keyframes shine {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    .gold-title {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #b38728 0%, #fbf5b7 25%, #bf953f 50%, #fcf6ba 75%, #aa771c 100%);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: shine 4s linear infinite;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.8);
        margin-bottom: 0px;
    }

    /* Tarjetas de métricas y contenedores modernos */
    div.stMetric, div[data-testid="stVerticalBlock"] > div {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2d2d2d;
    }

    /* Ajustes para la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #181818;
        border-right: 1px solid #2d2d2d;
    }
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
    st.session_state.tasa_dolar = 36.50  # Tasa inicial de referencia

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
# BARRA LATERAL (CONTROL DE ACCESO Y TASA)
# -------------------------------------------------------------
st.sidebar.markdown("<h3 style='color: #fbf5b7; text-align: center;'>✂️ God's Time Admin</h3>", unsafe_allow_html=True)
st.sidebar.info(f"💱 Tasa del Día: **{st.session_state.tasa_dolar:.2f} Bs/$**")

if not st.session_state.autenticado:
    st.sidebar.divider()
    with st.sidebar.expander("🔑 Acceso Administrador"):
        with st.form("form_login_side", clear_on_submit=True):
            usuario = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit_login = st.form_submit_button("Ingresar", use_container_width=True)
            
            if submit_login:
                if usuario == "admin" and password == "1234":
                    st.session_state.autenticado = True
                    st.success("¡Bienvenido admin!")
                    st.rerun()
                else:
                    st.error("Datos incorrectos")
else:
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
# ENCABEZADO CON EFECTO DORADO BRILLANTE
# -------------------------------------------------------------
st.markdown("<h1 class='gold-title'>✂️ BARBERIA GOD'S TIME</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 1.1rem;'>Sistema de Control y Gestión Profesional</p>", unsafe_allow_html=True)
st.divider()

# -------------------------------------------------------------
# VISTA PÚBLICA (CLIENTES: AGENDAR CITA Y VER PRECIOS)
# -------------------------------------------------------------
if not st.session_state.autenticado:
    tab1, tab2 = st.tabs(["📅 Agendar Cita", "💵 Ver Precios"])
    
    with tab1:
        st.subheader("Reserva tu espacio")
        with st.form("form_cita_publica", clear_on_submit=True):
            col_1, col_2 = st.columns(2)
            with col_1:
                cliente_cita = st.text_input("Tu Nombre y Apellido")
            with col_2:
                telefono_cita = st.text_input("Tu Número de Teléfono (Ej: 4121234567)")
            
            servicio_cita = st.selectbox("Selecciona el Servicio", list(SERVICIOS_PRECIOS.keys()))
            precio_cita_usd = SERVICIOS_PRECIOS[servicio_cita]
            precio_cita_bs = precio_cita_usd * st.session_state.tasa_dolar
            
            st.info(f"💵 Precio estimado: **${precio_cita_usd:.2f}** | 🇻🇪 **Bs {precio_cita_bs:,.2f}**")
            
            col_f, col_h, col_b = st.columns(3)
            with col_f:
                fecha_cita = st.date_input("Fecha de la Cita")
            with col_h:
                hora_cita = st.time_input("Hora de la Cita")
            with col_b:
                barbero_cita = st.selectbox("Barbero Preferido", ["Francisco", "Jonder"])
            
            submit_cita = st.form_submit_button("Agendar y Enviar a WhatsApp", use_container_width=True)
            
            if submit_cita:
                if cliente_cita and telefono_cita:
                    mensaje = (
                        f"¡Hola! 👋 Quiero confirmar una cita en *Barberia God's Time* ✂️.\n\n"
                        f"👤 Cliente: {cliente_cita}\n"
                        f"📅 Fecha: {fecha_cita}\n"
                        f"⏰ Hora: {hora_cita}\n"
                        f"💈 Servicio: {servicio_cita}\n"
                        f"👨‍🦱 Barbero: {barbero_cita}\n"
                        f"💰 Precio: ${precio_cita_usd:.2f} (Bs {precio_cita_bs:,.2f})"
                    )
                    
                    tel_limpio = "".join(filter(str.isdigit, telefono_cita))
                    if len(tel_limpio) == 10 and tel_limpio.startswith("4"):
                        tel_limpio = "58" + tel_limpio
                        
                    url_whatsapp = f"https://wa.me/{tel_limpio}?text={urllib.parse.quote(mensaje)}"
                    
                    st.session_state.citas.append({
                        "cliente": cliente_cita,
                        "telefono": telefono_cita,
                        "servicio": servicio_cita,
                        "fecha": str(fecha_cita),
                        "hora": str(hora_cita),
                        "barbero": barbero_cita,
                        "link": url_whatsapp
                    })
                    
                    st.success("¡Cita registrada con éxito!")
                    st.markdown(f"### 👉 [Haz clic aquí para enviar tu confirmación por WhatsApp]({url_whatsapp})", unsafe_allow_html=True)
                else:
                    st.error("Por favor ingresa tu nombre y número de teléfono.")

    with tab2:
        st.subheader("Nuestra Lista de Precios")
        st.caption(f"Valores calculados a tasa de: {st.session_state.tasa_dolar:.2f} Bs/$")
        
        for serv, precio_usd in SERVICIOS_PRECIOS.items():
            precio_bs = precio_usd * st.session_state.tasa_dolar
            st.markdown(f"**{serv}** — 💵 **${precio_usd:.2f}** / 🇻🇪 **Bs {precio_bs:,.2f}**")

# -------------------------------------------------------------
# VISTA PANEL DE ADMINISTRADOR (CUANDO ESTÁ LOGUEADO)
# -------------------------------------------------------------
else:
    if opcion_admin == "📊 Panel de Control":
        st.title("📊 Panel de Control")
        
        total_ventas_usd = sum(v["monto_usd"] for v in st.session_state.ventas)
        total_ventas_bs = total_ventas_usd * st.session_state.tasa_dolar
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Ventas Totales ($)", f"${total_ventas_usd:.2f}")
        col2.metric("Ventas Totales (Bs)", f"Bs {total_ventas_bs:,.2f}")
        col3.metric("Servicios Realizados", len(st.session_state.ventas))
        
        st.divider()
        st.subheader("📋 Últimos servicios registrados")
        if st.session_state.ventas:
            for v in reversed(st.session_state.ventas[-5:]):
                st.write(f"🔹 **{v['servicio']}** | 💵 ${v['monto_usd']:.2f} (Bs {v['monto_bs']:,.2f}) - Barbero: *{v['barbero']}*")
        else:
            st.info("Aún no hay ventas registradas hoy.")

    elif opcion_admin == "💰 Registrar Venta":
        st.title("💰 Registrar Nuevo Servicio")
        
        with st.form("form_venta_admin", clear_on_submit=True):
            servicio_seleccionado = st.selectbox("Seleccionar Servicio", list(SERVICIOS_PRECIOS.keys()))
            precio_sugerido_usd = SERVICIOS_PRECIOS[servicio_seleccionado]
            monto_usd = st.number_input("Monto en Dólares ($)", min_value=0.0, value=precio_sugerido_usd, step=1.0)
            monto_bs = monto_usd * st.session_state.tasa_dolar
            st.info(f"Equivalente en Bolívares: **Bs {monto_bs:,.2f}**")
            
            barbero = st.selectbox("Barbero Responsable", ["Francisco", "Jonder"])
            cliente = st.text_input("Nombre del Cliente")
            if not cliente:
                cliente = "Cliente General"
                
            submit_venta = st.form_submit_button("Guardar Venta", use_container_width=True)
            
            if submit_venta:
                st.session_state.ventas.append({
                    "servicio": servicio_seleccionado,
                    "monto_usd": monto_usd,
                    "monto_bs": monto_bs,
                    "barbero": barbero,
                    "cliente": cliente
                })
                st.success("¡Venta registrada con éxito!")

    elif opcion_admin == "📋 Citas Guardadas":
        st.title("📋 Citas Solicitadas por Clientes")
        if st.session_state.citas:
            for c in reversed(st.session_state.citas):
                st.markdown(f"**{c['cliente']}** ({c['telefono']}) — *{c['servicio']}* con **{c['barbero']}** el {c['fecha']} a las {c['hora']}")
                st.markdown(f"[💬 Enviar/Revisar WhatsApp]({c['link']})", unsafe_allow_html=True)
                st.divider()
        else:
            st.info("No hay citas registradas todavía.")

    elif opcion_admin == "🚪 Cerrar Sesión":
        st.session_state.autenticado = False
        st.rerun()
