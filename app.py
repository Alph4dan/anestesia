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
#  ESTILOS — BOSQUE REFINADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400;500;600&display=swap');

:root {
    /* Verdes de bosque por capas */
    --forest-0:   #080f09;   /* suelo */
    --forest-1:   #0d1a0f;   /* base */
    --forest-2:   #111f13;   /* fondo */
    --forest-3:   #172918;   /* tarjeta */
    --forest-4:   #1d3320;   /* input */
    --forest-5:   #243d27;   /* hover */

    /* Bordes */
    --border-1:   rgba(90,140,95,0.18);
    --border-2:   rgba(90,140,95,0.40);
    --border-3:   rgba(110,170,115,0.65);

    /* Acentos */
    --sage:       #8bbf92;
    --sage-light: #b3d4b8;
    --sage-dim:   #5a8c5f;
    --amber:      #c8a870;   /* único acento cálido */
    --amber-dim:  #9a7a4a;

    /* Texto */
    --tx-hi:   #cee8d2;
    --tx-mid:  #8caf92;
    --tx-lo:   #527558;
}

/* ── Base ─────────────────────────────────── */
html, body, .stApp {
    background-color: var(--forest-1) !important;
    color: var(--tx-hi) !important;
    font-family: 'Jost', sans-serif !important;
}

/* ── Malla de fondo — niebla de bosque ──── */
.stApp {
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(40,90,45,0.22) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(20,60,25,0.18) 0%, transparent 60%),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 39px,
            rgba(50,100,55,0.04) 40px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 39px,
            rgba(50,100,55,0.04) 40px
        ) !important;
}

/* ── Layout central ─────────────────────── */
.block-container {
    max-width: 660px !important;
    padding: 3.5rem 1.5rem 5rem !important;
}

/* ── Cabecera ───────────────────────────── */
.hd {
    text-align: center;
    padding-bottom: 2.4rem;
    margin-bottom: 2.6rem;
    position: relative;
}
.hd::after {
    content: '';
    position: absolute;
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 120px; height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-2), transparent);
}
.hd-badge {
    display: inline-block;
    font-family: 'Jost', sans-serif;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    color: var(--amber);
    -webkit-text-fill-color: var(--amber);
    border: 1px solid rgba(200,168,112,0.3);
    border-radius: 30px;
    padding: 0.28rem 0.9rem;
    margin-bottom: 1.1rem;
    background: rgba(200,168,112,0.05);
}
.hd-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 3.2rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
    color: var(--sage-light) !important;
    -webkit-text-fill-color: var(--sage-light) !important;
    line-height: 1 !important;
    margin: 0 0 0.5rem 0 !important;
}
.hd-title em {
    font-style: italic;
    color: var(--sage);
    -webkit-text-fill-color: var(--sage);
}
.hd-sub {
    font-size: 0.72rem !important;
    letter-spacing: 0.26em !important;
    text-transform: uppercase !important;
    color: var(--tx-lo) !important;
    -webkit-text-fill-color: var(--tx-lo) !important;
    margin: 0 !important;
    font-weight: 400 !important;
}

/* ── Tarjeta del formulario ─────────────── */
div[data-testid="stForm"] {
    background:
        linear-gradient(175deg,
            rgba(36,61,39,0.6) 0%,
            rgba(17,31,19,0.95) 55%,
            rgba(11,20,12,0.98) 100%
        ) !important;
    border: 1px solid var(--border-1) !important;
    border-top-color: var(--border-2) !important;
    border-radius: 20px !important;
    padding: 2.6rem 2.6rem 2.2rem !important;
    box-shadow:
        0 2px 0 0 rgba(110,170,115,0.12),
        0 30px 80px -10px rgba(0,0,0,0.7),
        0 8px 32px -4px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(180,230,185,0.05) !important;
    position: relative;
    overflow: hidden;
}
/* Reflejo de luz en la esquina superior */
div[data-testid="stForm"]::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(90,160,95,0.07) 0%, transparent 70%);
    pointer-events: none;
}

