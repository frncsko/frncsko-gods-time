import base64
import sqlite3
import urllib.parse
import pandas as pd
import streamlit as st

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Barbería Gods Time", page_icon="💈", layout="wide"
)


# --- CONEXIÓN Y CONFIGURACIÓN DE BASE DE DATOS SQLITE ---
def inicializar_bd():
    conn = sqlite3.connect("barberia_godstime.db")
    cursor = conn.cursor()

    # Tabla de Servicios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            cliente TEXT,
            telefono TEXT,
            barbero TEXT,
            servicio TEXT,
            precio REAL
        )
    """)

    # Tabla de Citas (Local y Domicilio)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora TEXT,
            cliente TEXT,
            telefono TEXT,
            barbero TEXT,
            servicio TEXT,
            tipo TEXT,
            direccion TEXT,
            costo_domicilio REAL,
            estado TEXT
        )
    """)

    # Tabla de Gastos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            barbero_asignacion TEXT,
            descripcion TEXT,
            monto REAL
        )
    """)

    # Tabla de Fiados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fiados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            telefono TEXT,
            deuda REAL,
            estado TEXT
        )
    """)

    conn.commit()
    conn.close()


# Ejecutar la creación de tablas al iniciar
inicializar_bd()


# Funciones auxiliares para leer y escribir en SQLite
def cargar_datos(tabla):
    conn = sqlite3.connect("barberia_godstime.db")
    df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
    conn.close()
    return df


