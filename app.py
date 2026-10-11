import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, time
import urllib.parse
import json
import os
import requests

# Configuración de la página
st.set_page_config(
    page_title="GOD'S TIME BARBERIA | 4K VIP Experience", 
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

# --- FUNCIÓN PARA OBTENER TASA BCV AUTOMÁTICA ---
def obtener_tasa_bcv_auto():
    try:
        response = requests.get("https://rates.dolarvzla.com/bcv/latest.json", timeout=4)
        if response.status_code == 200:
            data = response.json()
            return float(data.get("usd", 36.50))
    except Exception:
        pass
    return None

def limpiar_telefono(telefono):
    tel_limpio = telefono.strip().replace(" ", "").replace("-", "")
    if not tel_limpio.startswith("+"):
        if tel_limpio.startswith("58"):
            tel_limpio = "+" + tel_limpio
        else:
            tel_limpio = "+58" + tel_limpio.lstrip("0")
    return tel_limpio

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
tasa_en_red = obtener_tasa_bcv_auto()

if tasa_en_red:
    st.session_state.tasa_bcv = tasa_en_red
else:
    st.session_state.tasa_bcv = config_cargada.get("tasa_bcv", 36.50)

# CREDENCIALES Y ROLES DE USUARIOS
USUARIOS = {
    "Admin": {"clave": "1234", "rol": "admin"},
    "Jonder": {"clave": "barbero1", "rol": "barbero"}
}

PRECIOS_CORTES = {
    "Corte Clásico": 8.0,
    "Corte y Barba": 12.0,
    "Barba Completa": 5.0,
    "Combo (Corte + Barba+ Mascarilla)": 13.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Francisco", "Jonder", "Barbero 3"]
METODOS_PAGO = ["EFECTIVO", "PAGO MOVIL", "BINANCE"]

OPCIONES_HORAS = [
    time(h, m).strftime("%I:%M %p") 
    for h in range(8, 20) 
    for m in (0, 30)
]

# --- ESTILOS 4K ULTRA MODERNOS & LANDING VIP ---
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 50% -20%, #0c1a36 0%, #030712 60%, #010308 100%);
        color: #f8fafc;
    }

    .vip-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 240, 255, 0.08);
        border: 1px solid rgba(0, 240, 255, 0.3);
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 700;
        color: #00f0ff;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
        margin-bottom: 12px;
    }

    .vip-badge-dot {
        width: 8px;
        height: 8px;
        background-color: #00f0ff;
        border-radius: 50%;
        box-shadow: 0 0 10px #00f0ff;
        animation: pulse 1.8s infinite ease-in-out;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.7; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.7; }
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 20%, #80f5ff 60%, #0072ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }

    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 35px;
    }

    .price-preview-card {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.08) 0%, rgba(0, 114, 255, 0.12) 100%);
        border: 1px dashed rgba(0, 240, 255, 0.4);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00f0ff 0%, #0066cc 100%) !important;
        color: #030712 !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-radius: 16px !important;
        border: none !important;
        width: 100%;
        padding: 16px 28px !important;
        box-shadow: 0 12px 30px rgba(0, 240, 255, 0.35);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        box-shadow: 0 18px 40px rgba(0, 240, 255, 0.6);
        transform: translateY(-3px);
    }

    .btn-ws-glow {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        text-decoration: none;
        border-radius: 16px !important;
        padding: 16px 28px;
        font-weight: 800;
        font-size: 15px;
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.4);
    }

    [data-testid="stSidebar"] {
        background: rgba(4, 9, 20, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 240, 255, 0.15) !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: rgba(15, 23, 42, 0.6) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    [data-testid="stSidebar"] .stRadio div[aria-checked="true"] + label {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.2) 0%, rgba(0, 114, 255, 0.3) 100%) !important;
        color: #00f0ff !important;
        border: 1px solid rgba(0, 240, 255, 0.6) !important;
    }

    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid rgba(0, 240, 255, 0.2);
        padding-bottom: 12px;
        margin-bottom: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: INICIO CLIENTES 4K VIP LANDING + ACCESO PERSONAL