/* ── Separadores de sección ─────────────── */
.sec {
    display: flex !important;
    align-items: center !important;
    gap: 0.7rem !important;
    margin: 2rem 0 1.1rem !important;
}
.sec-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--amber);
    opacity: 0.7;
    flex-shrink: 0;
}
.sec-label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.34em !important;
    text-transform: uppercase !important;
    color: var(--amber-dim) !important;
    -webkit-text-fill-color: var(--amber-dim) !important;
    white-space: nowrap !important;
}
.sec-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-1), transparent);
}

/* ── Títulos generales ──────────────────── */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--sage-light) !important;
    -webkit-text-fill-color: var(--sage-light) !important;
}

/* ── Labels ─────────────────────────────── */
label {
    color: var(--tx-mid) !important;
    -webkit-text-fill-color: var(--tx-mid) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    font-family: 'Jost', sans-serif !important;
    text-transform: uppercase !important;
}

/* ── Inputs & textarea ──────────────────── */
.stTextInput input,
.stTextArea textarea,
.stDateInput input {
    background-color: var(--forest-4) !important;
    color: var(--tx-hi) !important;
    -webkit-text-fill-color: var(--tx-hi) !important;
    border: 1px solid var(--border-1) !important;
    border-radius: 8px !important;
    padding: 0.6rem 0.9rem !important;
    font-size: 0.92rem !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 300 !important;
    transition: border-color 0.18s ease, background 0.18s ease, box-shadow 0.18s ease !important;
    letter-spacing: 0.02em !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus {
    border-color: var(--border-3) !important;
    background-color: var(--forest-5) !important;
    box-shadow: 0 0 0 3px rgba(90,140,95,0.15) !important;
    outline: none !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: var(--tx-lo) !important;
    -webkit-text-fill-color: var(--tx-lo) !important;
    font-style: italic !important;
    font-weight: 300 !important;
}

/* ── Selectbox ──────────────────────────── */
div[data-baseweb="select"] > div {
    background-color: var(--forest-4) !important;
    border: 1px solid var(--border-1) !important;
    border-radius: 8px !important;
    transition: border-color 0.18s ease !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--border-3) !important;
    box-shadow: 0 0 0 3px rgba(90,140,95,0.15) !important;
}
div[data-baseweb="select"] * {
    color: var(--tx-hi) !important;
    -webkit-text-fill-color: var(--tx-hi) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 300 !important;
}
div[data-baseweb="select"] svg { fill: var(--sage-dim) !important; }

/* ── Dropdown lista ─────────────────────── */
ul[data-baseweb="menu"] {
    background-color: #1a2e1c !important;
    border: 1px solid var(--border-2) !important;
    border-radius: 10px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6) !important;
    padding: 0.3rem !important;
}
ul[data-baseweb="menu"] li {
    border-radius: 5px !important;
    margin: 1px 0 !important;
}
ul[data-baseweb="menu"] li:hover {
    background-color: rgba(90,140,95,0.2) !important;
}
ul[data-baseweb="menu"] * {
    color: var(--tx-hi) !important;
    -webkit-text-fill-color: var(--tx-hi) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 300 !important;
}

/* ── Multiselect chips ──────────────────── */
span[data-baseweb="tag"] {
    background: rgba(50,90,55,0.7) !important;
    border: 1px solid var(--border-2) !important;
    border-radius: 5px !important;
    backdrop-filter: blur(4px) !important;
}
span[data-baseweb="tag"] * {
    color: var(--sage-light) !important;
    -webkit-text-fill-color: var(--sage-light) !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
}

