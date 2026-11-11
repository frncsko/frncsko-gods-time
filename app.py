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

if "saldo_nuevo_usuario" not in st.session_state:
    st.session_state.saldo_nuevo_usuario = 10.00  # Bono de $10 USD para nuevos usuarios

if "bonus_reclamado" not in st.session_state:
    st.session_state.bonus_reclamado = True

# ----------------- ESTILOS EXACTOS DE LA IMAGEN -----------------
st.markdown("""
<style>
    /* Fondo general oscuro estilo AdSelect */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    header, footer {
        visibility: hidden;
    }
    .block-container {
        max-width: 440px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Tarjeta principal estilo tarjeta de crédito */
    .credit-card {
        background: linear-gradient(145deg, #18181a 0%, #0d0d0f 100%);
        border: 1px solid #28282e;
        border-radius: 20px;
        padding: 24px;
        position: relative;
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        margin-bottom: 20px;
    }
    .card-brand {
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 3px;
        font-size: 13px;
        color: #9c9ca3;
        text-transform: uppercase;
    }
    .card-chip {
        position: absolute;
        top: 24px;
        right: 24px;
        width: 38px;
        height: 28px;
        background: linear-gradient(135deg, #d4af37 0%, #aa8c2c 100%);
        border-radius: 6px;
        border: 1px solid #7a631c;
    }
    .card-balance {
        font-family: 'Times New Roman', serif;
        font-size: 42px;
        font-weight: 500;
        color: #ffffff;
        margin: 25px 0 15px 0;
    }
    .card-user {
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        font-size: 12px;
        color: #8f8f99;
        text-transform: uppercase;
    }

    /* Botón Cash Out */
    div[data-testid="stButton"] > button.cashout-btn {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        height: 48px !important;
        width: 100% !important;
        border: none !important;
    }

    /* Tarjeta Daily Bonus */
    .bonus-card {
        background-color: #0f0f12;
        border: 1px solid #1f1f26;
        border-radius: 18px;
        padding: 16px;
        margin-top: 18px;
    }
    .streak-dots {
        display: flex;
        gap: 6px;
        margin: 12px 0;
    }
    .dot-active {
        width: 22px;
        height: 5px;
        background-color: #d4af37;
        border-radius: 4px;
    }
    .dot-inactive {
        width: 14px;
        height: 5px;
        background-color: #27272f;
        border-radius: 4px;
    }

    /* Caja Earned Today */
    .earned-card {
        background-color: #0a0a0d;
        border: 1px solid #1a1a22;
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
# VISTA 1: INTERFAZ DE USUARIO NUEVO (ESTILO ADSELECT)
# =========================================================
def vista_usuario_nuevo():
    # Barra superior discreta
    c_logo, c_admin = st.columns([3, 1])
    with c_admin:
        if st.button("Acceso Admin", use_container_width=True):
            st.session_state.mostrar_login = not st.session_state.mostrar_login
            st.rerun()

    # Formulario desplegable si toca "Acceso Admin"
    if st.session_state.mostrar_login:
        with st.container(border=True):
            st.caption("Panel Privado (fran / 1234)")
            user = st.text_input("Usuario", key="login_u")
            clave = st.text_input("Clave", type="password", key="login_p")
            if st.button("Ingresar al Gestor", type="primary", use_container_width=True):
                if user == ADMIN_USER and clave == ADMIN_PASS:
                    st.session_state.autenticado = True
                    st.session_state.mostrar_login = False
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

    # 1. Tarjeta bancaria negra (AdSelect Card)
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
        if st.button("Cash Out", key="btn_cashout", use_container_width=True):
            st.info("Mínimo de retiro: $50.00 USD. Completa tus misiones diarias para retirar.")

    # 3. Módulo Daily Bonus
    st.markdown("""
    <div class="bonus-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background-color: #1a1a20; border: 1px solid #2f2f3a; border-radius: 10px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 18px;">
                    🎁
                </div>
                <div>
                    <div style="font-weight: 600; font-size: 14px; color: #f4f4f5;">Daily Bonus • Day 1/30</div>
                    <div style="font-size: 11px; color: #71717a; letter-spacing: 1px;">NEXT 23:59:59</div>
                </div>
            </div>
            <div style="background-color: #1c1c22; border: 1px solid #2e2e38; color: #a1a1aa; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 600;">
                Claimed
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
        <div style="font-size: 11px; color: #71717a; line-height: 1.4;">
            Come back tomorrow to earn more bonuses. Miss a day and the streak restarts from day 1.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Sección Earned Today
    st.markdown("""
    <div class="earned-card">
        <div style="font-size: 11px; letter-spacing: 2px; color: #71717a; font-weight: 600; text-transform: uppercase;">
            EARNED TODAY
        </div>
        <div style="font-family: 'Times New Roman', serif; font-size: 18px; color: #d4af37; font-weight: 600;">
            $10.00
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# VISTA 2: PANEL DE ADMINISTRADOR EXCLUSIVO (FRAN / 1234)
# =========================================================
def vista_admin():
    with st.sidebar:
        st.title("Fran ADS")
        st.caption("Panel de Control Privado")
        st.divider()
        st.metric("Saldo Admin", "$350.00 USD")
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

    st.title("Consola Administrativa - Fran ADS")
    st.caption("Solo visible tras ingresar con usuario: fran")

    k1, k2, k3 = st.columns(3)
    k1.metric("Usuarios Nuevos", "48")
    k2.metric("Bonos Asignados", "$480.00 USD")
    k3.metric("Campañas Activas", "4")

    st.divider()
    st.subheader("Enlace Promocional de Invitación")
    st.code("https://frncsko-gods-time.streamlit.app/?ref=FRAN10", language="text")
    st.caption("Los usuarios que ingresen verán la tarjeta AdSelect con sus $10.00 USD acreditados.")


# =========================================================
# CONTROL PRINCIPAL
# =========================================================
if st.session_state.autenticado:
    vista_admin()
else:
    vista_usuario_nuevo()
