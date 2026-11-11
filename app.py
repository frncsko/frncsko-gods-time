import streamlit as st

st.set_page_config(page_title="Fran ADS", layout="wide")

# Estados de sesion
if "saldo" not in st.session_state:
    st.session_state.saldo = 350.0

if "bono_listo" not in st.session_state:
    st.session_state.bono_listo = False

if "campanas" not in st.session_state:
    # Datos base compactados para evitar cortes de linea
    datos_raw = [
        (1, "Promo VIP", "TikTok Reels", "Activo", "3,120", 15.0, "Radio Local"),
        (2, "Audiencia Local", "Instagram Feed", "Activo", "1,240", 10.0, "General 18-35"),
        (3, "Lanzamiento Edicion", "Shorts", "Pausado", "470", 5.0, "Moda y Estilo"),
        (4, "Branding Semanal", "Display Red", "Activo", "890", 8.0, "Remarketing")
    ]
    st.session_state.campanas = [
        {"id": d[0], "nombre": d[1], "red": d[2], "estado": d[3], "clics": d[4], "presupuesto": d[5], "aud": d[6]}
        for d in datos_raw
    ]

# Deteccion segura de link de referido (?ref=...)
ref_code = None
try:
    if hasattr(st, "query_params"):
        ref_code = st.query_params.get("ref", None)
except Exception:
    pass

if ref_code and not st.session_state.bono_listo:
    st.session_state.saldo += 10.0
    st.session_state.bono_listo = True

# Barra lateral
with st.sidebar:
    st.title("Fran ADS")
    st.divider()
    menu = st.radio("Menu", ["Panel General", "Programa de Referidos"])
    st.divider()
    st.metric("Saldo Disponible", f"${st.session_state.saldo:.2f} USD")
    if st.session_state.bono_listo:
        st.success("Bono $10 USD activo")

# Secciones
if menu == "Programa de Referidos":
    st.title("Enlace de Registro y Bono")
    st.write("Comparte este enlace para nuevos usuarios ($10.00 USD de bienvenida):")
    st.code("https://frncsko-gods-time.streamlit.app/?ref=FRAN10", language="text")
    st.divider()
    st.subheader("Registro Manual")
    with st.form("form_ref"):
        nombre = st.text_input("Nombre de Usuario")
        enviar = st.form_submit_button("Registrar con Bono", type="primary")
        if enviar:
            if not st.session_state.bono_listo:
                st.session_state.saldo += 10.0
                st.session_state.bono_listo = True
                st.success(f"Usuario {nombre} registrado (+ $10.00 USD)")
                st.rerun()
            else:
                st.info("El bono ya fue aplicado en esta sesion.")
else:
    if st.session_state.bono_listo and ref_code:
        st.success("Bono de bienvenida de $10.00 USD acreditado exitosamente.")

    c_tit, c_btn = st.columns([3, 1])
    c_tit.title("Panel de Control - Fran ADS")
    c_btn.button("+ Nuevo Creativo", use_container_width=True, type="primary")

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Impresiones", "124,520", "+12.4%")
    k2.metric("Clics", "4,830", "+8.1%")
    k3.metric("CTR", "3.88%", "+0.45%")
    k4.metric("Gasto", "$38.00", "-$7.20")

    st.divider()
    col_izq, col_der = st.columns([1.8, 1.2], gap="large")

    with col_izq:
        st.subheader("Campanas en Circulacion")
        for c in st.session_state.campanas:
            with st.container(border=True):
                info, badge, accion = st.columns([3, 1, 1])
                info.markdown(f"**{c['nombre']}** ({c['red']})  \n{c['clics']} clics  •  ${c['presupuesto']:.2f}/dia")
                if c["estado"] == "Activo":
                    badge.success("Activo")
                else:
                    badge.warning("Pausado")
                btn_txt = "Pausar" if c["estado"] == "Activo" else "Activar"
                if accion.button(btn_txt, key=f"btn_{c['id']}", use_container_width=True):
                    c["estado"] = "Pausado" if c["estado"] == "Activo" else "Activo"
                    st.rerun()

    with col_der:
        st.subheader("Ajuste de Campana")
        with st.container(border=True):
            st.info("Formato 9:16 (TikTok / Reels)")
            nombres = [c["nombre"] for c in st.session_state.campanas]
            sel = st.selectbox("Seleccionar", nombres)
            item = next(x for x in st.session_state.campanas if x["nombre"] == sel)

            nuevo_p = st.slider("Presupuesto USD", 5.0, 150.0, float(item["presupuesto"]), 1.0)
            auds = ["Radio Local", "General 18-35", "Moda y Estilo", "Remarketing"]
            nueva_a = st.selectbox("Audiencia", auds, index=auds.index(item["aud"]) if item["aud"] in auds else 0)
            estado = st.toggle("En Emision", value=(item["estado"] == "Activo"))

            if st.button("Guardar Cambios", type="primary", use_container_width=True):
                item["presupuesto"] = nuevo_p
                item["aud"] = nueva_a
                item["estado"] = "Activo" if estado else "Pausado"
                st.success("Guardado con exito.")
                st.rerun()
