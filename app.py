import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import urllib.parse
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="Test Barberia - Ultra 4K", 
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
    "Admin": {"clave": "1234", "rol": "admin"},
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

# GENERADOR DE OPCIONES DE HORAS (AM / PM)
OPCIONES_HORAS = [
    time(h, m).strftime("%I:%M %p") 
    for h in range(8, 20) 
    for m in (0, 30)
]

# ESTILOS ULTRA 4K / CYBERPUNK GLOW
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    /* Fondo Ultra 4K con gradiente espacial y animación suave */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #0d1117 0%, #05070a 60%, #000000 100%);
        font-family: 'Rajdhani', sans-serif;
        color: #f0f6fc;
    }

    /* BARRA LATERAL ESTILO GLASSMORPHISM */
    [data-testid="stSidebar"] {
        background: rgba(13, 17, 23, 0.75) !important;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid rgba(0, 240, 255, 0.25) !important;
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.8);
    }

    /* MENÚ OVALADO CON EFECTO NEÓN Y GLOW 4K */
    [data-testid="stSidebar"] .stRadio label {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.1) 0%, rgba(0, 114, 255, 0.2) 100%) !important;
        border-radius: 30px !important;
        padding: 12px 20px !important;
        color: #ffffff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 13px !important;
        letter-spacing: 1.5px !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5), inset 0 0 10px rgba(0, 240, 255, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        transform: translateY(-2px) scale(1.02);
        border-color: #00f0ff !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.6), inset 0 0 15px rgba(0, 240, 255, 0.3) !important;
    }

    [data-testid="stSidebar"] .stRadio div[aria-checked="true"] + label {
        background: linear-gradient(135deg, #00f0ff 0%, #0055ff 100%) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border: 1px solid #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.9), 0 0 50px rgba(0, 114, 255, 0.5) !important;
    }

    /* TARJETAS VIP DE VIDRIO 4K */
    .card-4k {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .card-4k:hover {
        border-color: rgba(0, 240, 255, 0.4);
        box-shadow: 0 20px 50px rgba(0, 240, 255, 0.15);
    }

    /* BOTONES STREAMLIT ULTRA GLOW */
    .stButton > button {
        background: linear-gradient(135deg, #00f0ff 0%, #0066ff 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        letter-spacing: 1px;
        border-radius: 50px !important;
        border: none !important;
        padding: 12px 28px !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.8) !important;
        color: #fff !important;
    }

    /* BOTÓN WHATSAPP NEÓN */
    .btn-ws-4k {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%) !important;
        color: #000000 !important;
        font-family: 'Orbitron', sans-serif;
        text-decoration: none;
        border-radius: 50px;
        padding: 14px 28px;
        font-weight: 900;
        font-size: 14px;
        letter-spacing: 1px;
        box-shadow: 0 0 25px rgba(0, 255, 135, 0.5);
        transition: all 0.3s ease;
    }

    .btn-ws-4k:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 40px rgba(0, 255, 135, 0.9);
        color: #000000 !important;
    }

    /* TÍTULO HOLOGRAMA 4K */
    .title-4k {
        font-family: 'Orbitron', sans-serif;
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(180deg, #ffffff 0%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 240, 255, 0.5);
        text-align: center;
        letter-spacing: 4px;
    }

    .section-header-4k {
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #00f0ff;
        letter-spacing: 2px;
        border-bottom: 2px solid rgba(0, 240, 255, 0.3);
        padding-bottom: 8px;
        margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: INICIO CLIENTES
# ---------------------------------------------------------
if not st.session_state.autenticado:
    col_header, col_login_btn = st.columns([5, 1.2])
    
    with col_login_btn:
        with st.popover("Acceso Personal 🔐", use_container_width=True):
            st.markdown("<h4 style='text-align: center; color: #ffffff;'>ACCESO PERSONAL</h4>", unsafe_allow_html=True)
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
        <div style="text-align: center; margin-top: -10px;">
            <div class="title-4k">TEST BARBERIA</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #8b949e; font-weight: 600; font-size: 18px; margin-top: 5px; margin-bottom: 30px;'>EXPERIENCIA VIP & CORTE DE ALTA PRECISIÓN</p>", unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown('<div class="card-4k">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #00f0ff; font-family: Orbitron;'>RESERVA TU CITA</h3>", unsafe_allow_html=True)
        with st.form("form_cita_login"):
            nombre_c = st.text_input("Nombre Completo")
            
            # AUTOMÁTICO +58
            col_pref, col_tel = st.columns([1, 3])
            with col_pref:
                prefijo = st.text_input("Código", value="+58", disabled=True)
            with col_tel:
                num_tel = st.text_input("Teléfono WhatsApp", placeholder="4121234567")
            
            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita_login")
            
            col_f1, col_h1 = st.columns(2)
            with col_f1:
                fecha_c = st.date_input("Fecha", min_value=date.today(), key="fecha_cita_login")
            with col_h1:
                hora_c = st.selectbox("Hora", OPCIONES_HORAS, key="hora_cita_login")

            servicio_c = st.selectbox("Servicio", list(PRECIOS_CORTES.keys()), key="servicio_cita_login")
            
            btn_agendar_login = st.form_submit_button("AGENDAR CITA AHORA")

        if btn_agendar_login:
            if nombre_c and num_tel:
                telefono_c = f"+58{num_tel.strip().lstrip('0')}"
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
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Test Barberia el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-4k">
                        CONFIRMAR POR WHATSAPP
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.error("Por favor ingresa tu nombre y número telefónico.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 2: PANEL PRINCIPAL
# ---------------------------------------------------------
else:
    user_info = USUARIOS.get(st.session_state.usuario_actual, {"rol": "invitado"})
    es_admin = user_info["rol"] == "admin"

    with st.sidebar:
        st.markdown('''
            <div style="text-align: center; padding: 10px 0;">
                <div class="title-4k" style="font-size: 22px;">TEST BARBERIA</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #8b949e; font-size: 13px;'>Barbero: <b style='color:#00f0ff;'>{st.session_state.usuario_actual}</b></p>", unsafe_allow_html=True)
        st.markdown("---")
        
        opciones_menu = {
            "📊  Panel General": "Panel General",
            "✂️  Registrar Corte": "Registrar Corte",
            "💈  Historial Barberos": "Historial Barberos",
            "📅  Citas y WhatsApp": "Citas y WhatsApp",
            "⚙️  Administración": "Administración"
        }
        
        seleccion_label = st.radio(
            label="", 
            options=list(opciones_menu.keys()),
            label_visibility="collapsed"
        )
        
        opcion_menu = opciones_menu[seleccion_label]
        
        st.markdown("---")
        
        st.markdown("<p style='font-size: 12px; color: #00f0ff; font-family: Orbitron;'>💵 TASA BCV ($)</p>", unsafe_allow_html=True)
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
        st.markdown('<div class="section-header-4k">📊 PANEL GENERAL</div>', unsafe_allow_html=True)
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos_usd = df_cortes["Precio ($)"].sum() if (not df_cortes.empty and "Precio ($)" in df_cortes.columns) else (df_cortes["Precio"].sum() if not df_cortes.empty else 0.0)
        total_ingresos_bs = total_ingresos_usd * st.session_state.tasa_bcv
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="card-4k"><h4 style="color:#8b949e; margin:0; font-family:Orbitron;">TOTAL CORTES</h4><h1 style="margin:5px 0 0 0; color:#00f0ff;">{total_cortes}</h1></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-4k"><h4 style="color:#8b949e; margin:0; font-family:Orbitron;">INGRESOS TOTALES</h4><h2 style="margin:5px 0 0 0; color:#00ff87;">${total_ingresos_usd:.2f} <span style="font-size:16px; color:#ffffff;">({total_ingresos_bs:.2f} BS)</span></h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-4k"><h4 style="color:#8b949e; margin:0; font-family:Orbitron;">CITAS AGENDADAS</h4><h1 style="margin:5px 0 0 0; color:#00f0ff;">{citas_pendientes}</h1></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header-4k" style="margin-top: 30px;">💵 TARIFA DE SERVICIOS</div>', unsafe_allow_html=True)
        precios_tabla = [
            {"Servicio / Corte": k, "Precio ($)": f"${v:.2f}", "Precio (BS)": f"{v * st.session_state.tasa_bcv:.2f} BS"}
            for k, v in PRECIOS_CORTES.items()
        ]
        st.table(pd.DataFrame(precios_tabla))

    # 2. REGISTRAR CORTE
    elif opcion_menu == "Registrar Corte":
        st.markdown('<div class="section-header-4k">✂️ REGISTRO DE NUEVO CORTE</div>', unsafe_allow_html=True)
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

    # 3. HISTORIAL
    elif opcion_menu == "Historial Barberos":
        st.markdown('<div class="section-header-4k">💈 HISTORIAL Y REGISTRO POR BARBERO</div>', unsafe_allow_html=True)
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
            st.write("No hay datos registrados aún.")

    # 4. CITAS Y WHATSAPP
    elif opcion_menu == "Citas y WhatsApp":
        st.markdown('<div class="section-header-4k">📅 GESTIÓN DE CITAS Y WHATSAPP</div>', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            
            # AUTOMÁTICO +58 EN PANEL DE ADMIN
            col_pref_a, col_tel_a = st.columns([1, 3])
            with col_pref_a:
                st.text_input("Código", value="+58", disabled=True, key="pref_admin")
            with col_tel_a:
                num_tel_admin = st.text_input("Teléfono WhatsApp", placeholder="4121234567", key="tel_admin")

            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha de la cita", min_value=date.today())
            hora_c = st.selectbox("Hora de la cita", OPCIONES_HORAS, key="hora_cita_admin")
            servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("REGISTRAR CITA Y CONFIRMAR POR WHATSAPP"):
            if nombre_c and num_tel_admin:
                telefono_c = f"+58{num_tel_admin.strip().lstrip('0')}"
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
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Test Barberia el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-4k">
                        ENVIAR CONFIRMACIÓN POR WHATSAPP
                    </a>
                ''', unsafe_allow_html=True)

        st.markdown('<div class="section-header-4k" style="margin-top:30px;">CITAS REGISTRADAS</div>', unsafe_allow_html=True)
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. ADMINISTRACIÓN
    elif opcion_menu == "Administración":
        st.markdown('<div class="section-header-4k">⚙️ PANEL DE ADMINISTRACIÓN</div>', unsafe_allow_html=True)
        
        if es_admin:
            st.warning("⚠️ **Atención:** Borrado permanente del historial de citas y cortes.")
            if st.button("REINICIAR HISTORIAL COMPLETO"):
                st.session_state.cortes_db = []
                st.session_state.citas_db = []
                guardar_datos(CORTES_FILE, [])
                guardar_datos(CITAS_FILE, [])
                st.success("El historial completo ha sido borrado.")
                st.rerun()
        else:
            st.error("🔒 **Acceso restringido:** Se requieren permisos de administrador.")
