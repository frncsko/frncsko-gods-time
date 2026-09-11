import streamlit as st
import urllib.parse

# Configuración de la página (ancho centrado simulando app móvil/moderna)
st.set_page_config(page_title="Barberia God's Time", page_icon="✂️", layout="centered")

# -------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (ESTILO APP MÓVIL OSCURA / AMARILLO OCRE)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo general oscuro estilo app */
    .stApp {
        background-color: #161616;
        color: #f0f0f0;
    }
    
    /* Efecto de letras doradas con brillo de espejo animado */
    @keyframes shine {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    .gold-title {
        font-size: 2.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #b38728 0%, #ffdf73 25%, #d4af37 50%, #fff1a8 75%, #aa771c 100%);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: shine 4s linear infinite;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 0px;
    }

    /* Tarjetas oscuras modernas */
    div.stMetric, div[data-testid="stVerticalBlock"] > div {
        background-color: #212121;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #333333;
    }

    /* Botones principales estilo ocre/dorado de la app de referencia */
    .stButton > button {
        background-color: #d4af37;
        color: #121212;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #f3c653;
        color: #000000;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
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
# BARRA LATERAL (ADMINISTRACIÓN Y TASA)
# -------------------------------------------------------------
st.sidebar.markdown("<h3 style='color: #d4af37; text-align: center;'>✂️ God's Time</h3>", unsafe_allow_html=True)
st.sidebar.info(f"💱 Tasa del Día: **{st.session_state.tasa_dolar:.2f} Bs/$**")

if not st.session_state.autenticado:
    st.sidebar.divider()
    with st.sidebar.expander("🔑 Acceso Administrador"):
        with st.form("form_login_side", clear_on_submit=True):
            usuario = st.text_input("Correo / Usuario")
            password = st.text_input("Contraseña", type="password")
            submit_login = st.form_submit_button("LOG IN", use_container_width=True)
            
            if submit_login:
                if usuario == "admin" and password == "1234":
                    st.session_state.autenticado = True
                    st.success("¡Bienvenido!")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
else:
    st.sidebar.divider()
    st.sidebar.success("Sesión Activa (Admin)")
    nueva_tasa = st.sidebar.number_input("Actualizar Tasa (Bs)", min_value=1.0, value=st.session_state.tasa_dolar, step=0.1)
    if nueva_tasa != st.session_state.tasa_dolar:
        st.session_state.tasa_dolar = nueva_tasa
        
    opcion_admin = st.sidebar.radio("Menú Admin:", [
        "📊 Dashboard General", 
        "💰 Registrar Venta", 
        "📋 Citas Pendientes", 
        "🚪 Cerrar Sesión"
    ])

# -------------------------------------------------------------
# ENCABEZADO CON EFECTO DORADO BRILLANTE
# -------------------------------------------------------------
st.markdown("<h1 class='gold-title'>BARBERIA GOD'S TIME</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 0.95rem; letter-spacing: 2px;'>SINCE 2026 💈</p>", unsafe_allow_html=True)
st.divider()

# -------------------------------------------------------------
# VISTA PÚBLICA (CLIENTES)
# -------------------------------------------------------------
if not st.session_state.autenticado:
    
    # Categorías / Pestañas estilo interfaz móvil de referencia
    tab_cita, tab_precios, tab_barberos = st.tabs(["📅 Reservar Cita", "✂️ Servicios", "👨‍🦱 Barberos"])
    
    with tab_cita:
        st.subheader("Selecciona tu estilo y cita")
        with st.form("form_cita_app", clear_on_submit=True):
            cliente_cita = st.text_input("Nombre y Apellido")
            telefono_cita = st.text_input("Teléfono de Contacto (Ej: 4121234567)")
            
            servicio_cita = st.selectbox("Servicio Seleccionado", list(SERVICIOS_PRECIOS.keys()))
            precio_usd = SERVICIOS_PRECIOS[servicio_cita]
            precio_bs = precio_usd * st.session_state.tasa_dolar
            
            st.info(f"💵 Inversión: **${precio_usd:.2f}** / 🇻🇪 **Bs {precio_bs:,.2f}**")
            
            c1, c2 = st.columns(2)
            with c1:
                fecha_cita = st.date_input("Fecha")
            with c2:
                hora_cita = st.time_input("Hora")
                
            barbero_cita = st.selectbox("Barbero Disponible", ["Francisco", "Jonder"])
            
            book_btn = st.form_submit_button("BOOK AN APPOINTMENT", use_container_width=True)
            
            if book_btn:
                if cliente_cita and telefono_cita:
                    mensaje = (
                        f"¡Hola! 👋 Quiero confirmar mi cita en *Barberia God's Time* ✂️.\n\n"
                        f"👤 Cliente: {cliente_cita}\n"
                        f"📅 Fecha: {fecha_cita}\n"
                        f"⏰ Hora: {hora_cita}\n"
                        f"💈 Servicio: {servicio_cita}\n"
                        f"👨‍🦱 Barbero: {barbero_cita}\n"
                        f"💰 Total: ${precio_usd:.2f} (Bs {precio_bs:,.2f})"
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
                    
                    st.success("¡Cita lista para enviar!")
                    st.markdown(f"### 👉 [Toca aquí para enviar los datos por WhatsApp]({url_whatsapp})", unsafe_allow_html=True)
                else:
                    st.error("Por favor completa tu nombre y número de teléfono.")

    with tab_precios:
        st.subheader("Catálogo de Servicios")
        st.caption(f"Precios actualizados a tasa: {st.session_state.tasa_dolar:.2f} Bs/$")
        for serv, p_usd in SERVICIOS_PRECIOS.items():
            p_bs = p_usd * st.session_state.tasa_dolar
            st.markdown(f"✔️ **{serv}** — 💵 **${p_usd:.2f}** | 🇻🇪 **Bs {p_bs:,.2f}**")

    with tab_barberos:
        st.subheader("Nuestro Equipo Profesional")
        st.markdown("""
        - 💈 **Francisco** (Especialista en cortes modernos y barba)
        - 💈 **Jonder** (Especialista en fades y estilos clásicos)
        """)

# -------------------------------------------------------------
# VISTA ADMINISTRADOR (PANEL DE CONTROL TIPO TREINTA / SHEARBA)
# -------------------------------------------------------------
else:
    if opcion_admin == "📊 Dashboard General":
        st.title("Panel de control")
        st.caption("Resumen de estadísticas del negocio")
        
        total_usd = sum(v["monto_usd"] for v in st.session_state.ventas)
        total_bs = total_usd * st.session_state.tasa_dolar
        
        # Tarjetas de estadísticas simulando la imagen de referencia
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Citas Hoy", len(st.session_state.citas))
        c2.metric("Ventas Hoy", f"${total_usd:.2f}")
        c3.metric("Bolívares", f"Bs {total_bs:,.2f}")
        c4.metric("Servicios", len(st.session_state.ventas))
        
        st.divider()
        st.subheader("Citas de hoy")
        if st.session_state.citas:
            for c in reversed(st.session_state.citas[-5:]):
                st.write(f"🕒 {c['hora']} | 👤 {c['cliente']} | 💈 {c['barbero']} - {c['servicio']}")
        else:
            st.info("No hay citas registradas para esta fecha")

    elif opcion_admin == "💰 Registrar Venta":
        st.title("💰 Registrar Venta")
        with st.form("form_venta_admin", clear_on_submit=True):
            servicio_sel = st.selectbox("Servicio", list(SERVICIOS_PRECIOS.keys()))
            p_sugerido = SERVICIOS_PRECIOS[servicio_sel]
            monto_u = st.number_input("Monto en Dólares ($)", min_value=0.0, value=p_sugerido, step=1.0)
            monto_b = monto_u * st.session_state.tasa_dolar
            st.info(f"Equivalente: **Bs {monto_b:,.2f}**")
            
            barb = st.selectbox("Barbero", ["Francisco", "Jonder"])
            cli = st.text_input("Cliente", value="Cliente General")
            
            if st.form_submit_button("Guardar Transacción", use_container_width=True):
                st.session_state.ventas.append({
                    "servicio": servicio_sel,
                    "monto_usd": monto_u,
                    "monto_bs": monto_b,
                    "barbero": barb,
                    "cliente": cli
                })
                st.success("¡Venta registrada exitosamente!")

    elif opcion_admin == "📋 Citas Pendientes":
        st.title("📋 Gestión de Citas")
        if st.session_state.citas:
            for c in st.session_state.citas:
                st.markdown(f"**{c['cliente']}** ({c['telefono']}) — *{c['servicio']}* con **{c['barbero']}** ({c['fecha']} - {c['hora']})")
                st.markdown(f"[💬 Abrir WhatsApp de Cita]({c['link']})", unsafe_allow_html=True)
                st.divider()
        else:
            st.info("No hay citas guardadas en este momento.")

    elif opcion_admin == "🚪 Cerrar Sesión":
        st.session_state.autenticado = False
        st.rerun()
