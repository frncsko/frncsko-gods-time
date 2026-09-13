import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse
import json
import os

# Configuración de la página
st.set_page_config(page_title="Barbería God's Time", layout="wide", initial_sidebar_state="collapsed")

# --- PERSISTENCIA LOCAL DE DATOS ---
CORTES_FILE = "cortes_data.json"
CITAS_FILE = "citas_data.json"

def cargar_datos(archivo, por_defecto=[]):
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

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "cortes_db" not in st.session_state:
    st.session_state.cortes_db = cargar_datos(CORTES_FILE, [])
if "citas_db" not in st.session_state:
    st.session_state.citas_db = cargar_datos(CITAS_FILE, [])

PRECIOS_CORTES = {
    "Corte Clásico": 10.0,
    "Degradado / Fade": 12.0,
    "Barba Completa": 8.0,
    "Combo (Corte + Barba)": 18.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Barbero 1", "Barbero 2", "Barbero 3"]
METODOS_PAGO = ["EFECTIVO", "PAGO MOVIL", "BINANCE"]

# ESTILOS MODERNOS Y LIMPIOS CON BOTONES BRILLANTES Y DE NEÓN
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1b2a 0%, #050811 100%);
        color: #e2e8f0;
    }

    /* CABECERA */
    .header-title {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }

    .title-electric {
        font-size: 32px;
        font-weight: 800;
        color: #00f0ff !important;
        text-align: center;
        letter-spacing: 1px;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
    }

    h1, h2, h3 {
        color: #00f0ff !important;
        font-weight: 800 !important;
    }

    /* MENÚ (TABS) */
    div[data-baseweb="tab-list"] {
        background: rgba(13, 27, 42, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 8px !important;
        gap: 12px !important;
    }

    button[data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        color: #94a3b8 !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        color: #00f0ff !important;
        border-color: rgba(0, 240, 255, 0.3) !important;
    }

    button[aria-selected="true"] {
        background: linear-gradient(135deg, #00f0ff 0%, #0072ff 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(0, 240, 255, 0.4) !important;
        transform: translateY(-2px);
    }

    /* TARJETAS Y FORMULARIOS */
    .card-3d, [data-testid="stForm"] {
        background: rgba(10, 16, 30, 0.85);
        backdrop-filter: blur(14px);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(0, 240, 255, 0.25);
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

    /* BOTÓN WHATSAPP CON EFECTO BRILLANTE */
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
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4), 0 0 15px rgba(37, 211, 102, 0.6);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .btn-ws-glow:hover {
        box-shadow: 0 6px 30px rgba(37, 211, 102, 0.8), 0 0 25px rgba(255, 255, 255, 0.5);
        transform: translateY(-3px) scale(1.02);
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: INICIO DE SESIÓN / CLIENTES
# ---------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''
        <div class="header-title">
            <div class="title-electric">BARBERÍA GOD\'S TIME</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-weight: 600;'>Excelencia, estilo y precisión en cada detalle</p>", unsafe_allow_html=True)
    
    tab_login, tab_cita_cliente = st.tabs(["⚡ ACCESO PERSONAL", "📅 AGENDAR CITA"])

    with tab_login:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.markdown("<h3 style='text-align: center; color: #ffffff;'>ACCESO AL SISTEMA</h3>", unsafe_allow_html=True)
                usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario")
                contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")
                submit = st.form_submit_button("ENTRAR AL SISTEMA")

            if submit:
                if usuario == "admin" and contrasena == "admin":
                    st.session_state.autenticado = True
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
                fecha_c = st.date_input("Fecha de la cita", min_value=date.today(), key="fecha_cita_login")
                hora_c = st.time_input("Hora de la cita", key="hora_cita_login")
                servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita_login")
                
                btn_agendar_login = st.form_submit_button("📅 CONCORDAR CITA")

            if btn_agendar_login:
                if nombre_c and telefono_c:
                    cita = {
                        "Cliente": nombre_c,
                        "Teléfono": telefono_c,
                        "Barbero": barbero_c,
                        "Fecha": str(fecha_c),
                        "Hora": str(hora_c),
                        "Servicio": servicio_c
                    }
                    st.session_state.citas_db.append(cita)
                    guardar_datos(CITAS_FILE, st.session_state.citas_db)
                    
                    mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c}."
                    mensaje_encoded = urllib.parse.quote(mensaje)
                    phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                    ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                    
                    st.success("¡Cita agendada exitosamente!")
                    st.markdown(f'''
                        <a href="{ws_url}" target="_blank" class="btn-ws-glow">
                            <i class="fab fa-whatsapp" style="font-size: 22px;"></i> Confirmar por WhatsApp
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.error("Por favor completa tu nombre y número de teléfono.")

# ---------------------------------------------------------
# VISTA 2: PANEL PRINCIPAL ADMINISTRATIVO
# ---------------------------------------------------------
else:
    col_t, col_l = st.columns([4, 1])
    with col_t:
        st.markdown('''
            <div class="header-title" style="justify-content: flex-start;">
                <div class="title-electric" style="font-size:26px;">BARBERÍA GOD\'S TIME</div>
            </div>
        ''', unsafe_allow_html=True)
    with col_l:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.autenticado = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    tab_inicio, tab_cortes, tab_barberos, tab_citas, tab_admin = st.tabs([
        "🏠 PANEL PRINCIPAL", 
        "✂️ REGISTRAR CORTE", 
        "💈 REGISTRO BARBEROS", 
        "📅 CITAS & WHATSAPP",
        "⚙️ ADMINISTRACIÓN"
    ])

    # 1. PANEL PRINCIPAL
    with tab_inicio:
        st.markdown("### 📊 Métricas Operativas")
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos = df_cortes["Precio"].sum() if not df_cortes.empty else 0.0
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Total Cortes</h4><h2 style="margin:5px 0 0 0;">{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Ingresos Totales</h4><h2 style="margin:5px 0 0 0;">${total_ingresos:.2f}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Citas Agendadas</h4><h2 style="margin:5px 0 0 0;">{citas_pendientes}</h2></div>', unsafe_allow_html=True)

        st.markdown("### 💵 Lista de Servicios y Precios")
        precios_df = pd.DataFrame(list(PRECIOS_CORTES.items()), columns=["Servicio / Corte", "Precio ($)"])
        st.table(precios_df)

    # 2. REGISTRAR CORTE
    with tab_cortes:
        st.markdown("### ✂️ Registrar Nuevo Corte")
        with st.form("form_corte"):
            col1, col2 = st.columns(2)
            with col1:
                barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS)
                corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
                precio_corte = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
                cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            
            with col2:
                metodo_pago = st.selectbox("Método de Pago", METODOS_PAGO)
                referencia_pago = st.text_input("N° de Referencia / Transacción", placeholder="N/A para Efectivo")

            btn_guardar = st.form_submit_button("GUARDAR CORTE")
            
            if btn_guardar:
                ref_final = referencia_pago.strip() if referencia_pago.strip() else ("N/A" if metodo_pago == "EFECTIVO" else "Sin ref.")
                
                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Barbero": barbero_sel,
                    "Servicio": corte_sel,
                    "Precio": precio_corte,
                    "Método Pago": metodo_pago,
                    "Referencia": ref_final,
                    "Cliente": cliente_nombre if cliente_nombre else "Cliente Ocasional"
                }
                st.session_state.cortes_db.append(nuevo_registro)
                guardar_datos(CORTES_FILE, st.session_state.cortes_db)
                st.success(f"Corte registrado a {barbero_sel} correctamente vía {metodo_pago}.")

    # 3. REGISTRO POR BARBERO
    with tab_barberos:
        st.markdown("### 💈 Historial por Barbero")
        barbero_filtro = st.selectbox("Selecciona un Barbero", BARBEROS, key="filtro_barbero")
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            if not df_filtrado.empty:
                st.dataframe(df_filtrado, use_container_width=True)
                st.info(f"Total acumulado por **{barbero_filtro}**: **${df_filtrado['Precio'].sum():.2f}** ({len(df_filtrado)} cortes)")
            else:
                st.warning(f"No hay registros para {barbero_filtro}.")
        else:
            st.write("No hay datos de cortes.")

    # 4. CITAS Y WHATSAPP
    with tab_citas:
        st.markdown("### 📅 Agendar Nueva Cita (Interno)")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            telefono_c = st.text_input("Teléfono (Ej: +584120000000)")
            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha de la cita", min_value=date.today())
            hora_c = st.time_input("Hora de la cita")
            servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("AGENDAR Y NOTIFICAR POR WHATSAPP"):
            if nombre_c and telefono_c:
                cita = {
                    "Cliente": nombre_c,
                    "Teléfono": telefono_c,
                    "Barbero": barbero_c,
                    "Fecha": str(fecha_c),
                    "Hora": str(hora_c),
                    "Servicio": servicio_c
                }
                st.session_state.citas_db.append(cita)
                guardar_datos(CITAS_FILE, st.session_state.citas_db)
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c}."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-glow">
                        <i class="fab fa-whatsapp" style="font-size: 22px;"></i> Enviar Confirmación por WhatsApp
                    </a>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Citas Registradas")
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. ADMINISTRACIÓN
    with tab_admin:
        st.markdown("### ⚙️ Panel de Control del Administrador")
        st.warning("⚠️ **Atención:** La siguiente opción borrará permanentemente las citas y cortes.")
        if st.button("🔴 REINICIAR TODO EL HISTORIAL"):
            st.session_state.cortes_db = []
            st.session_state.citas_db = []
            guardar_datos(CORTES_FILE, [])
            guardar_datos(CITAS_FILE, [])
            st.success("El historial completo ha sido borrado.")
            st.rerun()
