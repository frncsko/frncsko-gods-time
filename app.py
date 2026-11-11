import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(
    page_title="Fran ADS",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CREDENCIALES ADMINISTRADOR -----------------
ADMIN_USER = "fran"
ADMIN_PASS = "1234"

# ----------------- ESTADOS DE SESIÓN -----------------
if "autenticado_admin" not in st.session_state:
    st.session_state.autenticado_admin = False

if "usuario_activo" not in st.session_state:
    st.session_state.usuario_activo = None

if "modo_login_admin" not in st.session_state:
    st.session_state.modo_login_admin = False

# Fondo administrativo de $50,000 USD
if "saldo_admin" not in st.session_state:
    st.session_state.saldo_admin = 50000.00

# Base de datos en memoria para control de usuarios
if "usuarios_db" not in st.session_state:
    st.session_state.usuarios_db = {}

# Historial de retiros y transferencias
if "solicitudes_retiro" not in st.session_state:
    st.session_state.solicitudes_retiro = []

if "historial_envios" not in st.session_state:
    st.session_state.historial_envios = []

# ----------------- ESTILOS NEGRO CON AZUL -----------------
st.markdown("""
<style>
    .stApp {
        background-color: #030712;
        color: #f8fafc;
    }
    
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: block !important;
    }

    /* Tarjeta estilo crédito AdSelect */
    .credit-card {
        background: linear-gradient(135deg, #0b1528 0%, #030712 60%, #020c1e 100%);
        border: 1px solid #1e3a8a;
        border-radius: 20px;
        padding: 24px;
        position: relative;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.35);
        margin-bottom: 20px;
    }
    .card-brand {
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 3px;
        font-size: 13px;
        color: #38bdf8;
        font-weight: bold;
        text-transform: uppercase;
    }
    .card-chip {
        position: absolute;
        top: 24px;
        right: 24px;
        width: 38px;
        height: 28px;
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%);
        border-radius: 6px;
        border: 1px solid #60a5fa;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
    .card-balance {
        font-family: 'Times New Roman', serif;
        font-size: 42px;
        font-weight: 500;
        color: #ffffff;
        margin: 25px 0 15px 0;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
    }
    .card-user {
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
    }

    /* Tarjeta Bono por Referido */
    .bonus-card {
        background-color: #080f1e;
        border: 1px solid #1e293b;
        border-left: 3px solid #2563eb;
        border-radius: 18px;
        padding: 16px;
        margin-top: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }
    .streak-dots {
        display: flex;
        gap: 6px;
        margin: 12px 0;
    }
    .dot-active {
        width: 22px;
        height: 5px;
        background-color: #38bdf8;
        border-radius: 4px;
        box-shadow: 0 0 8px #38bdf8;
    }
    .dot-inactive {
        width: 14px;
        height: 5px;
        background-color: #1e293b;
        border-radius: 4px;
    }

    /* Earned Today */
    .earned-card {
        background-color: #050b17;
        border: 1px solid #1e3a8a;
        border-radius: 14px;
        padding: 14px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# VISTA 1: REGISTRO E INICIO DE USUARIOS NUEVOS
# =========================================================
def vista_registro_nuevo_usuario():
    col_l, col_center, col_r = st.columns([1, 1.4, 1])

    with col_center:
        # Botón discreto para acceso admin
        c_espacio, c_adm = st.columns([2, 1])
        with c_adm:
            if st.button("Acceso Admin", use_container_width=True):
                st.session_state.modo_login_admin = not st.session_state.modo_login_admin
                st.rerun()

        if st.session_state.modo_login_admin:
            with st.container(border=True):
                st.caption("Consola Fran ADS (fran / 1234)")
                u_adm = st.text_input("Usuario Admin", key="admin_u")
                p_adm = st.text_input("Clave", type="password", key="admin_p")
                if st.button("Ingresar como Admin", type="primary", use_container_width=True):
                    if u_adm == ADMIN_USER and p_adm == ADMIN_PASS:
                        st.session_state.autenticado_admin = True
                        st.session_state.modo_login_admin = False
                        st.rerun()
                    else:
                        st.error("Credenciales de administrador incorrectas.")

        tab_reg, tab_log = st.tabs(["Crear Cuenta (+ $5 USD)", "Iniciar Sesión"])

        with tab_reg:
            with st.container(border=True):
                st.title("Fran ADS")
                st.write("Regístrate y recibe **$5.00 USD** de bienvenida en tu tarjeta.")
                st.divider()

                with st.form("form_registro"):
                    user_reg = st.text_input("Nombre de Usuario", placeholder="ejemplo: fran01")
                    email_reg = st.text_input("Correo Electrónico", placeholder="tuemail@gmail.com")
                    pass_reg = st.text_input("Contraseña", type="password", placeholder="Ingresa tu clave")
                    btn_registro = st.form_submit_button("Crear Cuenta y Recibir $5 USD", type="primary", use_container_width=True)

                    if btn_registro:
                        if not user_reg or not email_reg or not pass_reg:
                            st.error("Por favor llena todos los campos.")
                        elif user_reg in st.session_state.usuarios_db:
                            st.warning("Este usuario ya existe. Intenta iniciar sesión.")
                        else:
                            st.session_state.usuarios_db[user_reg] = {
                                "email": email_reg,
                                "password": pass_reg,
                                "saldo": 5.00,
                                "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M")
                            }
                            st.session_state.usuario_activo = user_reg
                            st.success("¡Registro exitoso! Se han acreditado $5.00 USD a tu cuenta.")
                            st.rerun()

        with tab_log:
            with st.container(border=True):
                st.title("Iniciar Sesión")
                st.caption("Accede para ver tu saldo y solicitar retiros.")
                st.divider()

                with st.form("form_login_user"):
                    u_in = st.text_input("Usuario")
                    p_in = st.text_input("Contraseña", type="password")
                    btn_in = st.form_submit_button("Entrar", type="primary", use_container_width=True)

                    if btn_in:
                        if u_in in st.session_state.usuarios_db and st.session_state.usuarios_db[u_in]["password"] == p_in:
                            st.session_state.usuario_activo = u_in
                            st.rerun()
                        else:
                            st.error("Usuario o contraseña incorrectos.")


# =========================================================
# VISTA 2: PANEL DEL USUARIO REGISTRADO (INTERFAZ ADSELECT)
# =========================================================
def vista_dashboard_usuario():
    col_izq, col_mid, col_der = st.columns([1, 1.8, 1])
    usuario_data = st.session_state.usuarios_db[st.session_state.usuario_activo]

    with col_mid:
        c_saludo, c_salir = st.columns([3, 1])
        with c_saludo:
            st.caption(f"Conectado como: **@{st.session_state.usuario_activo}**")
        with c_salir:
            if st.button("Cerrar Sesión", key="btn_exit_user", use_container_width=True):
                st.session_state.usuario_activo = None
                st.rerun()

        # 1. Tarjeta estilo crédito AdSelect
        st.markdown(f"""
        <div class="credit-card">
            <div class="card-brand">FRAN ADS</div>
            <div class="card-chip"></div>
            <div class="card-balance">${usuario_data['saldo']:.2f}</div>
            <div class="card-user">{st.session_state.usuario_activo.upper()}</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Menú de Retiro por Binance
        with st.expander("💳 Retirar Fondos por Binance (Cash Out)", expanded=True):
            st.caption("Solicitud directa de retiro a tu billetera Binance (USDT / Binance Pay).")
            with st.form("form_retiro_binance"):
                binance_id = st.text_input("Binance Pay ID o Correo de Binance", placeholder="Ej: 12345678 o email@binance.com")
                monto_retiro = st.number_input(
                    "Monto a retirar (USD)",
                    min_value=1.0,
                    max_value=float(usuario_data["saldo"]),
                    value=float(usuario_data["saldo"]) if usuario_data["saldo"] > 0 else 1.0,
                    step=1.0
                )
                btn_retirar = st.form_submit_button("Solicitar Retiro", type="primary", use_container_width=True)

                if btn_retirar:
                    if not binance_id:
                        st.error("Debes ingresar tu Binance Pay ID o correo asociado.")
                    elif monto_retiro > usuario_data["saldo"]:
                        st.error("Saldo insuficiente.")
                    else:
                        usuario_data["saldo"] -= monto_retiro
                        st.session_state.solicitudes_retiro.insert(0, {
                            "usuario": st.session_state.usuario_activo,
                            "binance_id": binance_id,
                            "monto": monto_retiro,
                            "estado": "Pendiente",
                            "fecha": datetime.now().strftime("%d/%m %H:%M")
                        })
                        st.success(f"Solicitud de ${monto_retiro:.2f} USD enviada a revisión.")
                        st.rerun()

        # 3. Bono por Referido
        st.markdown("""
        <div class="bonus-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background-color: #0f172a; border: 1px solid #1e3a8a; border-radius: 10px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 18px;">
                        🎁
                    </div>
                    <div>
                        <div style="font-weight: 700; font-size: 14px; color: #f8fafc;">BONO POR REFERIDO</div>
                        <div style="font-size: 11px; color: #38bdf8; letter-spacing: 1px;">ESTADO ACTIVO • REGISTRO</div>
                    </div>
                </div>
                <div style="background-color: #1e3a8a; border: 1px solid #3b82f6; color: #ffffff; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 600;">
                    Reclamado
                </div>
            </div>
            <div class="streak-dots">
                <div class="dot-active"></div>
                <div class="dot-inactive"></div>
                <div class="dot-inactive"></div>
                <div class="dot-inactive"></div>
                <div class="dot-inactive"></div>
                <div class="dot-inactive"></div>
                <div class="dot-inactive"></div>
            </div>
            <div style="font-size: 11px; color: #94a3b8; line-height: 1.4;">
                Has recibido $5.00 USD por registro inicial en la plataforma.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. Sección Earned Today
        st.markdown("""
        <div class="earned-card">
            <div style="font-size: 11px; letter-spacing: 2px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">
                EARNED TODAY
            </div>
            <div style="font-family: 'Times New Roman', serif; font-size: 20px; color: #38bdf8; font-weight: 600;">
                $5.00
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# VISTA 3: PANEL ADMIN (CONTROL TOTAL DE USUARIOS)
# =========================================================
def vista_admin():
    with st.sidebar:
        st.title("Fran ADS")
        st.caption("Consola Administrativa")
        st.divider()

        st.metric("Mi Dinero Disponible", f"${st.session_state.saldo_admin:,.2f} USD")
        st.metric("Total Usuarios", len(st.session_state.usuarios_db))
        st.divider()

        if st.button("Cerrar Sesión Admin", use_container_width=True):
            st.session_state.autenticado_admin = False
            st.rerun()

    tab_usuarios, tab_enviar, tab_retiros = st.tabs([
        "👥 Control de Usuarios", 
        "💸 Enviar Dinero ($50.000)", 
        "📥 Retiros de Binance"
    ])

    # PESTAÑA 1: CONTROL DE USUARIOS
    with tab_usuarios:
        st.title("Usuarios Registrados")
        st.caption("Supervisa cada cuenta creada con su saldo y credenciales.")

        if not st.session_state.usuarios_db:
            st.info("Aún no hay usuarios registrados.")
        else:
            for u_nombre, u_info in st.session_state.usuarios_db.items():
                with st.container(border=True):
                    c_det, c_sal, c_acc = st.columns([3, 1.5, 1.5])
                    with c_det:
                        st.markdown(f"**Usuario:** `{u_nombre}`")
                        st.caption(f"Email: {u_info['email']}  |  Clave: `{u_info['password']}`  |  Fecha: {u_info['fecha_registro']}")
                    with c_sal:
                        st.metric("Saldo", f"${u_info['saldo']:.2f} USD")
                    with c_acc:
                        nuevo_monto = st.number_input("Ajustar saldo", min_value=0.0, value=float(u_info['saldo']), step=5.0, key=f"adj_{u_nombre}")
                        if st.button("Actualizar", key=f"btn_adj_{u_nombre}", use_container_width=True):
                            u_info['saldo'] = nuevo_monto
                            st.success(f"Saldo de {u_nombre} actualizado.")
                            st.rerun()

    # PESTAÑA 2: ENVIAR DINERO
    with tab_enviar:
        st.title("Transferir Fondos a Usuarios")
        st.caption(f"Fondos disponibles en tu cuenta admin: **${st.session_state.saldo_admin:,.2f} USD**")

        if not st.session_state.usuarios_db:
            st.warning("No hay usuarios registrados a quienes transferir.")
        else:
            with st.container(border=True):
                with st.form("form_transferir_fondos", clear_on_submit=True):
                    lista_users = list(st.session_state.usuarios_db.keys())
                    usuario_sel = st.selectbox("Seleccionar Usuario Destinatario", lista_users)
                    monto_a_enviar = st.number_input(
                        "Monto a transferir (USD)",
                        min_value=1.0,
                        max_value=float(st.session_state.saldo_admin),
                        value=10.0,
                        step=5.0
                    )
                    btn_enviar_fondos = st.form_submit_button("Transferir Dinero", type="primary", use_container_width=True)

                    if btn_enviar_fondos:
                        st.session_state.saldo_admin -= monto_a_enviar
                        st.session_state.usuarios_db[usuario_sel]["saldo"] += monto_a_enviar
                        st.session_state.historial_envios.insert(0, {
                            "destinatario": usuario_sel,
                            "monto": monto_a_enviar,
                            "fecha": datetime.now().strftime("%d/%m %H:%M")
                        })
                        st.success(f"¡Transferencia exitosa! Se enviaron ${monto_a_enviar:,.2f} USD a @{usuario_sel}.")
                        st.rerun()

        if st.session_state.historial_envios:
            st.subheader("Historial de Transferencias")
            for h in st.session_state.historial_envios:
                with st.container(border=True):
                    st.write(f"Enviado a **@{h['destinatario']}** — **${h['monto']:,.2f} USD** ({h['fecha']})")

    # PESTAÑA 3: SOLICITUDES DE RETIRO BINANCE
    with tab_retiros:
        st.title("Solicitudes de Retiro por Binance")
        st.caption("Aprueba o procesa las peticiones de retiro enviadas por los usuarios.")

        if not st.session_state.solicitudes_retiro:
            st.info("No hay solicitudes de retiro pendientes.")
        else:
            for idx, req in enumerate(st.session_state.solicitudes_retiro):
                with st.container(border=True):
                    col_r1, col_r2, col_r3 = st.columns([2.5, 1.5, 1])
                    with col_r1:
                        st.markdown(f"**Usuario:** @{req['usuario']}")
                        st.caption(f"Binance Pay ID / Correo: `{req['binance_id']}`")
                        st.caption(f"Fecha: {req['fecha']}")
                    with col_r2:
                        st.metric("Monto a Pagar", f"${req['monto']:.2f} USD")
                        st.write(f"Estado: **{req['estado']}**")
                    with col_r3:
                        if req['estado'] == "Pendiente":
                            if st.button("Marcar Pagado", key=f"pay_{idx}", type="primary", use_container_width=True):
                                req['estado'] = "Completado"
                                st.success("Retiro marcado como completado.")
                                st.rerun()


# =========================================================
# CONTROL PRINCIPAL DE RUTAS
# =========================================================
if st.session_state.autenticado_admin:
    vista_admin()
elif st.session_state.usuario_activo:
    vista_dashboard_usuario()
else:
    vista_registro_nuevo_usuario()
