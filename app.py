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

# --- ESTILOS VISUALES AVANZADOS (TONOS VERDES Y CAMPOS MEJORADOS) ---
st.markdown("""
    <style>
    /* Fondo general oscuro verde (Verde Quirófano Profundo) */
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
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
    }
    
    /* Títulos con gradiente esmeralda */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #6ee7b7 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    
    /* Color de las etiquetas (Labels) de los campos */
    label, p {
        color: #a7f3d0 !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }

    /* === DISEÑO MEJORADO DE LOS CAMPOS DE TEXTO === */
    .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {
        background-color: #065f46 !important; /* Fondo verde translúcido */
        color: #ffffff !important;
        border: 2px solid #059669 !important; /* Borde verde medio */
        border-radius: 12px !important; /* Bordes redondeados modernos */
        padding: 0.6rem 1rem !important; /* Más espacio interior para respirar */
        transition: all 0.3s ease !important; /* Animación suave */
        font-size: 1rem !important;
    }
    
    /* Efecto al seleccionar/escribir en un campo (Glow verde claro) */
    .stTextInput input:focus, .stTextArea textarea:focus, div[data-baseweb="select"] > div:focus-within {
        border-color: #34d399 !important;
        box-shadow: 0 0 0 4px rgba(52, 211, 153, 0.25) !important;
        background-color: #047857 !important;
    }

    /* === DISEÑO DEL BOTÓN PRINCIPAL === */
    button[kind="formSubmit"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    button[kind="formSubmit"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
    }
    
    /* Diseño del desplegable (Expander) */
    .streamlit-expanderHeader {
        background-color: #065f46 !important;
        border-radius: 10px !important;
        border: 1px solid #047857 !important;
        color: #a7f3d0 !important;
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
st.markdown("<p style='color: #34d399; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: -0.5rem;'>Quirófano Suite</p>", unsafe_allow_html=True)
st.title("🌿 AnesthesiaLog")
st.markdown("<p style='color: #6ee7b7;'>Registro clínico seguro y sincronizado en tiempo real.</p>", unsafe_allow_html=True)

# --- PANEL DE CONTROL DIGITAL (Métricas en tonos verdes) ---
hoja_datos = conectar_google_sheets()
total_casos = 0

if hoja_datos is not None:
    try:
        total_casos = len(hoja_datos.get_all_values()) - 1
        if total_casos < 0: total_casos = 0
    except:
        pass

# Dashboard minimalista superior adaptado al verde
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<div style='background-color: #064e3b; padding: 1rem; border-radius: 12px; border-left: 4px solid #6ee7b7; border-top: 1px solid #047857;'> <span style='color: #a7f3d0; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;'>Casos Totales</span> <br> <span style='font-size: 1.8rem; font-weight: 800; color: #ecfdf5;'>{total_casos}</span></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div style='background-color: #064e3b; padding: 1rem; border-radius: 12px; border-left: 4px solid #10b981; border-top: 1px solid #047857;'> <span style='color: #a7f3d0; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;'>Estado</span> <br> <span style='font-size: 1.2rem; font-weight: 800; color: #10b981; line-height: 2.2rem;'>● ONLINE</span></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div style='background-color: #064e3b; padding: 1rem; border-radius: 12px; border-left: 4px solid #059669; border-top: 1px solid #047857;'> <span style='color: #a7f3d0; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;'>Conexión</span> <br> <span style='font-size: 1.2rem; font-weight: 800; color: #34d399; line-height: 2.2rem;'>Drive Segura</span></div>", unsafe_allow_html=True)

st.write("")
st.write("")

# --- FORMULARIO DE ENTRADA ---
with st.form("formulario_cirugia", clear_on_submit=True):
    
    st.markdown("<h3 style='color: #6ee7b7; font-size: 1.3rem; margin-top: 0;'>📝 Datos del Procedimiento</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fecha_cirugia = st.date_input("📅 Fecha de Intervención", datetime.now())
        quirofano = st.text_input("🏛️ Quirófano / Sala", placeholder="Ej: Q3, Reanimación")
    with c2:
        especialidad = st.selectbox("🩺 Especialidad Quirúrgica", [
            "Cg. General", "Traumatología", "Ginecología/Obstetricia", 
            "Urología", "Otorrino", "Oftalmología", "Cg. Vascular", 
            "Neurocirugía", "Pediatría", "Cg. Plástica", "Otros"
        ])
        asa = st.selectbox("📊 Estado Físico (ASA)", ["ASA I", "ASA II", "ASA III", "ASA IV", "ASA V"])

    procedimiento = st.text_input("⚔️ Procedimiento Específico", placeholder="Ej: Apendicectomía laparoscópica, By-pass")
    
    st.markdown("<h3 style='color: #6ee7b7; font-size: 1.3rem; margin-top: 1rem;'>💉 Técnica Anestésica</h3>", unsafe_allow_html=True)
    
    tipo_anestesia = st.multiselect("Selecciona las técnicas aplicadas:", [
        "General - TET (Intubación)", "General - ML (Mascarilla)", "TIVA", 
        "Epidural", "Intradural / Espinal", "Bloqueo Mascarilla / Sedación", 
        "Bloqueo Periférico (Plexo)", "Local + Sedación", "Combinada"
    ])
    
    # Campo expandible para mantener la limpieza visual
    with st.expander("➕ Añadir observaciones clínicas o incidencias"):
        notas = st.text_area("Notas / Vía aérea:", placeholder="Ej: Intubación al primer intento. Vía venosa central canalizada sin incidencias...")
    
    boton_guardar = st.form_submit_button("✅ REGISTRAR CASO CLÍNICO")

# Lógica de procesamiento de datos
if boton_guardar:
    if not procedimiento:
        st.error("⚠️ Operación rechazada: Especifica el nombre del procedimiento quirúrgico.")
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
                    notas if 'notas' in locals() else ""
                ]
                hoja_datos.append_row(nueva_fila)
                st.balloons()
                st.success("✨ Registro procesado y guardado en Google Sheets.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar los datos: {e}")

st.write("")

# --- VISUALIZACIÓN DE HISTORIAL ---
st.markdown("<h3 style='color: #ecfdf5; font-size: 1.4rem;'>📊 Últimos Casos Registrados</h3>", unsafe_allow_html=True)

if hoja_datos is not None:
    try:
        datos = hoja_datos.get_all_records()
        if datos:
            df = pd.DataFrame(datos)
            # Invertimos el orden para mostrar la última cirugía arriba
            df_invertido = df.iloc[::-1]
            st.dataframe(df_invertido.head(5), width="stretch")
        else:
            st.info("No hay casos registrados en esta hoja todavía.")
    except Exception as e:
        st.caption(f"Fallo al cargar la vista previa: {e}")
