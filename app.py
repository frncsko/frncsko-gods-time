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
VISITAS_FILE = "visitas_data.json"
CALIFICACIONES_FILE = "calificaciones_data.json"

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

if "visitas_db" not in st.session_state:
    total_visitas = cargar_datos(VISITAS_FILE, 0) + 1
    st.session_state.visitas_db = total_visitas
    guardar_datos(VISITAS_FILE, total_visitas)

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "cortes_db" not in st.session_state:
    st.session_state.cortes_db = cargar_datos(CORTES_FILE, [])
if "citas_db" not in st.session_state:
    st.session_state.citas_db = cargar_datos(CITAS_FILE, [])
if "calificaciones_db" not in st.session_state:
    st.session_state.calificaciones_db = cargar_datos(CALIFICACIONES_FILE, [])

PRECIOS_CORTES = {
    "Corte Clásico": 10.0,
    "Degradado / Fade": 12.0,
    "Barba Completa": 8.0,
    "Combo (Corte + Barba)": 18.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Barbero 1", "Barbero 2", "Barbero 3"]

# ESTILOS CON RAYOS REALISTAS, GOKU MEJORADO Y CRÉDITO REUBICADO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1b2a 0%, #050811 100%);
        color: #e2e8f0;
        overflow-x: hidden;
    }

    /* RAYOS ELÉCTRICOS REALISTAS */
    .lightning-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }

    .real-lightning {
        position: absolute;
        top: -10px;
        width: 4px;
        height: 100vh;
        background: #ffffff;
        box-shadow: 0 0 10px #00f0ff, 0 0 25px #00f0ff, 0 0 50px #7000ff;
        opacity: 0;
        clip-path: polygon(50% 0%, 0% 20%, 70% 35%, 10% 60%, 80% 75%, 30% 100%, 60% 100%, 90% 73%, 20% 58%, 80% 33%, 20% 18%);
        animation: lightningStrike 5s infinite ease-in-out;
    }

    .rl1 { left: 15%; animation-delay: 0.8s; }
    .rl2 { left: 82%; animation-delay: 2.7s; }
    .rl3 { left: 48%; animation-delay: 4.2s; }

    @keyframes lightningStrike {
        0%, 94%, 100% { opacity: 0; }
        95% { opacity: 1; filter: drop-shadow(0 0 20px #00f0ff); }
        96% { opacity: 0.2; }
        97% { opacity: 1; filter: drop-shadow(0 0 30px #ffffff); }
        98% { opacity: 0; }
    }

    /* FIRMA EN LA ESQUINA SUPERIOR IZQUIERDA */
    .dev-badge-top {
        position: fixed;
        top: 15px;
        left: 15px;
        background: rgba(10, 16, 30, 0.85);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 240, 255, 0.5);
        border-radius: 12px;
        padding: 6px 14px;
        color: #00f0ff;
        font-size: 11px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(0, 240, 255, 0.3);
        z-index: 99999;
    }

    /* CABECERA CON GOKU */
    .header-dbz {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 10px;
    }

    .goku-img {
        width: 75px;
        height: auto;
        object-fit: contain;
        filter: drop-shadow(0 0 12px rgba(0, 240, 255, 0.8));
        animation: floatGoku 3s infinite ease-in-out;
    }

    @keyframes floatGoku {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .title-electric {
        font-size: 30px;
        font-weight: 800;
        color: #00f0ff !important;
        text-align: center;
        letter-spacing: 1px;
        text-shadow: 0 0 15px #00f0ff, 0 0 30px #7000ff;
    }

    h1, h2, h3 {
        color: #00f0ff !important;
        font-weight: 800 !important;
    }

    div[data-baseweb="tab-list"] {
        background: rgba(13, 27, 42, 0.6) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 18px !important;
        padding: 6px !important;
        gap: 8px !important;
    }

    button[data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    button[aria-selected="true"] {
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 20px rgba(0, 240, 255, 0.4) !important;
    }

    .card-3d, [data-testid="stForm"] {
        background: rgba(10, 16, 30, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(0, 240, 255, 0.18);
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
    }
    </style>

    <div class="lightning-container">
        <div class="real-lightning rl1"></div>
        <div class="real-lightning rl2"></div>
        <div class="real-lightning rl3"></div>
    </div>

    <div class="dev-badge-top">⚡ Dev: FranciscoBRB</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: LOGIN
# ---------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('''
            <div class="header-dbz">
                <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnYydm5rdzBrbzFoc2lpaW13dGoxcnBscDliNnVraWVvdmsyYzFnZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/u00R4eeSj7K80/giphy.gif" class="goku-img" alt="Goku DBZ">
                <div class="title-electric">BARBERÍA GOD\'S TIME</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-weight: 600;'>Excelencia, estilo y precisión en cada detalle</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: #ffffff;'>⚡ ACCESO AL SISTEMA</h3>", unsafe_allow_html=True)
            usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")
            submit = st.form_submit_button("ENTRAR AL SISTEMA")

        if submit:
            if usuario == "admin" and contrasena == "1234":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

# ---------------------------------------------------------
# VISTA 2: PANEL PRINCIPAL
# ---------------------------------------------------------
else:
    col_t, col_l = st.columns([4, 1])
    with col_t:
        st.markdown('''
            <div class="header-dbz" style="justify-content: flex-start;">
                <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnYydm5rdzBrbzFoc2lpaW13dGoxcnBscDliNnVraWVvdmsyYzFnZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/u00R4eeSj7K80/giphy.gif" class="goku-img" style="width:55px;" alt="Goku DBZ">
                <div class="title-electric" style="font-size:24px;">BARBERÍA GOD\'S TIME</div>
            </div>
        ''', unsafe_allow_html=True)
    with col_l:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.autenticado = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    tab_inicio, tab_cortes, tab_barberos, tab_citas, tab_feedback, tab_admin = st.tabs([
        "🏠 PANEL PRINCIPAL", 
        "✂️ REGISTRAR CORTE", 
        "💈 REGISTRO BARBEROS", 
        "📅 CITAS & WHATSAPP",
        "⭐ CALIFICAR APP",
        "⚙️ ADMINISTRACIÓN"
    ])

    # 1. PANEL PRINCIPAL
    with tab_inicio:
        st.markdown("### 📊 Métricas Operativas y Visitas")
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3, c4 = st.columns(4)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos = df_cortes["Precio"].sum() if not df_cortes.empty else 0.0
        citas_pendientes = len(st.session_state.citas_db)
        total_visitas = st.session_state.visitas_db

        with c1:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Total Cortes</h4><h2 style="margin:5px 0 0 0;">{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Ingresos Totales</h4><h2 style="margin:5px 0 0 0;">${total_ingresos:.2f}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">Citas Agendadas</h4><h2 style="margin:5px 0 0 0;">{citas_pendientes}</h2></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="card-3d"><h4 style="color:#94a3b8; margin:0;">👁️ Visitas Recibidas</h4><h2 style="margin:5px 0 0 0;">{total_visitas}</h2></div>', unsafe_allow_html=True)

        st.markdown("### 💵 Lista de Servicios y Precios")
        precios_df = pd.DataFrame(list(PRECIOS_CORTES.items()), columns=["Servicio / Corte", "Precio ($)"])
        st.table(precios_df)

    # 2. REGISTRAR CORTE
    with tab_cortes:
        st.markdown("### ✂️ Registrar Nuevo Corte")
        with st.form("form_corte"):
            barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS)
            corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
            precio_corte = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
            cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            btn_guardar = st.form_submit_button("GUARDAR CORTE")
            
            if btn_guardar:
                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Barbero": barbero_sel,
                    "Servicio": corte_sel,
                    "Precio": precio_corte,
                    "Cliente": cliente_nombre if cliente_nombre else "Cliente Ocasional"
                }
                st.session_state.cortes_db.append(nuevo_registro)
                guardar_datos(CORTES_FILE, st.session_state.cortes_db)
                st.success(f"Corte registrado a {barbero_sel} correctamente.")

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
        st.markdown("### 📅 Agendar Nueva Cita")
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
                st.markdown(f'<a href="{ws_url}" target="_blank" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color:white; border:none; padding:14px; border-radius:14px; font-weight:bold; cursor:pointer; width:100%;">📲 Enviar Confirmación por WhatsApp</button></a>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Citas Registradas")
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. CALIFICAR LA APP
    with tab_feedback:
        st.markdown("### ⭐ Califica la Aplicación")
        with st.form("form_rating"):
            puntuacion = st.select_slider("¿Qué tan satisfecho estás con el sistema?", options=["1 ⭐", "2 ⭐⭐", "3 ⭐⭐⭐", "4 ⭐⭐⭐⭐", "5 ⭐⭐⭐⭐⭐"], value="5 ⭐⭐⭐⭐⭐")
            comentario = st.text_area("Deja tu sugerencia o comentario")
            btn_calificar = st.form_submit_button("ENVIAR CALIFICACIÓN")
            
            if btn_calificar:
                nueva_calificacion = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Puntuación": puntuacion,
                    "Comentario": comentario if comentario else "Sin comentario"
                }
                st.session_state.calificaciones_db.append(nueva_calificacion)
                guardar_datos(CALIFICACIONES_FILE, st.session_state.calificaciones_db)
                st.success("¡Gracias por tu calificación!")

        st.markdown("---")
        st.markdown("### 💬 Opiniones Recibidas")
        if st.session_state.calificaciones_db:
            st.dataframe(pd.DataFrame(st.session_state.calificaciones_db), use_container_width=True)
        else:
            st.write("Aún no hay calificaciones registradas.")

    # 6. ADMINISTRACIÓN
    with tab_admin:
        st.markdown("### ⚙️ Panel de Control del Administrador")
        st.warning("⚠️ **Atención:** La siguiente opción borrará permanentemente las citas, cortes y opiniones.")
        if st.button("🔴 REINICIAR TODO EL HISTORIAL"):
            st.session_state.cortes_db = []
            st.session_state.citas_db = []
            st.session_state.calificaciones_db = []
            guardar_datos(CORTES_FILE, [])
            guardar_datos(CITAS_FILE, [])
            guardar_datos(CALIFICACIONES_FILE, [])
            st.success("El historial completo ha sido borrado.")
            st.rerun()