def ejecutar_sql(query, params=()):
    conn = sqlite3.connect("barberia_godstime.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


# 2. Cargar imagen de fondo local con centrado perfecto y sin recortes (contain)
bg_css = ""
try:
    with open("GTBARBER.jpg", "rb") as f:
        bytes_imagen = f.read()
        imagen_base64 = base64.b64encode(bytes_imagen).decode()
        bg_css = f"""
        .stApp {{
            background-color: #0E0E10;
            background-image: linear-gradient(rgba(14, 14, 16, 0.82), rgba(14, 14, 16, 0.82)), 
                        url("data:image/jpeg;base64,{imagen_base64}");
            background-size: contain;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        """
except FileNotFoundError:
    bg_css = """
    .stApp {
        background-color: #0E0E10;
    }
    """

# 3. Estilo CSS personalizado con giro interno (solo el contenido del icono) y texto brillante
st.markdown(
    f"""
    <style>
    {bg_css}
    .stApp {{ color: #E0E0E0; }}
    
    /* Animación de brillo para el texto */
    @keyframes shine {{
        0% {{
            background-position: -200% center;
        }}
        100% {{
            background-position: 200% center;
        }}
    }}

    /* Animación de giro para el interior del ícono */
    @keyframes spin-interno {{
        0% {{
            transform: rotate(0deg);
        }}
        100% {{
            transform: rotate(360deg);
        }}
    }}

    .titulo-contenedor {{
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        letter-spacing: 1.5px;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }}

    /* Contenedor estático del icono de la barbería */
    .icono-base {{
        display: inline-block;
        color: #D4AF37;
        text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5);
    }}

    /* Elemento interno que realiza el giro continuo */
    .icono-giratorio-interno {{
        display: inline-block;
        animation: spin-interno 3s linear infinite;
        transform-origin: center center;
    }}

    .texto-brillante {{
        background: linear-gradient(90deg, #D4AF37 0%, #FFF8DC 35%, #FFD700 50%, #FFF8DC 65%, #D4AF37 100%);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.4);
    }}

    /* Contenedor flotante para llevar el botón a la esquina superior derecha absoluta */
    .header-esquina-derecha {{
        position: absolute;
        top: 20px;
        right: 30px;
        z-index: 999;
    }}

    /* Estilo llamativo para el botón superior derecho */
    .btn-agendar-superior {{
        background: linear-gradient(135deg, #FFD700 0%, #D4AF37 50%, #AA771C 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        padding: 10px 20px !important;
        border-radius: 30px !important;
        border: 2px solid #FFF8DC !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.7) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease-in-out;
    }}
    .btn-agendar-superior:hover {{
        transform: scale(1.08);
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.95) !important;
        background: linear-gradient(135deg, #FFF8DC 0%, #FFD700 50%, #D4AF37 100%) !important;
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
        border-radius: 8px;
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
        border-radius: 6px !important;
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
        border-radius: 6px;
    }}
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {{
        border-color: #D4AF37 !important;
    }}
    input {{ color: #FFFFFF !important; }}
    div[data-testid="stExpander"] {{
        background-color: #161619 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px;
    }}
    div[data-testid="stExpander"]:hover {{ border-color: #D4AF37 !important; }}
    div[data-testid="stExpander"] summary span {{
        color: #D4AF37 !important;
        font-weight: bold;
    }}
    div[data-testid="stDataFrame"] {{
        border: 1px solid #333333;
        border-radius: 6px;
    }}
    hr {{
        border-color: #D4AF37 !important;
        opacity: 0.3;
    }}
    /* Estilos personalizados para el menú lateral con letras negras */
    .menu-header {{
        color: #000000 !important;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 15px;
        margin-bottom: 5px;
        font-weight: bold;
        background-color: #D4AF37;
        padding: 4px 8px;
        border-radius: 4px;
        text-align: center;
    }}
    .sidebar-title {{
        color: #000000 !important;
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuración de WhatsApp del Administrador/Barbería
NUMERO_WHATSAPP_ADMIN = "584125205165"

USUARIOS_VALIDOS = {
    "admin": "admin",
    "francisco": "francisco",
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

# Inicialización de Estados de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "ver_agendar_publico" not in st.session_state:
    st.session_state.ver_agendar_publico = False
if "opcion_menu" not in st.session_state:
    st.session_state.opcion_menu = "📊 Caja y Resumen"
if "usuario_recordado" not in st.session_state:
    st.session_state.usuario_recordado = ""
if "password_recordada" not in st.session_state:
    st.session_state.password_recordada = ""

# --- PANTALLA PÚBLICA / INICIO DE SESIÓN ---
if not st.session_state.autenticado:
    # Botón flotante en la esquina superior derecha extrema
    if not st.session_state.ver_agendar_publico:
        st.markdown(
            "<div class='header-esquina-derecha'>", unsafe_allow_html=True
        )
        if st.button("📅 ¡AGENDAR CITA AQUÍ! ✨", key="btn_top_agendar"):
            st.session_state.ver_agendar_publico = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<h1 class='titulo-contenedor'><span class='icono-base'><span class='icono-giratorio-interno'>💈</span></span> <span class='texto-brillante'>BARBERÍA GODS TIME</span></h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #D4AF37 !important; font-size: 1.1em;'><i>Excelencia, estilo y precisión en cada detalle.</i></p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    col_centered = st.columns([1, 2, 1])
    with col_centered[1]:
        # Formulario de Cita Pública
        cli_pub = st.text_input("Tu Nombre y Apellido")
        tel_pub = st.text_input("Tu Teléfono")
        barbero_pub = st.selectbox("Selecciona Barbero", ["Cualquiera", "Barbero 1", "Barbero 2"])
        serv_pub = st.selectbox("Servicio", ["Corte", "Barba", "Corte + Barba"])
        dir_pub = st.text_input("Dirección (Solo si es A Domicilio)")
        fecha_pub = st.date_input("Fecha de la Cita")
        hora_pub = st.time_input("Hora de la Cita")  
        fecha_hora_str = f"{fecha_pub} a las {hora_pub}"
            st.success("¡Cita registrada con éxito en el sistema!")
            st.markdown(
                f'<a href="{wsp_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:6px; font-weight:bold; width:100%; cursor:pointer; font-size:1.1em;">💬 Haz Clic Aquí para Notificar por WhatsApp</button></a>',
                unsafe_allow_html=True
            )
        
        fecha_hora_str = f"{fecha_pub} a las {hora_pub}"
        
        submitted = st.form_submit_button("Confirmar Cita")

        if submitted:
            if tipo_reserva_pub == "A Domicilio":
                texto_wsp = f"🏠 NUEVA CITA A DOMICILIO - Cliente: {cli_pub}, Tel: {tel_pub}, Barbero: {barbero_pub}, Servicio: {serv_pub}, Dir: {dir_pub}, Fecha: {fecha_hora_str}"
            else:
                texto_wsp = f"💈 NUEVA CITA EN LOCAL - Cliente: {cli_pub}, Tel: {tel_pub}, Barbero: {barbero_pub}, Servicio: {serv_pub}, Fecha: {fecha_hora_str}"

            mensaje_wsp = urllib.parse.quote(texto_wsp)
            wsp_link = f"https://wa.me/{NUMERO_WHATSAPP_ADMIN}?text={mensaje_wsp}"

            st.success("¡Cita registrada con éxito en el sistema!")
            st.markdown(
                f'<a href="{wsp_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:6px; font-weight:bold; width:100%; cursor:pointer; font-size:1.1em;">💬 Haz Clic Aquí para Notificar por WhatsApp</button></a>',
                unsafe_allow_html=True
            )
            with st.form("form_cita_publica"):
                cli_pub = st.text_input("Tu Nombre Completo")
                tel_pub = st.text_input(
                    "Tu Número de WhatsApp (ej. +584121234567)"
                )
                barbero_pub = st.selectbox("Selecciona Barbero", lista_barberos)
                serv_pub = st.selectbox("Servicio Deseado", servicios_lista)

                dir_pub = ""
                costo_dom_pub = 0.0
          
                if submit_pub and cli_pub and tel_pub:
                    if tipo_reserva_pub == "A Domicilio" and not dir_pub:
                        st.error(
                            "Por favor ingresa la dirección para el domicilio."
                        )
                    else:
                        fecha_hora_str = (
                            f"{fecha_pub} {hora_pub.strftime('%H:%M')}"
                        )
                        ejecutar_sql(
                            "INSERT INTO citas (fecha_hora, cliente, telefono, barbero, servicio, tipo, direccion, costo_domicilio, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                fecha_hora_str,
                                cli_pub,
                                tel_pub,
                                barbero_pub,
                                serv_pub,
                                tipo_reserva_pub,
                                dir_pub if dir_pub else "N/A",
                                costo_dom_pub,
                                "Pendiente (Online)",
                            ),
                        )

                        if tipo_reserva_pub == "A Domicilio":
                            mensaje_wsp = urllib.parse.quote(
                                f"🏠 *NUEVA CITA A DOMICILIO EN LÍNEA*\n\n"
                                f"👤 *Cliente:* {cli_pub}\n"
                                f"📱 *Teléfono:* {tel_pub}\n"
                                f"✂️ *Barbero:* {barbero_pub}\n"
                                f"💈 *Servicio:* {serv_pub}\n"
                                f"📍 *Dirección:* {dir_pub}\n"
                                f"💵 *Costo Traslado:* ${costo_dom_pub:,.2f}\n"
                                f"📅 *Fecha y Hora:* {fecha_hora_str}"
                            )
                        else:
                            mensaje_wsp = urllib.parse.quote(
                                f"💈 *NUEVA CITA EN LOCAL EN LÍNEA*\n\n"
                                f"👤 *Cliente:* {cli_pub}\n"
                                f"📱 *Teléfono:* {tel_pub}\n"
                                f"✂️ *Barbero:* {barbero_pub}\n"
                                f"💈 *Servicio:* {serv_pub}\n"
                                f"📅 *Fecha y Hora:* {fecha_hora_str}"
                            )

                        wsp_link = f"https://wa.me/{NUMERO_WHATSAPP_ADMIN}?text={mensaje_wsp}"

                        st.success("¡Cita registrada con éxito en el sistema!")
                        st.markdown(
                            f'<a href="{wsp_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:6px; font-weight:bold; width:100%; cursor:pointer; font-size:1.1em;">💬 Haz Clic Aquí para Notificar por WhatsApp</button></a>',
                            unsafe_allow_html=True,
                        )

            st.write("")
            if st.button("⬅️ Volver al Inicio de Sesión"):
                st.session_state.ver_agendar_publico = False
                st.rerun()

        # Inicio de Sesión
        else:
            st.subheader("🔑 Iniciar Sesión")
with st.form("form_login"):
                usuario_input = st.text_input(
                    "Usuario", value=st.session_state.usuario_recordado
                )
                password_input = st.text_input(
                    "Contraseña",
                    type="password",
                    value=st.session_state.password_recordada,
                )

                col_rec1, col_rec2 = st.columns(2)
                with col_rec1:
                    recordar_usuario = st.checkbox("Recordar usuario")
                with col_rec2:
                    recordar_password = st.checkbox("Recordar contraseña")

                btn_login = st.form_submit_button("Ingresar al Sistema")

                if btn_login:
                    usuario_limpio = usuario_input.strip().lower()
                    if (
                        usuario_limpio in USUARIOS_VALIDOS
                        and USUARIOS_VALIDOS[usuario_limpio] == password_input
                    ):
                        st.session_state.autenticado = True
                        st.session_state.usuario_actual = (
                            usuario_limpio.capitalize()
                        )

                        # Gestionar almacenamiento de usuario
                        if recordar_usuario:
                            st.session_state.usuario_recordado = usuario_input
                        else:
                            st.session_state.usuario_recordado = ""

                        # Gestionar almacenamiento de contraseña
                        if recordar_password:
                            st.session_state.password_recordada = password_input
                        else:
                            st.session_state.password_recordada = ""

                        st.success(
                            f"¡Bienvenido, {st.session_state.usuario_actual}!"
                        )
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos.")



# --- MENÚ LATERAL IZQUIERDO ---
with st.sidebar:
    st.markdown(
        f"<div style='background-color: #D4AF37; padding: 10px; border-radius: 6px; text-align: center;'><span class='sidebar-title'>👤 <b>{st.session_state.usuario_actual}</b></span></div>",
        unsafe_allow_html=True,
    )
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.usuario_actual = ""
        st.session_state.ver_agendar_publico = False
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div class='menu-header' style='background-color:transparent; color:#D4AF37 !important; font-size:1rem; text-align:left;'>📌 <b>MENÚ PRINCIPAL</b></div>",
        unsafe_allow_html=True,
    )

    # Categoría: Operaciones Diarias
    st.markdown(
        "<div class='menu-header'>Operaciones</div>", unsafe_allow_html=True
    )
    if st.button("📊 Caja y Resumen", use_container_width=True):
        st.session_state.opcion_menu = "📊 Caja y Resumen"
    if st.button("✂️ Registrar Servicio", use_container_width=True):
        st.session_state.opcion_menu = "✂️ Registrar Servicio"
    if st.button("📅 Agendar Citas", use_container_width=True):
        st.session_state.opcion_menu = "📅 Agendar Citas"
    if st.button("🏠 Citas a Domicilio", use_container_width=True):
        st.session_state.opcion_menu = "🏠 Citas a Domicilio"

    # Categoría: Clientes
    st.markdown(
        "<div class='menu-header'>Seguimiento</div>", unsafe_allow_html=True
    )
    if st.button("⏰ Recordatorio de Cortes", use_container_width=True):
        st.session_state.opcion_menu = "⏰ Recordatorio de Cortes"
    if st.button("📝 Cobrar Fiados", use_container_width=True):
        st.session_state.opcion_menu = "📝 Cobrar Fiados"

    # Categoría: Administración y Finanzas
    st.markdown(
        "<div class='menu-header'>Finanzas</div>", unsafe_allow_html=True
    )
    if st.button("👥 Barberos y Comisión", use_container_width=True):
        st.session_state.opcion_menu = "👥 Barberos y Comisión"
    if st.button("📤 Gastos del Local", use_container_width=True):
        st.session_state.opcion_menu = "📤 Gastos del Local"
    if st.button("🔍 Verificar Pagos", use_container_width=True):
        st.session_state.opcion_menu = "🔍 Verificar Pagos"

# --- SISTEMA PRINCIPAL (ADMINISTRACIÓN) ---
st.markdown(
    "<h1 class='titulo-contenedor'><span class='icono-base'><span class='icono-giratorio-interno'>💈</span></span> <span class='texto-brillante'>BARBERÍA GODS TIME</span></h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #D4AF37 !important; font-size: 1.1em;'><i>Excelencia, estilo y precisión en cada detalle.</i></p>",
    unsafe_allow_html=True,
)
st.markdown("---")

opcion_menu = st.session_state.opcion_menu

# 1. CAJA Y RESUMEN GENERAL
if opcion_menu == "📊 Caja y Resumen":
    st.header("Caja del Día y Resumen Financiero")

    df_servicios = cargar_datos("servicios")
    df_gastos = cargar_datos("gastos")

    total_ingresos = (
        df_servicios["precio"].sum() if not df_servicios.empty else 0.0
    )
    total_gastos = df_gastos["monto"].sum() if not df_gastos.empty else 0.0
    balance_neto = total_ingresos - total_gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos por Servicios", f"${total_ingresos:,.2f}")
    col2.metric("Gastos Operativos Totales", f"${total_gastos:,.2f}")
    col3.metric("Balance Neto en Caja", f"${balance_neto:,.2f}")

    st.markdown("---")
    st.subheader("Historial de Servicios Registrados")
    if not df_servicios.empty:
        df_mostrar = df_servicios[
            ["fecha", "cliente", "telefono", "barbero", "servicio", "precio"]
        ].rename(
            columns={
                "fecha": "Fecha",
                "cliente": "Cliente",
                "telefono": "Teléfono",
                "barbero": "Barbero",
                "servicio": "Servicio",
                "precio": "Precio ($)",
            }
        )
        st.dataframe(df_mostrar, use_container_width=True)
    else:
        st.info("Aún no se han registrado servicios.")

# 2. REGISTRAR SERVICIO
elif opcion_menu == "✂️ Registrar Servicio":
    st.header("Registrar Nuevo Corte o Servicio")

    with st.form("form_servicio"):
        cliente_corte = st.text_input("Nombre del Cliente")
        telefono_corte = st.text_input(
            "Número de Teléfono (ej. +584121234567)"
        )
        barbero_asigna = st.selectbox("Barbero que atendió", lista_barberos)
        tipo_servicio = st.selectbox("Servicio Realizado", servicios_lista)
        precio_servicio = st.number_input(
            "Precio Cobrado ($)", min_value=0.0, step=1.0
        )

        submit_servicio = st.form_submit_button("✂️ Registrar Servicio")

        if submit_servicio and cliente_corte:
            fecha_actual = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            ejecutar_sql(
                "INSERT INTO servicios (fecha, cliente, telefono, barbero, servicio, precio) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    fecha_actual,
                    cliente_corte,
                    telefono_corte if telefono_corte else "N/A",
                    barbero_asigna,
                    tipo_servicio,
                    precio_servicio,
                ),
            )
            st.success("¡Servicio registrado y guardado permanentemente!")
            st.rerun()

# 3. AGENDAR CITAS (ADMIN)
elif opcion_menu == "📅 Agendar Citas":
    st.header("Agendamiento de Citas en Local")

    with st.form("form_cita"):
        cli_cita = st.text_input("Nombre del Cliente")
        tel_cita = st.text_input(
            "Número de Teléfono (ej. +584121234567)", key="tel_cita_input"
        )
        barbero_cita = st.selectbox(
            "Barbero Asignado", lista_barberos, key="barb_cita_sel"
        )
        serv_cita = st.selectbox(
            "Servicio Requerido", servicios_lista, key="serv_cita_sel"
        )

        col_f, col_h = st.columns(2)
        with col_f:
            fecha_cita = st.date_input("Fecha de la Cita")
        with col_h:
            hora_cita = st.time_input("Hora de la Cita")

        submit_cita = st.form_submit_button("📅 Agendar Cita en Local")

        if submit_cita and cli_cita:
            fecha_hora_str = f"{fecha_cita} {hora_cita.strftime('%H:%M')}"
            ejecutar_sql(
                "INSERT INTO citas (fecha_hora, cliente, telefono, barbero, servicio, tipo, direccion, costo_domicilio, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    fecha_hora_str,
                    cli_cita,
                    tel_cita if tel_cita else "N/A",
                    barbero_cita,
                    serv_cita,
                    "En Local",
                    "N/A",
                    0.0,
                    "Pendiente",
                ),
            )
            st.success("¡Cita agendada correctamente!")
            st.rerun()

    st.markdown("---")
    st.subheader("Agenda de Citas Programadas")

    df_citas = cargar_datos("citas")
    if not df_citas.empty:
        for idx, row in df_citas.iterrows():
            tipo_etiqueta = row.get("tipo", "En Local")
            with st.expander(
                f"📅 [{tipo_etiqueta}] {row['fecha_hora']} - {row['cliente']} ({row['barbero']}) - [{row['estado']}]"
            ):
                st.write(f"**Servicio:** {row['servicio']}")
                st.write(f"**Número de Teléfono:** {row['telefono']}")
                if tipo_etiqueta == "A Domicilio":
                    st.write(f"**Dirección:** {row.get('direccion', 'N/A')}")
                    st.write(
                        f"**Costo Traslado:** ${row.get('costo_domicilio', 0.0):,.2f}"
                    )

                tel_clean = "".join(filter(str.isdigit, str(row["telefono"])))
                if tel_clean:
                    if tipo_etiqueta == "A Domicilio":
                        msg = urllib.parse.quote(
                            f"Hola {row['cliente']}, te recordamos tu cita a domicilio en Barbería Gods Time para el {row['fecha_hora']} en la dirección: {row.get('direccion', '')}."
                        )
                    else:
                        msg = urllib.parse.quote(
                            f"Hola {row['cliente']}, te recordamos tu cita en Barbería Gods Time para el {row['fecha_hora']}."
                        )
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Notificar Cita por WhatsApp</button></a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("Sin número válido registrado.")

                st.write("")
                if st.button(
                    f"Completar / Eliminar Cita de {row['cliente']}",
                    key=f"del_cita_{row['id']}",
                ):
                    ejecutar_sql(
                        "DELETE FROM citas WHERE id = ?", (row["id"],)
                    )
                    st.success("¡Cita removida!")
                    st.rerun()
    else:
        st.info("No hay citas programadas actualmente.")

# 4. CITAS A DOMICILIO
elif opcion_menu == "🏠 Citas a Domicilio":
    st.header("🏠 Gestión de Citas a Domicilio")
    st.write(
        "Programa servicios a domicilio especificando la dirección del cliente y el recargo por traslado."
    )

    with st.form("form_cita_domicilio"):
        cli_dom = st.text_input("Nombre del Cliente")
        tel_dom = st.text_input("Número de Teléfono (ej. +584121234567)")
        dir_dom = st.text_input(
            "Dirección Exacta (Urbanización, Calle, Casa/Edificio)"
        )
        barbero_dom = st.selectbox("Barbero Asignado", lista_barberos)
        serv_dom = st.selectbox("Servicio Requerido", servicios_lista)
        costo_dom = st.number_input(
            "Costo Extra por Traslado / Delivery ($)",
            min_value=0.0,
            step=1.0,
            value=5.0,
        )

        col_fd, col_hd = st.columns(2)
        with col_fd:
            fecha_dom = st.date_input("Fecha de la Cita a Domicilio")
        with col_hd:
            hora_dom = st.time_input("Hora de la Cita a Domicilio")

        submit_dom = st.form_submit_button("🏠 Agendar Cita a Domicilio")

        if submit_dom and cli_dom and dir_dom:
            fecha_hora_str = f"{fecha_dom} {hora_dom.strftime('%H:%M')}"
            ejecutar_sql(
                "INSERT INTO citas (fecha_hora, cliente, telefono, barbero, servicio, tipo, direccion, costo_domicilio, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    fecha_hora_str,
                    cli_dom,
                    tel_dom if tel_dom else "N/A",
                    barbero_dom,
                    serv_dom,
                    "A Domicilio",
                    dir_dom,
                    costo_dom,
                    "Pendiente",
                ),
            )
            st.success("¡Cita a domicilio registrada con éxito!")
            st.rerun()

    st.markdown("---")
    st.subheader("Listado de Citas a Domicilio Activas")

    df_citas = cargar_datos("citas")
    if not df_citas.empty and "tipo" in df_citas.columns:
        df_domicilios = df_citas[df_citas["tipo"] == "A Domicilio"]
        if not df_domicilios.empty:
            for idx, row in df_domicilios.iterrows():
                with st.expander(
                    f"🏠 {row['fecha_hora']} - {row['cliente']} (Barbero: {row['barbero']})"
                ):
                    st.write(f"**Servicio:** {row['servicio']}")
                    st.write(f"**Teléfono:** {row['telefono']}")
                    st.write(f"**Dirección:** {row['direccion']}")
                    st.write(
                        f"**Costo Traslado:** ${row['costo_domicilio']:,.2f}"
                    )

                    tel_clean = "".join(
                        filter(str.isdigit, str(row["telefono"]))
                    )
                    if tel_clean:
                        msg = urllib.parse.quote(
                            f"Hola {row['cliente']}, te recordamos tu cita a domicilio en Barbería Gods Time para el {row['fecha_hora']} en la dirección: {row['direccion']}."
                        )
                        wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                        st.markdown(
                            f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Enviar Detalles por WhatsApp</button></a>',
                            unsafe_allow_html=True,
                        )

                    st.write("")
                    if st.button(
                        f"Completar / Eliminar Domicilio de {row['cliente']}",
                        key=f"del_dom_{row['id']}",
                    ):
                        ejecutar_sql(
                            "DELETE FROM citas WHERE id = ?", (row["id"],)
                        )
                        st.success("¡Cita a domicilio removida!")
                        st.rerun()
        else:
            st.info("No hay citas a domicilio programadas.")
    else:
        st.info("No hay citas a domicilio programadas.")

# 5. RECORDATORIO DE CORTES
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

    df_serv = cargar_datos("servicios")

    if not df_serv.empty:
        df_serv["Fecha_dt"] = pd.to_datetime(df_serv["fecha"])
        hoy = pd.Timestamp.now()

        ultimos_cortes = df_serv.groupby("cliente").last().reset_index()
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
                    f"👤 {row['cliente']} (Hace {row['Dias_transcurridos']} días)"
                ):
                    st.write(
                        f"**Servicio anterior:** {row['servicio']} - {row['fecha']}"
                    )
                    st.write(f"**Número de Teléfono:** {row['telefono']}")

                    tel_clean = "".join(
                        filter(str.isdigit, str(row["telefono"]))
                    )
                    if tel_clean:
                        msg = urllib.parse.quote(
                            f"Hola {row['cliente']}! Saludos de Barbería Gods Time. Ya pasaron {row['Dias_transcurridos']} días desde tu último corte. ¿Te agendamos un espacio esta semana?"
                        )
                        wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                        st.markdown(
                            f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Enviar Recordatorio por WhatsApp</button></a>',
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

    df_serv = cargar_datos("servicios")
    df_gastos = cargar_datos("gastos")

    if not df_serv.empty:
        resumen_barberos = []
        for barbero in lista_barberos:
            serv_b = df_serv[df_serv["barbero"] == barbero]
            total_gen = serv_b["precio"].sum() if not serv_b.empty else 0.0
            comision_bruta = total_gen * comision_pct

            gastos_b = (
                df_gastos[df_gastos["barbero_asignacion"] == barbero][
                    "monto"
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
            "Descripción del gasto (ej. Cuchillas, gel, adelanto, etc.)"
        )
        monto_gasto = st.number_input(
            "Monto ($)", min_value=0.0, step=0.5
        )

        submit_gasto = st.form_submit_button("Guardar Gasto")

        if submit_gasto and desc_gasto:
            fecha_actual = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            ejecutar_sql(
                "INSERT INTO gastos (fecha, barbero_asignacion, descripcion, monto) VALUES (?, ?, ?, ?)",
                (fecha_actual, quien_gasto, desc_gasto, monto_gasto),
            )
            st.success("Gasto registrado y guardado permanentemente.")
            st.rerun()

    st.markdown("---")
    st.subheader("Historial General de Gastos")
    df_gastos = cargar_datos("gastos")
    if not df_gastos.empty:
        df_mostrar_g = df_gastos[
            ["fecha", "barbero_asignacion", "descripcion", "monto"]
        ].rename(
            columns={
                "fecha": "Fecha",
                "barbero_asignacion": "Barbero / Asignación",
                "descripcion": "Descripción",
                "monto": "Monto ($)",
            }
        )
        st.dataframe(df_mostrar_g, use_container_width=True)
    else:
        st.info("Aún no se han registrado gastos.")

# 8. VERIFICAR PAGOS DE CLIENTES
elif opcion_menu == "🔍 Verificar Pagos":
    st.header("🔍 Verificación de Pagos por Cliente")
    st.write(
        "Busca y consulta el historial de pagos y servicios realizados por cada cliente en la barbería."
    )

    df_servicios = cargar_datos("servicios")

    if not df_servicios.empty:
        lista_clientes = sorted(df_servicios["cliente"].unique().tolist())
        cliente_seleccionado = st.selectbox(
            "Selecciona o busca un cliente", lista_clientes
        )

        if cliente_seleccionado:
            df_cliente_serv = df_servicios[
                df_servicios["cliente"] == cliente_seleccionado
            ]

            total_pagado_cliente = df_cliente_serv["precio"].sum()
            telefono_cliente = (
                df_cliente_serv["telefono"].iloc[0]
                if not df_cliente_serv.empty
                else "N/A"
            )
            cantidad_visitas = len(df_cliente_serv)

            col_v1, col_v2, col_v3 = st.columns(3)
            col_v1.metric(
                "Total Pagado Acumulado", f"${total_pagado_cliente:,.2f}"
            )
            col_v2.metric("Servicios / Visitas", cantidad_visitas)
            col_v3.metric(
                "Teléfono de Contacto",
                str(telefono_cliente) if telefono_cliente else "N/A",
            )

            st.markdown("---")
            st.subheader(f"Historial de Pagos de: {cliente_seleccionado}")

            df_mostrar_cli = df_cliente_serv[
                ["fecha", "barbero", "servicio", "precio"]
            ].rename(
                columns={
                    "fecha": "Fecha y Hora",
                    "barbero": "Barbero Atendió",
                    "servicio": "Servicio",
                    "precio": "Monto Pagado ($)",
                }
            )
            st.dataframe(df_mostrar_cli, use_container_width=True)

            tel_clean = "".join(filter(str.isdigit, str(telefono_cliente)))
            if tel_clean and tel_clean != "N/A":
                detalle_servicios_str = ""
                for _, s_row in df_cliente_serv.iterrows():
                    detalle_servicios_str += f"- {s_row['fecha']}: {s_row['servicio']} (${s_row['precio']:,.2f})\n"

                msg_wsp_pago = urllib.parse.quote(
                    f"Hola {cliente_seleccionado}, aquí tienes el resumen y verificación de tus pagos en Barbería Gods Time:\n\n"
                    f"{detalle_servicios_str}\n"
                    f"💵 *Total Acumulado Pagado:* ${total_pagado_cliente:,.2f}\n\n"
                    f"¡Gracias por tu preferencia y confianza!"
                )
                wsp_pago_url = (
                    f"https://wa.me/{tel_clean}?text={msg_wsp_pago}"
                )
                st.markdown(
                    f'<a href="{wsp_pago_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 16px; border-radius:6px; font-weight:bold; cursor:pointer; width:100%;">💬 Enviar Resumen de Pagos por WhatsApp</button></a>',
                    unsafe_allow_html=True,
                )
            else:
                st.caption(
                    "El cliente no cuenta con un número de teléfono válido registrado para enviar el resumen por WhatsApp."
                )
    else:
        st.info("No hay servicios registrados en la base de datos todavía.")

# 9. COBRAR FIADOS
elif opcion_menu == "📝 Cobrar Fiados":
    st.header("📝 Cuentas Pendientes y Cobro (Fiados)")

    with st.form("form_fiados"):
        cli_fiado = st.text_input("Nombre del Cliente")
        tel_fiado = st.text_input("Número de Teléfono (ej. +584121234567)")
        monto_fiado = st.number_input(
            "Saldo Pendiente ($)", min_value=0.0, step=1.0
        )

        submit_fiado = st.form_submit_button("Registrar Deuda")

        if submit_fiado and cli_fiado:
            ejecutar_sql(
                "INSERT INTO fiados (cliente, telefono, deuda, estado) VALUES (?, ?, ?, ?)",
                (
                    cli_fiado,
                    tel_fiado if tel_fiado else "N/A",
                    monto_fiado,
                    "Pendiente",
                ),
            )
            st.success("Deuda registrada correctamente.")
            st.rerun()

    st.markdown("---")
    st.subheader("Cuentas Pendientes")

    df_fiados = cargar_datos("fiados")
    if not df_fiados.empty:
        for idx, row in df_fiados.iterrows():
            with st.expander(
                f"📌 {row['cliente']} - ${row['deuda']:,.2f}"
            ):
                st.write(f"**Número de Teléfono:** {row['telefono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["telefono"])))
                if tel_clean:
                    msg = urllib.parse.quote(
                        f"Hola {row['cliente']}, te recordamos que tienes un saldo pendiente de ${row['deuda']:,.2f} en Barbería Gods Time."
                    )
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Cobrar por WhatsApp</button></a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("Sin número válido registrado.")

                st.write("")
                if st.button(
                    f"Marcar como Pagado ({row['cliente']})",
                    key=f"pay_debt_{row['id']}",
                ):
                    ejecutar_sql("DELETE FROM fiados WHERE id = ?", (row["id"],))
                    st.success("¡Deuda saldada!")
                    st.rerun()
    else:
        st.info("No hay cuentas pendientes.")
