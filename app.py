import streamlit as st
import pandas as pd
from datetime import datetime
import gspread

# Configuración de la página
st.set_page_config(page_title="Registro de Anestesia", page_icon="💉", layout="centered")

# Función para conectar directamente con Google Sheets usando los Secrets
def conectar_google_sheets():
    try:
        # Reconstruir las credenciales desde el TOML de Secrets
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
        
        # Autenticar con Google
        gc = gspread.service_account_from_dict(credentials_info)
        
        # Abrir la hoja por su URL
        url_hoja = st.secrets["connections"]["gsheets"]["spreadsheet"]
        sh = gc.open_by_url(url_hoja)
        return sh.get_worksheet(0)  # Devolvemos la primera pestaña
    except Exception as e:
        st.error(f"⚠️ Error crítico de conexión con Google: {e}")
        return None

# Título de la app
st.title("💉 Registro Diario de Anestesia")
st.write("Conexión directa con tu cuenta de Google Sheets.")

st.divider()

# --- FORMULARIO DE REGISTRO ---
with st.form("formulario_cirugia", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        fecha_cirugia = st.date_input("Fecha", datetime.now())
        quirofano = st.text_input("Quirófano / Sala", placeholder="Ej: Q1, Paritorio")
        
    with col2:
        especialidad = st.selectbox("Especialidad", [
            "Cg. General", "Traumatología", "Ginecología/Obstetricia", 
            "Urología", "Otorrino", "Oftalmología", "Cg. Vascular", 
            "Neurocirugía", "Pediatría", "Cg. Plástica", "Otros"
        ])
        asa = st.selectbox("Clasificación ASA", ["ASA I", "ASA II", "ASA III", "ASA IV", "ASA V"])

    procedimiento = st.text_input("Procedimiento / Cirugía", placeholder="Ej: Colecistectomía laparoscópica, RTU")
    
    tipo_anestesia = st.multiselect("Tipo de Anestesia", [
        "General - TET", "General - ML", "TIVA", "Epidural", 
        "Intradural / Espinal", "Bloqueo Mascarilla / Sedación", 
        "Bloqueo Periférico (Plexo)", "Local + Sedación", "Combinada"
    ])
    
    notas = st.text_area("Notas / Incidencias / Vía Aérea", placeholder="Ej: Vía aérea difícil (Cormack III)...")

    boton_guardar = st.form_submit_button("Registrar Intervención")

# Acción al pulsar el botón
if boton_guardar:
    if not procedimiento:
        st.error("Por favor, introduce al menos el nombre del procedimiento.")
    else:
        # Intentar conectar
        hoja = conectar_google_sheets()
        
        if hoja is not None:
            try:
                # Preparar la fila exactamente en el orden de las columnas de tu Excel
                nueva_fila = [
                    fecha_cirugia.strftime("%Y-%m-%d"),
                    quirofano,
                    especialidad,
                    procedimiento,
                    ", ".join(tipo_anestesia),
                    asa,
                    notas
                ]
                
                # Insertar al final de la hoja
                hoja.append_row(nueva_fila)
                st.success("✅ ¡Guardado en Google Sheets con éxito!")
            except Exception as e:
                st.error(f"Error al escribir en la hoja: {e}")

st.divider()

# --- VISUALIZACIÓN EN TIEMPO REAL ---
st.subheader("📊 Historial Actual en la Nube")
hoja_vista = conectar_google_sheets()

if hoja_vista is not None:
    try:
        datos = hoja_vista.get_all_records()
        if datos:
            df = pd.DataFrame(datos)
            # Aquí aplicamos la corrección de visualización que pedía el log de Streamlit
            st.dataframe(df.tail(10), width="stretch")
        else:
            st.info("La hoja de cálculo está conectada pero no tiene registros aún.")
    except Exception as e:
        st.caption(f"No se pudo cargar la vista previa en pantalla: {e}")
