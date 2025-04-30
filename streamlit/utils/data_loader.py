# En utils/data_loader.py
import pandas as pd
import streamlit as st
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
@st.cache_data
def cargar_datos(sheet_name: str) -> pd.DataFrame:
    load_dotenv()
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scopes=scope)
    gs_client = gspread.authorize(creds)
    spreadsheet_key = os.getenv("KEY_SHEET")        
    spreadsheet = gs_client.open_by_key(spreadsheet_key)
    
    sheet = spreadsheet.worksheet(sheet_name)
    data = sheet.get_all_values()
    headers, rows = data[0], data[1:]
    df = pd.DataFrame(rows, columns=headers)
    df.columns = df.columns.str.strip().str.upper()

    # Renombrar columnas según la hoja
    if sheet_name.lower().startswith("gastos"):
        df = df.rename(columns={"FECHA": "Fecha", "MONTO": "Monto"})
    else:
        df = df.rename(columns={"FECHA": "Fecha", "VALOR": "Monto"})

    # Convertir tipos y limpiar
    if not sheet_name.lower().startswith("datos"):
        df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")
        df = df.dropna(subset="Monto")
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
    df = df.dropna(subset="Fecha" )

    # Columna para agrupar
    df["MesAño"] = df["Fecha"].dt.to_period("M").astype(str)
    df["año"] = df["Fecha"].dt.year
    df["mes"] = df["Fecha"].dt.month
    
    # Limpiar Mascota y Proveedor si existen
    for col in ("MASCOTA", "PROVEEDOR"):
        if col in df.columns:
            df[col] = df[col].str.upper().str.strip()

    return df