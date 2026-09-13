import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Barbería God's Time", layout="wide", initial_sidebar_state="expanded")

# Inicialización del estado de la aplicación (Base de Datos en Sesión)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "cortes_db" not in st.session_state:
    st.session_state.cortes_db = []
if "citas_db" not in st.session_state:
    st.session_state.citas_db = []

# Precios base predeterminados
PRECIOS_CORTES = {
    "Corte Clásico": 10.0,
    "Degradado / Fade": 12.0,
    "Barba Completa": 8.0,
    "Combo (Corte + Barba)": 18.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Barbero 1", "Barbero 2", "Barbero 3"]

# Estilos CSS Modernos en 3D
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d0e12 0%, #1a1c23 100%);
        color: #e0e0e0;
    }
    
    /* Formulario de Login 3D */
    [data-testid="stForm"] {
        background: #14161d;
        border-radius: 20px;
        padding: 30px 20px;
        box-shadow: 10px 10px 25px rgba(0, 0, 0, 0.7), -5px -5px 15px rgba(255, 255, 255, 0.03), inset 0px 1px 1px rgba(212, 175, 55, 0.3);
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* Tarjetas 3D para métricas y datos */
    .card-3d {
        background: #14161d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 6px 6px 12px rgba(0,0,0,0.6), -3px -3px 8px rgba(255,255,255,0.02);
        border: 1px solid rgba(212, 175, 55, 0.15);
    }
    
    /* Botones principales estilo 3D */
    .stButton > button {
        background: linear-gradient(145deg, #e6c247, #b89528);
        color: #000000;
        font-weight: 800;
        border-radius: 12px;
        border: none;
        width: 100%;
        padding: 10px 15px;
        box-shadow: 0px 5px 0px #8a6f1c, 0px 8px 12px rgba(0, 0, 0, 0.4);
        transition: all 0.1s ease-in-out;
    }
    .stButton > button:active {
        transform: translateY(3px);
        box-shadow: 0px 2px 0px #8a6f1c;
    }

    /* Entradas de texto 3D */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #0f1015 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #2a2d37 !important;
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.6) !important;
    }
    
    .title-3d {
        font-size: 28px;
        font-weight: 900;
        color: #d4af37;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), 0 0 10px rgba(212, 175, 55, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: LOGIN ACTUALIZADO
# ---------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="title-3d">BARBERÍA GOD\'S TIME</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a0a5b5;'>Excelencia, estilo y precisión en cada detalle</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: #ffffff;'>Acceso al Sistema</h3>", unsafe_allow_html=True)
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
    # Encabezado principal y botón para cerrar sesión
    col_t, col_l = st.columns([4, 1])
    with col_t:
        st.markdown('<h2 style="color: #d4af37;">BARBERÍA GOD\'S TIME</h2>', unsafe_allow_html=True)
    with col_l:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.rerun()

    st.markdown("---")

    # Menú principal por pestañas (Tabs)
    tab_inicio, tab_cortes, tab_barberos, tab_citas, tab_admin = st.tabs([
        "🏠 Menú Principal", 
        "✂️ Registrar Corte", 
        "💈 Registro por Barbero", 
        "📅 Agendar Citas / WhatsApp",
        "⚙️ Administración"
    ])

    # 1. PESTAÑA: MENÚ PRINCIPAL
    with tab_inicio:
        st.markdown("### 📊 Resumen General")
        
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos = df_cortes["Precio"].sum() if not df_cortes.empty else 0.0
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="card-3d"><h3>Total Cortes</h3><h2>{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h3>Ingresos Totales</h3><h2>${total_ingresos:.2f}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h3>Citas Agendadas</h3><h2>{citas_pendientes}</h2></div>', unsafe_allow_html=True)

        st.markdown("### 💵 Catálogo de Servicios y Precios")
        precios_df = pd.DataFrame(list(PRECIOS_CORTES.items()), columns=["Servicio / Corte", "Precio ($)"])
        st.table(precios_df)

    # 2. PESTAÑA: REGISTRAR CORTES
    with tab_cortes:
        st.markdown("### ✂️ Registrar Nuevo Corte")
        
        with st.form("form_corte"):
            barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS)
            corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
            precio_corte = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
            cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            
            btn_guardar = st.form_submit_button("REGISTRAR CORTE")
            
            if btn_guardar:
                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Barbero": barbero_sel,
                    "Servicio": corte_sel,
                    "Precio": precio_corte,
                    "Cliente": cliente_nombre if cliente_nombre else "Cliente Ocasional"
                }
                st.session_state.cortes_db.append(nuevo_registro)
                st.success(f"Corte registrado a {barbero_sel} correctamente.")

    # 3. PESTAÑA: REGISTRO POR BARBERO
    with tab_barberos:
        st.markdown("### 💈 Historial Individual de Barberos")
        barbero_filtro = st.selectbox("Filtrar por Barbero", BARBEROS, key="filtro_barbero")
        
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            
            if not df_filtrado.empty:
                st.dataframe(df_filtrado, use_container_width=True)
                st.info(f"Total generado por **{barbero_filtro}**: **${df_filtrado['Precio'].sum():.2f}** ({len(df_filtrado)} cortes)")
            else:
                st.warning(f"No hay registros cargados para {barbero_filtro}.")
        else:
            st.write("No hay datos de cortes registrados en el sistema.")

    # 4. PESTAÑA: AGENDAR CITAS Y WHATSAPP
    with tab_citas:
        st.markdown("### 📅 Agendar Cita")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            telefono_c = st.text_input("Teléfono (con código de país ej: +58...)")
            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha", min_value=date.today())
            hora_c = st.time_input("Hora de la cita")
            servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("AGENDAR Y PREPARAR WHATSAPP"):
            if nombre_c y telefono_c:
                cita = {
                    "Cliente": nombre_c,
                    "Teléfono": telefono_c,
                    "Barbero": barbero_c,
                    "Fecha": str(fecha_c),
                    "Hora": str(hora_c),
                    "Servicio": servicio_c
                }
                st.session_state.citas_db.append(cita)
                
                # Generación del enlace de WhatsApp
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c}."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                
                st.success("¡Cita agendada con éxito!")
                st.markdown(f'<a href="{ws_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 Enviar Confirmación por WhatsApp</button></a>', unsafe_allow_html=True)
            else:
                st.error("Por favor completa el nombre y el número telefónico.")

        st.markdown("---")
        st.markdown("### 📋 Citas Registradas")
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)
        else:
            st.write("No hay citas pendientes.")

    # 5. PESTAÑA: ADMINISTRACIÓN Y REINICIO DE HISTORIAL
    with tab_admin:
        st.markdown("### ⚙️ Opciones de Administrador")
        st.warning("⚠️ **Zona de Peligro:** La siguiente acción borrará la base de datos de la sesión actual.")
        
        # Botón para reiniciar el historial completo
        if st.button("🔴 REINICIAR TODO EL HISTORIAL"):
            st.session_state.cortes_db = []
            st.session_state.citas_db = []
            st.success("El historial de cortes y citas se ha borrado correctamente.")
            st.rerun()
