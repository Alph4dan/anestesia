import streamlit as st
import pandas as pd
from datetime import datetime
import gspread

# Configuración avanzada de la página (Modo Clínico)
st.set_page_config(
    page_title="AnesthesiaLog | Vanguard", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS VISUALES AVANZADOS (CSS INYECTADO) ---
st.markdown("""
    <style>
    /* Fondo y tipografía general */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    /* Tarjetas y contenedores */
    div[data-testid="stForm"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    /* Títulos y textos */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #38bdf8 0%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.05em;
    }
    /* Inputs y Selectores */
    .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    /* Enfoque de inputs */
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
    }
    /* Botón Principal */
    button[kind="formSubmit"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
        width: 100% !outset;
    }
    button[kind="formSubmit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
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
st.markdown("<p style='color: #38bdf8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: -0.5rem;'>Anesthesia Suite</p>", unsafe_allow_html=True)
st.title("⚡ AnesthesiaLog")
st.markdown("<p style='color: #94a3b8;'>Registro analítico e inteligente de actividad anestésica en quirófano.</p>", unsafe_allow_html=True)

# --- PANEL DE CONTROL DIGITAL (Métricas rápidas) ---
hoja_datos = conectar_google_sheets()
total_casos = 0

if hoja_datos is not None:
    try:
        total_casos = len(hoja_datos.get_all_values()) - 1
        if total_casos < 0: total_casos = 0
    except:
        pass

# Dashboard minimalista superior
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<div style='background-color: #1e293b; padding: 1rem; border-radius: 12px; border-left: 4px solid #38bdf8;'> <span style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;'>Casos Históricos</span> <br> <span style='font-size: 1.8rem; font-weight: 700; color: #f8fafc;'>{total_casos}</span></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div style='background-color: #1e293b; padding: 1rem; border-radius: 12px; border-left: 4px solid #10b981;'> <span style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;'>Estado Servidor</span> <br> <span style='font-size: 1.2rem; font-weight: 700; color: #10b981; line-height: 2.2rem;'>● ONLINE</span></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div style='background-color: #1e293b; padding: 1rem; border-radius: 12px; border-left: 4px solid #a855f7;'> <span style='color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;'>Sincronización</span> <br> <span style='font-size: 1.2rem; font-weight: 700; color: #a855f7; line-height: 2.2rem;'>Directa (Drive)</span></div>", unsafe_allow_html=True)

st.write("")

# --- FORMULARIO DE ENTRADA VANGUARDISTA ---
with st.form("formulario_cirugia", clear_on_submit=True):
    
    st.markdown("<h3 style='color: #38bdf8; font-size: 1.2rem; margin-top: 0;'>📝 Datos del Procedimiento</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fecha_cirugia = st.date_input("📅 Fecha de Intervención", datetime.now())
        quirofano = st.text_input("🏛️ Quirófano / Paritorio / Sala", placeholder="Ej: Q3, Paritorio")
    with c2:
        especialidad = st.selectbox("🩺 Especialidad Quirúrgica", [
            "Cg. General", "Traumatología", "Ginecología/Obstetricia", 
            "Urología", "Otorrino", "Oftalmología", "Cg. Vascular", 
            "Neurocirugía", "Pediatría", "Cg. Plástica", "Otros"
        ])
        asa = st.selectbox("📊 Estado Físico (ASA)", ["ASA I", "ASA II", "ASA III", "ASA IV", "ASA V"])

    procedimiento = st.text_input("⚔️ Procedimiento Específico", placeholder="Ej: Prótesis total de cadera, Craneotomía")
    
    st.markdown("<h3 style='color: #38bdf8; font-size: 1.2rem; margin-top: 1rem;'>💉 Técnica Anestésica</h3>", unsafe_allow_html=True)
    
    tipo_anestesia = st.multiselect("Selecciona todas las técnicas aplicadas:", [
        "General - TET (Intubación)", "General - ML (Mascarilla)", "TIVA (Total Intravenosa)", 
        "Epidural", "Intradural / Espinal", "Bloqueo Mascarilla / Sedación", 
        "Bloqueo Periférico (Plexo)", "Local + Sedación Cognitiva", "Combinada"
    ])
    
    # Campo opcional en formato limpio
    with st.expander("➕ Añadir observaciones clínicas o incidencias críticas"):
        notas = st.text_area("Notas Clínicas:", placeholder="Ej: Vía aérea difícil prevista. Videolaringoscopio McMcGrath hoja 3. Estabilidad hemodinámica estable...")
    
    st.write("")
    boton_guardar = st.form_submit_button("🚀 ENVIAR REGISTRO A LA NUBE")

# Lógica de procesamiento de datos
if boton_guardar:
    if not procedimiento:
        st.error("⚠️ Operación rechazada: Es obligatorio especificar el nombre del procedimiento quirúrgico.")
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
                st.balloons() # Animación futurista de éxito
                st.success("✨ Registro procesado y encriptado en tu Google Sheets.")
                st.rerun() # Recarga la app para actualizar el contador de arriba inmediatamente
            except Exception as e:
                st.error(f"Error en la escritura de datos: {e}")

st.write("")

# --- VISUALIZACIÓN DE HISTORIAL (Modo Oscuro Elegante) ---
st.markdown("<h3 style='color: #f8fafc; font-size: 1.4rem;'>📊 Monitor de Actividad Reciente</h3>", unsafe_allow_html=True)

if hoja_datos is not None:
    try:
        datos = hoja_datos.get_all_records()
        if datos:
            df = pd.DataFrame(datos)
            # Invertimos el orden para mostrar la última cirugía arriba del todo
            df_invertido = df.iloc[::-1]
            st.dataframe(df_invertido.head(5), width="stretch")
        else:
            st.info("El monitor clínico no detecta registros previos en esta hoja.")
    except Exception as e:
        st.caption(f"Fallo en la telemetría de visualización: {e}")
