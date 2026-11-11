import streamlit as st

st.set_page_config(
    page_title="Fran ADS",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------- CREDENCIALES ADMINISTRADOR -----------------
ADMIN_USER = "fran"
ADMIN_PASS = "1234"

# ----------------- ESTADOS DE SESIÓN -----------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "mostrar_login" not in st.session_state:
    st.session_state.mostrar_login = False

# Saldo del administrador configurado en $50,000.00 USD
if "saldo_admin" not in st.session_state:
    st.session_state.saldo_admin = 50000.00

# Saldo para usuario nuevo (bono inicial)
if "saldo_nuevo_usuario" not in st.session_state:
    st.session_state.saldo_nuevo_usuario = 10.00

# Historial de transferencias
if "historial_envios" not in st.session_state:
    st.session_state.historial_envios = []

# ----------------- ESTILOS NEGRO CON AZUL -----------------
st.markdown("""
<style>
    .stApp {
        background-color: #030712;
        color: #f8fafc;
    }
    header, footer {
        visibility: hidden;
    }
    .block-container {
        max-width: 440px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Tarjeta estilo crédito */
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
# VISTA 1: USUARIO NUEVO (ESTILO ADSELECT NEGRO Y AZUL)
# =========================================================
def vista_usuario_nuevo():
    c_logo, c_admin = st.columns([3, 1])
    with c_admin:
        if st.button("Acceso Admin", use_container_width=True):
            st.session_state.mostrar_login = not st.session_state.mostrar_login
            st.rerun()

    if st.session_state.mostrar_login:
        with st.container(border=True):
            st.caption("Panel Administrativo (fran / 1234)")
            user = st.text_input("Usuario", key="login_u")
            clave = st.text_input("Clave", type="password", key="login_p")
            if st.button("Ingresar", type="primary", use_container_width=True):
                if user == ADMIN_USER and clave == ADMIN_PASS:
                    st.session_state.autenticado = True
                    st.session_state.mostrar_login = False
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

    # 1. Tarjeta estilo crédito
    st.markdown(f"""
    <div class="credit-card">
        <div class="card-brand">FRAN ADS</div>
        <div class="card-chip"></div>
        <div class="card-balance">${st.session_state.saldo_nuevo_usuario:.2f}</div>
        <div class="card-user">NUEVO MIEMBRO</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Botón Cash Out
    col_co1, col_co2, col_co3 = st.columns([1, 2, 1])
    with col_co2:
        if st.button("Cash Out", key="btn_cashout", use_container_width=True, type="primary"):
            st.info("Mínimo de retiro: $50.00 USD. Completa las condiciones para retirar.")

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
            Has recibido $10.00 USD por registrarte mediante enlace de invitación.
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
            $10.00
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# VISTA 2: PANEL DE ADMINISTRADOR CON OPCIÓN DE ENVIAR DINERO
# =========================================================
def vista_admin():
    with st.sidebar:
        st.title("Fran ADS")
        st.caption("Consola Administrativa")
        st.divider()

        menu = st.radio(
            "Menú",
            ["Panel General", "Enviar Dinero", "Mis Creativos", "Programa de Referidos"],
            index=0
        )

        st.divider()
        # Muestra tu dinero disponible de 50.000$
        st.metric("Mi Dinero Disponible", f"${st.session_state.saldo_admin:,.2f} USD")

        st.divider()
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

    # OPCIÓN: ENVIAR DINERO A USUARIOS NUEVOS
    if menu == "Enviar Dinero":
        st.title("Enviar Dinero a Usuarios")
        st.caption("Transfiere saldo directamente a la tarjeta de un nuevo miembro.")

        with st.container(border=True):
            st.subheader(f"Fondos disponibles: ${st.session_state.saldo_admin:,.2f} USD")
            st.write("")

            with st.form("form_enviar_fondos", clear_on_submit=True):
                nombre_dest = st.text_input("Nombre del usuario destinatario", placeholder="Ej. Carlos Mendoza")
                monto_envio = st.number_input("Monto a enviar (USD)", min_value=1.0, max_value=float(st.session_state.saldo_admin), value=10.0, step=5.0)

                btn_transferir = st.form_submit_button("Transferir Fondos", type="primary", use_container_width=True)

                if btn_transferir:
                    if not nombre_dest.strip():
                        st.error("Por favor, ingresa el nombre del usuario.")
                    elif monto_envio > st.session_state.saldo_admin:
                        st.error("Saldo insuficiente para realizar el envío.")
                    else:
                        st.session_state.saldo_admin -= monto_envio
                        st.session_state.saldo_nuevo_usuario += monto_envio
                        st.session_state.historial_envios.insert(0, {
                            "usuario": nombre_dest,
                            "monto": monto_envio
                        })
                        st.success(f"¡Envío exitoso! Se transfirieron ${monto_envio:,.2f} USD a {nombre_dest}.")
                        st.rerun()

        # Historial de envíos recientes
        if st.session_state.historial_envios:
            st.divider()
            st.subheader("Envíos Recientes")
            for item in st.session_state.historial_envios:
                with st.container(border=True):
                    col_u, col_m = st.columns([3, 1])
                    col_u.write(f"Destinatario: **{item['usuario']}**")
                    col_m.write(f"**-${item['monto']:,.2f} USD**")

    # OPCIÓN: PROGRAMA DE REFERIDOS
    elif menu == "Programa de Referidos":
        st.title("Programa de Referidos")
        st.write("Comparte este enlace para nuevos usuarios con bono:")
        st.code("https://frncsko-gods-time.streamlit.app/?ref=FRAN10", language="text")

    # OPCIÓN: PANEL GENERAL
    else:
        st.title("Panel de Control - Fran ADS")
        st.caption("Resumen general y métricas de la plataforma.")

        k1, k2 = st.columns(2)
        k1.metric("Mi Dinero Total", f"${st.session_state.saldo_admin:,.2f} USD")
        k2.metric("Total Envíos Realizados", f"{len(st.session_state.historial_envios)}")

        st.divider()
        st.info("Para asignar saldos a miembros específicos, ingresa a la opción 'Enviar Dinero' en el menú lateral.")


# =========================================================
# CONTROL PRINCIPAL
# =========================================================
if st.session_state.autenticado:
    vista_admin()
else:
    vista_usuario_nuevo()
