import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Registro de Anestesia", page_icon="💉", layout="centered")

# Nombre del archivo donde se guardarán los datos
DATA_FILE = "registro_anestesias.csv"

# Función para cargar datos existentes
def cargar_datos():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Fecha", "Quirófano", "Especialidad", "Procedimiento", 
            "Tipo Anestesia", "ASA", "Notas/Complicaciones"
        ])

# Función para guardar un nuevo registro
def guardar_registro(datos_nuevos):
    df = cargar_datos()
    # Usar pd.concat en lugar de append (obsoleto)
    df = pd.concat([df, pd.DataFrame([datos_nuevos])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8")

# Título de la app
st.title("💉 Registro Diario de Anestesia")
st.write("Introduce los datos de la intervención para mantener tu histórico actualizado.")

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
    
    notas = st.text_area("Notas / Incidencias / Vía Aérea", placeholder="Ej: Vía aérea difícil (Cormack III), requiere videolaringo. Inestabilidad en inducción...")

    # Botón de envío
    boton_guardar = st.form_submit_button("Registrar Intervención")

# Acción al pulsar el botón
if boton_guardar:
    if not procedimiento:
        st.error("Por favor, introduce al menos el nombre del procedimiento.")
    else:
        nuevo_registro = {
            "Fecha": fecha_cirugia.strftime("%Y-%m-%d"),
            "Quirófano": quirofano,
            "Especialidad": especialidad,
            "Procedimiento": procedimiento,
            "Tipo Anestesia": ", ".join(tipo_anestesia),
            "ASA": asa,
            "Notas/Complicaciones": notas
        }
        guardar_registro(nuevo_registro)
        st.success("✅ Cirugía registrada correctamente.")

st.divider()

# --- VISUALIZACIÓN Y DESCARGA DE DATOS ---
st.subheader("📊 Historial Reciente")
df_actual = cargar_datos()

if not df_actual.empty:
    # Mostrar las últimas intervenciones primero
    st.dataframe(df_actual.tail(10), use_container_width=True)
    
    # Botón para descargar todo en Excel/CSV
    csv = df_actual.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar todo el registro (CSV)",
        data=csv,
        file_name=f"registro_anestesia_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )
else:
    st.info("Aún no hay cirugías registradas hoy.")