# ---------------------------------------------------------
if not st.session_state.autenticado:
    col_nav_left, col_nav_right = st.columns([4, 1.3])
    
    with col_nav_right:
        with st.popover("🔑 Acceso Personal / Barberos", use_container_width=True):
            st.markdown("<h4 style='text-align: center; color: #ffffff; margin-bottom: 12px; font-size: 18px;'>PORTAL ADMINISTRATIVO</h4>", unsafe_allow_html=True)
            with st.form("login_form_popover"):
                usuario = st.text_input("Usuario", placeholder="Tu usuario asignado")
                contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")
                submit = st.form_submit_button("INICIAR SESIÓN")

                if submit:
                    if usuario in USUARIOS and USUARIOS[usuario]["clave"] == contrasena:
                        st.session_state.autenticado = True
                        st.session_state.usuario_actual = usuario
                        st.rerun()
                    else:
                        st.error("Credenciales de acceso incorrectas")

    st.markdown(f'''
        <div style="text-align: center; padding: 10px 0 0 0;">
            <div class="vip-badge">
                <span class="vip-badge-dot"></span> TASA BCV ACTUAL: {st.session_state.tasa_bcv:.2f} BS
            </div>
            <div class="hero-title">GOD'S TIME BARBERIA</div>
            <div class="hero-subtitle">⚡ El corte perfecto en el momento exacto. Agenda tu turno sin esperas. ⚡</div>
        </div>
    ''', unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns([1, 2.4, 1])
    with col_c2:
        with st.form("form_cita_login"):
            st.markdown("<h3 style='text-align: center; color: #ffffff; margin-bottom: 20px; font-weight: 700;'><i class='fa-regular fa-calendar-check' style='color:#00f0ff;'></i> Reserva Tu Cita Online</h3>", unsafe_allow_html=True)
            
            nombre_c = st.text_input("Nombre Completo", placeholder="Ej: Francisco Hurtado")
            telefono_c = st.text_input("Número de Teléfono WhatsApp", placeholder="Ej: 04121234567")
            barbero_c = st.selectbox("Barbero de Preferencia", BARBEROS, key="barbero_cita_login")
            
            col_f1, col_h1 = st.columns(2)
            with col_f1:
                fecha_c = st.date_input("Fecha de la Cita", min_value=date.today(), key="fecha_cita_login")
            with col_h1:
                hora_c = st.selectbox("Hora Preferida", OPCIONES_HORAS, key="hora_cita_login")

            servicio_c = st.selectbox("Servicio Solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita_login")
            
            precio_est_usd = PRECIOS_CORTES[servicio_c]
            
            st.markdown(f'''
                <div class="price-preview-card">
                    <span style="color: #94a3b8; font-size: 13px; font-weight: 600;">VALOR DEL SERVICIO:</span><br>
                    <b style="color: #00f0ff; font-size: 26px;">${precio_est_usd:.2f} USD</b>
                </div>
            ''', unsafe_allow_html=True)

            btn_agendar_login = st.form_submit_button("CONFIRMAR Y AGENDAR CITA")

        if btn_agendar_login:
            if nombre_c and telefono_c:
                tel_final = limpiar_telefono(telefono_c)
                cita = {
                    "Cliente": nombre_c,
                    "Teléfono": tel_final,
                    "Barbero": barbero_c,
                    "Fecha": str(fecha_c),
                    "Hora": hora_c,
                    "Servicio": servicio_c
                }
                st.session_state.citas_db.append(cita)
                guardar_datos(CITAS_FILE, st.session_state.citas_db)
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en GOD'S TIME BARBERIA el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_est_usd:.2f})."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = tel_final.replace("+", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                
                st.success("¡Cita reservada con éxito!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-glow" style="margin-top: 15px;">
                        <i class="fa-brands fa-whatsapp" style="font-size: 20px;"></i> Confirmar Cita por WhatsApp
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.error("Por favor completa tu nombre y número de teléfono.")

# ---------------------------------------------------------
# VISTA 2: DASHBOARD PRINCIPAL 4K
# ---------------------------------------------------------
else:
    user_info = USUARIOS.get(st.session_state.usuario_actual, {"rol": "invitado"})
    es_admin = user_info["rol"] == "admin"

    with st.sidebar:
        st.markdown('''
            <div style="text-align: center; padding: 15px 0;">
                <div style="font-family: 'Outfit'; font-size: 22px; font-weight: 900; color: #00f0ff;">GOD'S TIME</div>
                <p style='color: #94a3b8; font-size: 12px; margin-top: 4px;'>Panel de Control 4K</p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f"<div style='background: rgba(0,240,255,0.08); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid rgba(0,240,255,0.2); margin-bottom: 15px;'><span style='font-size: 13px; color: #cbd5e1;'>Barbero Activo:</span><br><b style='color:#00f0ff; font-size: 15px;'>{st.session_state.usuario_actual}</b></div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 12px; color: #00f0ff; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px;'>MENÚ DE NAVEGACIÓN</p>", unsafe_allow_html=True)

        opciones_menu = {
            "📊 Panel General": "Panel General",
            "✂️ Registrar Corte": "Registrar Corte",
            "💈 Historial Barberos": "Historial Barberos",
            "📅 Citas y WhatsApp": "Citas y WhatsApp",
            "⚙️ Administración": "Administración"
        }
        
        seleccion_label = st.radio(
            label="", 
            options=list(opciones_menu.keys()),
            label_visibility="collapsed"
        )
        
        opcion_menu = opciones_menu[seleccion_label]
        
        st.markdown("---")
        
        st.markdown(f"<p style='font-size: 12px; color: #00f0ff; font-weight: 800; letter-spacing: 1px; margin-bottom: 8px;'>💵 TASA BCV (Auto): <b>{st.session_state.tasa_bcv:.2f} BS</b></p>", unsafe_allow_html=True)
        nueva_tasa_input = st.number_input("Tasa BS", value=float(st.session_state.tasa_bcv), step=0.10, label_visibility="collapsed")
        if st.button("FORZAR O CAMBIAR TASA"):
            st.session_state.tasa_bcv = nueva_tasa_input
            guardar_datos(CONFIG_FILE, {"tasa_bcv": nueva_tasa_input})
            st.success(f"Tasa fijada manualmente: {nueva_tasa_input:.2f} BS")
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.rerun()

    # 1. PANEL GENERAL
    if opcion_menu == "Panel General":
        st.markdown('<div class="section-header"><i class="fa-solid fa-chart-pie" style="color: #00f0ff;"></i> PANEL GENERAL - DASHBOARD 4K</div>', unsafe_allow_html=True)
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos_usd = df_cortes["Precio ($)"].sum() if (not df_cortes.empty and "Precio ($)" in df_cortes.columns) else 0.0
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'''
                <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; text-align: center; padding: 20px;">
                    <div style="color: #94a3b8; font-size: 14px; font-weight: 600; text-transform: uppercase;">Total Cortes Realizados</div>
                    <div style="font-size: 36px; font-weight: 800; color: #00f0ff; margin-top: 8px;">{total_cortes}</div>
                </div>
            ''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''
                <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; text-align: center; padding: 20px;">
                    <div style="color: #94a3b8; font-size: 14px; font-weight: 600; text-transform: uppercase;">Ingresos Totales</div>
                    <div style="font-size: 32px; font-weight: 800; color: #10b981; margin-top: 8px;">${total_ingresos_usd:.2f}</div>
                </div>
            ''', unsafe_allow_html=True)
        with c3:
            st.markdown(f'''
                <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; text-align: center; padding: 20px;">
                    <div style="color: #94a3b8; font-size: 14px; font-weight: 600; text-transform: uppercase;">Citas Agendadas</div>
                    <div style="font-size: 36px; font-weight: 800; color: #f59e0b; margin-top: 8px;">{citas_pendientes}</div>
                </div>
            ''', unsafe_allow_html=True)

        if not df_cortes.empty:
            st.markdown('<div class="section-header" style="margin-top: 35px;"><i class="fa-solid fa-bolt" style="color: #00f0ff;"></i> ANALÍTICA DE RENDIMIENTO EN TIEMPO REAL</div>', unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                st.markdown("##### Ingresos por Barbero ($)")
                df_barberos = df_cortes.groupby("Barbero")["Precio ($)"].sum().reset_index()
                fig_barb = px.bar(
                    df_barberos, x="Barbero", y="Precio ($)", 
                    text_auto='.2f', color="Barbero",
                    color_discrete_sequence=['#00f0ff', '#3b82f6', '#8b5cf6', '#ec4899']
                )
                fig_barb.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#f8fafc', margin=dict(t=20, b=20, l=20, r=20),
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                )
                st.plotly_chart(fig_barb, use_container_width=True)

            with col_g2:
                st.markdown("##### Distribución por Método de Pago")
                df_pagos = df_cortes.groupby("Método Pago")["Precio ($)"].sum().reset_index()
                fig_pagos = px.pie(
                    df_pagos, names="Método Pago", values="Precio ($)", 
                    hole=0.45, color_discrete_sequence=['#10b981', '#3b82f6', '#f59e0b', '#ec4899']
                )
                fig_pagos.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#f8fafc', margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_pagos, use_container_width=True)

            st.markdown("##### Ingresos por Tipo de Servicio ($)")
            df_servicios = df_cortes.groupby("Servicio")["Precio ($)"].sum().reset_index()
            fig_serv = px.bar(
                df_servicios, x="Servicio", y="Precio ($)", 
                text_auto='.2f', color="Servicio",
                color_discrete_sequence=['#00f0ff', '#10b981', '#f59e0b', '#8b5cf6']
            )
            fig_serv.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#f8fafc', showlegend=False, margin=dict(t=20, b=20, l=20, r=20),
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig_serv, use_container_width=True)

        st.markdown('<div class="section-header" style="margin-top: 35px;"><i class="fa-solid fa-tags" style="color: #00f0ff;"></i> TARIFA OFICIAL DE SERVICIOS</div>', unsafe_allow_html=True)
        precios_tabla = [
            {"Servicio / Corte": k, "Precio ($)": f"${v:.2f}"}
            for k, v in PRECIOS_CORTES.items()
        ]
        st.table(pd.DataFrame(precios_tabla))

    # 2. REGISTRAR CORTE
    elif opcion_menu == "Registrar Corte":
        st.markdown('<div class="section-header"><i class="fa-solid fa-scissors" style="color: #00f0ff;"></i> REGISTRO DE NUEVO CORTE</div>', unsafe_allow_html=True)
        with st.form("form_corte"):
            col1, col2 = st.columns(2)
            with col1:
                idx_barbero = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
                barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS, index=idx_barbero)
                corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
                precio_corte_usd = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
                cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            
            with col2:
                metodo_pago = st.selectbox("Método de Pago", METODOS_PAGO)
                referencia_pago = st.text_input("N° de Referencia / Transacción", placeholder="N/A para Efectivo")

            btn_guardar = st.form_submit_button("GUARDAR CORTE Y REGISTRAR EN SISTEMA")
            
            if btn_guardar:
                ref_final = referencia_pago.strip() if referencia_pago.strip() else ("N/A" if metodo_pago == "EFECTIVO" else "Sin ref.")
                
                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
                    "Barbero": barbero_sel,
                    "Servicio": corte_sel,
                    "Precio ($)": precio_corte_usd,
                    "Método Pago": metodo_pago,
                    "Referencia": ref_final,
                    "Cliente": cliente_nombre.strip() if cliente_nombre.strip() else "Cliente Ocasional"
                }
                st.session_state.cortes_db.append(nuevo_registro)
                guardar_datos(CORTES_FILE, st.session_state.cortes_db)
                st.success(f"¡Corte registrado exitosamente a {barbero_sel} (${precio_corte_usd:.2f}) vía {metodo_pago}!")

    # 3. HISTORIAL Y REGISTRO DE CLIENTES POR BARBERO
    elif opcion_menu == "Historial Barberos":
        st.markdown('<div class="section-header"><i class="fa-solid fa-users-viewfinder" style="color: #00f0ff;"></i> HISTORIAL Y GESTIÓN DE CLIENTES</div>', unsafe_allow_html=True)
        idx_filtro = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
        barbero_filtro = st.selectbox("Selecciona un Barbero", BARBEROS, index=idx_filtro, key="filtro_barbero")
        
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            
            if not df_filtrado.empty:
                col_precio = "Precio ($)" if "Precio ($)" in df_filtrado.columns else "Precio"
                total_usd = df_filtrado[col_precio].sum()
                st.info(f"Rendimiento de **{barbero_filtro}**: **${total_usd:.2f} USD** ({len(df_filtrado)} servicios prestados)")

                tab_hist, tab_cli = st.tabs(["📋 HISTORIAL DE CORTES", "👥 CLIENTES ATENDIDOS"])
                
                with tab_hist:
                    st.dataframe(df_filtrado, use_container_width=True)
                
                with tab_cli:
                    st.markdown(f"### Base de Datos de Clientes - {barbero_filtro}")
                    df_clientes = df_filtrado.groupby("Cliente").agg(
                        Visitas=("Servicio", "count"),
                        Total_Gastado_USD=(col_precio, "sum"),
                        Ultima_Visita=("Fecha", "max")
                    ).reset_index()
                    st.dataframe(df_clientes, use_container_width=True)
            else:
                st.warning(f"No hay registros de cortes para {barbero_filtro} todavía.")
        else:
            st.write("No hay datos de cortes registrados en la base de datos.")

    # 4. CITAS Y WHATSAPP
    elif opcion_menu == "Citas y WhatsApp":
        st.markdown('<div class="section-header"><i class="fa-regular fa-calendar-days" style="color: #00f0ff;"></i> GESTIÓN DE CITAS Y WHATSAPP</div>', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            telefono_c = st.text_input("Teléfono (Ej: 04121234567 o +584121234567)")
            barbero_c = st.selectbox("Barbero de Preferencia", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha de la Cita", min_value=date.today())
            hora_c = st.selectbox("Hora de la Cita", OPCIONES_HORAS, key="hora_cita_admin")
            servicio_c = st.selectbox("Servicio Solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("REGISTRAR CITA Y ENVIAR RECORDATORIO"):
            if nombre_c and telefono_c:
                tel_final = limpiar_telefono(telefono_c)
                cita = {
                    "Cliente": nombre_c,
                    "Teléfono": tel_final,
                    "Barbero": barbero_c,
                    "Fecha": str(fecha_c),
                    "Hora": hora_c,
                    "Servicio": servicio_c
                }
                st.session_state.citas_db.append(cita)
                guardar_datos(CITAS_FILE, st.session_state.citas_db)
                
                precio_usd = PRECIOS_CORTES[servicio_c]
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en GOD'S TIME BARBERIA el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f})."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = tel_final.replace("+", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                st.success("¡Cita agendada correctamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-glow" style="margin-top: 15px;">
                        <i class="fa-brands fa-whatsapp" style="font-size: 20px;"></i> Enviar Confirmación por WhatsApp
                    </a>
                ''', unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:35px;">CITAS PROGRAMADAS EN AGENDA</div>', unsafe_allow_html=True)
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. ADMINISTRACIÓN
    elif opcion_menu == "Administración":
        st.markdown('<div class="section-header"><i class="fa-solid fa-shield-halved" style="color: #00f0ff;"></i> PANEL DE ADMINISTRACIÓN</div>', unsafe_allow_html=True)
        
        if es_admin:
            st.warning("⚠️ **Zona de Peligro:** La siguiente acción eliminará permanentemente todos los registros de cortes y citas guardadas en el sistema.")
            if st.button("REINICIAR TODO EL HISTORIAL DE LA BARBERÍA"):
                st.session_state.cortes_db = []
                st.session_state.citas_db = []
                guardar_datos(CORTES_FILE, [])
                guardar_datos(CITAS_FILE, [])
                st.success("El historial completo ha sido reiniciado con éxito.")
                st.rerun()
        else:
            st.error("🔒 **Acceso Restringido:** Esta sección requiere permisos de Administrador.")
