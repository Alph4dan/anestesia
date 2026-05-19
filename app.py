import streamlit as st
import pandas as pd
from datetime import datetime
import gspread

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AnesthesiaLog",
    page_icon="🌲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  ESTILOS: BOSQUE PROFUNDO — ELEGANTE & ORGÁNICO
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Paleta de bosque profundo ──────────────── */
:root {
    --bg-base:       #0e1a10;
    --bg-surface:    #142016;
    --bg-card:       #1b2e1e;
    --bg-input:      #162419;
    --border-subtle: #2e4a32;
    --border-glow:   #4a7c52;
    --accent-sage:   #7aab82;
    --accent-light:  #a8d4b0;
    --accent-gold:   #c9a96e;
    --text-primary:  #ddeedd;
    --text-muted:    #7a9e7e;
    --text-label:    #9dc4a2;
    --shadow-deep:   0 24px 60px rgba(0,0,0,0.6);
}

/* ── Reset base ─────────────────────────────── */
html, body, .stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Patrón de textura de bosque (puntos sutiles) */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, rgba(74,124,82,0.08) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
    z-index: 0;
}

/* ── Bloque principal ───────────────────────── */
.block-container {
    max-width: 700px !important;
    padding-top: 3rem !important;
    padding-bottom: 4rem !important;
    position: relative;
    z-index: 1;
}

/* ── Cabecera ornamental ────────────────────── */
.header-wrap {
    text-align: center;
    margin-bottom: 2.8rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border-subtle);
    position: relative;
}
.header-wrap::after {
    content: '✦';
    display: block;
    color: var(--accent-gold);
    font-size: 1rem;
    margin-top: 1rem;
    opacity: 0.7;
}
.app-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 3rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    color: var(--accent-light) !important;
    -webkit-text-fill-color: var(--accent-light) !important;
    line-height: 1.1 !important;
    margin: 0 !important;
}
.app-subtitle {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.28em !important;
    text-transform: uppercase !important;
    color: var(--accent-gold) !important;
    -webkit-text-fill-color: var(--accent-gold) !important;
    margin-top: 0.4rem !important;
    font-weight: 500 !important;
}
.app-icon {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 18px rgba(122,171,130,0.5));
}

/* ── Formulario ─────────────────────────────── */
div[data-testid="stForm"] {
    background: linear-gradient(160deg, var(--bg-card) 0%, #192b1c 100%) !important;
    border: 1px solid var(--border-subtle) !important;
    border-top: 1px solid #3a5e40 !important;
    border-radius: 18px !important;
    padding: 2.8rem 2.4rem !important;
    box-shadow: var(--shadow-deep), inset 0 1px 0 rgba(168,212,176,0.06) !important;
}

/* ── Sección divisora dentro del form ──────── */
.section-label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.32em !important;
    text-transform: uppercase !important;
    color: var(--accent-gold) !important;
    -webkit-text-fill-color: var(--accent-gold) !important;
    font-weight: 500 !important;
    margin: 1.8rem 0 0.8rem 0 !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    display: block !important;
}

/* ── Títulos generales ──────────────────────── */
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--accent-light) !important;
    -webkit-text-fill-color: var(--accent-light) !important;
    font-weight: 600 !important;
}

