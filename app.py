import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import urllib.parse
import json
import os

# Configuración de página
st.set_page_config(
    page_title="Barbería NextGen - Dynamic Dark VIP", 
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

OPCIONES_HORAS = [
    time(h, m).strftime("%I:%M %p") 
    for h in range(8, 20) 
    for m in (0, 30)
]

# --- FONDO ANIMADO CON FONDO OSCURO SÓLIDO ---
st.markdown("""
    <canvas id="barberCanvas" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none;"></canvas>

    <script>
    const canvas = document.getElementById('barberCanvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    const icons = ['✂️', '💈', '🪮', '💈', '✂️'];
    const particles = [];

    for (let i = 0; i < 25; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 20 + 16,
            icon: icons[Math.floor(Math.random() * icons.length)],
            speedX: (Math.random() - 0.5) * 0.8,
            speedY: (Math.random() - 0.5) * 0.8,
            opacity: Math.random() * 0.25 + 0.05,
            rotation: Math.random() * 360,
            rotSpeed: (Math.random() - 0.5) * 0.02
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Fondo oscuro sólido profesional (Dark Midnight / Navy)
        ctx.fillStyle = '#0a0e17'; 
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;
            p.rotation += p.rotSpeed;

            if (p.x < -30) p.x = canvas.width + 30;
            if (p.x > canvas.width + 30) p.x = -30;
            if (p.y < -30) p.y = canvas.height + 30;
            if (p.y > canvas.height + 30) p.y = -30;

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rotation);
            ctx.globalAlpha = p.opacity;
            ctx.font = `${p.size}px sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(p.icon, 0, 0);
            ctx.restore();
        });

        requestAnimationFrame(animate);
    }
    animate();
    </script>
""", unsafe_allow_html=True)

# --- ESTILOS INTERFAZ ULTRA MODERN / CYBERPUNK GLASSMORPHISM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@500;700&display=swap');

    :root {
        --card-bg: rgba(10, 16, 28, 0.65);
        --accent-cyan: #00f2fe;
        --accent-blue: #4facfe;
        --accent-green: #00ff87;
        --border-color: rgba(0, 242, 254, 0.2);
    }

    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif;
        background-color: transparent !important;
        color: #f1f5f9 !important;
    }

    [data-testid="stSidebarCollapseButton"] { display: none !important; }

    /* SIDEBAR MODERNA */
    [data-testid="stSidebar"] {
        background: rgba(6, 10, 18, 0.85) !important;
        backdrop-filter: blur(25px) saturate(200%);
        border-right: 1px solid var(--border-color) !important;
    }

    /* MENÚ INTERACTIVO EN SIDEBAR CON EFECTO HOVER NEÓN */
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 14px !important;
        padding: 12px 18px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 6px;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        color: #ffffff !important;
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.35), inset 0 0 10px rgba(0, 242, 254, 0.1) !important;
        transform: translateX(6px);
    }

    [data-testid="stSidebar"] .stRadio div[aria-checked="true"] + label {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: 1px solid #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.6) !important;
    }

    /* TARJETAS GLASSMORPHISM CON INTERACCIÓN */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 26px;
        border: 1px solid var(--border-color);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(0, 242, 254, 0.5);
        box-shadow: 0 20px 40px rgba(0, 242, 254, 0.25);
    }

    /* EFECTOS HOVER AVANZADOS EN BOTONES GENERALES DE STREAMLIT */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #050811 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 14px 28px !important;
        box-shadow: 0 8px 20px rgba(0, 242, 254, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 30px rgba(0, 242, 254, 0.5), 0 0 15px rgba(0, 242, 254, 0.8) !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
    }

    /* BOTÓN DE WHATSAPP CON GLOW VERDE INTERACTIVO */
    .btn-ws-nextgen {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%) !important;
        color: #050811 !important;
        font-family: 'Space Grotesk', sans-serif;
        text-decoration: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 8px 20px rgba(0, 255, 135, 0.3);
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    .btn-ws-nextgen:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 255, 135, 0.6), 0 0 20px rgba(0, 255, 135, 0.8);
        color: #000000 !important;
    }

    /* ENCABEZADOS Y TEXTOS */
    .title-nextgen {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 30%, var(--accent-cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -1px;
    }

    .section-header-nextgen {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--accent-cyan);
        letter-spacing: 0.5px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }

    div[data-baseweb="input"] > div:hover, div[data-baseweb="select"] > div:hover {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: INICIO CLIENTES
# ---------------------------------------------------------
if not st.session_state.autenticado:
    col_header, col_login_btn = st.columns([5, 1.3])
    
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
            <div class="title-nextgen">BARBERÍA GOD'S TIME</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 15px; margin-top: 5px; margin-bottom: 35px;'>ESTILO DE VANGUARDIA & RESERVA AUTOMÁTICA</p>", unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #00f2fe; font-family: Space Grotesk; margin-bottom: 20px;'>AGENDAR CITA</h3>", unsafe_allow_html=True)
        with st.form("form_cita_login"):
            nombre_c = st.text_input("Nombre Completo")
            
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
            
            btn_agendar_login = st.form_submit_button("REGISTRAR MI CITA")

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
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-nextgen" style="margin-top: 15px;">
                        CONFIRMAR VÍA WHATSAPP
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.error("Por favor completa tu nombre y número de teléfono.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 2: PANEL PRINCIPAL ADMINISTRACIÓN/BARBEROS
# ---------------------------------------------------------
else:
    user_info = USUARIOS.get(st.session_state.usuario_actual, {"rol": "invitado"})
    es_admin = user_info["rol"] == "admin"

    with st.sidebar:
        st.markdown('''
            <div style="text-align: center; padding: 10px 0;">
                <div class="title-nextgen" style="font-size: 20px;">GOD'S TIME</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 13px;'>Barbero Activo: <b style='color:#00f2fe;'>{st.session_state.usuario_actual}</b></p>", unsafe_allow_html=True)
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
        
        st.markdown("<p style='font-size: 12px; color: #00f2fe; font-weight: 800;'>💵 TASA DEL DÓLAR (BCV)</p>", unsafe_allow_html=True)
        nueva_tasa_input = st.number_input("Tasa BS", value=float(st.session_state.tasa_bcv), step=0.10, label_visibility="collapsed")
        if st.button("ACTUALIZAR TASA"):
            st.session_state.tasa_bcv = nueva_tasa_input
            guardar_datos(CONFIG_FILE, {"tasa_bcv": nueva_tasa_input})
            st.success(f"Tasa actualizada: {nueva_tasa_input:.2f} BS")
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 CERRAR SESIÓN"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.rerun()

    # 1. PANEL GENERAL
    if opcion_menu == "Panel General":
        st.markdown('<div class="section-header-nextgen">📊 PANEL GENERAL</div>', unsafe_allow_html=True)
        df_cortes = pd.DataFrame(st.session_state.cortes_db)
        
        c1, c2, c3 = st.columns(3)
        total_cortes = len(df_cortes) if not df_cortes.empty else 0
        total_ingresos_usd = df_cortes["Precio ($)"].sum() if (not df_cortes.empty and "Precio ($)" in df_cortes.columns) else (df_cortes["Precio"].sum() if not df_cortes.empty else 0.0)
        total_ingresos_bs = total_ingresos_usd * st.session_state.tasa_bcv
        citas_pendientes = len(st.session_state.citas_db)

        with c1:
            st.markdown(f'<div class="glass-card"><h4 style="color:#94a3b8; margin:0; font-family:Space Grotesk; font-size:14px;">TOTAL CORTES</h4><h1 style="margin:8px 0 0 0; color:#00f2fe;">{total_cortes}</h1></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="glass-card"><h4 style="color:#94a3b8; margin:0; font-family:Space Grotesk; font-size:14px;">INGRESOS TOTALES</h4><h2 style="margin:8px 0 0 0; color:#00ff87;">${total_ingresos_usd:.2f} <span style="font-size:15px; color:#ffffff;">({total_ingresos_bs:.2f} BS)</span></h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="glass-card"><h4 style="color:#94a3b8; margin:0; font-family:Space Grotesk; font-size:14px;">CITAS PROGRAMADAS</h4><h1 style="margin:8px 0 0 0; color:#00f2fe;">{citas_pendientes}</h1></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header-nextgen" style="margin-top: 35px;">💵 TARIFARIO VIGENTE</div>', unsafe_allow_html=True)
        precios_tabla = [
            {"Servicio / Corte": k, "Precio ($)": f"${v:.2f}", "Precio (BS)": f"{v * st.session_state.tasa_bcv:.2f} BS"}
            for k, v in PRECIOS_CORTES.items()
        ]
        st.table(pd.DataFrame(precios_tabla))

    # 2. REGISTRAR CORTE
    elif opcion_menu == "Registrar Corte":
        st.markdown('<div class="section-header-nextgen">✂️ REGISTRO DE SERVICIO</div>', unsafe_allow_html=True)
        with st.form("form_corte"):
            col1, col2 = st.columns(2)
            with col1:
                idx_barbero = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
                barbero_sel = st.selectbox("Selecciona el Barbero", BARBEROS, index=idx_barbero)
                corte_sel = st.selectbox("Tipo de Corte / Servicio", list(PRECIOS_CORTES.keys()))
                precio_corte_usd = st.number_input("Precio ($)", value=float(PRECIOS_CORTES[corte_sel]), step=1.0)
                precio_corte_bs = precio_corte_usd * st.session_state.tasa_bcv
                st.info(f"Monto en BS (Tasa {st.session_state.tasa_bcv:.2f}): **{precio_corte_bs:.2f} BS**")
                cliente_nombre = st.text_input("Nombre del Cliente (Opcional)")
            
            with col2:
                metodo_pago = st.selectbox("Método de Pago", METODOS_PAGO)
                referencia_pago = st.text_input("N° de Referencia", placeholder="N/A para Efectivo")

            btn_guardar = st.form_submit_button("REGISTRAR Y GUARDAR CORTE")
            
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
                st.success(f"Corte registrado exitosamente a {barbero_sel} (${precio_corte_usd:.2f} / {precio_corte_bs:.2f} BS).")

    # 3. HISTORIAL
    elif opcion_menu == "Historial Barberos":
        st.markdown('<div class="section-header-nextgen">💈 HISTORIAL DE SERVICIOS POR BARBERO</div>', unsafe_allow_html=True)
        idx_filtro = BARBEROS.index(st.session_state.usuario_actual) if st.session_state.usuario_actual in BARBEROS else 0
        barbero_filtro = st.selectbox("Selecciona un Barbero", BARBEROS, index=idx_filtro, key="filtro_barbero")
        
        if st.session_state.cortes_db:
            df_cortes = pd.DataFrame(st.session_state.cortes_db)
            df_filtrado = df_cortes[df_cortes["Barbero"] == barbero_filtro]
            
            if not df_filtrado.empty:
                col_precio = "Precio ($)" if "Precio ($)" in df_filtrado.columns else "Precio"
                total_usd = df_filtrado[col_precio].sum()
                total_bs = total_usd * st.session_state.tasa_bcv
                st.info(f"Total producido por **{barbero_filtro}**: **${total_usd:.2f} USD** / **{total_bs:.2f} BS** ({len(df_filtrado)} cortes)")

                tab_hist, tab_cli = st.tabs(["HISTORIAL REGISTRADO", "CLIENTES DE ESTE BARBERO"])
                
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
                st.warning(f"No hay servicios registrados para {barbero_filtro}.")
        else:
            st.write("Sin información de cortes en el sistema.")

    # 4. CITAS Y WHATSAPP
    elif opcion_menu == "Citas y WhatsApp":
        st.markdown('<div class="section-header-nextgen">📅 GESTIÓN DE CITAS & CONFIRMACIÓN</div>', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_c = st.text_input("Nombre del Cliente")
            
            col_pref_a, col_tel_a = st.columns([1, 3])
            with col_pref_a:
                st.text_input("Código", value="+58", disabled=True, key="pref_admin")
            with col_tel_a:
                num_tel_admin = st.text_input("Teléfono WhatsApp", placeholder="4121234567", key="tel_admin")

            barbero_c = st.selectbox("Barbero asignado", BARBEROS, key="barbero_cita")
        with col_f2:
            fecha_c = st.date_input("Fecha", min_value=date.today())
            hora_c = st.selectbox("Hora", OPCIONES_HORAS, key="hora_cita_admin")
            servicio_c = st.selectbox("Servicio", list(PRECIOS_CORTES.keys()), key="servicio_cita")
            
        if st.button("AGENDAR CITA Y ENVIAR WHATSAPP"):
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
                
                mensaje = f"Hola {nombre_c}, confirmamos tu cita en Barbería God's Time el {fecha_c} a las {hora_c} con {barbero_c} para {servicio_c} (${precio_usd:.2f} / {precio_bs:.2f} BS)."
                mensaje_encoded = urllib.parse.quote(mensaje)
                phone_clean = telefono_c.replace("+", "").replace(" ", "").replace("-", "")
                ws_url = f"https://wa.me/{phone_clean}?text={mensaje_encoded}"
                st.success("¡Cita agendada exitosamente!")
                st.markdown(f'''
                    <a href="{ws_url}" target="_blank" class="btn-ws-nextgen" style="margin-top: 15px;">
                        ENVIAR NOTIFICACIÓN POR WHATSAPP
                    </a>
                ''', unsafe_allow_html=True)

        st.markdown('<div class="section-header-nextgen" style="margin-top:35px;">LISTA DE CITAS PENDIENTES</div>', unsafe_allow_html=True)
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. ADMINISTRACIÓN
    elif opcion_menu == "Administración":
        st.markdown('<div class="section-header-nextgen">⚙️ CONFIGURACIÓN Y MANTENIMIENTO</div>', unsafe_allow_html=True)
        
        if es_admin:
            st.warning("⚠️ **Atención:** Reiniciar el sistema vaciará todos los registros guardados.")
            if st.button("REINICIAR TODO EL HISTORIAL"):
                st.session_state.cortes_db = []
                st.session_state.citas_db = []
                guardar_datos(CORTES_FILE, [])
                guardar_datos(CITAS_FILE, [])
                st.success("El sistema ha sido reiniciado a cero.")
                st.rerun()
        else:
            st.error("🔒 **Acceso Denegado:** Se requieren permisos de nivel administrador.")
