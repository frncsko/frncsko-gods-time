import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import urllib.parse
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="God's Time Barbería", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- PERSISTENCIA LOCAL DE DATOS ---
CORTES_FILE = "cortes_data.json"
CITAS_FILE = "citas_data.json"
GASTOS_FILE = "gastos_data.json"
INVENTARIO_FILE = "inventario_data.json"
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
if "gastos_db" not in st.session_state:
    st.session_state.gastos_db = cargar_datos(GASTOS_FILE, [])
if "inventario_db" not in st.session_state:
    st.session_state.inventario_db = cargar_datos(INVENTARIO_FILE, [
        {"Producto": "Cera para Cabello", "Stock": 10, "Precio ($)": 8.0},
        {"Producto": "Aceite para Barba", "Stock": 6, "Precio ($)": 6.0},
        {"Producto": "Minoxidil", "Stock": 4, "Precio ($)": 15.0}
    ])

config_cargada = cargar_datos(CONFIG_FILE, {"tasa_bcv": 36.50})
if "tasa_bcv" not in st.session_state:
    st.session_state.tasa_bcv = config_cargada.get("tasa_bcv", 36.50)

# CREDENCIALES Y ROLES DE USUARIOS
USUARIOS = {
    "Francisco": {"clave": "admin123", "rol": "admin"},
    "Jonder": {"clave": "barbero1", "rol": "barbero"}
}