/* ── Labels ─────────────────────────────────── */
label, .stTextInput label, .stSelectbox label,
.stTextArea label, .stDateInput label, .stMultiSelect label {
    color: var(--text-label) !important;
    -webkit-text-fill-color: var(--text-label) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Inputs, textareas, fecha ───────────────── */
.stTextInput input,
.stTextArea textarea,
.stDateInput input {
    background-color: var(--bg-input) !important;
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    padding: 0.65rem 1rem !important;
    font-size: 0.95rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus {
    border-color: var(--border-glow) !important;
    box-shadow: 0 0 0 3px rgba(74,124,82,0.2) !important;
    background-color: #1d3020 !important;
    outline: none !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: var(--text-muted) !important;
    -webkit-text-fill-color: var(--text-muted) !important;
}

/* ── Selectbox ──────────────────────────────── */
div[data-baseweb="select"] > div {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] * {
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="select"] svg { fill: var(--accent-sage) !important; }

/* ── Dropdown de opciones ───────────────────── */
ul[data-baseweb="menu"] {
    background-color: #1d3020 !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    box-shadow: 0 16px 40px rgba(0,0,0,0.5) !important;
}
ul[data-baseweb="menu"] li {
    border-radius: 6px !important;
}
ul[data-baseweb="menu"] li:hover {
    background-color: rgba(74,124,82,0.25) !important;
}
ul[data-baseweb="menu"] * {
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Multiselect chips ──────────────────────── */
span[data-baseweb="tag"] {
    background-color: #2e5233 !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 6px !important;
}
span[data-baseweb="tag"] * {
    color: var(--accent-light) !important;
    -webkit-text-fill-color: var(--accent-light) !important;
    font-weight: 500 !important;
}

/* ── Botón principal ────────────────────────── */
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[kind="primary"],
div[data-testid="stForm"] button {
    background: linear-gradient(135deg, #2e5a35 0%, #1e3d24 100%) !important;
    color: var(--accent-light) !important;
    -webkit-text-fill-color: var(--accent-light) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    margin-top: 1.6rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(168,212,176,0.1) !important;
}
div[data-testid="stForm"] button:hover {
    background: linear-gradient(135deg, #3a6e43 0%, #28502e 100%) !important;
    border-color: var(--accent-sage) !important;
    box-shadow: 0 6px 28px rgba(74,124,82,0.3), inset 0 1px 0 rgba(168,212,176,0.15) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stForm"] button:active {
    transform: translateY(0) !important;
}

/* ── Expander ───────────────────────────────── */
.streamlit-expanderHeader {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
}
.streamlit-expanderHeader * {
    color: var(--text-label) !important;
    -webkit-text-fill-color: var(--text-label) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Mensajes de alerta ─────────────────────── */
.stSuccess {
    background-color: #1b3a1e !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    color: var(--accent-light) !important;
}
.stError {
    background-color: #2a1a1a !important;
    border: 1px solid #6b3535 !important;
    border-radius: 10px !important;
}

/* ── Divisor ────────────────────────────────── */
hr {
    border-color: var(--border-subtle) !important;
    margin: 2rem 0 !important;
}

/* ── Columnas ───────────────────────────────── */
[data-testid="column"] { gap: 1rem !important; }

/* ── Scrollbar ──────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
    background: var(--border-subtle);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--border-glow); }

/* ── Pie ornamental ─────────────────────────── */
.footer-ornament {
    text-align: center;
    margin-top: 3rem;
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONEXIÓN A GOOGLE SHEETS
# ─────────────────────────────────────────────
def conectar_google_sheets():
    try:
        credentials_info = {
            "type":                        st.secrets["connections"]["gsheets"]["type"],
            "project_id":                  st.secrets["connections"]["gsheets"]["project_id"],
            "private_key_id":              st.secrets["connections"]["gsheets"]["private_key_id"],
            "private_key":                 st.secrets["connections"]["gsheets"]["private_key"].replace("\\n", "\n"),
            "client_email":                st.secrets["connections"]["gsheets"]["client_email"],
            "auth_uri":                    st.secrets["connections"]["gsheets"]["auth_uri"],
            "token_uri":                   st.secrets["connections"]["gsheets"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url":        st.secrets["connections"]["gsheets"]["client_x509_cert_url"],
        }
        gc = gspread.service_account_from_dict(credentials_info)
        url_hoja = st.secrets["connections"]["gsheets"]["spreadsheet"]
        sh = gc.open_by_url(url_hoja)
        return sh.get_worksheet(0)
    except Exception as e:
        st.error(f"⚠️ Error de enlace con Google Sheets: {e}")
        return None


# ─────────────────────────────────────────────
#  CABECERA
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <span class="app-icon">🌲</span>
    <h1 class="app-title">AnesthesiaLog</h1>
    <p class="app-subtitle">Registro clínico · Anestesiología</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FORMULARIO PRINCIPAL
# ─────────────────────────────────────────────
with st.form("registro_anestesia", clear_on_submit=True):

    # ── Datos del paciente ───────────────────
    st.markdown('<span class="section-label">Datos del paciente</span>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        nombre_paciente = st.text_input("Nombre completo", placeholder="Apellido, Nombre")
    with col2:
        fecha_cirugia = st.date_input("Fecha de intervención", value=datetime.today())

    col3, col4 = st.columns(2)
    with col3:
        edad = st.text_input("Edad", placeholder="años")
    with col4:
        peso = st.text_input("Peso (kg)", placeholder="kg")

    # ── Procedimiento ────────────────────────
    st.markdown('<span class="section-label">Procedimiento</span>', unsafe_allow_html=True)

    tipo_cirugia = st.selectbox(
        "Tipo de cirugía",
        ["— Seleccionar —", "Cirugía General", "Ortopédica", "Cardiovascular",
         "Neurocirugía", "Ginecología", "Urología", "Oftalmología", "ORL", "Otra"]
    )

    col5, col6 = st.columns(2)
    with col5:
        tipo_anestesia = st.selectbox(
            "Tipo de anestesia",
            ["— Seleccionar —", "General", "Regional — Epidural", "Regional — Espinal",
             "Regional — Bloqueo periférico", "Sedación", "Local + Sedación"]
        )
    with col6:
        asa = st.selectbox("Clasificación ASA", ["— —", "ASA I", "ASA II", "ASA III", "ASA IV", "ASA V"])

    # ── Fármacos ─────────────────────────────
    st.markdown('<span class="section-label">Fármacos administrados</span>', unsafe_allow_html=True)

    farmacos = st.multiselect(
        "Seleccionar fármacos",
        ["Propofol", "Fentanilo", "Remifentanilo", "Sufentanilo", "Ketamina",
         "Midazolam", "Rocuronio", "Succinilcolina", "Sevoflurano", "Desflurano",
         "Isoflurano", "Neostigmina", "Atropina", "Ondansetrón", "Dexametasona"]
    )

    dosis_notas = st.text_area(
        "Dosis y observaciones farmacológicas",
        placeholder="Ej: Propofol 2 mg/kg inducción · Fentanilo 2 mcg/kg · Rocuronio 0.6 mg/kg...",
        height=90
    )

    # ── Incidencias y notas ──────────────────
    st.markdown('<span class="section-label">Evolución intraoperatoria</span>', unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        duracion = st.text_input("Duración (min)", placeholder="minutos")
    with col8:
        sangrado = st.text_input("Sangrado estimado (mL)", placeholder="mL")

    incidencias = st.multiselect(
        "Incidencias registradas",
        ["Sin incidencias", "Hipotensión", "Hipertensión", "Bradicardia", "Taquicardia",
         "Laringoespasmo", "Broncoespasmo", "Náuseas / Vómitos", "Reacción alérgica",
         "Dificultad de intubación", "Despertar intraoperatorio", "Otra"]
    )

    with st.expander("📋 Notas adicionales y plan postoperatorio"):
        notas_libres = st.text_area(
            "Notas clínicas",
            placeholder="Observaciones, plan de analgesia postoperatoria, indicaciones...",
            height=120
        )

    # ── Botón enviar ──────────────────────────
    enviado = st.form_submit_button("✦  Registrar caso")


# ─────────────────────────────────────────────
#  LÓGICA DE ENVÍO
# ─────────────────────────────────────────────
if enviado:
    if not nombre_paciente or tipo_cirugia == "— Seleccionar —":
        st.error("⚠️  Completa al menos el nombre del paciente y el tipo de cirugía.")
    else:
        hoja = conectar_google_sheets()
        if hoja:
            fila = [
                str(fecha_cirugia),
                nombre_paciente.strip(),
                edad, peso,
                tipo_cirugia,
                tipo_anestesia,
                asa,
                ", ".join(farmacos),
                dosis_notas,
                duracion, sangrado,
                ", ".join(incidencias),
                notas_libres if 'notas_libres' in dir() else "",
                datetime.now().strftime("%H:%M:%S")
            ]
            hoja.append_row(fila)
            st.success("✦  Caso registrado correctamente.")
        else:
            # Demo sin conexión
            st.success("✦  Registro guardado (modo demo — sin conexión a Sheets).")

# ─────────────────────────────────────────────
#  PIE DE PÁGINA
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer-ornament">
    AnesthesiaLog &nbsp;·&nbsp; Uso clínico interno &nbsp;·&nbsp; 🌲
</div>
""", unsafe_allow_html=True)