import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Barbería God's Time", layout="wide", initial_sidebar_state="expanded")

# Inicialización del estado de la aplicación (Base de Datos en Sesión)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "cortes_db" not in st.session_state:
    st.session_state.cortes_db = []
if "citas_db" not in st.session_state:
    st.session_state.citas_db = []

# Precios base predeterminados
PRECIOS_CORTES = {
    "Corte Clásico": 10.0,
    "Degradado / Fade": 12.0,
    "Barba Completa": 8.0,
    "Combo (Corte + Barba)": 18.0,
    "Diseño / Cejas": 5.0
}

BARBEROS = ["Barbero 1", "Barbero 2", "Barbero 3"]

# Estilos CSS Modernos en 3D
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d0e12 0%, #1a1c23 100%);
        color: #e0e0e0;
    }
    
    /* Formulario de Login 3D */
    [data-testid="stForm"] {
        background: #14161d;
        border-radius: 20px;
        padding: 30px 20px;
        box-shadow: 10px 10px 25px rgba(0, 0, 0, 0.7), -5px -5px 15px rgba(255, 255, 255, 0.03), inset 0px 1px 1px rgba(212, 175, 55, 0.3);
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* Tarjetas 3D para métricas y datos */
    .card-3d {
        background: #14161d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 6px 6px 12px rgba(0,0,0,0.6), -3px -3px 8px rgba(255,255,255,0.02);
        border: 1px solid rgba(212, 175, 55, 0.15);
    }
    
    /* Botones principales estilo 3D */
    .stButton > button {
        background: linear-gradient(145deg, #e6c247, #b89528);
        color: #000000;
        font-weight: 800;
        border-radius: 12px;
        border: none;
        width: 100%;
        padding: 10px 15px;
        box-shadow: 0px 5px 0px #8a6f1c, 0px 8px 12px rgba(0, 0, 0, 0.4);
        transition: all 0.1s ease-in-out;
    }
    .stButton > button:active {
        transform: translateY(3px);
        box-shadow: 0px 2px 0px #8a6f1c;
    }

    /* Entradas de texto 3D */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #0f1015 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #2a2d37 !important;
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.6) !important;
    }
    
    .title-3d {
        font-size: 28px;
        font-weight: 900;
        color: #d4af37;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), 0 0 10px rgba(212, 175, 55, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: LOGIN ACTUALIZADO
# ---------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="title-3d">BARBERÍA GOD\'S TIME</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a0a5b5;'>Excelencia, estilo y precisión en cada detalle</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: #ffffff;'>Acceso al Sistema</h3>", unsafe_allow_html=True)
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
    # Encabezado principal y botón para cerrar sesión
    col_t, col_l = st.columns([4, 1])
    with col_t:
        st.markdown('<h2 style="color: #d4af37;">BARBERÍA GOD\'S TIME</h2>', unsafe_allow_html=True)
    with col_l:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.rerun()

    st.markdown("---")

    # Menú principal por pestañas (Tabs)
    tab_inicio, tab_cortes, tab_barberos, tab_citas, tab_admin = st.tabs([
        "🏠 Menú Principal", 
        "✂️ Registrar Corte", 
        "💈 Registro por Barbero", 
        "📅 Agendar Citas / WhatsApp",
        "⚙️ Administración"
    ])

    # 1. PESTAÑA: MENÚ PRINCIPAL
    with tab_inicio:
        st.markdown("### 📊 Resumen General")
        
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos = df_cortes["Precio"].sum() if not df_cortes.empty else 0.0
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="card-3d"><h3>Total Cortes</h3><h2>{total_cortes}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card-3d"><h3>Ingresos Totales</h3><h2>${total_ingresos:.2f}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-3d"><h3>Citas Agendadas</h3><h2>{citas_pendientes}</h2></div>', unsafe_allow_html=True)

        st.markdown("### 💵 Catálogo de Servicios y Precios")
        precios_df = pd.DataFrame(list(PRECIOS_CORTES.items()), columns=["Servicio / Corte", "Precio ($)"])
        st.table(precios_df)

    # 2. PESTAÑA: REGISTRAR CORTES
    with tab_cortes:
        st.markdown("### ✂️ Registrar Nuevo Corte")
        
        with st.form("form_corte"):
            barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS)
            corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
            precio_corte = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
            cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            
            btn_guardar = st.form_submit_button("REGISTRAR CORTE")
            
            if btn_guardar:
                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Barbero": barbero_sel,
                    "Servicio": corte_sel,
                    "Precio": precio_corte,
                    "Cliente": cliente_nombre if cliente_nombre else "Cliente Ocasional"
                }
                st.session_state.cortes_db.append(nuevo_registro)
                st.success(f"Corte registrado a {barbero_sel} correctamente.")

    # 3. PESTAÑA: REGISTRO POR BARBERO
    with tab_barberos:
        st.markdown("### 💈 Historial Individual de Barberos")
        barbero_filtro = st.selectbox("Filtrar por Barbero", BARBEROS, key="filtro_barbero")
        
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            
            if not df_filtrado.empty:
                st.dataframe(df_filtrado, use_container_width=True)
                st.info(f"Total generado por **{barbero_filtro}**: **${df_filtrado['Precio'].sum():.2f}** ({len(df_filtrado)} cortes)")
            else:
                st.warning(f"No hay registros cargados para {barbero_filtro}.")
        else:
            st.write("No hay datos de cortes registrados en el sistema.")

    # 4. PESTAÑA: AGENDAR CITAS Y WHATSAPP
    with tab_citas:
        st.markdown("### 📅 Agendar Cita")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            telefono_c = st.text_input("Teléfono (con código de país ej: +58...)")
            barbero_c = st.selectbox("Barbero de preferencia", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha", min_value=date.today())
            hora_c = st.time_input("Hora de la cita")
            servicio_c = st.selectbox("Servicio solicitado", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("AGENDAR Y PREPARAR WHATSAPP"):
            if nombre_c y telefono_c:
                cita = {
                    "Cliente": nombre_c,
                    "Teléfono": telefono_c,
                    "Barbero": barbero_c,
                    "Fecha": str(fecha_c),
                    "Hora": str(hora_c),
                    "Servicio": servicio_c
                }
                st.session_state.citas_db.append(cita)
                
                # Generación del enlace de WhatsApp
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c}."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                
                st.success("¡Cita agendada con éxito!")
                st.markdown(f'<a href="{ws_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 Enviar Confirmación por WhatsApp</button></a>', unsafe_allow_html=True)
            else:
                st.error("Por favor completa el nombre y el número telefónico.")

        st.markdown("---")
        st.markdown("### 📋 Citas Registradas")
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)
        else:
            st.write("No hay citas pendientes.")

    # 5. PESTAÑA: ADMINISTRACIÓN Y REINICIO DE HISTORIAL
    with tab_admin:
        st.markdown("### ⚙️ Opciones de Administrador")
        st.warning("⚠️ **Zona de Peligro:** La siguiente acción borrará la base de datos de la sesión actual.")
        
        # Botón para reiniciar el historial completo
        if st.button("🔴 REINICIAR TODO EL HISTORIAL"):
            st.session_state.cortes_db = []
            st.session_state.citas_db = []
            st.success("El historial de cortes y citas se ha borrado correctamente.")
            st.rerun()