PRECIOS_CORTES = {
    "Corte Clásico": 10.0,
    "Corte y Barba": 12.0,
    "Barba Completa": 5.0,
    "Combo (Corte + Barba + Mascarilla)": 13.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Francisco", "Jonder", "Barbero 3"]
METODOS_PAGO = ["EFECTIVO", "PAGO MOVIL", "BINANCE"]

OPCIONES_HORAS = [
    time(h, m).strftime("%I:%M %p") 
    for h in range(8, 20) 
    for m in (0, 30)
]

# ESTILOS FUTURISTAS Y BOTONES 3D BRILLANTES (GLOSSY PILL BUTTONS)
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

    [data-testid="stSidebar"] {
        background: rgba(10, 17, 30, 0.95) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
    }

    [data-testid="stSidebar"] .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    [data-testid="stSidebar"] .stRadio label {
        position: relative;
        background: linear-gradient(180deg, #00c6ff 0%, #0072ff 100%) !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease !important;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 15px rgba(0, 114, 255, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.7) !important;
        overflow: hidden;
    }

    [data-testid="stSidebar"] .stRadio label::before {
        content: '';
        position: absolute;
        top: 2px;
        left: 10%;
        right: 10%;
        height: 40%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0) 100%);
        border-radius: 50px 50px 20px 20px;
        pointer-events: none;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 12px 20px rgba(0, 240, 255, 0.6), inset 0 2px 6px rgba(255, 255, 255, 0.9) !important;
    }

    [data-testid="stSidebar"] .stRadio div[aria-checked="true"] + label {
        background: linear-gradient(180deg, #00f0ff 0%, #0040a0 100%) !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.9), inset 0 2px 6px rgba(255, 255, 255, 1) !important;
    }

    .stButton > button {
        position: relative;
        background: linear-gradient(180deg, #00f0ff 0%, #0066cc 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-radius: 50px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        width: 100%;
        padding: 14px 28px !important;
        box-shadow: 0 8px 18px rgba(0, 102, 204, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.8) !important;
        transition: all 0.3s ease-in-out;
        overflow: hidden;
    }

    .stButton > button:hover {
        box-shadow: 0 12px 25px rgba(0, 240, 255, 0.8), inset 0 2px 6px rgba(255, 255, 255, 1) !important;
        transform: translateY(-2px);
    }

    .btn-ws-glow {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: linear-gradient(180deg, #25D366 0%, #128C7E 100%) !important;
        color: white !important;
        text-decoration: none;
        border-radius: 50px !important;
        padding: 14px 28px;
        font-weight: 800;
        font-size: 15px;
        letter-spacing: 1px;
        text-transform: uppercase;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 18px rgba(37, 211, 102, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
        overflow: hidden;
    }

    .btn-ws-glow:hover {
        box-shadow: 0 12px 25px rgba(37, 211, 102, 0.8), inset 0 2px 6px rgba(255, 255, 255, 1);
        transform: translateY(-2px);
        color: white !important;
    }

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
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: INICIO CLIENTES (AGENDAR CITAS)
# ---------------------------------------------------------
if not st.session_state.autenticado:
    col_header, col_login_btn = st.columns([5, 1.2])
    
    with col_login_btn:
        with st.popover("Acceso Personal 🔐", use_container_width=True):
            st.markdown("<h4 style='text-align: center; color: #ffffff; margin-bottom: 10px;'>ACCESO PERSONAL</h4>", unsafe_allow_html=True)
            with st.form("login_form_popover"):
                usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario")
                contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")
                submit = st.form_submit_button("ENTRAR")

                if submit:
                    if usuario in USUARIOS and USUARIOS[usuario]["clave"] == contrasena:
                        st.session_state.autenticado = True
                        st.session_state.usuario_actual = usuario
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas")

    st.markdown('''
        <div style="text-align: center; margin-top: -20px;">
            <div class="title-electric">GOD'S TIME BARBERÍA</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #00f0ff; font-weight: 700; font-size: 18px; margin-top: 10px; margin-bottom: 30px;'>🔥 ¡Eleva tu presencia! El corte perfecto en el momento exacto. ⚡</p>", unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown("<h3 style='text-align: center; color: #ffffff;'>Reserva tu Cita</h3>", unsafe_allow_html=True)
        with st.form("form_cita_login"):
            nombre_c = st.text_input("Tu Nombre Completo")
            
            # --- CAMPO DE TELÉFONO CON CÓDIGO +58 AUTOMÁTICO ---
            col_cod, col_num = st.columns([1, 3])
            with col_cod:
                st.text_input("Código", value="+58", disabled=True, key="cod_ve_login")
            with col_num:
                num_local_c = st.text_input("Teléfono (Ej: 4120000000)", key="num_local_login")

            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita_login")
            
            col_f1, col_h1 = st.columns(2)
            with col_f1:
                fecha_c = st.date_input("Fecha de la cita", min_value=date.today(), key="fecha_cita_login")
            with col_h1:
                hora_c = st.selectbox("Hora de la cita", OPCIONES_HORAS, key="hora_cita_login")

            servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita_login")
            btn_agendar_login = st.form_submit_button("REGISTRAR CITA")

        if btn_agendar_login:
            num_limpio = num_local_c.replace(" ", "").replace("-", "").strip()
            if nombre_c and num_limpio:
                # Se fuerza el código +58 por delante
                telefono_c = f"+58{num_limpio.lstrip('0')}"
                
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
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en God's Time Barbería el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "")
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
# VISTA 2: PANEL PRINCIPAL (ADMIN Y BARBEROS)
# ---------------------------------------------------------
else:
    user_info = USUARIOS.get(st.session_state.usuario_actual, {"rol": "invitado"})
    es_admin = user_info["rol"] == "admin"

    with st.sidebar:
        st.markdown('''
            <div style="text-align: center; padding: 10px 0;">
                <div class="title-electric" style="font-size: 20px;">GOD'S TIME BARBERÍA</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 13px;'>Usuario: <b style='color:#00f0ff;'>{st.session_state.usuario_actual}</b></p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("<p style='font-size: 13px; color: #00f0ff; font-weight: 800; margin-bottom: 8px;'>MENÚ PRINCIPAL</p>", unsafe_allow_html=True)

        opciones_menu = {
            "📊 Panel General": "Panel General",
            "✂️ Registrar Corte": "Registrar Corte",
            "💈 Historial Barberos": "Historial Barberos",
            "📅 Citas y WhatsApp": "Citas y WhatsApp",
            "💸 Gastos / Caja Chica": "Gastos",
            "📦 Inventario Productos": "Inventario",
            "⚙️ Administración": "Administración"
        }
        
        seleccion_label = st.radio(
            label="", 
            options=list(opciones_menu.keys()),
            label_visibility="collapsed"
        )
        
        opcion_menu = opciones_menu[seleccion_label]
        
        st.markdown("---")
        st.markdown("<p style='font-size: 13px; color: #00f0ff; font-weight: 800; margin-bottom: 5px;'>💵 TASA DEL DÓLAR ($)</p>", unsafe_allow_html=True)
        nueva_tasa_input = st.number_input("Tasa BS", value=float(st.session_state.tasa_bcv), step=0.10, label_visibility="collapsed")
        if st.button("ACTUALIZAR TASA"):
            st.session_state.tasa_bcv = nueva_tasa_input
            guardar_datos(CONFIG_FILE, {"tasa_bcv": nueva_tasa_input})
            st.success(f"Tasa actualizada: {nueva_tasa_input:.2f} BS")
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.rerun()

    # 1. PANEL GENERAL
    if opcion_menu == "Panel General":
        st.markdown('<div class="section-header">📊 PANEL GENERAL - GOD\'S TIME BARBERÍA</div>', unsafe_allow_html=True)
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        df_gastos = pd.DataFrame(st.session_state.gastos_db)
        
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos_usd = df_cortes["Precio ($)"].sum() if (not df_cortes.empty and "Precio ($)" in df_cortes.columns) else 0.0
        total_gastos_usd = df_gastos["Monto ($)"].sum() if (not df_gastos.empty and "Monto ($)" in df_gastos.columns) else 0.0
        
        total_ingresos_bs = total_ingresos_usd * st.session_state.tasa_bcv
        citas_pendientes = len(st.session_state.citas_db)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0; font-size:14px;">Total Cortes</h4><h2 style="margin:5px 0 0 0;">{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0; font-size:14px;">Ingresos Brutos</h4><h2 style="margin:5px 0 0 0; font-size: 20px;">${total_ingresos_usd:.2f}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0; font-size:14px;">Gastos Locales</h4><h2 style="margin:5px 0 0 0; font-size: 20px; color:#ff4d4d;">${total_gastos_usd:.2f}</h2></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0; font-size:14px;">Citas Activas</h4><h2 style="margin:5px 0 0 0;">{citas_pendientes}</h2></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top: 30px;">💵 TARIFA DE SERVICIOS OFICIALES</div>', unsafe_allow_html=True)
        precios_tabla = [
            {"Servicio / Corte": k, "Precio ($)": f"${v:.2f}", "Precio (BS)": f"{v * st.session_state.tasa_bcv:.2f} BS"}
            for k, v in PRECIOS_CORTES.items()
        ]
        st.table(pd.DataFrame(precios_tabla))

    # 2. REGISTRAR CORTE
    elif opcion_menu == "Registrar Corte":
        st.markdown('<div class="section-header">✂️ REGISTRO DE NUEVO CORTE</div>', unsafe_allow_html=True)
        with st.form("form_corte"):
            col1, col2 = st.columns(2)
            with col1:
                idx_barbero = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
                barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS, index=idx_barbero)
                corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
                precio_corte_usd = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
                precio_corte_bs = precio_corte_usd * st.session_state.tasa_bcv
                st.info(f"Monto en Bolívares (Tasa {st.session_state.tasa_bcv:.2f}): **{precio_corte_bs:.2f} BS**")
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
                st.success(f"Corte registrado a {barbero_sel} correctamente (${precio_corte_usd:.2f} / {precio_corte_bs:.2f} BS).")

    # 3. HISTORIAL Y COMISIONES POR BARBERO
    elif opcion_menu == "Historial Barberos":
        st.markdown('<div class="section-header">💈 HISTORIAL Y COMISIONES POR BARBERO</div>', unsafe_allow_html=True)
        idx_filtro = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
        barbero_filtro = st.selectbox("Selecciona un Barbero", BARBEROS, index=idx_filtro, key="filtro_barbero")
        
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            
            if not df_filtrado.empty:
                col_precio = "Precio ($)" if "Precio ($)" in df_filtrado.columns else "Precio"
                total_usd = df_filtrado[col_precio].sum()
                comision_barbero = total_usd * 0.50 # 50% de comisión
                total_bs = total_usd * st.session_state.tasa_bcv
                
                st.info(f"Total recaudado por **{barbero_filtro}**: **${total_usd:.2f} USD** ({len(df_filtrado)} cortes) | Comisión estimada (50%): **${comision_barbero:.2f}**")

                tab_hist, tab_cli = st.tabs(["HISTORIAL DE CORTES", "CLIENTES ATENDIDOS"])
                
                with tab_hist:
                    st.dataframe(df_filtrado, use_container_width=True)
                
                with tab_cli:
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
        st.markdown('<div class="section-header">📅 GESTIÓN DE CITAS Y WHATSAPP</div>', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            
            # --- CÓDIGO +58 AUTOMÁTICO EN PANEL ADMIN ---
            col_cod_adm, col_num_adm = st.columns([1, 3])
            with col_cod_adm:
                st.text_input("Código", value="+58", disabled=True, key="cod_ve_admin")
            with col_num_adm:
                num_local_adm = st.text_input("Teléfono (Ej: 4120000000)", key="num_local_admin")

            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha de la cita", min_value=date.today())
            hora_c = st.selectbox("Hora de la cita", OPCIONES_HORAS, key="hora_cita_admin")
            servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("REGISTRAR CITA Y NOTIFICAR"):
            num_limpio_adm = num_local_adm.replace(" ", "").replace("-", "").strip()
            if nombre_c and num_limpio_adm:
                telefono_c = f"+58{num_limpio_adm.lstrip('0')}"
                
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
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en God's Time Barbería el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-glow">
                        Enviar Confirmación por WhatsApp
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.error("Por favor ingresa el nombre y el teléfono.")

        st.markdown('<div class="section-header" style="margin-top:30px;">CITAS REGISTRADAS</div>', unsafe_allow_html=True)
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. GASTOS / CAJA CHICA
    elif opcion_menu == "Gastos":
        st.markdown('<div class="section-header">💸 CONTROL DE GASTOS Y CAJA CHICA</div>', unsafe_allow_html=True)
        with st.form("form_gastos"):
            c_g1, c_g2 = st.columns(2)
            with c_g1:
                concepto_gasto = st.text_input("Concepto del Gasto (Ej: Compra de Cuchillas, Insumos, Limpieza)")
                monto_gasto_usd = st.number_input("Monto en ($)", min_value=0.0, step=1.0)
            with c_g2:
                categoria_gasto = st.selectbox("Categoría", ["Insumos", "Servicios Básicos", "Mantenimiento", "Otros"])
                responsable_gasto = st.selectbox("Registrado por", BARBEROS)

            btn_reg_gasto = st.form_submit_button("REGISTRAR GASTO")
            if btn_reg_gasto:
                if concepto_gasto and monto_gasto_usd > 0:
                    gasto_item = {
                        "Fecha": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
                        "Concepto": concepto_gasto,
                        "Categoría": categoria_gasto,
                        "Monto ($)": monto_gasto_usd,
                        "Responsable": responsable_gasto
                    }
                    st.session_state.gastos_db.append(gasto_item)
                    guardar_datos(GASTOS_FILE, st.session_state.gastos_db)
                    st.success(f"Gasto registrado: ${monto_gasto_usd:.2f} en {concepto_gasto}")
                else:
                    st.error("Por favor ingresa un concepto válido y un monto mayor a 0.")

        st.markdown("### Historial de Gastos")
        if st.session_state.gastos_db:
            st.dataframe(pd.DataFrame(st.session_state.gastos_db), use_container_width=True)
        else:
            st.info("No hay gastos registrados.")

    # 6. INVENTARIO DE PRODUCTOS
    elif opcion_menu == "Inventario":
        st.markdown('<div class="section-header">📦 INVENTARIO DE PRODUCTOS</div>', unsafe_allow_html=True)
        df_inv = pd.DataFrame(st.session_state.inventario_db)
        st.dataframe(df_inv, use_container_width=True)

        with st.form("form_nuevo_prod"):
            st.markdown("#### Agregar o Actualizar Stock")
            np1, np2, np3 = st.columns(3)
            with np1:
                p_nombre = st.text_input("Nombre del Producto")
            with np2:
                p_stock = st.number_input("Cantidad en Stock", min_value=0, step=1)
            with np3:
                p_precio = st.number_input("Precio de Venta ($)", min_value=0.0, step=0.5)

            btn_add_prod = st.form_submit_button("GUARDAR / ACTUALIZAR PRODUCTO")
            if btn_add_prod and p_nombre:
                encontrado = False
                for item in st.session_state.inventario_db:
                    if item["Producto"].lower() == p_nombre.lower():
                        item["Stock"] = p_stock
                        item["Precio ($)"] = p_precio
                        encontrado = True
                        break
                if not encontrado:
                    st.session_state.inventario_db.append({
                        "Producto": p_nombre,
                        "Stock": p_stock,
                        "Precio ($)": p_precio
                    })
                guardar_datos(INVENTARIO_FILE, st.session_state.inventario_db)
                st.success(f"Producto '{p_nombre}' actualizado correctamente.")
                st.rerun()

    # 7. ADMINISTRACIÓN
    elif opcion_menu == "Administración":
        st.markdown('<div class="section-header">⚙️ PANEL DE ADMINISTRACIÓN</div>', unsafe_allow_html=True)
        
        if es_admin:
            st.warning("⚠️ **Atención:** Las opciones a continuación modifican datos críticos del negocio.")
            if st.button("REINICIAR TODO EL HISTORIAL DE CORTES Y CITAS"):
                st.session_state.cortes_db = []
                st.session_state.citas_db = []
                st.session_state.gastos_db = []
                guardar_datos(CORTES_FILE, [])
                guardar_datos(CITAS_FILE, [])
                guardar_datos(GASTOS_FILE, [])
                st.success("Historial reiniciado exitosamente.")
                st.rerun()
        else:
            st.error("🔒 **Acceso restringido:** Tu usuario no posee permisos de administrador.")