/* ── Botón principal ────────────────────── */
div[data-testid="stForm"] button {
    background: linear-gradient(160deg, #1f3d24 0%, #142918 100%) !important;
    color: var(--sage-light) !important;
    -webkit-text-fill-color: var(--sage-light) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    border: 1px solid var(--border-2) !important;
    border-top-color: var(--border-3) !important;
    border-radius: 9px !important;
    padding: 0.9rem 2rem !important;
    width: 100% !important;
    margin-top: 1.8rem !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(180,230,185,0.07) !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="stForm"] button::after {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(160deg, rgba(140,200,145,0.06) 0%, transparent 60%) !important;
    pointer-events: none !important;
}
div[data-testid="stForm"] button:hover {
    background: linear-gradient(160deg, #284f2e 0%, #1a341f 100%) !important;
    border-color: var(--border-3) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(110,170,115,0.2), inset 0 1px 0 rgba(180,230,185,0.12) !important;
    transform: translateY(-1px) !important;
    color: #d0ecd4 !important;
    -webkit-text-fill-color: #d0ecd4 !important;
}
div[data-testid="stForm"] button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4) !important;
}

/* ── Expander ───────────────────────────── */
details {
    background: rgba(23,41,24,0.5) !important;
    border: 1px solid var(--border-1) !important;
    border-radius: 9px !important;
}
summary {
    color: var(--tx-mid) !important;
    -webkit-text-fill-color: var(--tx-mid) !important;
    font-size: 0.8rem !important;
    font-family: 'Jost', sans-serif !important;
    padding: 0.7rem 1rem !important;
}

/* ── Alertas ────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 9px !important;
}

/* ── Scrollbar ──────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--forest-1); }
::-webkit-scrollbar-thumb { background: var(--forest-5); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--sage-dim); }

/* ── Pie ─────────────────────────────────── */
.footer {
    text-align: center;
    margin-top: 3.5rem;
    font-size: 0.62rem !important;
    letter-spacing: 0.28em !important;
    text-transform: uppercase !important;
    color: var(--tx-lo) !important;
    -webkit-text-fill-color: var(--tx-lo) !important;
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
<div class="hd">
    <div class="hd-badge">Registro · Anestesiología</div>
    <h1 class="hd-title">Anesthesia<em>Log</em></h1>
    <p class="hd-sub">Sistema de documentación clínica</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FORMULARIO PRINCIPAL
# ─────────────────────────────────────────────
with st.form("registro_anestesia", clear_on_submit=True):

    # ── Datos del paciente ───────────────────
    st.markdown("""
    <div class="sec">
        <span class="sec-dot"></span>
        <span class="sec-label">Datos del paciente</span>
        <span class="sec-line"></span>
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown("""
    <div class="sec">
        <span class="sec-dot"></span>
        <span class="sec-label">Procedimiento</span>
        <span class="sec-line"></span>
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown("""
    <div class="sec">
        <span class="sec-dot"></span>
        <span class="sec-label">Fármacos administrados</span>
        <span class="sec-line"></span>
    </div>
    """, unsafe_allow_html=True)

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

    # ── Evolución intraoperatoria ────────────
    st.markdown("""
    <div class="sec">
        <span class="sec-dot"></span>
        <span class="sec-label">Evolución intraoperatoria</span>
        <span class="sec-line"></span>
    </div>
    """, unsafe_allow_html=True)

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

    with st.expander("📋  Notas adicionales y plan postoperatorio"):
        notas_libres = st.text_area(
            "Notas clínicas",
            placeholder="Observaciones, plan de analgesia postoperatoria, indicaciones...",
            height=120
        )

    # ── Botón enviar ─────────────────────────
    enviado = st.form_submit_button("Registrar caso")


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
            st.success("✦  Registro guardado (modo demo — sin conexión a Sheets).")


# ─────────────────────────────────────────────
#  PIE
# ─────────────────────────────────────────────
st.markdown('<p class="footer">AnesthesiaLog &nbsp;·&nbsp; Uso clínico interno</p>', unsafe_allow_html=True)
