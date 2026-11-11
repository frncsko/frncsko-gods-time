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

# Saldo del administrador configurado en $50,000 USD
if "saldo_admin" not in st.session_state:
    st.session_state.saldo_admin = 50000.00

# Base de datos en memoria para control de usuarios
if "usuarios_db" not in st.session_state:
    st.session_state.usuarios_db = {}

# Historial de transferencias realizadas por admin
if "historial_envios" not in st.session_state:
    st.session_state.historial_envios = []

# Bandera para mostrar la broma de retiro
if "broma_retiro" not in st.session_state:
    st.session_state.broma_retiro = False

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

    /* Cartel de broma de retiro */
    .caiste-box {
        background-color: #1a0505;
        border: 2px solid #ef4444;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.4);
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# VISTA 1: REGISTRO E INICIO DE SESIÓN DE USUARIOS
# =========================================================
def vista_registro():
    col_l, col_center, col_r = st.columns([1, 1.4, 1])

    with col_center:
        # Botón discreto para login de admin
        c_esp, c_adm = st.columns([2, 1])
        with c_adm:
            if st.button("Acceso Admin", use_container_width=True):
                st.session_state.modo_login_admin = not st.session_state.modo_login_admin
                st.rerun()

        if st.session_state.modo_login_admin:
            with st.container(border=True):
                st.caption("Consola Fran ADS (fran / 1234)")
                u_adm = st.text_input("Usuario Admin", key="admin_u")
                p_adm = st.text_input("Clave Admin", type="password", key="admin_p")
                if st.button("Entrar Admin", type="primary", use_container_width=True):
                    if u_adm == ADMIN_USER and p_adm == ADMIN_PASS:
                        st.session_state.autenticado_admin = True
                        st.session_state.modo_login_admin = False
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas.")

        tab_reg, tab_log = st.tabs(["Crear Cuenta (+ $5 USD)", "Iniciar Sesión"])

        with tab_reg:
            with st.container(border=True):
                st.title("Fran ADS")
                st.write("Regístrate y recibe **$5.00 USD** de saldo inicial en tu tarjeta.")
                st.divider()

                with st.form("form_reg_usuario"):
                    u_nuevo = st.text_input("Nombre de Usuario", placeholder="ejemplo: fran01")
                    e_nuevo = st.text_input("Correo Electrónico", placeholder="tuemail@gmail.com")
                    p_nuevo = st.text_input("Contraseña", type="password", placeholder="Ingresa tu clave")
                    btn_crear = st.form_submit_button("Crear Cuenta y Recibir $5 USD", type="primary", use_container_width=True)

                    if btn_crear:
                        if not u_nuevo or not e_nuevo or not p_nuevo:
                            st.error("Por favor completa todos los campos.")
                        elif u_nuevo in st.session_state.usuarios_db:
                            st.warning("Este usuario ya existe. Inicia sesión en la otra pestaña.")
                        else:
                            st.session_state.usuarios_db[u_nuevo] = {
                                "email": e_nuevo,
                                "password": p_nuevo,
                                "saldo": 5.00,
                                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                            }
                            st.session_state.usuario_activo = u_nuevo
                            st.session_state.broma_retiro = False
                            st.success("¡Cuenta creada! Se han acreditado $5.00 USD.")
                            st.rerun()

        with tab_log:
            with st.container(border=True):
                st.title("Iniciar Sesión")
                st.caption("Accede con tus datos para ver tu tarjeta y saldo.")
                st.divider()

                with st.form("form_log_usuario"):
                    u_in = st.text_input("Usuario")
                    p_in = st.text_input("Contraseña", type="password")
                    btn_entrar = st.form_submit_button("Entrar a mi Cuenta", type="primary", use_container_width=True)

                    if btn_entrar:
                        if u_in in st.session_state.usuarios_db and st.session_state.usuarios_db[u_in]["password"] == p_in:
                            st.session_state.usuario_activo = u_in
                            st.session_state.broma_retiro = False
                            st.rerun()
                        else:
                            st.error("Usuario o contraseña incorrectos.")


# =========================================================
# VISTA 2: PANEL DEL USUARIO NUEVO (ESTILO ADSELECT)
# =========================================================
def vista_usuario():
    col_l, col_mid, col_r = st.columns([1, 1.8, 1])
    u_data = st.session_state.usuarios_db[st.session_state.usuario_activo]

    with col_mid:
        c_user, c_out = st.columns([3, 1])
        with c_user:
            st.caption(f"Miembro: **@{st.session_state.usuario_activo}**")
        with c_out:
            if st.button("Salir", use_container_width=True):
                st.session_state.usuario_activo = None
                st.session_state.broma_retiro = False
                st.rerun()

        # 1. Tarjeta estilo crédito AdSelect
        st.markdown(f"""
        <div class="credit-card">
            <div class="card-brand">FRAN ADS</div>
            <div class="card-chip"></div>
            <div class="card-balance">${u_data['saldo']:.2f}</div>
            <div class="card-user">{st.session_state.usuario_activo.upper()}</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Módulo de Retiro por Binance
        with st.expander("💳 Retirar Fondos por Binance (Cash Out)", expanded=True):
            st.caption("Transferencia directa a billetera Binance Pay / USDT.")
            
            with st.form("form_retiro_binance"):
                binance_id = st.text_input("Binance Pay ID o Correo", placeholder="Ej: 83920194 o cuenta@binance.com")
                monto_solicitado = st.number_input(
                    "Monto a retirar (USD)",
                    min_value=1.0,
                    max_value=float(u_data["saldo"]) if u_data["saldo"] > 0 else 5.0,
                    value=float(u_data["saldo"]) if u_data["saldo"] > 0 else 5.0,
                    step=1.0
                )
                btn_solicitar = st.form_submit_button("Solicitar Retiro Inmediato", type="primary", use_container_width=True)

                if btn_solicitar:
                    if not binance_id:
                        st.error("Ingresa tu ID de Binance para continuar.")
                    else:
                        st.session_state.broma_retiro = True
                        st.rerun()

        # Mensaje de broma al solicitar retiro
        if st.session_state.broma_retiro:
            st.markdown("""
            <div class="caiste-box">
                <h1 style="color: #ef4444; margin: 0; font-size: 38px; font-weight: bold; letter-spacing: 2px;">
                    CAÍSTE JAJAJA 😂
                </h1>
                <p style="color: #fca5a5; font-size: 14px; margin-top: 8px;">
                    ¿Pensaste que era tan fácil retirar? ¡Sigue participando en Fran ADS!
                </p>
            </div>
            """, unsafe_allow_html=True)

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
                Has recibido $5.00 USD por registrarte en la plataforma.
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
# VISTA 3: PANEL ADMIN (CONTROL DE USUARIOS + ENVIAR DINERO)
# =========================================================
def vista_admin():
    with st.sidebar:
        st.title("Fran ADS")
        st.caption("Consola Administrativa")
        st.divider()

        st.metric("Mi Dinero Total", f"${st.session_state.saldo_admin:,.2f} USD")
        st.metric("Usuarios Totales", len(st.session_state.usuarios_db))
        st.divider()

        if st.button("Cerrar Sesión Admin", use_container_width=True):
            st.session_state.autenticado_admin = False
            st.rerun()

    tab_control, tab_enviar = st.tabs([
        "👥 Control de Usuarios Registrados", 
        "💸 Enviar Dinero ($50.000 USD)"
    ])

    # PESTAÑA 1: CONTROL DE CADA USUARIO
    with tab_control:
        st.title("Control de Usuarios")
        st.caption("Listado completo de cuentas registradas con sus datos y saldo.")

        if not st.session_state.usuarios_db:
            st.info("Aún no se ha registrado ningún usuario nuevo.")
        else:
            for user_key, datos in st.session_state.usuarios_db.items():
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1.5, 1.5])
                    with c1:
                        st.markdown(f"**Usuario:** `@{user_key}`")
                        st.write(f"📧 Correo: `{datos['email']}`")
                        st.write(f"🔑 Contraseña: `{datos['password']}`")
                        st.caption(f"Fecha de registro: {datos['fecha']}")
                    with c2:
                        st.metric("Saldo en Tarjeta", f"${datos['saldo']:.2f} USD")
                    with c3:
                        nuevo_saldo = st.number_input(
                            "Modificar saldo",
                            min_value=0.0,
                            value=float(datos['saldo']),
                            step=5.0,
                            key=f"input_saldo_{user_key}"
                        )
                        if st.button("Guardar Saldo", key=f"btn_save_{user_key}", use_container_width=True):
                            datos['saldo'] = nuevo_saldo
                            st.success(f"Saldo de @{user_key} actualizado a ${nuevo_saldo:.2f} USD.")
                            st.rerun()

    # PESTAÑA 2: ENVIAR DINERO DESDE LOS $50.000 USD
    with tab_enviar:
        st.title("Transferir Dinero a Usuarios")
        st.caption(f"Fondos disponibles para repartir: **${st.session_state.saldo_admin:,.2f} USD**")

        if not st.session_state.usuarios_db:
            st.warning("No hay usuarios registrados a los que enviar dinero.")
        else:
            with st.container(border=True):
                with st.form("form_admin_enviar_fondos", clear_on_submit=True):
                    opciones_dest = list(st.session_state.usuarios_db.keys())
                    dest_elegido = st.selectbox("Seleccionar Usuario", opciones_dest)
                    monto_transferencia = st.number_input(
                        "Monto a enviar (USD)",
                        min_value=1.0,
                        max_value=float(st.session_state.saldo_admin),
                        value=10.0,
                        step=5.0
                    )
                    btn_confirmar = st.form_submit_button("Confirmar Transferencia", type="primary", use_container_width=True)

                    if btn_confirmar:
                        if monto_transferencia > st.session_state.saldo_admin:
                            st.error("No tienes fondos suficientes en tu cuenta.")
                        else:
                            st.session_state.saldo_admin -= monto_transferencia
                            st.session_state.usuarios_db[dest_elegido]["saldo"] += monto_transferencia
                            st.session_state.historial_envios.insert(0, {
                                "usuario": dest_elegido,
                                "monto": monto_transferencia,
                                "fecha": datetime.now().strftime("%d/%m %H:%M")
                            })
                            st.success(f"Se han enviado ${monto_transferencia:,.2f} USD a @{dest_elegido} exitosamente.")
                            st.rerun()

            # Historial de transferencias
            if st.session_state.historial_envios:
                st.divider()
                st.subheader("Historial de Envíos Realizados")
                for item in st.session_state.historial_envios:
                    with st.container(border=True):
                        c_u, c_m = st.columns([3, 1])
                        c_u.write(f"Enviado a **@{item['usuario']}** ({item['fecha']})")
                        c_m.write(f"**-${item['monto']:,.2f} USD**")


# =========================================================
# ENRUTADOR PRINCIPAL
# =========================================================
if st.session_state.autenticado_admin:
    vista_admin()
elif st.session_state.usuario_activo:
    vista_usuario()
else:
    vista_registro()
