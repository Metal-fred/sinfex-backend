from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI(title="Sinfex API - Google Sheets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExamenMedico(BaseModel):
    codigoExamen: str
    nombresExamen: str
    laboratoriosProcesamiento: str
    preparacionPaciente: str
    muestraRequerida: str
    estabilidadMuestra: str
    condicionesEnvio: str
    metodoUtilizado: str
    intervaloReferencia: str
    valorCritico: str
    parametrosDesempeno: str
    informacionClinica: str
    referencias: str

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1vOvzaInEYOkJ2WiybcyN6UWkowhXLcUgyB0MfnRhC0w").sheet1

# 1. Función para GUARDAR datos (POST)
@app.post("/api/examenes")
async def guardar_examen(examen: ExamenMedico):
    nueva_fila = [
        examen.codigoExamen, examen.nombresExamen, examen.laboratoriosProcesamiento,
        examen.preparacionPaciente, examen.muestraRequerida, examen.estabilidadMuestra,
        examen.condicionesEnvio, examen.metodoUtilizado, examen.intervaloReferencia,
        examen.valorCritico, examen.parametrosDesempeno, examen.informacionClinica,
        examen.referencias
    ]
    sheet.append_row(nueva_fila) 
    return {"mensaje": "¡Examen guardado exitosamente en Google Sheets!", "datos": nueva_fila}

# 2. Función para LEER datos para el buscador (GET)
@app.get("/api/examenes")
async def obtener_examenes():
    # Esta función lee todas las filas de tu Google Sheet
    todas_las_filas = sheet.get_all_values()
    return {"datos": todas_las_filas}