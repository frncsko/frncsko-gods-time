import streamlit as st
import pandas as pd
import json
import os
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Restaurante - Menú Digital",
    page_icon="🍔",
    layout="wide"
)

# Configuración de Moneda / Tasa de Cambio
TASA_BS = 40.00  # Cambiar por la tasa del día
TELEFONO_RESTAURANTE = "584120000000"  # Número con código de país (ej: 58 para Venezuela)

# 2. ARCHIVOS LOCALES (PERSISTENCIA)
MENU_FILE = "restaurante_menu.json"

MENU_POR_DEFECTO = [
    {"id": 1, "nombre": "Hamburguesa Doble Carne", "categoria": "Platos Fuertes", "precio": 8.50, "descripcion": "Dos carnes de 150g, queso cheddar, tocineta y salsa especial.", "imagen": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500"},
    {"id": 2, "nombre": "Papas Fritas Rústicas", "categoria": "Entradas", "precio": 3.50, "descripcion": "Papas crujientes sazonadas con especias y alioli.", "imagen": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500"},
    {"id": 3, "nombre": "Refresco 500ml", "categoria": "Bebidas", "precio": 1.50, "descripcion": "Lata fría de sabor a elección.", "imagen": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500"},
    {"id": 4, "nombre": "Brownie con Helado", "categoria": "Postres", "precio": 4.00, "descripcion": "Brownie tibio de chocolate servido con helado de vainilla.", "imagen": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500"}
]

def cargar_menu():
    if os.path.exists(MENU_FILE):
        try:
            with open(MENU_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return MENU_POR_DEFECTO
    return MENU_POR_DEFECTO

# 3. ESTADOS DE SESIÓN
if "menu" not in st.session_state:
    st.session_state.menu = cargar_menu()

if "carrito" not in st.session_state:
    st.session_state.carrito = {}

# 4. FUNCIONES DEL CARRITO
def agregar_al_carrito(plato_id):
    if plato_id in st.session_state.carrito:
        st.session_state.carrito[plato_id] += 1
    else:
        st.session_state.carrito[plato_id] = 1

def remover_del_carrito(plato_id):
    if plato_id in st.session_state.carrito:
        if st.session_state.carrito[plato_id] > 1:
            st.session_state.carrito[plato_id] -= 1
        else:
            del st.session_state.carrito[plato_id]

# 5. INTERFAZ PRINCIPAL
st.title("🍔 Menú Digital & Pedidos")
st.markdown(f"**Tasa de cambio referencial:** 1 USD = {TASA_BS:.2f} Bs.")

col_menu, col_carrito = st.columns([2, 1])

# --- COLUMNA 1: CATÁLOGO DE PLATILLOS ---
with col_menu:
    st.header("📖 Nuestro Menú")
    
    categorias = ["Todos", "Entradas", "Platos Fuertes", "Bebidas", "Postres"]
    cat_seleccionada = st.selectbox("Filtrar por categoría:", categorias)
    
    for plato in st.session_state.menu:
        if cat_seleccionada == "Todos" or plato["categoria"] == cat_seleccionada:
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(plato["imagen"], use_container_width=True)
                with c2:
                    st.subheader(plato["nombre"])
                    st.caption(plato["descripcion"])
                    precio_usd = plato["precio"]
                    precio_bs = precio_usd * TASA_BS
                    st.markdown(f"**${precio_usd:.2f} USD** / *{precio_bs:.2f} Bs.*")
                    st.button(f"➕ Agregar", key=f"add_{plato['id']}", on_click=agregar_al_carrito, args=(plato['id'],))
                st.markdown("---")

# --- COLUMNA 2: CARRITO Y CHECKOUT ---
with col_carrito:
    st.header("🛒 Tu Pedido")
    
    if not st.session_state.carrito:
        st.info("El carrito está vacío. Agrega platillos para comenzar.")
    else:
        total_usd = 0.0
        resumen_texto = []
        
        for p_id, cantidad in list(st.session_state.carrito.items()):
            plato = next((p for p in st.session_state.menu if p["id"] == p_id), None)
            if plato:
                subtotal = plato["precio"] * cantidad
                total_usd += subtotal
                
                st.write(f"**{plato['nombre']}** x{cantidad}")
                st.caption(f"Subtotal: ${subtotal:.2f} USD")
                
                col_b1, col_b2, _ = st.columns([1, 1, 2])
                col_b1.button("➖", key=f"sub_{p_id}", on_click=remover_del_carrito, args=(p_id,))
                col_b2.button("➕", key=f"add_cart_{p_id}", on_click=agregar_al_carrito, args=(p_id,))
                st.markdown("---")
                
                resumen_texto.append(f"• {plato['nombre']} x{cantidad} - ${subtotal:.2f}")

        total_bs = total_usd * TASA_BS
        st.subheader(f"Total: ${total_usd:.2f} USD")
        st.markdown(f"### **{total_bs:.2f} Bs.**")
        
        st.markdown("---")
        st.subheader("📋 Datos del Pedido")
        
        tipo_servicio = st.radio("Modalidad:", ["Para Llevar", "Delivery", "Mesa"])
        nombre_cliente = st.text_input("Tu Nombre:")
        detalle_adicional = st.text_input("Nº de Mesa / Dirección de Entrega:")
        
        if st.button("📲 Confirmar Pedido por WhatsApp", type="primary"):
            if not nombre_cliente:
                st.error("Por favor ingresa tu nombre antes de enviar.")
            else:
                # Construcción del mensaje para WhatsApp
                mensaje = f" *NUEVO PEDIDO - RESTAURANTE*\n"
                mensaje += f"-----------------------------------\n"
                mensaje += f"*Cliente:* {nombre_cliente}\n"
                mensaje += f"*Modalidad:* {tipo_servicio}\n"
                if detalle_adicional:
                    mensaje += f"*Ubicación/Mesa:* {detalle_adicional}\n"
                mensaje += f"-----------------------------------\n"
                mensaje += "*Detalle del Pedido:*\n"
                for item in resumen_texto:
                    mensaje += f"{item}\n"
                mensaje += f"-----------------------------------\n"
                mensaje += f"*TOTAL USD:* ${total_usd:.2f}\n"
                mensaje += f"*TOTAL BS:* {total_bs:.2f} Bs.\n\n"
                mensaje += "¡Quedo a la espera de su confirmación!"
                
                # Generar enlace de WhatsApp
                mensaje_encoded = urllib.parse.quote(mensaje)
                url_ws = f"https://wa.me/{TELEFONO_RESTAURANTE}?text={mensaje_encoded}"
                
                st.success("¡Pedido generado! Haz clic abajo para enviarlo:")
                st.markdown(f"[👉 Abrir WhatsApp para enviar pedido]({url_ws})", unsafe_allow_html=True)
