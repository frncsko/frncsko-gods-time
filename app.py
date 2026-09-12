import base64
import os
import urllib.parse
import pandas as pd
import streamlit as st

# 1. Configuración inicial de la página (Diseño compacto tipo app)
st.set_page_config(
    page_title="Barbería Gods Time", page_icon="🪒", layout="centered"
)

# 2. Cargar imagen de fondo local con manejo de errores
bg_css = ""
try:
    with open("GTBARBER.jpg", "rb") as f:
        bytes_imagen = f.read()
        imagen_base64 = base64.b64encode(bytes_imagen).decode()
        bg_css = f"""
        .stApp {{
            background-image: linear-gradient(rgba(14, 14, 16, 0.90), rgba(14, 14, 16, 0.90)), 
                        url("data:image/png;base64,{imagen_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
            background-attachment: fixed;
        }}
        """
except FileNotFoundError:
    bg_css = """
    .stApp {
        background-color: #0E0E10;
    }
    """

# 3. Estilo CSS personalizado (Incluyendo barra de navegación inferior tipo App)
st.markdown(
    f"""
    <style>
    {bg_css}
    .stApp {{ color: #E0E0E0; }}
    
    @keyframes shine {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    @keyframes girar {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    .icono-giratorio {{
        display: inline-block;
        animation: girar 4s linear infinite;
    }}

    .titulo-brillante {{
        font-size: 2.2rem;
        font-weight: 900;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        text-transform: uppercase;
        background: linear-gradient(90deg, #D4AF37 0%, #FFF8DC 35%, #D4AF37 70%, #996515 100%);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }}

    h2, h3 {{
        color: #D4AF37 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
    }}
    h4, h5, h6, p, label, span {{ color: #E0E0E0 !important; }}
    
    div[data-testid="stMetric"] {{
        background-color: #1A1A1E;
        border: 1px solid #D4AF37;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(212, 175, 55, 0.15);
    }}
    div[data-testid="stMetricLabel"] p {{ color: #C0C0C0 !important; }}
    div[data-testid="stMetricValue"] div {{ color: #F3E5AB !important; }}
    
    .stButton > button {{
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: #F3E5AB !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }}
    
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: #1A1A1E !important;
        border: 1px solid #444444 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
    }}
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {{
        border-color: #D4AF37 !important;
    }}
    input {{ color: #FFFFFF !important; }}
    
    div[data-testid="stExpander"] {{
        background-color: #161619 !important;
        border: 1px solid #333333 !important;
        border-radius: 10px;
    }}
    div[data-testid="stExpander"]:hover {{ border-color: #D4AF37 !important; }}
    div[data-testid="stExpander"] summary span {{
        color: #D4AF37 !important;
        font-weight: bold;
    }}
    
    hr {{
        border-color: #D4AF37 !important;
        opacity: 0.3;
    }}

    /* Estilo barra inferior tipo App móvil */
    .nav-bar-container {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #121215;
        border-top: 1px solid #2A2A30;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 99999;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuración de WhatsApp y Constantes
NUMERO_WHATSAPP_ADMIN = "584125205165"

USUARIOS_VALIDOS = {
    "admin": "admin",
    "francisco": "barbero1",
    "jonder": "barbero2",
}

lista_barberos = ["Barbero Francisco", "Barbero Jonder"]
servicios_lista = [
    "CORTE",
    "BARBA",
    "CORTE / BARBA",
    "Corte + Cejas",
    "Corte + Barba + Cejas (VIP)",
   
]


# --- FUNCIONES DE PERSISTENCIA (CSV) ---
CSV_SERVICIOS = "servicios.csv"
CSV_CITAS = "citas.csv"
CSV_GASTOS = "gastos.csv"
CSV_FIADOS = "fiados.csv"


def cargar_datos():
    if os.path.exists(CSV_SERVICIOS):
        servicios = pd.read_csv(CSV_SERVICIOS)
    else:
        servicios = pd.DataFrame(
            columns=[
                "Fecha",
                "Cliente",
                "Teléfono",
                "Barbero",
                "Servicio",
                "Precio ($)",
            ]
        )

    if os.path.exists(CSV_CITAS):
        citas = pd.read_csv(CSV_CITAS)
    else:
        citas = pd.DataFrame(
            columns=[
                "Fecha y Hora",
                "Cliente",
                "Teléfono",
                "Barbero",
                "Servicio",
                "Estado",
            ]
        )

    if os.path.exists(CSV_GASTOS):
        gastos = pd.read_csv(CSV_GASTOS)
    else:
        gastos = pd.DataFrame(
            columns=["Fecha", "Barbero / Asignación", "Descripción", "Monto ($)"]
        )

    if os.path.exists(CSV_FIADOS):
        fiados = pd.read_csv(CSV_FIADOS)
    else:
        fiados = pd.DataFrame(
            columns=["Cliente", "Teléfono", "Deuda Pendiente ($)", "Estado"]
        )

    return servicios, citas, gastos, fiados


def guardar_csv(df, tipo):
    if tipo == "servicios":
        df.to_csv(CSV_SERVICIOS, index=False)
    elif tipo == "citas":
        df.to_csv(CSV_CITAS, index=False)
    elif tipo == "gastos":
        df.to_csv(CSV_GASTOS, index=False)
    elif tipo == "fiados":
        df.to_csv(CSV_FIADOS, index=False)


# --- INICIALIZACIÓN DE ESTADOS ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "ver_agendar_publico" not in st.session_state:
    st.session_state.ver_agendar_publico = False
if "usuario_recordado" not in st.session_state:
    st.session_state.usuario_recordado = ""
if "password_recordado" not in st.session_state:
    st.session_state.password_recordado = ""
if "menu_actual" not in st.session_state:
    st.session_state.menu_actual = "🏠 Inicio"

# Cargar DataFrames desde archivos CSV
(
    st.session_state.servicios_realizados,
    st.session_state.citas,
    st.session_state.gastos_barberia,
    st.session_state.fiados,
) = cargar_datos()


def armar_telefono_wsp(codigo_pais, numero_local):
    num_limpio = "".join(filter(str.isdigit, str(numero_local)))
    if not num_limpio:
        return ""
    codigo_limpio = "".join(filter(str.isdigit, str(codigo_pais)))
    if num_limpio.startswith(codigo_limpio):
        return num_limpio
    return f"{codigo_limpio}{num_limpio}"


# --- PANTALLA PÚBLICA / INICIO DE SESIÓN ---
if not st.session_state.autenticado:
    st.markdown(
        '<h1 class="titulo-brillante"><span class="icono-giratorio">💈</span> BARBERÍA GODS TIME <span class="icono-giratorio">💈</span></h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #D4AF37 !important; font-size: 1.1em; text-align: center;'><i>Excelencia, estilo y precisión en cada detalle.</i></p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if st.session_state.ver_agendar_publico:
        st.subheader("📅 Agendar Cita de Barbería")
        st.write(
            "Llena el formulario para reservar tu turno. Se enviará la confirmación directamente por WhatsApp."
        )

        with st.form("form_cita_publica"):
            cli_pub = st.text_input("Tu Nombre Completo")

            c1_t, c2_t = st.columns([1, 2])
            with c1_t:
                cod_pub = st.selectbox(
                    "País", ["+58 (VE)", "+57 (CO)", "+1 (US)", "+34 (ES)"]
                )
            with c2_t:
                tel_pub_local = st.text_input("Tu Número (ej. 4121234567)")

            barbero_pub = st.selectbox("Selecciona Barbero", lista_barberos)
            serv_pub = st.selectbox("Servicio Deseado", servicios_lista)

            col_f_p, col_h_p = st.columns(2)
            with col_f_p:
                fecha_pub = st.date_input("Fecha preferida")
            with col_h_p:
                hora_pub = st.time_input("Hora preferida")

            submit_pub = st.form_submit_button(
                "📩 Reservar Turno y Notificar por WhatsApp"
            )

            if submit_pub and cli_pub and tel_pub_local:
                tel_completo = armar_telefono_wsp(cod_pub, tel_pub_local)
                fecha_hora_str = f"{fecha_pub} {hora_pub.strftime('%H:%M')}"

                nueva_cita = pd.DataFrame(
                    {
                        "Fecha y Hora": [fecha_hora_str],
                        "Cliente": [cli_pub],
                        "Teléfono": [tel_completo],
                        "Barbero": [barbero_pub],
                        "Servicio": [serv_pub],
                        "Estado": ["Pendiente (Online)"],
                    }
                )
                st.session_state.citas = pd.concat(
                    [st.session_state.citas, nueva_cita], ignore_index=True
                )
                guardar_csv(st.session_state.citas, "citas")

                mensaje_texto = (
                    f"Estimado/a *Barbería Gods Time*,\n\n"
                    f"Les escribo para confirmar una nueva cita agendada en línea.\n\n"
                    f"👤 *Cliente:* {cli_pub}\n"
                    f"📱 *Teléfono:* +{tel_completo}\n"
                    f"✂️ *Barbero:* {barbero_pub}\n"
                    f"💈 *Servicio:* {serv_pub}\n"
                    f"📅 *Fecha y Hora:* {fecha_hora_str}\n\n"
                    f"Agradezco su atención."
                )
                mensaje_wsp = urllib.parse.quote(mensaje_texto)
                wsp_link = (
                    f"https://wa.me/{NUMERO_WHATSAPP_ADMIN}?text={mensaje_wsp}"
                )

                st.success("¡Cita registrada con éxito en el sistema!")
                st.markdown(
                    f'<a href="{wsp_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:8px; font-weight:bold; width:100%; cursor:pointer; font-size:1.1em;">💬 Haz Clic Aquí para Notificar por WhatsApp</button></a>',
                    unsafe_allow_html=True,
                )

        st.write("")
        if st.button("⬅️ REGRESAR AL INICIO"):
            st.session_state.ver_agendar_publico = False
            st.rerun()

    else:
        st.subheader("🔑 Acceso")
        with st.form("form_login"):
            usuario_input = (
                st.text_input(
                    "Usuario", value=st.session_state.usuario_recordado
                )
                .strip()
                .lower()
            )
            password_input = st.text_input(
                "Contraseña",
                type="password",
                value=st.session_state.password_recordado,
            )
            recordar_credenciales = st.checkbox(
                "Recordar usuario/contraseña",
                value=bool(st.session_state.usuario_recordado),
            )
            btn_login = st.form_submit_button("Entrar al Sistema")

            if btn_login:
                if (
                    usuario_input in USUARIOS_VALIDOS
                    and USUARIOS_VALIDOS[usuario_input] == password_input
                ):
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = (
                        usuario_input.capitalize()
                    )
                    if recordar_credenciales:
                        st.session_state.usuario_recordado = usuario_input
                        st.session_state.password_recordado = password_input
                    else:
                        st.session_state.usuario_recordado = ""
                        st.session_state.password_recordado = ""

                    st.success(
                        f"¡Bienvenido, {st.session_state.usuario_actual}!"
                    )
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")

        st.markdown("---")
        st.write("¿Eres cliente y quieres reservar un turno?")
        if st.button("📅 Agendar Cita Aquí (Público)"):
            st.session_state.ver_agendar_publico = True
            st.rerun()

    st.stop()


# --- PANEL DE CONTROL PRINCIPAL (ESTILO TARJETAS / APP MÓVIL) ---
st.markdown(
    '<h1 class="titulo-brillante"><span class="icono-giratorio">💈</span> BARBERÍA GODS TIME <span class="icono-giratorio">💈</span></h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #D4AF37 !important; font-size: 1.0em; text-align: center;'><i>Excelencia, estilo y precisión en cada detalle.</i></p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Barra superior de perfil y cierre de sesión compacto
col_user_info, col_logout = st.columns([3, 1])
with col_user_info:
    st.markdown(f"👤 **Conectado como:** `{st.session_state.usuario_actual}`")
with col_logout:
    if st.button("🚪 LOG OUT"):
        st.session_state.autenticado = False
        st.session_state.usuario_actual = ""
        st.session_state.ver_agendar_publico = False
        st.rerun()

st.markdown("")

# --- NUEVO MENÚ EN TARJETAS TIPO APP ---
st.subheader("📌 Menú de Control Rápido")

# Fila 1 de botones de acceso rápido
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button(
        "📊\nBalance",
        use_container_width=True,
        help="Caja y Resumen Financiero",
    ):
        st.session_state.menu_actual = "📊 Caja y Resumen"
with c2:
    if st.button(
        "✂️\nServicio", use_container_width=True, help="Registrar Nuevo Corte"
    ):
        st.session_state.menu_actual = "✂️ Registrar Servicio"
with c3:
    if st.button(
        "📅\nCitas", use_container_width=True, help="Agendar y Ver Citas"
    ):
        st.session_state.menu_actual = "📅 Agendar Citas"
with c4:
    if st.button(
        "⏰\nAlertas", use_container_width=True, help="Recordatorios de Cortes"
    ):
        st.session_state.menu_actual = "⏰ Recordatorio de Cortes"

# Fila 2 de botones de acceso rápido
c5, c6, c7, c8 = st.columns(4)
with c5:
    if st.button(
        "👥\nComisiones",
        use_container_width=True,
        help="Control de Barberos",
    ):
        st.session_state.menu_actual = "👥 Barberos y Comisión"
with c6:
    if st.button(
        "📤\nGastos", use_container_width=True, help="Gastos de la Barbería"
    ):
        st.session_state.menu_actual = "📤 Gastos del Local"
with c7:
    if st.button(
        "📝\nFiados", use_container_width=True, help="Cuentas Pendientes"
    ):
        st.session_state.menu_actual = "📝 Cobrar Fiados"
with c8:
    if st.button(
        "📥\nRespaldos", use_container_width=True, help="Exportar e Importar CSV"
    ):
        st.session_state.menu_actual = "📥 Respaldar / Exportar Datos"

st.markdown(
    f"<p style='text-align:center; color:#D4AF37; font-size:0.9em;'>Sección activa: <b>{st.session_state.menu_actual}</b></p>",
    unsafe_allow_html=True,
)
st.markdown("---")

opcion_menu = st.session_state.menu_actual

# --- CONTENIDO DE LAS SECCIONES ---

# 1. CAJA Y RESUMEN
if opcion_menu == "📊 Caja y Resumen":
    st.header("REGISTRO DIARIO")

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
    col1.metric("Ingresos", f"${total_ingresos:,.2f}")
    col2.metric("Gastos", f"${total_gastos:,.2f}")
    col3.metric("Neto Caja", f"${balance_neto:,.2f}")

    st.markdown("---")
    st.subheader("Historial de Servicios del Día")
    if not df_servicios.empty:
        st.dataframe(df_servicios, use_container_width=True)
    else:
        st.info("Aún no se han registrado servicios hoy.")

# 2. REGISTRAR SERVICIO
elif opcion_menu == "✂️ Registrar Servicio":
    st.header("Registrar Nuevo Corte o Servicio")

    with st.form("form_servicio"):
        cliente_corte = st.text_input("Nombre del Cliente")

        c1_s, c2_s = st.columns([1, 2])
        with c1_s:
            cod_serv = st.selectbox(
                "Código País",
                ["+58 (VE)", "+57 (CO)", "+1 (US)", "+34 (ES)"],
                key="cod_s",
            )
        with c2_s:
            telefono_corte_local = st.text_input("Número (ej. 4121234567)")

        barbero_asigna = st.selectbox("Barbero que atendió", lista_barberos)
        tipo_servicio = st.selectbox("Servicio Realizado", servicios_lista)
        precio_servicio = st.number_input(
            "Precio Cobrado ($)", min_value=0.0, step=1.0
        )

        submit_servicio = st.form_submit_button("✂️ Registrar Servicio")

        if submit_servicio and cliente_corte:
            tel_completo = (
                armar_telefono_wsp(cod_serv, telefono_corte_local)
                if telefono_corte_local
                else "N/A"
            )
            nuevo_registro = pd.DataFrame(
                {
                    "Fecha": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")],
                    "Cliente": [cliente_corte],
                    "Teléfono": [tel_completo],
                    "Barbero": [barbero_asigna],
                    "Servicio": [tipo_servicio],
                    "Precio ($)": [precio_servicio],
                }
            )
            st.session_state.servicios_realizados = pd.concat(
                [st.session_state.servicios_realizados, nuevo_registro],
                ignore_index=True,
            )
            guardar_csv(st.session_state.servicios_realizados, "servicios")
            st.success("¡Servicio registrado con éxito!")
            st.rerun()

# 3. AGENDAR CITAS (ADMIN)
elif opcion_menu == "📅 Agendar Citas":
    st.header("Agendamiento de Citas y Recordatorios")

    with st.form("form_cita"):
        cli_cita = st.text_input("Nombre del Cliente")

        c1_c, c2_c = st.columns([1, 2])
        with c1_c:
            cod_cita_sel = st.selectbox(
                "Código País",
                ["+58 (VE)", "+57 (CO)", "+1 (US)", "+34 (ES)"],
                key="cod_c",
            )
        with c2_c:
            tel_cita_local = st.text_input(
                "Número (ej. 4121234567)", key="tel_cita_input"
            )

        barbero_cita = st.selectbox(
            "Barbero que atendió", lista_barberos, key="barb_cita_sel"
        )
        serv_cita = st.selectbox(
            "Servicio Realizado", servicios_lista, key="serv_cita_sel"
        )

        col_f, col_h = st.columns(2)
        with col_f:
            fecha_cita = st.date_input("Fecha de la Cita")
        with col_h:
            hora_cita = st.time_input("Hora de la Cita")

        submit_cita = st.form_submit_button("📅 Agendar Cita")

        if submit_cita and cli_cita:
            tel_completo = (
                armar_telefono_wsp(cod_cita_sel, tel_cita_local)
                if tel_cita_local
                else "N/A"
            )
            fecha_hora_str = f"{fecha_cita} {hora_cita.strftime('%H:%M')}"
            nueva_cita = pd.DataFrame(
                {
                    "Fecha y Hora": [fecha_hora_str],
                    "Cliente": [cli_cita],
                    "Teléfono": [tel_completo],
                    "Barbero": [barbero_cita],
                    "Servicio": [serv_cita],
                    "Estado": ["Pendiente"],
                }
            )
            st.session_state.citas = pd.concat(
                [st.session_state.citas, nueva_cita], ignore_index=True
            )
            guardar_csv(st.session_state.citas, "citas")
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
                st.write(f"**Teléfono:** +{row['Teléfono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["Teléfono"])))
                if tel_clean and tel_clean != "NA":
                    msg_texto = (
                        f"Estimado/a *{row['Cliente']}*,\n\n"
                        f"Le escribimos de *Barbería God's Time* para confirmarle su cita con "
                        f"el/la barbero/a *{row['Barbero']}* programada para el día *{row['Fecha y Hora']}*.\n\n"
                        f"Servicio solicitado: *{row['Servicio']}*.\n\n"
                        f"¡Le esperamos!"
                    )
                    msg = urllib.parse.quote(msg_texto)
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:6px; font-weight:bold; cursor:pointer;">💬 Notificar por WhatsApp</button></a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("Sin número válido registrado.")

                st.write("")
                if st.button(
                    f"Completar / Eliminar Cita de {row['Cliente']}",
                    key=f"del_cita_{idx}",
                ):
                    st.session_state.citas = st.session_state.citas.drop(
                        idx
                    ).reset_index(drop=True)
                    guardar_csv(st.session_state.citas, "citas")
                    st.success("¡Cita removida!")
                    st.rerun()
    else:
        st.info("No hay citas programadas actualmente.")

# 4. RECORDATORIO DE CORTES
elif opcion_menu == "⏰ Recordatorio de Cortes":
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
                    st.write(f"**Teléfono:** +{row['Teléfono']}")

                    tel_clean = "".join(
                        filter(str.isdigit, str(row["Teléfono"]))
                    )
                    if tel_clean and tel_clean != "NA":
                        msg_texto = (
                            f"Estimado/a *{row['Cliente']}*,\n\n"
                            f"Le saludamos cordialmente de *Barbería God's Time*. Han transcurrido {row['Dias_transcurridos']} días desde su último servicio ({row['Servicio']}).\n\n"
                            f"¿Desea que le agendemos un espacio esta semana?"
                        )
                        msg = urllib.parse.quote(msg_texto)
                        wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                        st.markdown(
                            f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:6px; font-weight:bold; cursor:pointer;">💬 Enviar Recordatorio por WhatsApp</button></a>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.caption("Sin número válido registrado.")
        else:
            st.info("No hay clientes que hayan superado el límite de días.")
    else:
        st.info("Registra servicios primero para calcular los recordatorios.")

# 5. BARBEROS Y COMISIONES
elif opcion_menu == "👥 Barberos y Comisión":
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
        st.info("Registra servicios para visualizar el desglose de comisiones.")

# 6. GASTOS DEL LOCAL
elif opcion_menu == "📤 Gastos del Local":
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
            "Descripción del gasto (ej. Cuchillas, gel, etc.)"
        )
        monto_gasto = st.number_input("Monto ($)", min_value=0.0, step=0.5)

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
            guardar_csv(st.session_state.gastos_barberia, "gastos")
            st.success("Gasto registrado con éxito.")
            st.rerun()

    st.markdown("---")
    st.subheader("Historial General de Gastos")
    if not st.session_state.gastos_barberia.empty:
        st.dataframe(st.session_state.gastos_barberia, use_container_width=True)
    else:
        st.info("Aún no se han registrado gastos hoy.")

# 7. COBRAR FIADOS
elif opcion_menu == "📝 Cobrar Fiados":
    st.header("📝 Cuentas Pendientes y Cobro (Fiados)")

    with st.form("form_fiados"):
        cli_fiado = st.text_input("Nombre del Cliente")

        c1_f, c2_f = st.columns([1, 2])
        with c1_f:
            cod_fiado_sel = st.selectbox(
                "Código País",
                ["+58 (VE)", "+57 (CO)", "+1 (US)", "+34 (ES)"],
                key="cod_f",
            )
        with c2_f:
            tel_fiado_local = st.text_input("Número (ej. 4121234567)")

        monto_fiado = st.number_input(
            "Saldo Pendiente ($)", min_value=0.0, step=1.0
        )

        submit_fiado = st.form_submit_button("Registrar Deuda")

        if submit_fiado and cli_fiado:
            tel_completo = (
                armar_telefono_wsp(cod_fiado_sel, tel_fiado_local)
                if tel_fiado_local
                else "N/A"
            )
            nueva_deuda = pd.DataFrame(
                {
                    "Cliente": [cli_fiado],
                    "Teléfono": [tel_completo],
                    "Deuda Pendiente ($)": [monto_fiado],
                    "Estado": ["Pendiente"],
                }
            )
            st.session_state.fiados = pd.concat(
                [st.session_state.fiados, nueva_deuda], ignore_index=True
            )
            guardar_csv(st.session_state.fiados, "fiados")
            st.success("Deuda registrada correctamente.")
            st.rerun()

    st.markdown("---")
    st.subheader("Cuentas Pendientes")

    if not st.session_state.fiados.empty:
        for idx, row in st.session_state.fiados.iterrows():
            with st.expander(
                f"📌 {row['Cliente']} - ${row['Deuda Pendiente ($)']:,.2f}"
            ):
                st.write(f"**Teléfono:** +{row['Teléfono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["Teléfono"])))
                if tel_clean and tel_clean != "NA":
                    msg_texto = (
                        f"Estimado/a *{row['Cliente']}*,\n\n"
                        f"Le escribimos de *Barbería God's Time* para recordarle amablemente que posee un saldo pendiente por cancelar de *${row['Deuda Pendiente ($)']:,.2f}*.\n\n"
                        f"Agradecemos su pronta atención."
                    )
                    msg = urllib.parse.quote(msg_texto)
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:6px; font-weight:bold; cursor:pointer;">💬 Cobrar por WhatsApp</button></a>',
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
                    guardar_csv(st.session_state.fiados, "fiados")
                    st.success("¡Deuda saldada!")
                    st.rerun()
    else:
        st.info("No hay cuentas pendientes.")

# 8. RESPALDAR / EXPORTAR DATOS
elif opcion_menu == "📥 Respaldar / Exportar Datos":
    st.header("📥 Respaldar y Descargar Historial")
    st.write(
        "Descarga tus archivos de respaldo directamente a tu computadora."
    )

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        st.subheader("Descargar Respaldos (CSV)")
        csv_servicios_bytes = (
            st.session_state.servicios_realizados.to_csv(index=False).encode(
                "utf-8"
            )
        )
        st.download_button(
            label="📥 Descargar Servicios",
            data=csv_servicios_bytes,
            file_name="respaldo_servicios.csv",
            mime="text/csv",
        )

        csv_citas_bytes = st.session_state.citas.to_csv(index=False).encode(
            "utf-8"
        )
        st.download_button(
            label="📥 Descargar Citas",
            data=csv_citas_bytes,
            file_name="respaldo_citas.csv",
            mime="text/csv",
        )

    with col_b2:
        st.subheader("‎")
        csv_gastos_bytes = (
            st.session_state.gastos_barberia.to_csv(index=False).encode(
                "utf-8"
            )
        )
        st.download_button(
            label="📥 Descargar Gastos",
            data=csv_gastos_bytes,
            file_name="respaldo_gastos.csv",
            mime="text/csv",
        )

        csv_fiados_bytes = st.session_state.fiados.to_csv(index=False).encode(
            "utf-8"
        )
        st.download_button(
            label="📥 Descargar Fiados",
            data=csv_fiados_bytes,
            file_name="respaldo_fiados.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.subheader("🔄 Restaurar Respaldo")
    archivo_subido = st.file_uploader(
        "Selecciona un archivo CSV", type=["csv"]
    )
    tipo_destino = st.selectbox(
        "¿A qué sección pertenece este archivo?",
        ["Servicios", "Citas", "Gastos", "Fiados"],
    )

    if archivo_subido is not None:
        if st.button("📤 Cargar y Sobrescribir"):
            df_subido = pd.read_csv(archivo_subido)
            if tipo_destino == "Servicios":
                st.session_state.servicios_realizados = df_subido
                guardar_csv(df_subido, "servicios")
            elif tipo_destino == "Citas":
                st.session_state.citas = df_subido
                guardar_csv(df_subido, "citas")
            elif tipo_destino == "Gastos":
                st.session_state.gastos_barberia = df_subido
                guardar_csv(df_subido, "gastos")
            elif tipo_destino == "Fiados":
                st.session_state.fiados = df_subido
                guardar_csv(df_subido, "fiados")

            st.success(
                f"¡El respaldo de {tipo_destino} se cargó correctamente!"
            )
            st.rerun()
