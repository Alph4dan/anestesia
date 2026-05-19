import streamlit as st
import pandas as pd
from datetime import datetime
import gspread

# Configuración de la página (Modo Quirófano Verde)
st.set_page_config(
    page_title="AnesthesiaLog | Green Edition", 
    page_icon="🌿", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS VISUALES AVANZADOS (CORRECCIÓN TOTAL DE COLORES) ---
st.markdown("""
    <style>
    /* Fondo general oscuro verde */
    .stApp {
        background-color: #022c22;
        color: #ecfdf5;
    }
    
    /* Contenedor del Formulario */
    div[data-testid="stForm"] {
        background-color: #064e3b !important;
        border: 1px solid #047857 !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
    }
    
    /* Títulos con gradiente esmeralda */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #6ee7b7 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    
    /* Color de las etiquetas (Labels) */
    label, p {
        color: #a7f3d0 !important;
        font-weight: 600 !important;
    }

    /* === DISEÑO BASE (Inputs, Textarea y Fecha) === */
    .stTextInput input, .stTextArea textarea, .stDateInput input, div[data-baseweb="select"] > div {
        background-color: #065f46 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important; /* Fuerza color blanco en el texto */
        border: 2px solid #059669 !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        font-size: 1rem !important;
    }
    
    /* === ARREGLO AGRESIVO PARA DESPLEGABLES (Selectbox) === */
    /* Fuerza el texto blanco dentro del cuadro de búsqueda del selectbox */
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    
    /* === ARREGLO PARA MULTISELECT (Etiquetas/Chips) === */
    span[data-baseweb="tag"] {
        background-color: #10b981 !important;
        border-radius: 6px !important;
        border: 1px solid #34d399 !important;
    }
    span[data-baseweb="tag"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* === ARREGLO PARA LA LISTA DE OPCIONES AL ABRIR === */
    ul[data-baseweb="menu"] {
        background-color: #065f46 !important;
        border: 1px solid #047857 !important;
    }
    ul[data-baseweb="menu"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* Efecto Glow al tocar el campo */
    .stTextInput input:focus, .stTextArea textarea:focus, .stDateInput input:focus, div[data-baseweb="select"] > div:focus-within {
        border-color: #34d399 !important;
        box-shadow: 0 0 0 4px rgba(52, 211, 153, 0.25) !important;
        background-color: #047857 !important;
    }

    /* === ARREGLO PARA EL BOTÓN PRINCIPAL === */
    div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        -webkit-text-fill-color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    div[data-testid="stForm"] button:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
    }
    
    /* Diseño del expander de notas */
    .streamlit-expanderHeader {
        background-color: #065f46 !important;
        border-radius: 10px !important;
        border: 1px solid #047857 !important;
    }
    .streamlit-expanderHeader * {
        color: #a7f3d0 !important;
        -webkit-text-fill-color: #a7f3d0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Función para conectar con Google Sheets
def conectar_google_sheets():
    try:
        credentials_info = {
            "type": st.secrets["connections"]["gsheets"]["type"],
            "project_id": st.secrets["connections"]["gsheets"]["project_id"],
            "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
            "private_key": st.secrets["connections"]["gsheets"]["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["connections"]["gsheets"]["client_email"],
            "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
            "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
        }
        gc = gspread.service_account_from_dict(credentials_info)
        url_hoja = st.secrets["connections"]["gsheets"]["spreadsheet"]
        sh = gc.open_by_url(url_hoja)
        return sh.get_worksheet(0)
    except Exception as e:
        st.error(f"⚠️ Error de enlace: {e}")
        return None

# --- CABECERA DE LA APP ---
st.markdown("<p style='color: #34d399; font-weight: 700; text-transform:
