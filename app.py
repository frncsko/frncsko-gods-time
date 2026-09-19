import streamlit as st
import pandas as pd
import json
import os
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="MI SASÓN.CA - Menú Oscuro",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILO CSS PERSONALIZADO (Dark Mode Gastronómico con Fondos HD)
st.markdown("""
    <style>
    /* Fondo principal oscuro con textura de comida */
    .stApp {
        background: linear-gradient(rgba(15, 15, 20, 0.88), rgba(15, 15, 20, 0.95)), 
                    url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1600') no-repeat center center fixed;
        background-size: cover;
        color: #f1f2f6;
    }

    /* Barra lateral oscura */
    [data-testid="stSidebar"] {
        background-color: #121216 !important;
        border-right: 1px solid #2a2a35;
    }

    /* Tarjetas de platillos en estilo Glassmorphism (Cristal Oscuro) */
    .card-plato-dark {
        background: rgba(26, 26, 36, 0.85);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 18px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #ff4757;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    .badge-categoria-dark {
        background-color: #ff4757;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .precio-highlight-dark {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2ed573;
        margin-top: 8px;
    }

    /* Ajustes generales de texto e inputs */
    h1, h2, h3, h4, label {
        color: #ffffff !important;
    }
    
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1a24 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración de Moneda y Datos
TASA_BS = 40.00
TELEFONO_RESTAURANTE = "584120000000"

# 2. ARCHIVOS LOCALES
MENU_FILE = "restaurante_menu.json"
GASTOS_FILE = "restaurante_gastos.json"

MENU_POR_DEFECTO = [
    {"id": 1, "nombre": "Empanadas Criollas (3 uds)", "categoria": "Desayunos", "precio": 3.50, "descripcion": "Empanadas de carne mechada, queso o pollo con guasacaca.", "imagen": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=500"},
    {"id": 2, "nombre": "Pabellón Criollo", "categoria": "Almuerzos", "precio": 9.00, "descripcion": "Carne mechada, caraotas negras, arroz blanco y tajadas de plátano frito.", "imagen": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500"},
    {"id": 3, "nombre": "Hamburguesa Especial", "categoria": "Cenas / Rápidas", "precio": 7.50, "descripcion": "Carne 180g, queso de mano, tocineta, huevo frito y papas hilo.", "imagen": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500"},
    {"id": 4, "nombre": "Jugo Natural (500ml)", "categoria": "Bebidas", "precio": 2.00, "descripcion": "Jugo natural frito de parchita, melón o mora.", "imagen": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500"}
]

def cargar_json(archivo, por_defecto):
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return por_defecto
    return por_defecto

def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# 3. ESTADOS DE SESIÓN
if "menu" not in st.session_state:
    st.session_state.menu = cargar_json(MENU_FILE, MENU_POR_DEFECTO)

if "gastos" not in st.session_state:
    st.session_state.gastos = cargar_json(GASTOS_FILE, [])

if "carrito" not in st.session_state:
    st.session_state.carrito = {}

# Funciones de carrito
def agregar_al_carrito(plato_id):
    st.session_state.carrito[plato_id] = st.session_state.carrito.get(plato_id, 0) + 1

def remover_del_carrito(plato_id):
    if plato_id in st.session_state.carrito:
        if st.session_state.carrito[plato_id] > 1:
            st.session_state.carrito[plato_id] -= 1
        else:
            del st.session_state.carrito[plato_id]

# 4. BARRA LATERAL (NAVEGACIÓN MODERNA)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3448/3448650.png", width=70)
st.sidebar.title("MI SASÓN.CA")
st.sidebar.caption(f"Tasa del día: 1 USD = {TASA_BS:.2f} Bs.")
st.sidebar.markdown("---")

seccion = st.sidebar.radio(
    "Navegación",
    ["📖 Menú Digital", "🛒 Carrito de Compras", "📊 Panel de Control & Gastos"]
)

# 5. VISTAS PRINCIPALES

# --- VISTA 1: MENÚ DIGITAL ---
if seccion == "📖 Menú Digital":
    st.title("📖 MI SASÓN.CA - Menú Digital")
    st.write("Desayunos, Almuerzos y las mejores especialidades.")
    
    categorias = ["Todos", "Desayunos", "Almuerzos", "Cenas / Rápidas", "Bebidas"]
    cat_sel = st.selectbox("Filtrar por comida:", categorias)
    
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        for plato in st.session_state.menu:
            if cat_sel == "Todos" or plato["categoria"] == cat_sel:
                st.markdown(f"""
                <div class="card-plato-dark">
                    <span class="badge-categoria-dark">{plato['categoria']}</span>
                    <h3 style="margin-top: 10px; margin-bottom: 5px;">{plato['nombre']}</h3>
                    <p style="color: #a4b0be; font-size: 0.9rem;">{plato['descripcion']}</p>
                    <div class="precio-highlight-dark">${plato['precio']:.2f} USD <small style="color: #747d8c; font-size: 0.85rem;">({plato['precio']*TASA_BS:.2f} Bs.)</small></div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.image(plato["imagen"], width=110)
                with c2:
                    st.button("➕ Añadir al Pedido", key=f"btn_add_{plato['id']}", on_click=agregar_al_carrito, args=(plato['id'],), type="primary")
                st.markdown("<br>", unsafe_allow_html=True)

    with col_der:
        st.info("💡 **Tip:** Añade tus platos preferidos y presiona **🛒 Carrito de Compras** en el menú lateral para enviar tu orden por WhatsApp.")

# --- VISTA 2: CARRITO DE COMPRAS ---
elif seccion == "🛒 Carrito de Compras":
    st.title("🛒 Carrito de Compras")
    
    if not st.session_state.carrito:
        st.warning("Tu carrito está vacío. Agrega platos desde el menú.")
    else:
        total_usd = 0.0
        resumen_texto = []
        
        for p_id, cantidad in list(st.session_state.carrito.items()):
            plato = next((p for p in st.session_state.menu if p["id"] == p_id), None)
            if plato:
                subtotal = plato["precio"] * cantidad
                total_usd += subtotal
                
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.markdown(f"**{plato['nombre']}**\n${plato['precio']:.2f} USD c/u")
                c2.markdown(f"**x{cantidad}** (${subtotal:.2f})")
                
                with c3:
                    b1, b2 = st.columns(2)
                    b1.button("➖", key=f"sub_cart_{p_id}", on_click=remover_del_carrito, args=(p_id,))
                    b2.button("➕", key=f"add_cart_{p_id}", on_click=agregar_al_carrito, args=(p_id,))
                st.markdown("---")
                resumen_texto.append(f"• {plato['nombre']} x{cantidad} - ${subtotal:.2f}")

        total_bs = total_usd * TASA_BS
        st.markdown(f"### Total a pagar: <span style='color:#2ed573;'>${total_usd:.2f} USD</span> / {total_bs:.2f} Bs.", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📋 Datos para el Envío")
        
        tipo_servicio = st.radio("Modalidad:", ["Para Llevar", "Delivery", "Mesa"])
        nombre_cliente = st.text_input("Nombre del Cliente:")
        ubicacion = st.text_input("Número de Mesa / Dirección de Delivery:")
        
        if st.button("📲 Generar Orden por WhatsApp", type="primary"):
            if not nombre_cliente:
                st.error("Por favor ingresa tu nombre.")
            else:
                msg = f"*NUEVA ORDEN - MI SASÓN.CA*\n"
                msg += f"Cliente: {nombre_cliente}\nModalidad: {tipo_servicio}\n"
                if ubicacion:
                    msg += f"Ubicación/Mesa: {ubicacion}\n"
                msg += "-----------------------------------\n"
                for item in resumen_texto:
                    msg += f"{item}\n"
                msg += "-----------------------------------\n"
                msg += f"*TOTAL USD:* ${total_usd:.2f}\n"
                msg += f"*TOTAL BS:* {total_bs:.2f} Bs.\n"
                
                url_ws = f"https://wa.me/{TELEFONO_RESTAURANTE}?text={urllib.parse.quote(msg)}"
                st.success("¡Orden generada!")
                st.markdown(f"[👉 Enviar Pedido por WhatsApp]({url_ws})", unsafe_allow_html=True)

# --- VISTA 3: PANEL DE CONTROL, PROPINAS Y GASTOS ---
elif seccion == "📊 Panel de Control & Gastos":
    st.title("📊 Panel Administrativo - MI SASÓN.CA")
    st.write("Control interno de propinas para el personal y egresos operativos.")
    
    tab_propinas, tab_gastos, tab_resumen = st.tabs(["💰 Propinas Personal", "💸 Gastos / Egresos", "📈 Resumen"])
    
    # 1. TAB PROPINAS
    with tab_propinas:
        st.subheader("💰 Distribución de Propinas")
        with st.form("form_propinas", clear_on_submit=True):
            col1, col2 = st.columns(2)
            trabajador = col1.text_input("Nombre del Trabajador / Mesero:")
            monto_propina = col2.number_input("Monto de Propina ($ USD):", min_value=0.01, step=0.50)
            fecha_propina = col1.date_input("Fecha:", datetime.now())
            metodo_pago = col2.selectbox("Método de Pago:", ["Efectivo", "Pago Móvil", "Binance", "Tarjeta"])
            
            btn_propina = st.form_submit_button("Registrar Propina")
            
            if btn_propina:
                if not trabajador:
                    st.error("Ingresa el nombre del trabajador.")
                else:
                    nuevo_registro = {
                        "tipo": "Propina",
                        "concepto": f"Propina asignada a {trabajador}",
                        "monto_usd": monto_propina,
                        "monto_bs": monto_propina * TASA_BS,
                        "beneficiario": trabajador,
                        "metodo": metodo_pago,
                        "fecha": str(fecha_propina)
                    }
                    st.session_state.gastos.append(nuevo_registro)
                    guardar_json(GASTOS_FILE, st.session_state.gastos)
                    st.success(f"Propina de ${monto_propina:.2f} registrada para {trabajador}.")

    # 2. TAB GASTOS GENERALES
    with tab_gastos:
        st.subheader("💸 Registro de Egresos y Compras")
        with st.form("form_gastos", clear_on_submit=True):
            concepto = st.text_input("Concepto del Gasto (ej: Insumos de Almuerzo, Gas, Empaques):")
            c_monto, c_cat = st.columns(2)
            monto_gasto = c_monto.number_input("Monto ($ USD):", min_value=0.01, step=1.00)
            cat_gasto = c_cat.selectbox("Categoría de Gasto:", ["Insumos / Ingredientes", "Servicios (Luz/Gas/Agua)", "Mantenimiento", "Otros"])
            fecha_gasto = st.date_input("Fecha del Gasto:", datetime.now())
            
            btn_gasto = st.form_submit_button("Registrar Gasto")
            
            if btn_gasto:
                if not concepto:
                    st.error("Ingresa el concepto del gasto.")
                else:
                    nuevo_gasto = {
                        "tipo": "Gasto General",
                        "concepto": f"[{cat_gasto}] {concepto}",
                        "monto_usd": monto_gasto,
                        "monto_bs": monto_gasto * TASA_BS,
                        "beneficiario": "Proveedor/Servicio",
                        "metodo": "Caja Chica",
                        "fecha": str(fecha_gasto)
                    }
                    st.session_state.gastos.append(nuevo_gasto)
                    guardar_json(GASTOS_FILE, st.session_state.gastos)
                    st.success(f"Gasto de ${monto_gasto:.2f} registrado exitosamente.")

    # 3. TAB RESUMEN HISTÓRICO
    with tab_resumen:
        st.subheader("📜 Historial de Registros")
        if not st.session_state.gastos:
            st.info("No hay gastos ni propinas registradas aún.")
        else:
            df_gastos = pd.DataFrame(st.session_state.gastos)
            
            total_propinas = df_gastos[df_gastos["tipo"] == "Propina"]["monto_usd"].sum()
            total_egresos = df_gastos[df_gastos["tipo"] == "Gasto General"]["monto_usd"].sum()
            
            m1, m2 = st.columns(2)
            m1.metric("Total Propinas Repartidas", f"${total_propinas:.2f} USD", f"{total_propinas*TASA_BS:.2f} Bs.")
            m2.metric("Total Egresos Operativos", f"${total_egresos:.2f} USD", f"{total_egresos*TASA_BS:.2f} Bs.")
            
            st.markdown("---")
            st.dataframe(df_gastos, use_container_width=True)
