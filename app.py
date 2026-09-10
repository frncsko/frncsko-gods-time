import base64
import urllib.parse
import pandas as pd
import streamlit as st

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Barbería Gods Time", page_icon="💈", layout="wide"
)

# 2. Cargar imagen de fondo local con manejo de errores
bg_css = ""
try:
    with open("GTBARBER.jpg", "rb") as f:
        bytes_imagen = f.read()
        imagen_base64 = base64.b64encode(bytes_imagen).decode()
        bg_css = f"""
        .stApp {{
            background-image: linear-gradient(rgba(14, 14, 16, 0.85), rgba(14, 14, 16, 0.85)), 
                    url("data:image/png;base64,{imagen_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
except FileNotFoundError:
    bg_css = """
    .stApp {
        background-color: #0E0E10;
    }
    """

# Inyectar el estilo de fondo
st.markdown(f"<style>{bg_css}</style>", unsafe_allow_html=True)

# Configuración de WhatsApp del Administrador/Barbería
NUMERO_WHATSAPP_ADMIN = "584125205165"

USUARIOS_VALIDOS = {
    "admin": "admin",
    "francisco": "barbero1",
    "jonder": "barbero2",
}

lista_barberos = ["Barbero Francisco", "Barbero Jonder"]

# Diccionario de servicios con sus precios predeterminados en dólares ($)
SERVICIOS_PRECIOS = {
    "CORTE": 8.0,
    "BARBA": 3.0,
    "CORTE / BARBA": 10.0,
    "Corte + Barba + Cejas (VIP)": 12.0,
    "MASCARILLA FACIAL": 1.0,
}
servicios_lista = list(SERVICIOS_PRECIOS.keys())

# Inicialización de Estados (Historial de servicios en cero)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "ver_agendar_publico" not in st.session_state:
    st.session_state.ver_agendar_publico = False

if "servicios_realizados" not in st.session_state:
    st.session_state.servicios_realizados = pd.DataFrame(
        columns=[
            "Fecha",
            "Cliente",
            "Teléfono",
            "Barbero",
            "Servicio",
            "Precio ($)",
        ]
    )

if "citas" not in st.session_state:
    st.session_state.citas = pd.DataFrame(
        columns=[
            "Fecha y Hora",
            "Cliente",
            "Teléfono",
            "Barbero",
            "Servicio",
            "Precio Estimado ($)",
            "Estado",
        ]
    )

if "gastos_barberia" not in st.session_state:
    st.session_state.gastos_barberia = pd.DataFrame(
        columns=["Fecha", "Barbero / Asignación", "Descripción", "Monto ($)"]
    )

if "fiados" not in st.session_state:
    st.session_state.fiados = pd.DataFrame(
        columns=["Cliente", "Teléfono", "Deuda Pendiente ($)", "Estado"]
    )

# --- PANTALLA PÚBLICA / INICIO DE SESIÓN ---
if not st.session_state.autenticado:
    st.title("💈 BARBERÍA GODS TIME")
    st.markdown(
        "<p style='color: #D4AF37 !important; font-size: 1.1em;'><i>Excelencia, estilo y precisión en cada detalle.</i></p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    col_centered = st.columns([1, 2, 1])
    with col_centered[1]:
        if st.session_state.ver_agendar_publico:
            st.subheader("📅 Agendar Cita de Barbería")
            st.write(
                "Llena el formulario para reservar tu turno. Se enviará la confirmación directamente por WhatsApp."
            )

            with st.form("form_cita_publica"):
                cli_pub = st.text_input("Tu Nombre Completo")
                tel_pub = st.text_input(
                    "Tu Número de WhatsApp (ej. +584121234567)"
                )
                barbero_pub = st.selectbox("Selecciona Barbero", lista_barberos)
                
                serv_pub = st.selectbox("Servicio Deseado", servicios_lista)
                precio_sugerido_pub = SERVICIOS_PRECIOS.get(serv_pub, 0.0)
                st.caption(f"💵 Precio automático: ${precio_sugerido_pub:,.2f}")

                col_f_p, col_h_p = st.columns(2)
                with col_f_p:
                    fecha_pub = st.date_input("Fecha preferida")
                with col_h_p:
                    hora_pub = st.time_input("Hora preferida")

                submit_pub = st.form_submit_button(
                    "📩 Reservar Turno y Notificar por WhatsApp"
                )

                if submit_pub and cli_pub and tel_pub:
                    fecha_hora_str = f"{fecha_pub} {hora_pub.strftime('%H:%M')}"
                    nueva_cita = pd.DataFrame(
                        {
                            "Fecha y Hora": [fecha_hora_str],
                            "Cliente": [cli_pub],
                            "Teléfono": [tel_pub],
                            "Barbero": [barbero_pub],
                            "Servicio": [serv_pub],
                            "Precio Estimado ($)": [precio_sugerido_pub],
                            "Estado": ["Pendiente (Online)"],
                        }
                    )
                    st.session_state.citas = pd.concat(
                        [st.session_state.citas, nueva_cita], ignore_index=True
                    )

                    svg_wsp = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16" style="vertical-align: middle; margin-right: 6px;"><path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.601 2.326zm-5.607 12.1a6.56 6.56 0 0 1-3.355-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.644-.182-.065-.315-.099-.445.099-.13.197-.506.644-.62.778-.114.133-.228.148-.425.05-.197-.1-.83-.306-1.583-.976-.585-.522-.982-1.166-1.096-1.363-.114-.197-.012-.304.087-.403.089-.088.197-.228.295-.342.1-.114.133-.197.198-.327.065-.13.032-.248-.016-.347-.049-.099-.445-1.072-.61-1.47-.16-.389-.323-.335-.445-.342l-.38-.008c-.13 0-.342.049-.522.248-.18.198-.695.678-.695 1.654 0 .976.712 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.837.327 1.124.418.475.152.908.13 1.25.079.382-.057 1.17-.478 1.335-.94.165-.463.165-.86.115-.94-.05-.079-.182-.13-.38-.228z"/></svg>'
                    mensaje_wsp = urllib.parse.quote(
                        f"💈 *NUEVA CITA AGENDADA EN LÍNEA*\n\n"
                        f"👤 *Cliente:* {cli_pub}\n"
                        f"📱 *Teléfono:* {tel_pub}\n"
                        f"✂️ *Barbero:* {barbero_pub}\n"
                        f"💈 *Servicio:* {serv_pub} (${precio_sugerido_pub:,.2f})\n"
                        f"📅 *Fecha y Hora:* {fecha_hora_str}"
                    )
                    wsp_link = (
                        f"https://wa.me/{NUMERO_WHATSAPP_ADMIN}?text={mensaje_wsp}"
                    )

                    st.success("¡Cita registrada con éxito en el sistema!")
                    st.markdown(
                        f'<a href="{wsp_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:6px; font-weight:bold; width:100%; cursor:pointer; font-size:1.1em; display:flex; align-items:center; justify-content:center;">{svg_wsp} Notificar por WhatsApp</button></a>',
                        unsafe_allow_html=True,
                    )

            st.write("")
            if st.button("⬅️ Volver al Inicio de Sesión"):
                st.session_state.ver_agendar_publico = False
                st.rerun()

        else:
            st.subheader("🔑 Iniciar Sesión")
            with st.form("form_login"):
                usuario_input = st.text_input("Usuario").strip().lower()
                password_input = st.text_input("Contraseña", type="password")
                btn_login = st.form_submit_button("Ingresar al Sistema")

                if btn_login:
                    if (
                        usuario_input in USUARIOS_VALIDOS
                        and USUARIOS_VALIDOS[usuario_input] == password_input
                    ):
                        st.session_state.autenticado = True
                        st.session_state.usuario_actual = (
                            usuario_input.capitalize()
                        )
                        st.success(
                            f"¡Bienvenido, {st.session_state.usuario_actual}!"
                        )
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos.")

            st.markdown("---")
            st.write("¿Eres cliente y quieres reservar un turno?")

            svg_wsp = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16" style="vertical-align: middle; margin-right: 6px;"><path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.601 2.326zm-5.607 12.1a6.56 6.56 0 0 1-3.355-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.644-.182-.065-.315-.099-.445.099-.13.197-.506.644-.62.778-.114.133-.228.148-.425.05-.197-.1-.83-.306-1.583-.976-.585-.522-.982-1.166-1.096-1.363-.114-.197-.012-.304.087-.403.089-.088.197-.228.295-.342.1-.114.133-.197.198-.327.065-.13.032-.248-.016-.347-.049-.099-.445-1.072-.61-1.47-.16-.389-.323-.335-.445-.342l-.38-.008c-.13 0-.342.049-.522.248-.18.198-.695.678-.695 1.654 0 .976.712 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.837.327 1.124.418.475.152.908.13 1.25.079.382-.057 1.17-.478 1.335-.94.165-.463.165-.86.115-.94-.05-.079-.182-.13-.38-.228z"/></svg>'
            wsp_menu_link = (
                f"https://wa.me/{NUMERO_WHATSAPP_ADMIN}?text="
                + urllib.parse.quote(
                    "Hola, quisiera consultar disponibilidad o agendar una cita en Barbería Gods Time."
                )
            )
            st.markdown(
                f'<a href="{wsp_menu_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 15px; border-radius:6px; font-weight:bold; width:100%; cursor:pointer; font-size:1em; display:flex; align-items:center; justify-content:center; margin-bottom: 10px;">{svg_wsp} Escríbenos al WhatsApp</button></a>',
                unsafe_allow_html=True,
            )

            if st.button("📅 Agendar Cita Aquí (Público)"):
                st.session_state.ver_agendar_publico = True
                st.rerun()

    st.stop()

# --- MENÚ LATERAL IZQUIERDO ---
with st.sidebar:
    st.markdown(f"👤 **Usuario:** {st.session_state.usuario_actual}")
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.session_state.usuario_actual = ""
        st.session_state.ver_agendar_publico = False
        st.rerun()

    st.markdown("---")
    st.subheader("📌 Menú Principal")

    opciones_menu = [
        "💵 Caja y Resumen",
        "✂️ Registrar Servicio",
        "✂️ Historial Francisco",
        "✂️ Historial Jonder",
        "📅 Agendar Citas",
        "⏰ Recordatorio de Cortes",
        "👥 Barberos y Comisión",
        "📤 Gastos del Local",
        "📝 Cobrar Fiados",
    ]

    opcion_menu = st.radio("", opciones_menu)

    # Restringir la opción de Reiniciar Datos solo para Administrador y Francisco (Oculto para Jonder)
    if st.session_state.usuario_actual in ["Admin", "Francisco"]:
        st.markdown("---")
        st.subheader("⚙️ Configuración")
        if st.button("🔄 Reiniciar Todos los Datos"):
            st.session_state.servicios_realizados = pd.DataFrame(
                columns=["Fecha", "Cliente", "Teléfono", "Barbero", "Servicio", "Precio ($)"]
            )
            st.session_state.citas = pd.DataFrame(
                columns=["Fecha y Hora", "Cliente", "Teléfono", "Barbero", "Servicio", "Precio Estimado ($)", "Estado"]
            )
            st.session_state.gastos_barberia = pd.DataFrame(
                columns=["Fecha", "Barbero / Asignación", "Descripción", "Monto ($)"]
            )
            st.session_state.fiados = pd.DataFrame(
                columns=["Cliente", "Teléfono", "Deuda Pendiente ($)", "Estado"]
            )
            st.success("¡Historial y datos reiniciados con éxito!")
            st.rerun()

# --- SISTEMA PRINCIPAL (ADMINISTRACIÓN) ---
st.title("💈 BARBERÍA GODS TIME")
st.markdown(
    "<p style='color: #D4AF37 !important; font-size: 1.1em;'><i>Excelencia, estilo y precisión en cada detalle.</i></p>",
    unsafe_allow_html=True,
)
st.markdown("---")

opcion_index = opciones_menu.index(opcion_menu)
svg_wsp = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16" style="vertical-align: middle; margin-right: 6px;"><path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.601 2.326zm-5.607 12.1a6.56 6.56 0 0 1-3.355-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.644-.182-.065-.315-.099-.445.099-.13.197-.506.644-.62.778-.114.133-.228.148-.425.05-.197-.1-.83-.306-1.583-.976-.585-.522-.982-1.166-1.096-1.363-.114-.197-.012-.304.087-.403.089-.088.197-.228.295-.342.1-.114.133-.197.198-.327.065-.13.032-.248-.016-.347-.049-.099-.445-1.072-.61-1.47-.16-.389-.323-.335-.445-.342l-.38-.008c-.13 0-.342.049-.522.248-.18.198-.695.678-.695 1.654 0 .976.712 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.837.327 1.124.418.475.152.908.13 1.25.079.382-.057 1.17-.478 1.335-.94.165-.463.165-.86.115-.94-.05-.079-.182-.13-.38-.228z"/></svg>'

# 0. CAJA Y RESUMEN GENERAL
if opcion_index == 0:
    st.header("Caja del Día y Resumen Financiero")

    df_servicios = st.session_state.servicios_realizados
    df_gastos = st.session_state.gastos_barberia

    total_ingresos = (
        df_servicios["Precio ($)"].sum() if not df_servicios.empty else 0.0
    )
    total_gastos = (
        df_gastos["Monto ($)"].sum() if not df_gastos.empty else 0.0
    )
    balance_neto = total_ingresos - total_gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos por Servicios", f"${total_ingresos:,.2f}")
    col2.metric("Gastos Operativos Totales", f"${total_gastos:,.2f}")
    col3.metric("Balance Neto en Caja", f"${balance_neto:,.2f}")

    st.markdown("---")
    st.subheader("Historial de Servicios del Día")
    if not df_servicios.empty:
        st.dataframe(df_servicios, use_container_width=True)
    else:
        st.info("Aún no se han registrado servicios hoy (Historial en cero).")

# 1. REGISTRAR SERVICIO
elif opcion_index == 1:
    st.header("Registrar Nuevo Corte o Servicio")

    cliente_corte = st.text_input("Nombre del Cliente")
    telefono_corte = st.text_input("Número de Teléfono (ej. +584121234567)")
    barbero_asigna = st.selectbox("Barbero que atendió", lista_barberos)
    
    tipo_servicio = st.selectbox("Servicio Realizado", servicios_lista, key="select_servicio_reg")
    
    precio_sugerido = SERVICIOS_PRECIOS.get(tipo_servicio, 0.0)
    
    with st.form("form_servicio"):
        precio_servicio = st.number_input(
            "Precio Cobrado ($) (Se actualiza automáticamente al cambiar el servicio)",
            min_value=0.0,
            step=1.0,
            value=precio_sugerido,
        )

        submit_servicio = st.form_submit_button("✂️ Registrar Servicio")

        if submit_servicio and cliente_corte:
            nuevo_registro = pd.DataFrame(
                {
                    "Fecha": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")],
                    "Cliente": [cliente_corte],
                    "Teléfono": [
                        telefono_corte if telefono_corte else "N/A"
                    ],
                    "Barbero": [barbero_asigna],
                    "Servicio": [tipo_servicio],
                    "Precio ($)": [precio_servicio],
                }
            )
            st.session_state.servicios_realizados = pd.concat(
                [st.session_state.servicios_realizados, nuevo_registro],
                ignore_index=True,
            )
            st.success("¡Servicio registrado con éxito!")
            st.rerun()

# 2. HISTORIAL FRANCISCO
elif opcion_index == 2:
    st.header("✂️ Historial y Trabajo - Barbero Francisco")
    st.write("Consulta el detalle exacto de cada servicio, producción y estadísticas del Barbero Francisco.")

    df_serv = st.session_state.servicios_realizados
    barbero_seleccionado = "Barbero Francisco"
    df_barbero = df_serv[df_serv["Barbero"] == barbero_seleccionado] if not df_serv.empty else pd.DataFrame()

    st.markdown("---")

    if not df_barbero.empty:
        total_barbero = df_barbero["Precio ($)"].sum()
        cantidad_cortes = len(df_barbero)

        col_b1, col_b2 = st.columns(2)
        col_b1.metric("Total Generado (Francisco)", f"${total_barbero:,.2f}")
        col_b2.metric("Servicios Realizados", f"{cantidad_cortes} servicios")

        st.write("")
        st.subheader("📋 Historial de Servicios")
        st.dataframe(
            df_barbero[["Fecha", "Cliente", "Teléfono", "Servicio", "Precio ($)"]],
            use_container_width=True,
        )

        st.markdown("---")
        st.subheader("📊 Tipos de Servicios Realizados")
        conteo_serv_barb = df_barbero["Servicio"].value_counts().reset_index()
        conteo_serv_barb.columns = ["Servicio", "Cantidad"]
        st.bar_chart(conteo_serv_barb.set_index("Servicio"))
    else:
        st.info("El barbero **Barbero Francisco** aún no tiene servicios registrados.")

# 3. HISTORIAL JONDER
elif opcion_index == 3:
    st.header("✂️ Historial y Trabajo - Barbero Jonder")
    st.write("Consulta el detalle exacto de cada servicio, producción y estadísticas del Barbero Jonder.")

    df_serv = st.session_state.servicios_realizados
    barbero_seleccionado = "Barbero Jonder"
    df_barbero = df_serv[df_serv["Barbero"] == barbero_seleccionado] if not df_serv.empty else pd.DataFrame()

    st.markdown("---")

    if not df_barbero.empty:
        total_barbero = df_barbero["Precio ($)"].sum()
        cantidad_cortes = len(df_barbero)

        col_b1, col_b2 = st.columns(2)
        col_b1.metric("Total Generado (Jonder)", f"${total_barbero:,.2f}")
        col_b2.metric("Servicios Realizados", f"{cantidad_cortes} servicios")

        st.write("")
        st.subheader("📋 Historial de Servicios")
        st.dataframe(
            df_barbero[["Fecha", "Cliente", "Teléfono", "Servicio", "Precio ($)"]],
            use_container_width=True,
        )

        st.markdown("---")
        st.subheader("📊 Tipos de Servicios Realizados")
        conteo_serv_barb = df_barbero["Servicio"].value_counts().reset_index()
        conteo_serv_barb.columns = ["Servicio", "Cantidad"]
        st.bar_chart(conteo_serv_barb.set_index("Servicio"))
    else:
        st.info("El barbero **Barbero Jonder** aún no tiene servicios registrados.")

# 4. AGENDAR CITAS (ADMIN)
elif opcion_index == 4:
    st.header("Agendamiento de Citas y Recordatorios")

    cli_cita = st.text_input("Nombre del Cliente", key="cli_cita_input")
    tel_cita = st.text_input(
        "Número de Teléfono (ej. +584121234567)", key="tel_cita_input"
    )
    barbero_cita = st.selectbox(
        "Barbero que atendió", lista_barberos, key="barb_cita_sel"
    )
    
    serv_cita = st.selectbox(
        "Servicio Realizado", servicios_lista, key="serv_cita_sel"
    )

    precio_sug_admin = SERVICIOS_PRECIOS.get(serv_cita, 0.0)

    with st.form("form_cita"):
        precio_cita_val = st.number_input(
            "Precio Estimado ($) (Automático según el servicio)",
            min_value=0.0,
            step=1.0,
            value=precio_sug_admin,
        )

        col_f, col_h = st.columns(2)
        with col_f:
            fecha_cita = st.date_input("Fecha de la Cita")
        with col_h:
            hora_cita = st.time_input("Hora de la Cita")

        submit_cita = st.form_submit_button("📅 Agendar Cita")

        if submit_cita and cli_cita:
            fecha_hora_str = f"{fecha_cita} {hora_cita.strftime('%H:%M')}"
            nueva_cita = pd.DataFrame(
                {
                    "Fecha y Hora": [fecha_hora_str],
                    "Cliente": [cli_cita],
                    "Teléfono": [tel_cita if tel_cita else "N/A"],
                    "Barbero": [barbero_cita],
                    "Servicio": [serv_cita],
                    "Precio Estimado ($)": [precio_cita_val],
                    "Estado": ["Pendiente"],
                }
            )
            st.session_state.citas = pd.concat(
                [st.session_state.citas, nueva_cita], ignore_index=True
            )
            st.success("¡Cita agendada con éxito!")
            st.rerun()

    st.markdown("---")
    st.subheader("Agenda de Citas Programadas")

    if not st.session_state.citas.empty:
        for idx, row in st.session_state.citas.iterrows():
            with st.expander(
                f"📅 {row['Fecha y Hora']} - {row['Cliente']} ({row['Barbero']}) - [{row.get('Estado', 'Pendiente')}]"
            ):
                st.write(f"**Servicio:** {row['Servicio']}")
                st.write(
                    f"**Precio Estimado:** ${row.get('Precio Estimado ($)', 0.0):,.2f}"
                )
                st.write(f"**Número de Teléfono:** {row['Teléfono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["Teléfono"])))
                if tel_clean:
                    msg = urllib.parse.quote(
                        f"Hola {row['Cliente']}, te recordamos tu cita en Barbería Gods Time para el {row['Fecha y Hora']}."
                    )
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer; display:flex; align-items:center;">{svg_wsp} Notificar Cita por WhatsApp</button></a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("Sin número válido registrado.")

                if st.button(
                    f"Completar / Eliminar Cita de {row['Cliente']}",
                    key=f"del_cita_{idx}",
                ):
                    st.session_state.citas = st.session_state.citas.drop(
                        idx
                    ).reset_index(drop=True)
                    st.success("¡Cita removida!")
                    st.rerun()
    else:
        st.info("No hay citas programadas actualmente.")

# 5. RECORDATORIO DE CORTES
elif opcion_index == 5:
    st.header("⏰ Recordatorio de Mantenimiento / Próximo Corte")
    st.write(
        "Notifica a tus clientes habituales cuando ya ha transcurrido cierto tiempo desde su último corte."
    )

    dias_limite = st.slider(
        "Días promedio para volver a cortar",
        min_value=7,
        max_value=60,
        value=21,
    )

    df_serv = st.session_state.servicios_realizados

    if not df_serv.empty:
        df_serv["Fecha_dt"] = pd.to_datetime(df_serv["Fecha"])
        hoy = pd.Timestamp.now()

        ultimos_cortes = df_serv.groupby("Cliente").last().reset_index()
        ultimos_cortes["Dias_transcurridos"] = (
            hoy - ultimos_cortes["Fecha_dt"]
        ).dt.days

        clientes_para_recordar = ultimos_cortes[
            ultimos_cortes["Dias_transcurridos"] >= dias_limite
        ]

        if not clientes_para_recordar.empty:
            st.subheader(
                f"Se encontraron {len(clientes_para_recordar)} clientes listos para un nuevo corte:"
            )
            for _, row in clientes_para_recordar.iterrows():
                with st.expander(
                    f"👤 {row['Cliente']} (Hace {row['Dias_transcurridos']} días)"
                ):
                    st.write(
                        f"**Servicio anterior:** {row['Servicio']} - {row['Fecha']}"
                    )
                    st.write(f"**Número de Teléfono:** {row['Teléfono']}")

                    tel_clean = "".join(
                        filter(str.isdigit, str(row["Teléfono"]))
                    )
                    if tel_clean:
                        msg = urllib.parse.quote(
                            f"Hola {row['Cliente']}! Saludos de Barbería Gods Time. Ya pasaron {row['Dias_transcurridos']} días desde tu último corte. ¿Te agendamos un espacio esta semana?"
                        )
                        wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                        st.markdown(
                            f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer; display:flex; align-items:center;">{svg_wsp} Enviar Recordatorio por WhatsApp</button></a>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.caption("Sin número válido registrado.")
        else:
            st.info(
                "No hay clientes que hayan superado el límite de días seleccionado."
            )
    else:
        st.info("Registra servicios primero para calcular los recordatorios.")

# 6. BARBEROS Y COMISIONES
elif opcion_index == 6:
    st.header("👥 Control de Comisiones y Balance por Barbero")
    st.write(
        "Calcula el porcentaje de comisión, resta los gastos asignados a cada barbero y obtiene la ganancia neta."
    )

    comision_pct = (
        st.slider(
            "Porcentaje de comisión para el barbero (%)",
            min_value=0,
            max_value=100,
            value=50,
        )
        / 100.0
    )

    df_serv = st.session_state.servicios_realizados
    df_gastos = st.session_state.gastos_barberia

    if not df_serv.empty:
        resumen_barberos = []
        for barbero in lista_barberos:
            serv_b = df_serv[df_serv["Barbero"] == barbero]
            total_gen = serv_b["Precio ($)"].sum() if not serv_b.empty else 0.0
            comision_bruta = total_gen * comision_pct

            gastos_b = (
                df_gastos[df_gastos["Barbero / Asignación"] == barbero][
                    "Monto ($)"
                ].sum()
                if not df_gastos.empty
                else 0.0
            )

            pago_neto = comision_bruta - gastos_b
            monto_local = total_gen - comision_bruta

            resumen_barberos.append(
                {
                    "Barbero": barbero,
                    "Total Generado ($)": total_gen,
                    "Comisión Bruta ($)": comision_bruta,
                    "Gastos Personales ($)": gastos_b,
                    "Pago Neto Barbero ($)": pago_neto,
                    "Para el Local ($)": monto_local,
                }
            )

        df_resumen = pd.DataFrame(resumen_barberos)
        st.dataframe(df_resumen, use_container_width=True)
    else:
        st.info(
            "Registra servicios en la opción correspondiente para visualizar el desglose de comisiones."
        )

# 7. GASTOS DEL LOCAL
elif opcion_index == 7:
    st.header("📤 Gastos de la Barbería y Barberos")
    st.write(
        "Registra compras de insumos, adelantos o gastos operacionales asignados a cada barbero o al local."
    )

    opciones_asignacion = ["General / Local"] + lista_barberos

    with st.form("form_gastos"):
        quien_gasto = st.selectbox(
            "¿A quién corresponde este gasto?", opciones_asignacion
        )
        desc_gasto = st.text_input(
            "Descripción del gasto (ej. Cuchillas, gel, adelanto, etc.)"
        )
        monto_gasto = st.number_input(
            "Monto ($)", min_value=0.0, step=0.5
        )

        submit_gasto = st.form_submit_button("Guardar Gasto")

        if submit_gasto and desc_gasto:
            nuevo_gasto = pd.DataFrame(
                {
                    "Fecha": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")],
                    "Barbero / Asignación": [quien_gasto],
                    "Descripción": [desc_gasto],
                    "Monto ($)": [monto_gasto],
                }
            )
            st.session_state.gastos_barberia = pd.concat(
                [st.session_state.gastos_barberia, nuevo_gasto],
                ignore_index=True,
            )
            st.success("Gasto registrado con éxito.")
            st.rerun()

    st.markdown("---")
    st.subheader("Historial General de Gastos")
    if not st.session_state.gastos_barberia.empty:
        st.dataframe(st.session_state.gastos_barberia, use_container_width=True)
    else:
        st.info("Aún no se han registrado gastos hoy.")

# 8. COBRAR FIADOS
elif opcion_index == 8:
    st.header("📝 Cuentas Pendientes y Cobro (Fiados)")

    with st.form("form_fiados"):
        cli_fiado = st.text_input("Nombre del Cliente")
        tel_fiado = st.text_input("Número de Teléfono (ej. +584121234567)")
        monto_fiado = st.number_input(
            "Saldo Pendiente ($)", min_value=0.0, step=1.0
        )

        submit_fiado = st.form_submit_button("Registrar Deuda")

        if submit_fiado and cli_fiado:
            nueva_deuda = pd.DataFrame(
                {
                    "Cliente": [cli_fiado],
                    "Teléfono": [tel_fiado if tel_fiado else "N/A"],
                    "Deuda Pendiente ($)": [monto_fiado],
                    "Estado": ["Pendiente"],
                }
            )
            st.session_state.fiados = pd.concat(
                [st.session_state.fiados, nueva_deuda], ignore_index=True
            )
            st.success("Deuda registrada correctamente.")
            st.rerun()

    st.markdown("---")
    st.subheader("Cuentas Pendientes")

    if not st.session_state.fiados.empty:
        for idx, row in st.session_state.fiados.iterrows():
            with st.expander(
                f"📌 {row['Cliente']} - ${row['Deuda Pendiente ($)']:,.2f}"
            ):
                st.write(f"**Número de Teléfono:** {row['Teléfono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["Teléfono"])))
                if tel_clean:
                    msg = urllib.parse.quote(
                        f"Hola {row['Cliente']}, te recordamos que tienes un saldo pendiente de ${row['Deuda Pendiente ($)']:,.2f} en Barbería Gods Time."
                    )
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer; display:flex; align-items:center;">{svg_wsp} Cobrar por WhatsApp</button></a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("Sin número válido registrado.")

                st.write("")
                if st.button(
                    f"Marcar como Pagado ({row['Cliente']})",
                    key=f"pay_debt_{idx}",
                ):
                    st.session_state.fiados = st.session_state.fiados.drop(
                        idx
                    ).reset_index(drop=True)
                    st.success("¡Deuda saldada!")
                    st.rerun()
    else:
        st.info("No hay cuentas pendientes.")