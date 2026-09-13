import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Barbería God's Time", layout="wide", initial_sidebar_state="expanded")

# Inicialización del estado de la aplicación
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "cortes_db" not in st.session_state:
    st.session_state.cortes_db = []
if "citas_db" not in st.session_state:
    st.session_state.citas_db = []

PRECIOS_CORTES = {
    "Corte Clásico": 10.0,
    "Degradado / Fade": 12.0,
    "Barba Completa": 8.0,
    "Combo (Corte + Barba)": 18.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Barbero 1", "Barbero 2", "Barbero 3"]

# Estilos CSS Avanzados: Tipografía mejorada y Navegación 3D
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0b0e 0%, #161821 100%);
        color: #f1f1f1;
    }

    /* Estilización del Menú de Pestañas (Tabs) */
    button[data-baseweb="tab"] {
        background: #12141c !important;
        border-radius: 12px 12px 0px 0px !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        padding: 12px 20px !important;
        margin-right: 6px !important;
        color: #a0a5b5 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        box-shadow: inset 0px -3px 0px rgba(0,0,0,0.5) !important;
        transition: all 0.2s ease-in-out !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #d4af37 !important;
        background: #1a1d28 !important;
    }

    button[aria-selected="true"] {
        background: linear-gradient(180deg, #1f2330 0%, #14161d 100%) !important;
        color: #d4af37 !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #d4af37 !important;
        box-shadow: 0px -4px 10px rgba(212, 175, 55, 0.2) !important;
    }

    /* Encabezados y Letras Destacadas */
    h1, h2, h3 {
        color: #d4af37 !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
    }

    label {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Tarjetas 3D mejoradas */
    .card-3d {
        background: #14161d;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 8px 8px 18px rgba(0,0,0,0.7), -4px -4px 12px rgba(255,255,255,0.02);
        border: 1px solid rgba(212, 175, 55, 0.25);
    }

    /* Formulario 3D */
    [data-testid="stForm"] {
        background: #14161d;
        border-radius: 20px;
        padding: 30px 24px;
        box-shadow: 10px 10px 25px rgba(0, 0, 0, 0.8), -5px -5px 15px rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.3);
    }

    /* Botones 3D con mayor contraste */
    .stButton > button {
        background: linear-gradient(145deg, #f0cc52, #b89528);
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 12px;
        border: none;
        width: 100%;
        padding: 12px 18px;
        box-shadow: 0px 5px 0px #8a6f1c, 0px 8px 15px rgba(0, 0, 0, 0.5);
        letter-spacing: 0.5px;
    }

    .stButton > button:active {
        transform: translateY(3px);
        box-shadow: 0px 2px 0px #8a6f1c;
    }

    .title-3d {
        font-size: 32px;
        font-weight: 900;
        color: #d4af37;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9), 0 0 15px rgba(212, 175, 55, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: LOGIN
# ---------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="title-3d">BARBERÍA GOD\'S TIME</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a0a5b5; font-weight: 600;'>Excelencia, estilo y precisión en cada detalle</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: #ffffff;'>🔑 ACCESO AL SISTEMA</h3>", unsafe_allow_html=True)
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
        st.markdown('<h2 style="color: #d4af37; margin:0;">💈 BARBERÍA GOD\'S TIME</h2>', unsafe_allow_html=True)
    with col_l:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.autenticado = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Menú Principal de Pestañas Estilizado
    tab_inicio, tab_cortes, tab_barberos, tab_citas, tab_admin = st.tabs([
        "🏠 MENÚ PRINCIPAL", 
        "✂️ REGISTRAR CORTE", 
        "💈 REGISTRO BARBEROS", 
        "📅 CITAS Y WHATSAPP",
        "⚙️ ADMINISTRACIÓN"
    ])

    # 1. MENÚ PRINCIPAL
    with tab_inicio:
        st.markdown("### 📊 Resumen de Actividad")
        
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos = df_cortes["Precio"].sum() if not df_cortes.empty else 0.0
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="card-3d"><h4 style="color:#a0a5b5; margin:0;">Total Cortes</h4><h2 style="margin:5px 0 0 0;">{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h4 style="color:#a0a5b5; margin:0;">Ingresos Totales</h4><h2 style="margin:5px 0 0 0;">${total_ingresos:.2f}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h4 style="color:#a0a5b5; margin:0;">Citas Agendadas</h4><h2 style="margin:5px 0 0 0;">{citas_pendientes}</h2></div>', unsafe_allow_html=True)

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
                st.success(f"Corte registrado a {barbero_sel} con éxito.")

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
                st.warning(f"No hay registros de cortes para {barbero_filtro}.")
        else:
            st.write("No hay cortes registrados en la base de datos.")

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
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c}."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'<a href="{ws_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:10px; font-weight:bold; cursor:pointer; width:100%;">📲 Enviar Confirmación por WhatsApp</button></a>', unsafe_allow_html=True)
            else:
                st.error("Completa el nombre y número de teléfono.")

        st.markdown("---")
        st.markdown("### 📋 Citas Registradas")
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)
        else:
            st.write("No hay citas registradas.")

    # 5. ADMINISTRACIÓN
    with tab_admin:
        st.markdown("### ⚙️ Panel de Control del Administrador")
        st.warning("⚠️ **Atención:** La siguiente opción borrará permanentemente las citas y cortes guardados en esta sesión.")
        
        if st.button("🔴 REINICIAR TODO EL HISTORIAL"):
            st.session_state.cortes_db = []
            st.session_state.citas_db = []
            st.success("El historial completo ha sido reiniciado.")
            st.rerun()
