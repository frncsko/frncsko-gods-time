import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Barberia God's Time", page_icon="✂️", layout="centered")

# Inicializar estados en la sesión
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
st.sidebar.title("✂️ Barberia God's Time")

# Mostrar tasa actual
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
        "📊 Inicio / Resumen", 
        "💰 Registrar Venta", 
        "📋 Ver Citas Guardadas", 
        "🚪 Cerrar Sesión"
    ])

# -------------------------------------------------------------
# VISTA PÚBLICA (CLIENTES: AGENDAR CITA Y VER PRECIOS)
# -------------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align: center;'>✂️ Barberia God's Time</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>¡Reserva tu cita fácil y rápido! Selecciona tu servicio a continuación.</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 Agendar Cita", "💵 Ver Precios"])
    
    with tab1:
        st.subheader("Reserva tu espacio")
        with st.form("form_cita_publica", clear_on_submit=True):
            cliente_cita = st.text_input("Tu Nombre y Apellido")
            telefono_cita = st.text_input("Tu Número de Teléfono (Ej: 4121234567)")
            
            servicio_cita = st.selectbox("Selecciona el Servicio", list(SERVICIOS_PRECIOS.keys()))
            precio_cita_usd = SERVICIOS_PRECIOS[servicio_cita]
            precio_cita_bs = precio_cita_usd * st.session_state.tasa_dolar
            
            st.write(f"💵 Precio estimado: **${precio_cita_usd:.2f}** | **Bs {precio_cita_bs:,.2f}**")
            
            col_f, col_h = st.columns(2)
            with col_f:
                fecha_cita = st.date_input("Fecha de la Cita")
            with col_h:
                hora_cita = st.time_input("Hora de la Cita")
                
            barbero_cita = st.selectbox("Elige tu Barbero Preferido", ["Francisco", "Jonder"])
            
            submit_cita = st.form_submit_button("Agendar y Enviar a WhatsApp", use_container_width=True)
            
            if submit_cita:
                if cliente_cita and telefono_cita:
                    # Estructurar mensaje para WhatsApp del negocio
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
                    
                    # Guardar cita en memoria
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
    if opcion_admin == "📊 Inicio / Resumen":
        st.title("📊 Panel de Control - Administrador")
        
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

    elif opcion_admin == "📋 Ver Citas Guardadas":
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
