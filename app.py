import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import urllib.parse
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="Barbería God's Time", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- PERSISTENCIA LOCAL DE DATOS ---
CORTES_FILE = "cortes_data.json"
CITAS_FILE = "citas_data.json"
CONFIG_FILE = "config_data.json"

def cargar_datos(archivo, por_defecto):
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return por_defecto
    return por_defecto

def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# Inicialización de Estados
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "cortes_db" not in st.session_state:
    st.session_state.cortes_db = cargar_datos(CORTES_FILE, [])
if "citas_db" not in st.session_state:
    st.session_state.citas_db = cargar_datos(CITAS_FILE, [])

config_cargada = cargar_datos(CONFIG_FILE, {"tasa_bcv": 36.50})
if "tasa_bcv" not in st.session_state:
    st.session_state.tasa_bcv = config_cargada.get("tasa_bcv", 36.50)

# CREDENCIALES Y ROLES DE USUARIOS
USUARIOS = {
    "admin": {"clave": "1234", "rol": "admin"},
    "Jonder": {"clave": "barbero1", "rol": "barbero"}
}

PRECIOS_CORTES = {
    "Corte Clásico": 10.0,
    "Degradado / Fade": 12.0,
    "Barba Completa": 8.0,
    "Combo (Corte + Barba)": 18.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Francisco", "Jonder", "Barbero 3"]
METODOS_PAGO = ["EFECTIVO", "PAGO MOVIL", "BINANCE"]

# GENERADOR DE OPCIONES DE HORAS (AM / PM)
OPCIONES_HORAS = [
    time(h, m).strftime("%I:%M %p") 
    for h in range(8, 20) 
    for m in (0, 30)
]

# ESTILOS FUTURISTAS, FUENTES MODERNAS Y ANIMACIONES
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 50% 10%, #080f1a 0%, #03050a 100%);
        color: #e2e8f0;
    }

    /* BARRA LATERAL IZQUIERDA MODERNIZADA */
    [data-testid="stSidebar"] {
        background: rgba(10, 17, 30, 0.95) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
    }

    [data-testid="stSidebar"] .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        color: #94a3b8 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        cursor: pointer;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        color: #00f0ff !important;
        border-color: rgba(0, 240, 255, 0.4) !important;
    }

    [data-testid="stSidebar"] .stRadio div[aria-checked="true"] + label {
        background: linear-gradient(135deg, #00f0ff 0%, #0072ff 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(0, 240, 255, 0.4) !important;
    }

    /* EFECTO LATIDO Y NEÓN EN EL TÍTULO */
    @keyframes heartbeat-glow {
        0% { transform: scale(1); text-shadow: 0 0 10px rgba(0, 240, 255, 0.5); }
        14% { transform: scale(1.04); text-shadow: 0 0 25px rgba(0, 240, 255, 0.9); }
        28% { transform: scale(1); text-shadow: 0 0 10px rgba(0, 240, 255, 0.5); }
        42% { transform: scale(1.02); text-shadow: 0 0 20px rgba(0, 240, 255, 0.8); }
        70% { transform: scale(1); text-shadow: 0 0 10px rgba(0, 240, 255, 0.5); }
    }

    .title-electric {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: #00f0ff !important;
        text-align: center;
        letter-spacing: 2px;
        display: inline-block;
        animation: heartbeat-glow 2.5s infinite ease-in-out;
    }

    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #00f0ff;
        border-bottom: 2px solid rgba(0, 240, 255, 0.3);
        padding-bottom: 8px;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }

    .card-3d, [data-testid="stForm"] {
        background: rgba(10, 18, 32, 0.85);
        backdrop-filter: blur(14px);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(0, 240, 255, 0.2);
    }

    .stButton > button {
        background: linear-gradient(135deg, #00f0ff 0%, #0072ff 100%);
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 14px;
        border: none;
        width: 100%;
        padding: 14px;
        box-shadow: 0 6px 20px rgba(0, 240, 255, 0.35);
        transition: all 0.3s ease-in-out;
    }

    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.8);
        transform: scale(1.02);
    }

    .btn-ws-glow {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        text-decoration: none;
        border-radius: 14px;
        padding: 14px 20px;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: INICIO DE SESIÓN / CLIENTES
# ---------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''
        <div style="text-align: center;">
            <div class="title-electric">BARBERÍA GOD'S TIME</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #00f0ff; font-weight: 700; font-size: 18px; margin-top: 10px; margin-bottom: 30px;'>🔥 ¡Eleva tu presencia! El corte perfecto en el momento exacto. ⚡</p>", unsafe_allow_html=True)

    tab_login, tab_cita_cliente = st.tabs(["ACCESO PERSONAL", "AGENDAR CITA"])

    with tab_login:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.markdown("<h3 style='text-align: center; color: #ffffff;'>ACCESO AL SISTEMA</h3>", unsafe_allow_html=True)
                usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario")
                contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")
                submit = st.form_submit_button("ENTRAR AL SISTEMA")

            if submit:
                if usuario in USUARIOS and USUARIOS[usuario]["clave"] == contrasena:
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = usuario
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

    with tab_cita_cliente:
        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        with col_c2:
            st.markdown("<h3 style='text-align: center;'>Reserva tu Cita</h3>", unsafe_allow_html=True)
            with st.form("form_cita_login"):
                nombre_c = st.text_input("Tu Nombre Completo")
                telefono_c = st.text_input("Teléfono (Ej: +584120000000)")
                barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita_login")
                
                col_f1, col_h1 = st.columns(2)
                with col_f1:
                    fecha_c = st.date_input("Fecha de la cita", min_value=date.today(), key="fecha_cita_login")
                with col_h1:
                    hora_c = st.selectbox("Hora de la cita", OPCIONES_HORAS, key="hora_cita_login")

                servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita_login")
                
                btn_agendar_login = st.form_submit_button("REGISTRAR CITA")

            if btn_agendar_login:
                if nombre_c and telefono_c:
                    cita = {
                        "Cliente": nombre_c,
                        "Teléfono": telefono_c,
                        "Barbero": barbero_c,
                        "Fecha": str(fecha_c),
                        "Hora": hora_c,
                        "Servicio": servicio_c
                    }
                    st.session_state.citas_db.append(cita)
                    guardar_datos(CITAS_FILE, st.session_state.citas_db)
                    
                    precio_usd = PRECIOS_CORTES[servicio_c]
                    precio_bs = precio_usd * st.session_state.tasa_bcv
                    
                    mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                    mensaje_encoded = urllib.parse.quote(mensaje)
                    phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                    ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                    
                    st.success("¡Cita agendada exitosamente!")
                    st.markdown(f'''
                        <a href="{ws_url}" target="_blank" class="btn-ws-glow">
                            Confirmar por WhatsApp
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.error("Por favor completa tu nombre y número de teléfono.")

# ---------------------------------------------------------
# VISTA 2: PANEL PRINCIPAL (MENÚ SIN ÍCONOS)
# ---------------------------------------------------------
else:
    user_info = USUARIOS.get(st.session_state.usuario_actual, {"rol": "invitado"})
    es_admin = user_info["rol"] == "admin"

    # SIDEBAR: MENÚ DE NAVEGACIÓN VERTICAL SIN ÍCONOS
    with st.sidebar:
        st.markdown('''
            <div style="text-align: center; padding: 10px 0;">
                <div class="title-electric" style="font-size: 22px;">GOD'S TIME</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 13px;'>Barbero: <b style='color:#00f0ff;'>{st.session_state.usuario_actual}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #00f0ff; font-weight: 700; font-size: 13px;'>Tasa del día: {st.session_state.tasa_bcv:.2f} BS</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("<p style='font-size: 12px; color: #00f0ff; font-weight: 800; letter-spacing: 1px; margin-bottom: 8px;'>MENÚ PRINCIPAL</p>", unsafe_allow_html=True)
        
        # OPCIONES SIN ÍCONOS
        opcion_menu = st.radio(
            label="Navegación",
            options=[
                "Panel General", 
                "Registrar Corte", 
                "Historial Barberos", 
                "Citas y WhatsApp", 
                "Administración"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.rerun()

    # 1. PANEL GENERAL
    if opcion_menu == "Panel General":
        st.markdown('<div class="section-header">PANEL GENERAL DE LA BARBERÍA</div>', unsafe_allow_html=True)
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos_usd = df_cortes["Precio ($)"].sum() if (not df_cortes.empty and "Precio ($)" in df_cortes.columns) else (df_cortes["Precio"].sum() if not df_cortes.empty else 0.0)
        total_ingresos_bs = total_ingresos_usd * st.session_state.tasa_bcv
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Total Cortes</h4><h2 style="margin:5px 0 0 0;">{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Ingresos Totales</h4><h2 style="margin:5px 0 0 0; font-size: 22px;">${total_ingresos_usd:.2f} <span style="color:#00f0ff; font-size:16px;">({total_ingresos_bs:.2f} BS)</span></h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Citas Agendadas</h4><h2 style="margin:5px 0 0 0;">{citas_pendientes}</h2></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top: 30px;">TARIFA DE SERVICIOS</div>', unsafe_allow_html=True)
        precios_tabla = [
            {"Servicio / Corte": k, "Precio ($)": f"${v:.2f}", "Precio (BS)": f"{v * st.session_state.tasa_bcv:.2f} BS"}
            for k, v in PRECIOS_CORTES.items()
        ]
        st.table(pd.DataFrame(precios_tabla))

    # 2. REGISTRAR CORTE
    elif opcion_menu == "Registrar Corte":
        st.markdown('<div class="section-header">REGISTRO DE NUEVO CORTE</div>', unsafe_allow_html=True)
        with st.form("form_corte"):
            col1, col2 = st.columns(2)
            with col1:
                idx_barbero = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
                barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS, index=idx_barbero)
                corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
                precio_corte_usd = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
                precio_corte_bs = precio_corte_usd * st.session_state.tasa_bcv
                st.info(f"Monto equivalente en Bolívares (Tasa {st.session_state.tasa_bcv:.2f}): **{precio_corte_bs:.2f} BS**")
                cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            
            with col2:
                metodo_pago = st.selectbox("Método de Pago", METODOS_PAGO)
                referencia_pago = st.text_input("N° de Referencia / Transacción", placeholder="N/A para Efectivo")

            btn_guardar = st.form_submit_button("GUARDAR CORTE Y REGISTRAR")
            
            if btn_guardar:
                ref_final = referencia_pago.strip() if referencia_pago.strip() else ("N/A" if metodo_pago == "EFECTIVO" else "Sin ref.")
                
                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
                    "Barbero": barbero_sel,
                    "Servicio": corte_sel,
                    "Precio ($)": precio_corte_usd,
                    "Precio (BS)": round(precio_corte_bs, 2),
                    "Método Pago": metodo_pago,
                    "Referencia": ref_final,
                    "Cliente": cliente_nombre.strip() if cliente_nombre.strip() else "Cliente Ocasional"
                }
                st.session_state.cortes_db.append(nuevo_registro)
                guardar_datos(CORTES_FILE, st.session_state.cortes_db)
                st.success(f"Corte registrado a {barbero_sel} correctamente (${precio_corte_usd:.2f} / {precio_corte_bs:.2f} BS) vía {metodo_pago}.")

    # 3. HISTORIAL Y REGISTRO DE CLIENTES POR BARBERO
    elif opcion_menu == "Historial Barberos":
        st.markdown('<div class="section-header">HISTORIAL Y REGISTRO DE CLIENTES POR BARBERO</div>', unsafe_allow_html=True)
        idx_filtro = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
        barbero_filtro = st.selectbox("Selecciona un Barbero", BARBEROS, index=idx_filtro, key="filtro_barbero")
        
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            
            if not df_filtrado.empty:
                col_precio = "Precio ($)" if "Precio ($)" in df_filtrado.columns else "Precio"
                total_usd = df_filtrado[col_precio].sum()
                total_bs = total_usd * st.session_state.tasa_bcv
                st.info(f"Total acumulado por **{barbero_filtro}**: **${total_usd:.2f} USD** / **{total_bs:.2f} BS** ({len(df_filtrado)} cortes)")

                tab_hist, tab_cli = st.tabs(["HISTORIAL DE CORTES", "CLIENTES ATENDIDOS"])
                
                with tab_hist:
                    st.dataframe(df_filtrado, use_container_width=True)
                
                with tab_cli:
                    st.markdown(f"### Clientes registrados con {barbero_filtro}")
                    df_clientes = df_filtrado.groupby("Cliente").agg(
                        Visitas=("Servicio", "count"),
                        Total_Gastado_USD=(col_precio, "sum"),
                        Ultima_Visita=("Fecha", "max")
                    ).reset_index()
                    df_clientes["Total_Gastado_BS"] = df_clientes["Total_Gastado_USD"] * st.session_state.tasa_bcv
                    st.dataframe(df_clientes, use_container_width=True)
            else:
                st.warning(f"No hay registros de cortes para {barbero_filtro}.")
        else:
            st.write("No hay datos de cortes registrados aún.")

    # 4. CITAS Y WHATSAPP
    elif opcion_menu == "Citas y WhatsApp":
        st.markdown('<div class="section-header">GESTIÓN DE CITAS Y RECORDATORIOS POR WHATSAPP</div>', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            telefono_c = st.text_input("Teléfono (Ej: +584120000000)")
            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha de la cita", min_value=date.today())
            hora_c = st.selectbox("Hora de la cita", OPCIONES_HORAS, key="hora_cita_admin")
            servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("REGISTRAR CITA Y NOTIFICAR POR WHATSAPP"):
            if nombre_c and telefono_c:
                cita = {
                    "Cliente": nombre_c,
                    "Teléfono": telefono_c,
                    "Barbero": barbero_c,
                    "Fecha": str(fecha_c),
                    "Hora": hora_c,
                    "Servicio": servicio_c
                }
                st.session_state.citas_db.append(cita)
                guardar_datos(CITAS_FILE, st.session_state.citas_db)
                
                precio_usd = PRECIOS_CORTES[servicio_c]
                precio_bs = precio_usd * st.session_state.tasa_bcv
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-glow">
                        Enviar Confirmación por WhatsApp
                    </a>
                ''', unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:30px;">CITAS REGISTRADAS</div>', unsafe_allow_html=True)
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. ADMINISTRACIÓN
    elif opcion_menu == "Administración":
        st.markdown('<div class="section-header">PANEL DE ADMINISTRACIÓN</div>', unsafe_allow_html=True)
        
        if es_admin:
            st.markdown("### Configuración de Tasa de Cambio")
            nueva_tasa = st.number_input("Tasa del día (BS / USD)", value=float(st.session_state.tasa_bcv), step=0.10)
            if st.button("ACTUALIZAR TASA EN EL SISTEMA"):
                st.session_state.tasa_bcv = nueva_tasa
                guardar_datos(CONFIG_FILE, {"tasa_bcv": nueva_tasa})
                st.success(f"Tasa del día actualizada a {nueva_tasa:.2f} BS")
                st.rerun()

            st.markdown("---")
            st.warning("⚠️ **Atención:** La siguiente opción borrará permanentemente las citas y los registros de cortes.")
            if st.button("REINICIAR TODO EL HISTORIAL"):
                st.session_state.cortes_db = []
                st.session_state.citas_db = []
                guardar_datos(CORTES_FILE, [])
                guardar_datos(CITAS_FILE, [])
                st.success("El historial completo ha sido borrado.")
                st.rerun()
        else:
            st.error("🔒 **Acceso restringido:** Tu usuario (Jonder) no posee permisos para modificar la tasa o reiniciar el historial de la barbería.")
