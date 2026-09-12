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
