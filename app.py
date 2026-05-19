import streamlit as st
import pandas as pd
from datetime import datetime
import gspread

# Configuración de la página (Modo Elegante)
st.set_page_config(
    page_title="AnesthesiaLog | Premium", 
    page_icon="⚕️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS VISUALES: RÉPLICA DEL DISEÑO REFINADO ---
st.markdown("""
    <style>
    /* Importar fuentes elegantes (Lora para el título, Inter para los datos) */
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600&display=swap');

    /* Fondo general musgo muy oscuro */
    .stApp {
        background-color: #1a211d;
        color: #a9c2a6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedor del Formulario (Tarjeta verde oscuro) */
    div[data-testid="stForm"] {
        background-color: #242f27 !important;
        border: 1px solid #2c3b2f !important;
        border-radius: 16px !important;
        padding: 3rem 2.5rem !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    
    /* === TIPOGRAFÍA DE CABECERA === */
    .title-container {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .main-title {
        font-family: 'Lora', serif;
        font-size: 3.5rem;
        color: #a9c2a6;
        font-weight: 500;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .main-title em {
        font-style: italic;
        font-weight: 400;
    }
    .sub-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #6e8573;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 500;
    }
    .title-divider {
        width: 150px;
        height: 1px;
        background: linear-gradient(90deg, transparent, #2c3b2f, transparent);
        margin: 1.5rem auto;
    }

    /* === TÍTULOS DE SECCIÓN (Detalle Dorado) === */
    .section-title {
        color: #aa8a59;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        margin-bottom: 1.5rem;
        margin-top: 1.5rem;
        display: flex;
        align-items: center;
    }
    .section-title::before {
        content: "•";
        margin-right: 8px;
        font-size: 1.2rem;
        color: #aa8a59;
    }

    /* === ETIQUETAS DE LOS CAMPOS (Labels) === */
    label, .st-emotion-cache-1wivap2 p {
        color: #8a9a8c !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 500 !important;
        margin-bottom: 0.25rem !important;
    }

    /* === DISEÑO DE LOS INPUTS === */
    .stTextInput input, .stTextArea textarea, .stDateInput input, div[data-baseweb="select"] > div {
        background-color: #1d2620 !important;
        color: #a9c2a6 !important;
        -webkit-text-fill-color: #a9c2a6 !important;
        border: 1px solid #2c3b2f !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: border-color 0.3s ease !important;
    }
    
    /* Placeholders en cursiva y más oscuros */
    ::placeholder {
        color: #4a5e4f !important;
        -webkit-text-fill-color: #4a5e4f !important;
        font-style: italic !important;
    }

    /* Textos seleccionados en desplegables */
    div[data-baseweb="select"] * {
        color: #a9c2a6 !important;
        -webkit-text-fill-color: #a9c2a6 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #6e8573 !important;
    }
    
    /* Multiselect (Chips) */
    span[data-baseweb="tag"] {
        background-color: #2c3b2f !important;
        border-radius: 4px !important;
        border: none !important;
    }
    span[data-baseweb="tag"] * {
        color: #a9c2a6 !important;
        -webkit-text-fill-color: #a9c2a6 !important;
        font-weight: 400 !important;
        font-size: 0.85rem !important;
    }
    
    /* Menú desplegable */
    ul[data-baseweb="menu"] {
        background-color: #242f27 !important;
        border: 1px solid #2c3b2f !important;
    }
    ul[data-baseweb="menu"] * {
        color: #a9c2a6 !important;
        -webkit-text-fill-color: #a9c2a6 !important;
    }
    
    /* Efecto Focus muy sutil */
    .stTextInput input:focus, .stTextArea textarea:focus, .stDateInput input:focus, div[data-baseweb="select"] > div:focus-within {
        border-color: #4a5e4f !important;
        box-shadow: none !important;
    }

    /* === BOTÓN PRINCIPAL REFINADO === */
    div[data-testid="stForm"] button {
        background-color: #1d2620 !important;
        color: #aa8a59 !important;
        -webkit-text-fill-color: #aa8a59 !important;
        border: 1px solid #aa8a59 !important;
        font-weight: 500 !important;
        letter-spacing: 2px !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        margin-top: 2rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stForm"] button:hover {
        background-color: #aa8a59 !important;
        color: #1d2620 !important;
        -webkit-text-fill-color: #1d2620 !important;
    }

    /* Ocultar elementos innecesarios */
    header {visibility: hidden;}
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
        return None

# --- CABECERA REFINADA (HTML Custom) ---
st.markdown("""
<div class="title-container">
    <h1 class="main-title">Anesthesia<em>Log</em></h1>
    <div class="sub-title">SISTEMA DE DOCUMENTACIÓN CLÍNICA</div>
    <div class="title-divider"></div>
</div>
""", unsafe_allow_html=True)

hoja_datos = conectar_google_sheets()

# --- FORMULARIO ELEGANTE ---
with st.form("formulario_cirugia", clear_on_submit=True):
    
    st.markdown("""<div class="section-title">DATOS DEL PROCEDIMIENTO</div>""", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fecha_cirugia = st.date_input("Fecha de Intervención", datetime.now())
        quirofano = st.text_input("Quirófano / Sala", placeholder="Ej: Q3, Reanimación")
    with c2:
        especialidad = st.selectbox("Especialidad Quirúrgica", [
            "— Seleccionar —", "Cg. General", "Traumatología", "Ginecología/Obstetricia", 
            "Urología", "Otorrino", "Oftalmología", "Cg. Vascular", 
            "Neurocirugía", "Pediatría", "Cg. Plástica", "Otros"
        ])
        asa = st.selectbox("Estado Físico (ASA)", ["— —", "ASA I", "ASA II", "ASA III", "ASA IV", "ASA V"])

    procedimiento = st.text_input("Procedimiento Específico", placeholder="Ej: Apendicectomía laparoscópica, By-pass")
    
    st.markdown("""<div class="section-title">TÉCNICA ANESTÉSICA</div>""", unsafe_allow_html=True)
    
    tipo_anestesia = st.multiselect("Seleccionar Técnicas", [
        "General — TET", "General — ML", "TIVA", 
        "Regional — Epidural", "Regional — Espinal", "Bloqueo Mascarilla", 
        "Bloqueo Plexo", "Local + Sedación", "Combinada"
    ])
    
    st.markdown("""<div class="section-title">FÁRMACOS Y OBSERVACIONES</div>""", unsafe_allow_html=True)
    notas = st.text_area("Dosis y Observaciones Clínicas", placeholder="Ej: Propofol 2 mg/kg inducción · Fentanilo 2 mcg/kg...")
    
    boton_guardar = st.form_submit_button("REGISTRAR CASO CLÍNICO")

# Lógica de procesamiento de datos
if boton_guardar:
    if not procedimiento:
        st.error("⚠️ Especifica el nombre del procedimiento quirúrgico.")
    else:
        if hoja_datos is not None:
            try:
                nueva_fila = [
                    fecha_cirugia.strftime("%Y-%m-%d"),
                    quirofano,
                    especialidad,
                    procedimiento,
                    ", ".join(tipo_anestesia),
                    asa,
                    notas
                ]
                hoja_datos.append_row(nueva_fila)
                st.success("✨ Registro almacenado correctamente.")
            except Exception as e:
                st.error(f"Error: {e}")

st.write("")

# --- VISUALIZACIÓN DE HISTORIAL ---
if hoja_datos is not None:
    try:
        datos = hoja_datos.get_all_records()
        if datos:
            st.markdown("""<div class="section-title">ÚLTIMOS CASOS</div>""", unsafe_allow_html=True)
            df = pd.DataFrame(datos)
            df_invertido = df.iloc[::-1]
            st.dataframe(df_invertido.head(5), width="stretch")
    except Exception as e:
        pass
