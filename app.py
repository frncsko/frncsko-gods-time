import base64
import sqlite3
import urllib.parse
import pandas as pd
import streamlit as st

# 1. Configuración inicial de la página
st.set_page_config(page_title="Barbería Gods Time", page_icon="💈", layout="wide")

# --- EFECTO / AMBIENTACIÓN DE HALLOWEEN ---
st.markdown(
    """
    <style>
    .halloween-banner {
        background: linear-gradient(90deg, #1f1b24, #3b2a1a);
        border: 2px solid #ff7518;
        padding: 10px;
        border-radius: 8px;
        color: #ffb020;
        text-align: center;
        font-weight: bold;
        box-shadow: 0px 0px 10px rgba(255, 117, 24, 0.5);
    }
    </style>
    
    <div class="halloween-banner">
        🎃 ¡Modo Halloween Activo en Barbería God's Time! 👻
    </div>
    """,
    unsafe_allow_html=True
)

activar_halloween = st.sidebar.checkbox("🎃 Activar Efecto Halloween", value=False)

if activar_halloween:
    st.sidebar.markdown(
        """
        <div style="background-color: #2e1a47; padding: 10px; border-radius: 5px; text-align: center; color: #ff9900; border: 1px dashed #ff7518;">
            🕸️ <i>Ambiente tenebroso activado</i> 🕷️
        </div>
        """,
        unsafe_allow_html=True
    )


# --- CONEXIÓN Y CONFIGURACIÓN DE BASE DE DATOS SQLITE ---
def inicializar_bd():
    conn = sqlite3.connect("barberia_godstime.db")
    cursor = conn.cursor()

    # Tabla de Servicios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            cliente TEXT,
            telefono TEXT,
            barbero TEXT,
            servicio TEXT,
            precio REAL
        )
    """)

    # Tabla de Gastos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            barbero_asignacion TEXT,
            descripcion TEXT,
            monto REAL
        )
    """)

    # Tabla de Fiados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fiados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            telefono TEXT,
            deuda REAL,
            estado TEXT
        )
    """)
    
    conn.commit()
    conn.close()


# Ejecutar la inicialización
inicializar_bd()

# Configuración de listas generales
lista_barberos = ["Barbero 1", "Barbero 2", "Barbero 3"]
servicios_lista = ["Corte Clásico", "Corte y Barba", "Barba", "Corte Infantil"]

# Funciones de apoyo para la BD
def ejecutar_sql(query, params=()):
    conn = sqlite3.connect("barberia_godstime.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def cargar_datos(tabla):
    conn = sqlite3.connect("barberia_godstime.db")
    df = pd.read_sql(f"SELECT * FROM {tabla}", conn)
    conn.close()
    return df


# --- MENÚ LATERAL Y NAVEGACIÓN (SIN CITAS) ---
st.sidebar.title("💈 Barbería God's Time")
st.sidebar.markdown("---")

opcion_menu = st.sidebar.selectbox(
    "Menú Principal",
    [
        "✂️ Registrar Servicio",
        "⏰ Recordatorio de Cortes",
        "👥 Barberos y Comisión",
        "📤 Gastos del Local",
        "🔍 Verificar Pagos",
        "📝 Cobrar Fiados",
    ],
)

# ==========================================
# 1. REGISTRAR SERVICIO
# ==========================================
if opcion_menu == "✂️ Registrar Servicio":
    st.header("✂️ Registrar Nuevo Servicio")
    st.write("Llena los datos del cliente y el servicio realizado.")

    with st.form("form_servicio", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            cliente_corte = st.text_input("Nombre del Cliente")
            telefono_corte = st.text_input("Número de Teléfono (ej. +584121234567)")
            barbero_asigna = st.selectbox("Barbero que Atendió", lista_barberos)
        with col2:
            tipo_servicio = st.selectbox("Tipo de Servicio", servicios_lista)
            precio_servicio = st.number_input("Precio ($)", min_value=0.0, step=1.0)

        submit_servicio = st.form_submit_button("✂️ Registrar Servicio")

        if submit_servicio and cliente_corte:
            fecha_actual = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            ejecutar_sql(
                "INSERT INTO servicios (fecha, cliente, telefono, barbero, servicio, precio) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    fecha_actual,
                    cliente_corte,
                    telefono_corte if telefono_corte else "N/A",
                    barbero_asigna,
                    tipo_servicio,
                    precio_servicio,
                ),
            )
            st.success("¡Servicio registrado y guardado permanentemente!")
            st.rerun()

# ==========================================
# 2. RECORDATORIO DE CORTES
# ==========================================
elif opcion_menu == "⏰ Recordatorio de Cortes":
    st.header("⏰ Recordatorio de Mantenimiento / Próximo Corte")
    st.write("Notifica a tus clientes habituales cuando ya ha transcurrido cierto tiempo desde su último corte.")

    dias_limite = st.slider(
        "Días promedio para volver a cortar",
        min_value=7,
        max_value=60,
        value=21,
    )

    df_serv = cargar_datos("servicios")

    if not df_serv.empty:
        df_serv["Fecha_dt"] = pd.to_datetime(df_serv["fecha"])
        hoy = pd.Timestamp.now()

        ultimos_cortes = df_serv.groupby("cliente").last().reset_index()
        ultimos_cortes["Dias_transcurridos"] = (hoy - ultimos_cortes["Fecha_dt"]).dt.days

        clientes_para_recordar = ultimos_cortes[
            ultimos_cortes["Dias_transcurridos"] >= dias_limite
        ]

        if not clientes_para_recordar.empty:
            st.subheader(f"Se encontraron {len(clientes_para_recordar)} clientes listos para un nuevo corte:")
            for _, row in clientes_para_recordar.iterrows():
                with st.expander(f"👤 {row['cliente']} (Hace {row['Dias_transcurridos']} días)"):
                    st.write(f"**Servicio anterior:** {row['servicio']} - {row['fecha']}")
                    st.write(f"**Número de Teléfono:** {row['telefono']}")

                    tel_clean = "".join(filter(str.isdigit, str(row["telefono"])))
                    if tel_clean:
                        msg = urllib.parse.quote(
                            f"Hola {row['cliente']}! Saludos de Barbería Gods Time. Ya pasaron {row['Dias_transcurridos']} días desde tu último corte. ¿Te agendamos un espacio esta semana?"
                        )
                        wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                        st.markdown(
                            f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Enviar Recordatorio por WhatsApp</button></a>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.caption("Sin número válido registrado.")
        else:
            st.info("No hay clientes que hayan superado el límite de días seleccionado.")
    else:
        st.info("Registra servicios primero para calcular los recordatorios.")

# ==========================================
# 3. BARBEROS Y COMISIONES
# ==========================================
elif opcion_menu == "👥 Barberos y Comisión":
    st.header("👥 Control de Comisiones y Balance por Barbero")
    st.write("Calcula el porcentaje de comisión, resta los gastos asignados a cada barbero y obtiene la ganancia neta.")

    comision_pct = (
        st.slider(
            "Porcentaje de comisión para el barbero (%)",
            min_value=0,
            max_value=100,
            value=50,
        )
        / 100.0
    )

    df_serv = cargar_datos("servicios")
    df_gastos = cargar_datos("gastos")

    if not df_serv.empty:
        resumen_barberos = []
        for barbero in lista_barberos:
            serv_b = df_serv[df_serv["barbero"] == barbero]
            total_gen = serv_b["precio"].sum() if not serv_b.empty else 0.0
            comision_bruta = total_gen * comision_pct

            gastos_b = (
                df_gastos[df_gastos["barbero_asignacion"] == barbero]["monto"].sum()
                if not df_gastos.empty
                else 0.0
            )

            pago_neto = comision_bruta - gastos_b
            monto_local = total_gen - comision_bruta

            resumen_barberos.append(
                {
                    "Barbero": barbero,
                    "Total Generado ($)": total_gen,
                    "Comisión Bruta ($)": comision_bruta,
                    "Gastos Personales ($)": gastos_b,
                    "Pago Neto Barbero ($)": pago_neto,
                    "Para el Local ($)": monto_local,
                }
            )

        df_resumen = pd.DataFrame(resumen_barberos)
        st.dataframe(df_resumen, use_container_width=True)
    else:
        st.info("Registra servicios en la opción correspondiente para visualizar el desglose de comisiones.")

# ==========================================
# 4. GASTOS DEL LOCAL
# ==========================================
elif opcion_menu == "📤 Gastos del Local":
    st.header("📤 Gastos de la Barbería y Barberos")
    st.write("Registra compras de insumos, adelantos o gastos operacionales asignados a cada barbero o al local.")

    opciones_asignacion = ["General / Local"] + lista_barberos

    with st.form("form_gastos"):
        quien_gasto = st.selectbox("¿A quién corresponde este gasto?", opciones_asignacion)
        desc_gasto = st.text_input("Descripción del gasto (ej. Cuchillas, gel, adelanto, etc.)")
        monto_gasto = st.number_input("Monto ($)", min_value=0.0, step=0.5)

        submit_gasto = st.form_submit_button("Guardar Gasto")

        if submit_gasto and desc_gasto:
            fecha_actual = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            ejecutar_sql(
                "INSERT INTO gastos (fecha, barbero_asignacion, descripcion, monto) VALUES (?, ?, ?, ?)",
                (fecha_actual, quien_gasto, desc_gasto, monto_gasto),
            )
            st.success("Gasto registrado y guardado permanentemente.")
            st.rerun()

    st.markdown("---")
    st.subheader("Historial General de Gastos")
    df_gastos = cargar_datos("gastos")
    if not df_gastos.empty:
        df_mostrar_g = df_gastos[["fecha", "barbero_asignacion", "descripcion", "monto"]].rename(
            columns={
                "fecha": "Fecha",
                "barbero_asignacion": "Barbero / Asignación",
                "descripcion": "Descripción",
                "monto": "Monto ($)",
            }
        )
        st.dataframe(df_mostrar_g, use_container_width=True)
    else:
        st.info("Aún no se han registrado gastos.")

# ==========================================
# 5. VERIFICAR PAGOS DE CLIENTES
# ==========================================
elif opcion_menu == "🔍 Verificar Pagos":
    st.header("🔍 Verificación de Pagos por Cliente")
    st.write("Busca y consulta el historial de pagos y servicios realizados por cada cliente en la barbería.")

    df_servicios = cargar_datos("servicios")

    if not df_servicios.empty:
        lista_clientes = sorted(df_servicios["cliente"].unique().tolist())
        cliente_seleccionado = st.selectbox("Selecciona o busca un cliente", lista_clientes)

        if cliente_seleccionado:
            df_cliente_serv = df_servicios[df_servicios["cliente"] == cliente_seleccionado]

            total_pagado_cliente = df_cliente_serv["precio"].sum()
            telefono_cliente = df_cliente_serv["telefono"].iloc[0] if not df_cliente_serv.empty else "N/A"
            cantidad_visitas = len(df_cliente_serv)

            col_v1, col_v2, col_v3 = st.columns(3)
            col_v1.metric("Total Pagado Acumulado", f"${total_pagado_cliente:,.2f}")
            col_v2.metric("Servicios / Visitas", cantidad_visitas)
            col_v3.metric("Teléfono de Contacto", str(telefono_cliente) if telefono_cliente else "N/A")

            st.markdown("---")
            st.subheader(f"Historial de Pagos de: {cliente_seleccionado}")

            df_mostrar_cli = df_cliente_serv[["fecha", "barbero", "servicio", "precio"]].rename(
                columns={
                    "fecha": "Fecha y Hora",
                    "barbero": "Barbero Atendió",
                    "servicio": "Servicio",
                    "precio": "Monto Pagado ($)",
                }
            )
            st.dataframe(df_mostrar_cli, use_container_width=True)

            tel_clean = "".join(filter(str.isdigit, str(telefono_cliente)))
            if tel_clean and tel_clean != "N/A":
                detalle_servicios_str = ""
                for _, s_row in df_cliente_serv.iterrows():
                    detalle_servicios_str += f"- {s_row['fecha']}: {s_row['servicio']} (${s_row['precio']:,.2f})\n"

                msg_wsp_pago = urllib.parse.quote(
                    f"Hola {cliente_seleccionado}, aquí tienes el resumen y verificación de tus pagos en Barbería Gods Time:\n\n"
                    f"{detalle_servicios_str}\n"
                    f"💵 *Total Acumulado Pagado:* ${total_pagado_cliente:,.2f}\n\n"
                    f"¡Gracias por tu preferencia y confianza!"
                )
                wsp_pago_url = f"https://wa.me/{tel_clean}?text={msg_wsp_pago}"
                st.markdown(
                    f'<a href="{wsp_pago_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 16px; border-radius:6px; font-weight:bold; cursor:pointer; width:100%;">💬 Enviar Resumen de Pagos por WhatsApp</button></a>',
                    unsafe_allow_html=True,
                )
            else:
                st.caption("El cliente no cuenta con un número de teléfono válido registrado para enviar el resumen por WhatsApp.")
    else:
        st.info("No hay servicios registrados en la base de datos todavía.")

# ==========================================
# 6. COBRAR FIADOS
# ==========================================
elif opcion_menu == "📝 Cobrar Fiados":
    st.header("📝 Cuentas Pendientes y Cobro (Fiados)")

    with st.form("form_fiados"):
        cli_fiado = st.text_input("Nombre del Cliente")
        tel_fiado = st.text_input("Número de Teléfono (ej. +584121234567)")
        monto_fiado = st.number_input("Saldo Pendiente ($)", min_value=0.0, step=1.0)

        submit_fiado = st.form_submit_button("Registrar Deuda")

        if submit_fiado and cli_fiado:
            ejecutar_sql(
                "INSERT INTO fiados (cliente, telefono, deuda, estado) VALUES (?, ?, ?, ?)",
                (cli_fiado, tel_fiado if tel_fiado else "N/A", monto_fiado, "Pendiente"),
            )
            st.success("Deuda registrada correctamente.")
            st.rerun()

    st.markdown("---")
    st.subheader("Cuentas Pendientes")

    df_fiados = cargar_datos("fiados")
    if not df_fiados.empty:
        for idx, row in df_fiados.iterrows():
            with st.expander(f"📌 {row['cliente']} - ${row['deuda']:,.2f}"):
                st.write(f"**Número de Teléfono:** {row['telefono']}")

                tel_clean = "".join(filter(str.isdigit, str(row["telefono"])))
                if tel_clean:
                    msg = urllib.parse.quote(
                        f"Hola {row['cliente']}, te recordamos que tienes un saldo pendiente de ${row['deuda']:,.2f} en Barbería Gods Time."
                    )
                    wsp_url = f"https://wa.me/{tel_clean}?text={msg}"
                    st.markdown(
                        f'<a href="{wsp_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:8px 12px; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Cobrar por WhatsApp</button></a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("Sin número válido registrado.")

                st.write("")
                if st.button(f"Marcar como Pagado ({row['cliente']})", key=f"pay_debt_{row['id']}"):
                    ejecutar_sql("DELETE FROM fiados WHERE id = ?", (row["id"],))
                    st.success("¡Deuda saldada!")
                    st.rerun()
    else:
        st.info("No hay cuentas pendientes.")
