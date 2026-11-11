import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="AdSelect - Panel de Control",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para panel oscuro limpio
st.markdown("""
<style>
    .metric-card {
        background-color: #1c1c20;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #2d2d35;
    }
    .ad-card {
        background-color: #1e1e24;
        border: 1px solid #2f2f38;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de campañas en sesión
if "campanas" not in st.session_state:
    st.session_state.campanas = [
        {
            "id": 1,
            "nombre": "Campaña Conversión Promo VIP",
            "plataforma": "TikTok Reels",
            "estado": "Activo",
            "clics": "3,120 clics",
            "presupuesto": 15.0,
            "audiencia": "Radio Local (10 km)"
        },
        {
            "id": 2,
            "nombre": "Re-engagement Audiencia Local",
            "plataforma": "Instagram Feed",
            "estado": "Activo",
            "clics": "1,240 clics",
            "presupuesto": 10.0,
            "audiencia": "Público General 18-35"
        },
        {
            "id": 3,
            "nombre": "Lanzamiento Edición Especial",
            "plataforma": "Historias / Shorts",
            "estado": "Pausado",
            "clics": "470 clics",
            "presupuesto": 5.0,
            "audiencia": "Intereses: Moda & Estilo"
        },
        {
            "id": 4,
            "nombre": "Branding Apertura de Semana",
            "plataforma": "Display Red",
            "estado": "Activo",
            "clics": "890 clics",
            "presupuesto": 8.0,
            "audiencia": "Remarketing"
        }
    ]

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.title("AdSelect")
    st.caption("Plataforma de Optimización Publicitaria")
    st.markdown("---")

    menu = st.radio(
        "Navegación",
        ["Panel General", "Mis Creativos", "Rendimiento / ROI", "Presupuesto & Facturación"],
        index=0
    )

    st.markdown("---")
    with st.container():
        st.caption("Saldo disponible en cuenta")
        st.subheader("$350.00 USD")
        st.caption("Método principal: Binance / Tarjeta")

# ----------------- ENCABEZADO Y ACCIÓN RÁPIDA -----------------
col_head, col_action = st.columns([3, 1])

with col_head:
    st.title("Gestor de Anuncios Activos")
    st.caption("Supervisa impresiones, rendimiento y distribución presupuestaria en tiempo real.")

with col_action:
    st.write("")
    modal_abrir = st.button("+ Nuevo Creativo", use_container_width=True, type="primary")

if modal_abrir:
    st.info("Formulario para subir material audiovisual (Reels, TikTok, Posts) habilitado abajo.")

# ----------------- TARJETAS DE MÉTRICAS (KPIs) -----------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Impresiones", value="124,520", delta="+12.4%")
with kpi2:
    st.metric(label="Clics Totales", value="4,830", delta="+8.1%")
with kpi3:
    st.metric(label="CTR Medio", value="3.88%", delta="+0.45%")
with kpi4:
    st.metric(label="Gasto Diario", value="$38.00", delta="-$7.20")

st.divider()

# ----------------- CUERPO PRINCIPAL -----------------
col_listado, col_control = st.columns([1.8, 1.2], gap="large")

with col_listado:
    st.subheader("Campañas & Creativos en Circulación")

    for i, camp in enumerate(st.session_state.campanas):
        with st.container():
            c_info, c_badge, c_toggle = st.columns([3, 1, 1])

            with c_info:
                st.markdown(f"**{camp['nombre']}**")
                st.caption(f"{camp['plataforma']}  •  {camp['clics']}  •  ${camp['presupuesto']:.2f}/día")

            with c_badge:
                if camp["estado"] == "Activo":
                    st.success("Activo")
                else:
                    st.warning("Pausado")

            with c_toggle:
                boton_label = "Pausar" if camp["estado"] == "Activo" else "Activar"
                if st.button(boton_label, key=f"btn_toggle_{camp['id']}", use_container_width=True):
                    camp["estado"] = "Pausado" if camp["estado"] == "Activo" else "Activo"
                    st.rerun()

            st.markdown("<hr style='margin: 8px 0; border-color: #2b2b36;'>", unsafe_allow_html=True)

with col_control:
    st.subheader("Control del Anuncio")

    with st.container(border=True):
        st.markdown("**Vista Previa del Creativo**")
        st.markdown(
            """
            <div style="background-color: #0e0e11; border: 2px dashed #3f3f4e; border-radius: 8px; height: 160px; display: flex; align-items: center; justify-content: center; color: #71717a;">
                Formatos 9:16 / 1:1 Activo
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")

        # Selección de campaña para editar
        opciones_campanas = [c["nombre"] for c in st.session_state.campanas]
        campana_sel_nombre = st.selectbox("Seleccionar Campaña", opciones_campanas)
        campana_sel = next(c for c in st.session_state.campanas if c["nombre"] == campana_sel_nombre)

        # Ajuste de presupuesto
        nuevo_presupuesto = st.slider(
            "Presupuesto Diario (USD)",
            min_value=5.0,
            max_value=150.0,
            value=float(campana_sel["presupuesto"]),
            step=1.0
        )

        # Segmentación
        nueva_audiencia = st.selectbox(
            "Audiencia Objetivo",
            ["Radio Local (10 km)", "Público General 18-35", "Intereses: Moda & Estilo", "Remarketing"],
            index=["Radio Local (10 km)", "Público General 18-35", "Intereses: Moda & Estilo", "Remarketing"].index(campana_sel["audiencia"])
        )

        # Switch de emisión
        estado_switch = st.toggle("Campaña en Emisión", value=(campana_sel["estado"] == "Activo"))

        if st.button("Guardar y Aplicar Cambios", type="primary", use_container_width=True):
            campana_sel["presupuesto"] = nuevo_presupuesto
            campana_sel["audiencia"] = nueva_audiencia
            campana_sel["estado"] = "Activo" if estado_switch else "Pausado"
            st.success(f"Cambios aplicados a '{campana_sel['nombre']}'")
            st.rerun()
