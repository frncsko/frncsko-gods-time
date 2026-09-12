import base64
import urllib.parse
import pandas as pd
import streamlit as st

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Barbería Gods Time", page_icon="💈", layout="wide"
)

# 2. Estilo CSS con fondo animado de TERROR (niebla y sombras con movimiento) y título arriba
bg_css = """
@keyframes terrorFog {
    0% { background-position: 0% 50%; filter: brightness(0.4) contrast(1.3); }
    50% { background-position: 100% 50%; filter: brightness(0.25) contrast(1.5) hue-rotate(-10deg); }
    100% { background-position: 0% 50%; filter: brightness(0.4) contrast(1.3); }
}

.stApp {
    background: linear-gradient(rgba(5, 5, 5, 0.92), rgba(15, 2, 2, 0.95)), 
                url("https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    animation: terrorFog 15s ease infinite alternate;
}
"""

# 3. Estilo CSS general (Título arriba con borde negro y diseño general)
st.markdown(
    f"""
    <style>
    {bg_css}
    
    /* TÍTULO BIEN ARRIBA CON BORDE NEGRO Y LETRAS BLANCAS */
    .border-title {{
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        color: #FFFFFF;
        -webkit-text-stroke: 2px #000000;
        text-shadow: 3px 3px 0px #000000, -1px -1px 0px #000000, 1px -1px 0px #000000, -1px 1px 0px #000000, 1px 1px 0px #000000;
        letter-spacing: 2px;
        margin-top: -65px;
        margin-bottom: 0px;
        padding-top: 0px;
    }}

    .stApp {{ color: #E0E0E0; }}
    h1, h2, h3 {{
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
    }}
    h4, h5, h6, p, label, span {{ color: #E0E0E0 !important; }}
    div[data-testid="stMetric"] {{
        background-color: #1A1A1E;
        border: 1px solid #444444;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }}
    div[data-testid="stMetricLabel"] p {{ color: #C0C0C0 !important; }}
    div[data-testid="stMetricValue"] div {{ color: #FFFFFF !important; }}
    .stButton > button {{
        background-color: #333333 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border: 1px solid #555555 !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: #555555 !important;
        border-color: #888888 !important;
    }}
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: #1A1A1E !important;
        border: 1px solid #444444 !important;
        color: #FFFFFF !important;
        border-radius: 6px;
    }}
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {{
        border-color: #888888 !important;
    }}
    input {{ color: #FFFFFF !important; }}
    div[data-testid="stExpander"] {{
        background-color: #161619 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px;
    }}
    div[data-testid="stExpander"]:hover {{ border-color: #666666 !important; }}
    div[data-testid="stExpander"] summary span {{
        color: #FFFFFF !important;
        font-weight: bold;
    }}
    div[data-testid="stDataFrame"] {{
        border: 1px solid #333333;
        border-radius: 6px;
    }}
    hr {{
        border-color: #444444 !important;
        opacity: 0.5;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuración de WhatsApp del Administrador/Barbería
NUMERO_WHATSAPP_ADMIN = "584125205165"

USUARIOS_VALIDOS = {
    "admin": "godstime123",
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

# Inicialización de Estados
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "ver_agendar_publico" not in st.session_state:
    st.session_state.ver_agendar_publico = False
if "usuario_guardado" not in st.session_state:
    st.session_state.usuario_guardado = ""

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

# --- MENÚ LATERAL IZQUIERDO (LOGIN PEQUEÑO Y DIVIDIDO POR SECCIONES ESTILO TREINTA) ---
with st.sidebar:
    st.markdown("### 🦇 💈 Barbería Gods Time")

    if not st.session_state.autenticado:
        st.markdown("#### 🔑 Iniciar Sesión")
        with st.form("form_login_sidebar"):
            usuario_input = (
                st.text_input("Usuario", value=st.session_state.usuario_guardado)
                .strip()
                .lower()
            )
            password_input = st.text_input("Contraseña", type="password")
            recordar_usuario = st.checkbox(
                "Recordar", value=bool(st.session_state.usuario_guardado)
            )
            btn_login = st.form_submit_button("Ingresar")

            if btn_login:
                if (
                    usuario_input in USUARIOS_VALIDOS
                    and USUARIOS_VALIDOS[usuario_input] == password_input
                ):
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = usuario_input.capitalize()

                    if recordar_usuario:
                        st.session_state.usuario_guardado = usuario_input
                    else:
                        st.session_state.usuario_guardado = ""

                    st.rerun()
                else:
                    st.error("Datos incorrectos.")
    else:
        st.markdown(f"👤 **Hola,** {st.session_state.usuario_actual}")
        st.markdown("---")

        # MENÚ DIVIDIDO ESTILO TREINTA
        st.markdown("#### 💼 **NEGOCIO**")
        opcion_caja = st.button(
            "📊 Caja y Resumen", use_container_width=True, key="btn_caja"
        )
        opcion_servicio = st.button(
            "✂️ Registrar Venta", use_container_width=True, key="btn_serv"
        )
        opcion_gastos = st.button(
            "📤 Gastos Operativos", use_container_width=True, key="btn_gastos"
        )

        st.markdown("#### 📅 **GESTIÓN**")
        opcion_citas = st.button(
            "📅 Agenda de Citas", use_container_width=True, key="btn_citas"
        )
        opcion_recordatorios = st.button(
            "⏰ Recordatorios", use_container_width=True, key="btn_recs"
        )
        opcion_comisiones = st.button(
            "👥 Barberos / Comisiones",
            use_container_width=True,
            key="btn_comis",
        )

        st.markdown("#### 👥 **CLIENTES**")
        opcion_fiados = st.button(
            "📝 Cuentas por Cobrar", use_container_width=True, key="btn_fiados"
        )

        if "menu_actual" not in st.session_state:
            st.session_state.menu_actual = "📊 Caja y Resumen"

        if opcion_caja:
            st.session_state.menu_actual = "📊 Caja y Resumen"
        elif opcion_servicio:
            st.session_state.menu_actual = "✂️ Registrar Servicio"
        elif opcion_gastos:
            st.session_state.menu_actual = "📤 Gastos del Local"
        elif opcion_citas:
            st.session_state.menu_actual = "📅 Agendar Citas"
        elif opcion_recordatorios:
            st.session_state.menu_actual = "⏰ Recordatorio de Cortes"
        elif opcion_comisiones:
            st.session_state.menu_actual = "👥 Barberos y Comisión"
        elif opcion_fiados:
            st.session_state.menu_actual = "📝 Cobrar Fiados"

        opcion_menu = st.session_state.menu_actual

        st.markdown("---")
        if st.button(
            "🚪 Cerrar Sesión",
            use_container_width=True,
            key="btn_cerrar_sesion",
        ):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.session_state.ver_agendar_publico = False
            st.rerun()

# --- SI NO ESTÁ AUTENTICADO: TÍTULO ARRIBA Y BOTÓN DE AGENDAR GRANDE EN EL CENTRO ---
if not st.session_state.autenticado:
    st.markdown(
        '<div class="border-title">🦇 Barbería Gods Time 🦇</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #FFFFFF !important; font-size: 1.2em; margin-top: 10px;'><i>El terror del mal estilo... precisión milimétrica.</i></p>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col_centrada = st.columns([1, 2, 1])
    with col_centrada[1]:
        if not st.session_state.ver_agendar_publico:
            # BOTÓN GRANDE Y CENTRADO PARA AGENDAR
            if st.button(
                "📅 ✂️ AGENDAR CITA EN LÍNEA 💈 📱",
                use_container_width=True,
                key="btn_grande_agendar",
            ):
                st.session_state.ver_agendar_publico = True
                st.rerun()
            st.markdown(
                "<p style='text-align: center; color: #AAAAAA !important; font-size: 0.95em; margin-top: 15px;'>Inicia sesión en el panel lateral izquierdo si eres parte del equipo, o haz clic en el botón superior para reservar tu cita.</p>",
                unsafe_allow_html=True,
            )
        else:
            st.subheader("📅 Agendar Turno - Barbería Gods Time")
            with st.form("form_cita_publica_centro"):
                cli_pub = st.text_input("Tu Nombre Completo")
                tel_pub = st.text_input(
                    "Tu Número de Teléfono / WhatsApp (ej. +58412...)"
                )
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

                if submit_pub and cli_pub and tel_pub:
                    fecha_hora_str = f"{fecha_pub} {hora_pub.strftime('%H:%M')}"
                    nueva_cita = pd.DataFrame(
                        {
                            "Fecha y Hora": [fecha_hora_str],
                            "Cliente": [cli_pub],
                            "Teléfono": [tel_pub],
                            "Barbero": [barbero_pub],
                            "Servicio": [serv_pub],
                            "Estado": ["Pendiente (Online)"],
                        }
                    )
                    st.session_state.citas = pd.concat(
                        [st.session_state.citas, nueva_cita], ignore_index=True
                    )

                    # MENSAJE DE WHATSAPP CON ICONOS DE BARBERÍA Y TELÉFONO
                    mensaje_wsp = urllib.parse.quote(
                        f"🦇 *¡NUEVA CITA RESERVADA EN LÍNEA!* ✂️\n\n"
                        f"👤 *Cliente:* {cli_pub}\n"
                        f"📱 *Teléfono:* {tel_pub}\n"
                        f"💈 *Barbero:* {barbero_pub}\n"
                        f"✂️ *Servicio:* {serv_pub}\n"
                        f"📅 *Fecha y Hora:* {fecha_hora_str}\n\n"
                        f"📍 *Barbería Gods Time*"
                    )
                    wsp_link = (
                        f"https://wa.me/{NUMERO_WHATSAPP_ADMIN}?text={mensaje_wsp}"
                    )

                    st.success("¡Cita registrada con éxito!")
                    st.markdown(
                        f'<a href="{wsp_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:6px; font-weight:bold; width:100%; cursor:pointer; font-size:1.1em;">💬 Haz Clic Aquí para Notificar por WhatsApp 📱</button></a>',
                        unsafe_allow_html=True,
                    )

            st.write("")
            if st.button("⬅️ Volver", use_container_width=True):
                st.session_state.ver_agendar_publico = False
                st.rerun()

    st.stop()

# --- SISTEMA PRINCIPAL (ADMINISTRACIÓN) ---
st.markdown(
    '<div class="border-title">🦇 Barbería Gods Time 🦇</div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #FFFFFF !important; font-size: 1.1em;'><i>El terror del mal estilo... precisión milimétrica.</i></p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# 1. CAJA Y RESUMEN GENERAL
if opcion_menu == "📊 Caja y Resumen":
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
        st.info("Aún no se han registrado servicios hoy.")

# 2. REGISTRAR SERVICIO
elif opcion_menu == "✂️ Registrar Servicio":
    st.header("Registrar Nuevo Corte o Servicio")

    with st.form("form_servicio"):
        cliente_corte = st.text_input("Nombre del Cliente")
        telefono_corte = st.text_input("Número de Teléfono (+58...)")
        barbero_asigna = st.selectbox("Barbero que atendió", lista_barberos)
        tipo_servicio = st.selectbox("Servicio Realizado", servicios_lista)
        precio_servicio = st.number_input(
            "Precio Cobrado ($)", min_value=0.0, step=1.0
        )

        submit_servicio = st.form_submit_button("✂️ Registrar Venta")

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
            st.success("¡Venta registrada con éxito!")
            st.rerun()

# 3. AGENDAR CITAS (ADMIN)
elif opcion_menu == "📅 Agendar Citas":
    st.header("Agendamiento de Citas y Recordatorios")

    with st.form("form_cita"):
        cli_cita = st.text_input("Nombre del Cliente")
        tel_cita = st.text_input("Número de Teléfono (+58...)", key="tel_cita_input")
        barbero_cita = st.selectbox(
            "Barbero asignado", lista_barberos, key="barb_cita_sel"
        )
        serv_cita = st.selectbox(
            "Servicio", servicios_lista, key="serv_cita_sel"
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
                st.write(f"**Teléfono:** {row['Teléfono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["Teléfono"])))
                if tel_clean:
                    msg = urllib.parse.quote(
                        f"🦇 *Hola {row['Cliente']},* te recordamos tu cita en *Barbería Gods Time* para el 📅 {row['Fecha y Hora']} con el servicio de ✂️ {row['Servicio']}. ¡Te esperamos! 📱"
                    )
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Notificar Cita por WhatsApp 📱</button></a>',
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
                    st.write(f"**Teléfono:** {row['Teléfono']}")

                    tel_clean = "".join(
                        filter(str.isdigit, str(row["Teléfono"]))
                    )
                    if tel_clean:
                        msg = urllib.parse.quote(
                            f"🦇 *¡Hola {row['Cliente']}!* Saludos de *Barbería Gods Time*. Ya pasaron {row['Dias_transcurridos']} días desde tu último corte ✂️. ¿Te agendamos un espacio esta semana? 📱"
                        )
                        wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                        st.markdown(
                            f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Enviar Recordatorio por WhatsApp 📱</button></a>',
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
        st.info(
            "Registra servicios en la opción correspondiente para visualizar el desglose de comisiones."
        )

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

# 7. COBRAR FIADOS
elif opcion_menu == "📝 Cobrar Fiados":
    st.header("📝 Cuentas Pendientes y Cobro (Fiados)")

    with st.form("form_fiados"):
        cli_fiado = st.text_input("Nombre del Cliente")
        tel_fiado = st.text_input("Número de Teléfono (+58...)")
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
                st.write(f"**Teléfono:** {row['Teléfono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["Teléfono"])))
                if tel_clean:
                    msg = urllib.parse.quote(
                        f"🦇 *¡Hola {row['Cliente']}!* Te recordamos que tienes un saldo pendiente de *${row['Deuda Pendiente ($)']:,.2f}* en *Barbería Gods Time*. ✂️📱"
                    )
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Cobrar por WhatsApp 📱</button></a>',
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
