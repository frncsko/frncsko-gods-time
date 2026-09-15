import streamlit as st
import pandas as pd
from datetime import datetime, date, time
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
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "cortes_db" not in st.session_state:
    st.session_state.cortes_db = cargar_datos(CORTES_FILE, [])
if "citas_db" not in st.session_state:
    st.session_state.citas_db = cargar_datos(CITAS_FILE, [])

# CREDENCIALES Y ROLES DE USUARIOS
USUARIOS = {
    "admin": {"clave": "1234", "rol": "admin"},
    "Jonder": {"clave": "barbero1", "rol": "barbero"}
}

# TASA DE CAMBIO DE REFERENCIA (BS / USD)
TASA_BCV = 36.50  # Puedes ajustar este valor según la tasa del día

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

# ESTILOS MODERNOS Y ANIMACIONES CSS
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

    /* ANIMACIÓN LATIDO Y BRILLO NEÓN DEL TÍTULO */
    @keyframes heartbeat-glow {
        0% {
            transform: scale(1);
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3);
        }
        14% {
            transform: scale(1.05);
            text-shadow: 0 0 25px rgba(0, 240, 255, 0.9), 0 0 40px rgba(0, 240, 255, 0.7);
        }
        28% {
            transform: scale(1);
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3);
        }
        42% {
            transform: scale(1.03);
            text-shadow: 0 0 20px rgba(0, 240, 255, 0.8), 0 0 30px rgba(0, 240, 255, 0.6);
        }
        70% {
            transform: scale(1);
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3);
        }
    }

    .header-title {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 5px;
    }

    .title-electric {
        font-size: 36px;
        font-weight: 900;
        color: #00f0ff !important;
        text-align: center;
        letter-spacing: 2px;
        display: inline-block;
        animation: heartbeat-glow 2.5s infinite ease-in-out;
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
            <div class="title-electric">BARBERÍA GOD'S TIME</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #00f0ff; font-weight: 700; font-size: 18px; margin-bottom: 30px;'>🔥 ¡Eleva tu presencia! El corte perfecto en el momento exacto. ⚡</p>", unsafe_allow_html=True)

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
                    precio_bs = precio_usd * TASA_BCV
                    
                    mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
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
    user_info = USUARIOS.get(st.session_state.usuario_actual, {"rol": "invitado"})
    es_admin = user_info["rol"] == "admin"

    col_t, col_l = st.columns([4, 1])
    with col_t:
        st.markdown(f'''
            <div class="header-title" style="justify-content: flex-start;">
                <div class="title-electric" style="font-size:26px;">BARBERÍA GOD'S TIME</div>
                <span style="margin-left: 15px; color: #94a3b8; font-weight: 600;">(Conectado como: <b style="color:#00f0ff;">{st.session_state.usuario_actual}</b>)</span>
            </div>
        ''', unsafe_allow_html=True)
    with col_l:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
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
        total_ingresos_usd = df_cortes["Precio ($)"].sum() if (not df_cortes.empty and "Precio ($)" in df_cortes.columns) else (df_cortes["Precio"].sum() if not df_cortes.empty else 0.0)
        total_ingresos_bs = total_ingresos_usd * TASA_BCV
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Total Cortes</h4><h2 style="margin:5px 0 0 0;">{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Ingresos Totales</h4><h2 style="margin:5px 0 0 0; font-size: 22px;">${total_ingresos_usd:.2f} <span style="color:#00f0ff; font-size:16px;">({total_ingresos_bs:.2f} BS)</span></h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Citas Agendadas</h4><h2 style="margin:5px 0 0 0;">{citas_pendientes}</h2></div>', unsafe_allow_html=True)

        st.markdown("### 💵 Lista de Servicios y Precios")
        precios_tabla = [
            {"Servicio / Corte": k, "Precio ($)": f"${v:.2f}", "Precio (BS)": f"{v * TASA_BCV:.2f} BS"}
            for k, v in PRECIOS_CORTES.items()
        ]
        st.table(pd.DataFrame(precios_tabla))

    # 2. REGISTRAR CORTE
    with tab_cortes:
        st.markdown("### ✂️ Registrar Nuevo Corte")
        with st.form("form_corte"):
            col1, col2 = st.columns(2)
            with col1:
                idx_barbero = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
                barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS, index=idx_barbero)
                corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
                precio_corte_usd = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
                precio_corte_bs = precio_corte_usd * TASA_BCV
                st.info(f"Monto equivalente en Bolívares: **{precio_corte_bs:.2f} BS**")
                cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            
            with col2:
                metodo_pago = st.selectbox("Método de Pago", METODOS_PAGO)
                referencia_pago = st.text_input("N° de Referencia / Transacción", placeholder="N/A para Efectivo")

            btn_guardar = st.form_submit_button("GUARDAR CORTE")
            
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
                    "Cliente": cliente_nombre if cliente_nombre else "Cliente Ocasional"
                }
                st.session_state.cortes_db.append(nuevo_registro)
                guardar_datos(CORTES_FILE, st.session_state.cortes_db)
                st.success(f"Corte registrado a {barbero_sel} correctamente (${precio_corte_usd:.2f} / {precio_corte_bs:.2f} BS) vía {metodo_pago}.")

    # 3. REGISTRO POR BARBERO
    with tab_barberos:
        st.markdown("### 💈 Historial por Barbero")
        idx_filtro = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
        barbero_filtro = st.selectbox("Selecciona un Barbero", BARBEROS, index=idx_filtro, key="filtro_barbero")
        
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            if not df_filtrado.empty:
                st.dataframe(df_filtrado, use_container_width=True)
                col_precio = "Precio ($)" if "Precio ($)" in df_filtrado.columns else "Precio"
                total_usd = df_filtrado[col_precio].sum()
                total_bs = total_usd * TASA_BCV
                st.info(f"Total acumulado por **{barbero_filtro}**: **${total_usd:.2f} USD** / **{total_bs:.2f} BS** ({len(df_filtrado)} cortes)")
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
                precio_bs = precio_usd * TASA_BCV
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
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

    # 5. ADMINISTRACIÓN (RESTRICCIÓN DE PERMISOS)
    with tab_admin:
        st.markdown("### ⚙️ Panel de Control del Administrador")
        
        if es_admin:
            st.warning("⚠️ **Atención:** La siguiente opción borrará permanentemente las citas y cortes.")
            if st.button("🔴 REINICIAR TODO EL HISTORIAL"):
                st.session_state.cortes_db = []
                st.session_state.citas_db = []
                guardar_datos(CORTES_FILE, [])
                guardar_datos(CITAS_FILE, [])
                st.success("El historial completo ha sido borrado.")
                st.rerun()
        else:
            st.error("🔒 **Acceso restringido:** Tu usuario (Jonder) no posee permisos para borrar o reiniciar el historial de la barbería.")
