"""
Dashboard de 101 Rescataditos - Versión optimizada y rediseñada
Con mejoras de diseño, funcionalidad y estructura de código
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from streamlit.components.v1 import html
import calendar
import json
import re
from datetime import datetime, timedelta
from utils.data_loader import cargar_datos
import os

# ------------------------------------
# CONFIGURACIÓN INICIAL
# ------------------------------------

st.set_page_config(
    page_title="Dashboard de @101_Rescataditos",
    page_icon="🐾",
    layout="wide" 
)
# ------------------------------------
# DEFINICIÓN DE CONSTANTES
# ------------------------------------

# Paleta de colores - Sistema unificado
COLORES = {
    'primario': '#3498db',         # Azul - color principal
    'secundario': '#2c3e50',       # Azul oscuro - textos y detalles
    'rescate': '#CC7722',          # Naranja - rescates
    'adopcion': '#2ecc71',         # Verde - adopciones exitosas
    'gastos': '#ff0000',           # Rojo - gastos
    'donaciones': '#9b59b6',       # Morado - donaciones
    'neutral': '#ecf0f1',          # Gris claro - fondos
    'alerta': '#f39c12',           # Amarillo - advertencias
    'texto': '#2c3e50',            # Azul oscuro - texto principal
    'texto_secundario': '#7f8c8d', # Gris - texto secundario
    'fondo': '#ffffff',            # Blanco - fondo de tarjetas
    'borde': '#bdc3c7'             # Gris claro - bordes
}

# ------------------------------------
# FUNCIONES PARA ESTILIZADO
# ------------------------------------
def aplicar_estilo_general():
    """
    Aplica el estilo general CSS a la aplicación para mantener la consistencia visual.
    """
    st.markdown("""
    <style>
    /* Variables CSS para sistema de diseño unificado */
    :root {
        --color-primario: #3498db;
        --color-secundario: #2c3e50;
        --color-rescate: #CC7722;
        --color-adopcion: #2ecc71;
        --color-gastos: #e74c3c;
        --color-donaciones: #9b59b6;
        --color-neutral: #ecf0f1;
        --color-alerta: #f39c12;
        --color-texto: #2c3e50;
        --color-texto-secundario: #000000;
        --color-fondo: #ffffff;
        --color-borde: #bdc3c7;
        --radio-borde: 8px;
        --sombra: 0 4px 6px rgba(0, 0, 0, 0.1);
        --espacio-xs: 4px;
        --espacio-s: 8px;
        --espacio-m: 16px;
        --espacio-l: 24px;
    }
    
    /* Ajustes generales de página */
    .block-container {
        padding-top: 1rem !important;
        gap: 0.5rem !important; /* Reducir espacio entre bloques */
    }
    
    /* IMPORTANTE: Arreglar el estilo del título */
    .custom-title {
        font-size: 2.2rem;
        font-weight: bold;
        color: #000000;
        text-align: center;
        padding: 10px 0;
        margin-top: -6px !important; /* Aseguramos que no tenga margin-top negativo */
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        display: block !important; /* Forzar que se muestre como bloque */
        visibility: visible !important; /* Asegurar que sea visible */
    }
    
    /* Corregir posible problema con contenedores ocultos */
    .element-container {
        margin-bottom: 0.5rem !important;
        display: block !important; /* Asegurar que todos los contenedores se muestren */
    }
    
    /* Solo ocultar los contenedores completamente vacíos */
    div:empty:not(.custom-title) {
        display: none !important;
    }
    
    /* Encabezados */
    h1 {
        color: var(--color-texto);
        font-weight: 600;
        margin-top: 0px !important; /* Cambiar de -5px a 0px */
        margin-bottom: 15px !important;
    }
    
    h2 {
        color: var(--color-texto);
        font-weight: 500;
        margin-top: 10px !important;
        font-size: 1.6rem !important;
    }
    
    h3 {
        color: var(--color-texto);
        font-weight: 500;
        margin-top: 10px !important;
        font-size: 1.2rem !important;
    }
    
    /* Tarjetas de métricas rediseñadas */
    .metric-card {
        background-color: var(--color-fondo);
        border-radius: var(--radio-borde);
        padding: var(--espacio-m);
        box-shadow: var(--sombra);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
        margin-bottom: 0 !important; /* Eliminar margen inferior */
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-icon {
        font-size: 28px;
        margin-right: 10px;
        margin-bottom: 5px;
        display: inline-block;
        vertical-align: middle;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 0px;
        line-height: 1;
    }
    
    .metric-title {
        font-size: 18px;
        color: var(--color-texto-secundario);
        margin-bottom: 8px;
    }
    
    .metric-trend {
        font-size: 14px;
        margin-top: 8px;
        padding: 4px 8px;
        border-radius: 12px;
        display: inline-block;
    }
    
    .metric-trend-up {
        background-color: rgba(46, 204, 113, 0.2);
        color: #27ae60;
    }
    
    .metric-trend-down {
        background-color: rgba(231, 76, 60, 0.2);
        color: #c0392b;
    }
    
    .metric-trend-neutral {
        background-color: rgba(52, 152, 219, 0.2);
        color: #2980b9;
    }
    
    /* Estilos para filtros en sidebar */
    .filtro-seccion {
        background-color: var(--color-fondo);
        border-radius: var(--radio-borde);
        padding: var(--espacio-m);
        margin-bottom: var(--espacio-m);
        box-shadow: var(--sombra);
    }
    
    .filtro-titulo {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: var(--espacio-xs);
        color: var(--color-texto);
    }
    
    .filtro-item {
        margin-bottom: var(--espacio-s);
    }
    
    /* Etiquetas de filtros activos */
    .filtro-activo {
        display: inline-block;
        background-color: var(--color-primario);
        color: white;
        border-radius: 16px;
        padding: 4px 12px;
        margin-right: 6px;
        margin-bottom: 6px;
        font-size: 12px;
    }
    
    .filtro-activo-container {
        margin-top: 10px;
        margin-bottom: 15px;
    }
    
    /* Personalización de la lluvia de animales */
    .falling-animal {
        position: fixed;
        top: -40px;
        font-size: 2rem;
        pointer-events: none;
        user-select: none;
        animation: fall linear infinite;
    }
    
    @keyframes fall {
        to { transform: translateY(110vh) rotate(360deg); }
    }
    
    /* Personalización para selectores y entradas */
    div[data-baseweb="select"] > div {
        font-size: 0.85rem;
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        min-height: 35px !important;
        border-radius: var(--radio-borde);
    }

    div[data-baseweb="input"] > div {
        font-size: 0.85rem;
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        min-height: 35px !important;
        border-radius: var(--radio-borde);
    }
    
    section[data-testid="stSidebar"] div[class*="stSelectbox"], 
    section[data-testid="stSidebar"] div[class*="stDateInput"] {
        margin-bottom: 0px;
    }
    
    /* Estilos para los copos adaptados con íconos de animales */
    div[class*="Snowflake"] {
        color: transparent !important;
        font-size: 1.5rem !important;
    }
    
    div[class*="Snowflake"]::before {
        content: "🐶" !important;
    }
    
    /* Estilos para tarjetas de contenido */
    .content-card {
        background-color: var(--color-fondo);
        border-radius: var(--radio-borde);
        padding: var(--espacio-m);
        box-shadow: var(--sombra);
        margin-bottom: var(--espacio-m);
        border-top: 3px solid var(--color-primario);
    }
    
    /* Sección de insights destacados */
    .insight-card {
        background-color: rgba(52, 152, 219, 0.1);
        border-left: 4px solid var(--color-primario);
        padding: var(--espacio-m);
        margin-bottom: var(--espacio-m);
        border-radius: 0 var(--radio-borde) var(--radio-borde) 0;
    }
    
    /* Tooltips para información adicional */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: var(--color-secundario);
        color: white;
        text-align: center;
        border-radius: var(--radio-borde);
        padding: var(--espacio-s);
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    /* IMPORTANTE: Asegurar que las tablas tengan color de texto visible */
    /* Esto fuerza a que el texto en todas las tablas sea negro */
    .stDataFrame [data-testid="stDataFrameContainer"] div[data-testid="stDataFrame"] {
        color: #000000 !important;
    }
    
    /* Asegurar que las celdas de la tabla tengan texto negro */
    .stDataFrame [data-testid="stDataFrameContainer"] div[data-testid="stDataFrame"] div[role="cell"] {
        color: #000000 !important;
    }
    
    /* Para encabezados de tabla */
    .stDataFrame [data-testid="stDataFrameContainer"] div[data-testid="stDataFrame"] div[role="columnheader"] {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    /* Si quieres colores específicos para columnas de diferencia */
    .color-positivo {
        color: #2ecc71 !important;  /* Verde para positivo */
    }
    
    .color-negativo {
        color: #e74c3c !important;  /* Rojo para negativo */
    }
    /* REDUCIR ESPACIOS EN LA BARRA LATERAL */
    
    /* Reducir espaciado entre título de sección y filtros */
    .filtro-titulo {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 2px !important; /* Reducido de var(--espacio-xs) */
        color: var(--color-texto);
        padding-bottom: 0 !important;
    }
    
    /* Reducir espacio entre elementos de filtro */
    section[data-testid="stSidebar"] div.stMarkdown {
        margin-bottom: 5px !important;
    }
    
    /* Reducir espacio en general en la sidebar */
    section[data-testid="stSidebar"] div.block-container {
        padding-top: 0.5rem !important;
        gap: 0.3rem !important;
    }
    
    /* Ajustar espaciado de labels en filtros */
    section[data-testid="stSidebar"] label {
        margin-bottom: 0px !important;
        font-size: 0.8rem !important;
        padding-bottom: 0 !important;
    }
    
    /* Reducir altura de selectbox */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        min-height: 30px !important;
        padding-top: 2px !important;
        padding-bottom: 2px !important;
    }
    
    /* Reducir espacio interno de selectbox */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        margin-bottom: 5px !important;
    }
    
    /* Ajustar espaciado de títulos h3/h4 en sidebar */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        font-size: 1.2rem !important;
    }
    
    /* Ajuste general para texto en la sidebar */
    section[data-testid="stSidebar"] div {
        line-height: 1.1 !important;
    }
    
    /* Más específico para el título de "Período de tiempo" */
    section[data-testid="stSidebar"] div.filtro-titulo {
        padding-bottom: 2px !important;
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
def crear_tarjeta_metrica(titulo, valor, icono, tendencia=None, tendencia_valor=None, color="#3498db"):
    """
    Crea una tarjeta de métrica con estilo mejorado, incluyendo ícono y tendencia.
    
    Args:
        titulo (str): Título de la métrica
        valor (str/int/float): Valor principal a mostrar
        icono (str): Emoji o ícono a mostrar
        tendencia (str, opcional): Dirección de la tendencia ('up', 'down', 'neutral')
        tendencia_valor (str, opcional): Valor de la tendencia (ej: '12%')
        color (str, opcional): Color principal de la tarjeta
    
    Returns:
        str: HTML de la tarjeta de métrica
    """
    # Determinar la clase CSS para la tendencia
    tendencia_clase = ""
    tendencia_html = ""
    
    if tendencia and tendencia_valor:
        if tendencia == 'up':
            tendencia_clase = "metric-trend-up"
            tendencia_simbolo = "↑"
        elif tendencia == 'down':
            tendencia_clase = "metric-trend-down"
            tendencia_simbolo = "↓"
        else:
            tendencia_clase = "metric-trend-neutral"
            tendencia_simbolo = "→"
            
        tendencia_html = f'<div class="metric-trend {tendencia_clase}">{tendencia_simbolo} {tendencia_valor}</div>'
    
    # Crear la tarjeta HTML
    html = f"""
    <div class="metric-card" style="border-top: 3px solid {color};">
        <div class="metric-title">{titulo}</div>
        <div style="display: flex; align-items: center;">
            <div class="metric-icon" style="color: {color}">{icono}</div>
            <div class="metric-value" style="color: {color}">{valor}</div>
        </div>
        {tendencia_html}
    </div>
    """
    
    return html

def mostrar_filtros_activos(filtros):
    """
    Muestra etiquetas visuales para los filtros activos actualmente.
    
    Args:
        filtros (dict): Diccionario con filtros activos
    """
    filtros_activos = []
    
    # Verificar cada filtro y agregarlo si está activo
    if filtros.get('fecha_inicio') and filtros.get('fecha_fin'):
        inicio = filtros['fecha_inicio'].strftime("%d/%m/%Y")
        fin = filtros['fecha_fin'].strftime("%d/%m/%Y")
        #if inicio != fin:
           # filtros_activos.append(f"Período: {inicio} - {fin}")
    
    if filtros.get('año') and filtros['año'] != "Todos":
        filtros_activos.append(f"Año: {filtros['año']}")
        
    if filtros.get('mes') and filtros['mes'] != "Todos":
        filtros_activos.append(f"Mes: {filtros['mes'].split(' - ')[1]}")
        
    if filtros.get('mascota') and filtros['mascota'] != "Todas":
        filtros_activos.append(f"Mascota: {filtros['mascota']}")
        
    if filtros.get('tipo_gasto') and filtros['tipo_gasto'] != "Todos":
        filtros_activos.append(f"Tipo de gasto: {filtros['tipo_gasto']}")
    
    # Si hay filtros activos, mostrarlos
    if filtros_activos:
        html = '<div class="filtro-activo-container">'
        for filtro in filtros_activos:
            html += f'<div class="filtro-activo">{filtro}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

# ------------------------------------
# FUNCIONES DE CARGA DE DATOS
# ------------------------------------

def procesar_datos_mascotas(df):
    """
    Procesa y limpia los datos de mascotas.
    
    Args:
        df (pd.DataFrame): DataFrame original
        
    Returns:
        pd.DataFrame: DataFrame procesado
    """
    try:
        if df.empty:
            return df
            
        # Crear una copia para no modificar el original
        df = df.copy()
        
        # Normalizar nombres de columnas
        df.columns = df.columns.str.strip().str.upper()
        
        # Renombrar columnas al formato final deseado
        rename_mapping = {
            'ID': 'ID',
            'NOMBRE': 'Nombre',
            'FECHA': 'Fecha',
            'TIPO ANIMAL': 'TipoAnimal',
            'UBICACION': 'Ubicacion',
            'EDAD': 'Edad',
            'COLOR DE PELO': 'ColorPelo',
            'CONDICIÓN DE SALUD INICIAL': 'CondicionSaludInicial',
            'ESTADO ACTUAL': 'EstadoActual',
            'FECHA DE ADOPCION': 'FechaAdopcion',
            'ADOPTANTE': 'Adoptante',
            'ID_POST': 'ID_Post',
            'URL_INSTAGRAM': 'URL_Instagram',
            'URL_DRIVE': 'URL_Drive',
            'MESAÑO': 'MesAño'
        }
        
        # Aplicar renombrado donde las columnas existan
        for old_col, new_col in rename_mapping.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Procesar fechas
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'],format="%d/%m/%Y %H:%M:%S", errors='coerce')
            
        if 'FechaAdopcion' in df.columns:
            df['FechaAdopcion'] = pd.to_datetime(df['FechaAdopcion'],format="%d/%m/%Y", errors='coerce')
        else:
            # Si no existe, intentar derivarla del estado
            df['FechaAdopcion'] = None
            adoptados_mask = df['EstadoActual'].str.contains('Adoptado', case=False, na=False)
            df.loc[adoptados_mask, 'FechaAdopcion'] = df.loc[adoptados_mask, 'Fecha'] + pd.Timedelta(days=30)
        
        # Procesar colores de pelo
        if 'ColorPelo' in df.columns and df['ColorPelo'].dtype == object:
            def extract_main_color(color_json):
                try:
                    if pd.isna(color_json) or color_json == '':
                        return 'No especificado'
                    
                    # Si es un JSON como string
                    if isinstance(color_json, str) and ('[' in color_json or '{' in color_json):
                        colors = json.loads(color_json.replace("'", "\""))
                        if isinstance(colors, list) and len(colors) > 0:
                            # Tomar el color con mayor porcentaje
                            main_color = max(colors, key=lambda x: x.get('porcentaje', 0))
                            return main_color.get('color', 'No especificado')
                    
                    # Si es un string simple
                    return color_json
                except:
                    return 'No especificado'
            
            df['ColorPrincipal'] = df['ColorPelo'].apply(extract_main_color)
        
        # Extraer edad si está en una ubicación diferente
        if 'Edad' not in df.columns and 'Ubicacion' in df.columns:
            def extract_age(location):
                if pd.isna(location):
                    return 'No especificado'
                
                age_pattern = r'(\d+)\s*(mes|meses|año|años|semanas?|días?)'
                match = re.search(age_pattern, str(location))
                if match:
                    return match.group(0)
                return 'No especificado'
            
            df['Edad'] = df['Ubicacion'].apply(extract_age)
        
        # Asignar coordenadas aproximadas para ubicaciones
        # Define coordenadas base para Capital Federal y GBA
        location_coords = {
            'villa 1 11 14': (-34.6383, -58.4344),
            'BAJO FLORES': (-34.6415, -58.4267),
            'CABA': (-34.6037, -58.3816),
            'CABALLITO': (-34.6186, -58.4336),
            'CIUDAD AUTÓNOMA DE BUENOS AIRES': (-34.6037, -58.3816),
            'FLORES': (-34.6315, -58.4503),
            'LUGANO': (-34.6740, -58.4745),
            'POMPEYA': (-34.6555, -58.4097),
            'VILLA CRESPO': (-34.5974, -58.4321),
            'SOLDATI': (-34.6778, -58.4608),
        }
        
        # Función para determinar las coordenadas
        def get_coordinates(location):
            if pd.isna(location):
                return (-34.6037, -58.3816)  # Coordenadas por defecto (Capital)
            
            # Buscar coincidencias exactas primero
            for key, coords in location_coords.items():
                if key.lower() in str(location).lower():
                    return coords
            
            # Si no hay coincidencia, asignar coordenadas por defecto
            return (-34.6037, -58.3816)
        
        # Aplicar la función para obtener coordenadas
        df['Coordenadas'] = df['Ubicacion'].apply(get_coordinates)
        df['Latitud'] = df['Coordenadas'].apply(lambda x: x[0])
        df['Longitud'] = df['Coordenadas'].apply(lambda x: x[1])
        
        # Añadir columnas de año y mes para filtrado
        df['año'] = df['Fecha'].dt.year
        df['mes'] = df['Fecha'].dt.month
        
        # Asegurarse de que las columnas necesarias estén presentes
        required_fields = ['Nombre', 'Fecha', 'TipoAnimal', 'Ubicacion', 'EstadoActual']
        for field in required_fields:
            if field not in df.columns:
                if field == 'TipoAnimal' and 'TIPO ANIMAL' in df.columns:
                    df['TipoAnimal'] = df['TIPO ANIMAL']
                elif field == 'TipoAnimal' and 'Tipo' in df.columns:
                    df['TipoAnimal'] = df['Tipo']
                else:
                    df[field] = 'No especificado'
        
        # Limpiar el DataFrame
        df = df.dropna(subset=['Fecha'])  # Eliminar filas sin fecha
        
        return df
    except Exception as e:
        st.error(f"Error al procesar datos de mascotas: {str(e)}")
        # Devolver un DataFrame mínimo para evitar errores posteriores
        return pd.DataFrame({
            'Nombre': ['Error'], 
            'Fecha': [datetime.now()],
            'TipoAnimal': ['Error'],
            'EstadoActual': ['Error'],
            'año': [datetime.now().year],
            'mes': [datetime.now().month]
        })


def filtrar_datos(_df, filtros):
    """
    Filtra un DataFrame según los filtros aplicados, manejando correctamente "Todos".
    
    Args:
        _df (pd.DataFrame): DataFrame a filtrar
        filtros (dict): Diccionario con filtros a aplicar
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    try:
        if _df.empty:
            return _df
            
        # Crear una copia para no modificar el original
        df = _df.copy()
           # Filtrar por año si está especificado (y no es "Todos")
        if 'año' in filtros and filtros['año'] != "Todos" and 'año' in df.columns:
            df = df[df['año'] == filtros['año']]
        # Filtrar por mes si está especificado (y no es "Todos")
        if 'mes' in filtros and filtros['mes'] != "Todos" and 'mes' in df.columns:
            # Extraer el número de mes y filtrar
            mes_num = int(filtros['mes'].split(" - ")[0])
            df = df[df['mes'] == mes_num]
           
        # Filtrar por rango de fechas solo si no se han seleccionado filtros específicos de año o mes
        if (('año' not in filtros or filtros['año'] == "Todos") and
            ('mes' not in filtros or filtros['mes'] == "Todos") and
            'fecha_inicio' in filtros and 'fecha_fin' in filtros and 'Fecha' in df.columns):
            df = df[
                (df['Fecha'].dt.date >= filtros['fecha_inicio']) &
                (df['Fecha'].dt.date <= filtros['fecha_fin'])
            ]
            
        # Filtro por mascota (para gastos)
        if 'mascota' in filtros and filtros['mascota'] != "Todas" and 'MASCOTA' in df.columns:
            df = df[df['MASCOTA'] == filtros['mascota']]
        elif 'mascota' in filtros and filtros['mascota'] != "Todas" and 'Nombre' in df.columns:
            df = df[df['Nombre'] == filtros['mascota']]
            
        # Filtro por tipo de gasto
        if 'tipo_gasto' in filtros and filtros['tipo_gasto'] != "Todos" and 'TIPO DE GASTO' in df.columns:
            df = df[df['TIPO DE GASTO'] == filtros['tipo_gasto']]
        return df
        
    except Exception as e:
        st.error(f"Error al filtrar datos: {str(e)}")
        return _df  # Devolver el DataFrame original en caso de error


def calcular_tendencias(df_actual, df_anterior, columna_valor):
    """
    Calcula las tendencias comparando con un período anterior.
    
    Args:
        df_actual (pd.DataFrame): DataFrame del período actual
        df_anterior (pd.DataFrame): DataFrame del período anterior
        columna_valor (str): Nombre de la columna de valores a comparar
        
    Returns:
        tuple: (tendencia, porcentaje_cambio)
            tendencia: 'up', 'down' o 'neutral'
            porcentaje_cambio: variación porcentual
    """
    try:
        if df_actual.empty or df_anterior.empty or columna_valor not in df_actual.columns:
            return None, None
            
        valor_actual = df_actual[columna_valor].sum()
        valor_anterior = df_anterior[columna_valor].sum()
        
        if valor_anterior == 0:
            return 'neutral', '∞%'
            
        cambio = valor_actual - valor_anterior
        porcentaje = (cambio / valor_anterior) * 100
        
        if abs(porcentaje) < 1:
            return 'neutral', '0%'
        elif porcentaje > 0:
            return 'up', f"{porcentaje:.1f}%"
        else:
            return 'down', f"{abs(porcentaje):.1f}%"
            
    except Exception as e:
        st.error(f"Error al calcular tendencias: {str(e)}")
        return None, None

# ------------------------------------
# COMPONENTES DE DASHBOARD
# ------------------------------------
def crear_seccion_metricas(df_mascotas, df_gastos, df_donaciones,df_mascotas_orig, df_gastos_orig, df_donaciones_orig, filtros):
        """
        Crea la sección de métricas principales con diseño mejorado, evitando espacios en blanco.
        
        Args:
            df_mascotas (pd.DataFrame): DataFrame de mascotas
            df_gastos (pd.DataFrame): DataFrame de gastos
            df_donaciones (pd.DataFrame): DataFrame de donaciones
            filtros (dict): Filtros aplicados
        """

        # Calcular las métricas actuales
        total_rescatados = len(df_mascotas)
        total_adoptados = df_mascotas[df_mascotas['EstadoActual'] == 'Adoptado'].shape[0]
        total_gastos = df_gastos['Monto'].sum() if 'Monto' in df_gastos.columns else 0
        total_donaciones = df_donaciones['Monto'].sum() if 'Monto' in df_donaciones.columns else 0
        
        # Crear filtros para período anterior (para calcular tendencias)
        
        filtros_periodo_anterior = filtros.copy()
        
        # Estrategia para determinar período anterior basado en filtros aplicados
       # Caso 1: Filtro por mes específico en un año específico
        if filtros.get('mes') != "Todos" and filtros.get('año') != "Todos":
            mes_actual = int(filtros['mes'].split(" - ")[0])  # Extraer número de mes como int
            año_actual = int(filtros['año'])  # Convertir año a int para cálculos
            
            if mes_actual == 1:
                mes_anterior = 12
                año_anterior = año_actual - 1
            else:
                mes_anterior = mes_actual - 1
                año_anterior = año_actual

            filtros_periodo_anterior['mes'] =  f"{mes_anterior} - {calendar.month_name[mes_anterior]}"  # Final en INT
            filtros_periodo_anterior['año'] = año_anterior  # Final en INT

        # Caso 2: Filtro solo por año específico (mes = Todos)
        elif filtros.get('año') != "Todos" and filtros.get('mes') == "Todos":
            año_actual = int(filtros['año'])
            filtros_periodo_anterior['año'] = año_actual - 1  # Final en INT
            filtros_periodo_anterior['mes'] = "Todos"         # Mes sigue siendo string

        # Caso 3: No hay filtros específicos (ambos en "Todos")
        elif filtros.get('año') == "Todos" and filtros.get('mes') == "Todos":
            if 'fecha_inicio' in filtros and 'fecha_fin' in filtros:
                dias_periodo = (filtros['fecha_fin'] - filtros['fecha_inicio']).days + 1
                filtros_periodo_anterior['fecha_fin'] = filtros['fecha_fin'] - timedelta(days=1)
                filtros_periodo_anterior['fecha_inicio'] = filtros['fecha_inicio']
                print("periodo anterior",filtros_periodo_anterior)
        # Obtener datos del período anterior
        df_mascotas_anterior = filtrar_datos(df_mascotas_orig, filtros_periodo_anterior)
        df_gastos_anterior = filtrar_datos(df_gastos_orig, filtros_periodo_anterior)
        df_donaciones_anterior = filtrar_datos(df_donaciones_orig, filtros_periodo_anterior)

        # Calcular métricas del período anterior
        total_rescatados_anterior = len(df_mascotas_anterior)
        total_adoptados_anterior = df_mascotas_anterior[df_mascotas_anterior['EstadoActual'] == 'Adoptado'].shape[0]
        total_gastos_anterior = df_gastos_anterior['Monto'].sum() if 'Monto' in df_gastos_anterior.columns else 0
        total_donaciones_anterior = df_donaciones_anterior['Monto'].sum() if 'Monto' in df_donaciones_anterior.columns else 0
        
        # Calcular tendencias
        tendencia_rescatados = ('up' if total_rescatados > total_rescatados_anterior else 
                             'down' if total_rescatados < total_rescatados_anterior else 'neutral')
        pct_rescatados = f"{abs((total_rescatados - total_rescatados_anterior) / max(1, total_rescatados_anterior) * 100):.1f}%"
        
        tendencia_adoptados = ('up' if total_adoptados > total_adoptados_anterior else 
                             'down' if total_adoptados < total_adoptados_anterior else 'neutral')
        pct_adoptados = f"{abs((total_adoptados - total_adoptados_anterior) / max(1, total_adoptados_anterior) * 100):.1f}%"
        
        tendencia_gastos = ('down' if total_gastos < total_gastos_anterior else 
                          'up' if total_gastos > total_gastos_anterior else 'neutral')
        pct_gastos = f"{abs((total_gastos - total_gastos_anterior) / max(1, total_gastos_anterior) * 100):.1f}%"
        
        tendencia_donaciones = ('up' if total_donaciones > total_donaciones_anterior else 
                             'down' if total_donaciones < total_donaciones_anterior else 'neutral')
        pct_donaciones = f"{abs((total_donaciones - total_donaciones_anterior) / max(1, total_donaciones_anterior) * 100):.1f}%"
        
        # Crear las columnas para las métricas
        # IMPORTANTE: Envolvemos todo en un solo contenedor para evitar espacios
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(
                    crear_tarjeta_metrica(
                        "Animales Rescatados", 
                        f"{total_rescatados}", 
                        "🐾", 
                        tendencia_rescatados, 
                        pct_rescatados,
                        COLORES['rescate']
                    ), 
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    crear_tarjeta_metrica(
                        "Animales Adoptados", 
                        f"{total_adoptados}", 
                        "🏠", 
                        tendencia_adoptados, 
                        pct_adoptados,
                        COLORES['adopcion']
                    ), 
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    crear_tarjeta_metrica(
                        "Total de Gastos", 
                        f"${total_gastos:,.0f}", 
                        "💰", 
                        tendencia_gastos, 
                        pct_gastos,
                        COLORES['gastos']
                    ), 
                    unsafe_allow_html=True
                )
            
            with col4:
                st.markdown(
                    crear_tarjeta_metrica(
                        "Total de Donaciones", 
                        f"${total_donaciones:,.0f}", 
                        "💸", 
                        tendencia_donaciones, 
                        pct_donaciones,
                        COLORES['donaciones']
                    ), 
                    unsafe_allow_html=True
                )
        
        # Información del período de comparación para mostrar en mensaje
        periodo_actual = ""
        periodo_anterior = ""
        
        # Asegurarse que existen los valores en filtros
        if filtros.get('mes') is not None and filtros.get('año') is not None:
            if filtros['mes'] != "Todos" and filtros['año'] != "Todos":
                # Ambos son específicos: año y mes
                mes_actual_nombre = filtros['mes'].split(" - ")[1]
                mes_anterior_nombre = filtros_periodo_anterior['mes'].split(" - ")[1]
                periodo_actual = f"{mes_actual_nombre} {filtros['año']}"
                periodo_anterior = f"{mes_anterior_nombre} {filtros_periodo_anterior['año']}"
            elif filtros['mes'] == "Todos" and filtros['año'] != "Todos":
                # Mes = Todos, pero año específico
                periodo_actual = f"{filtros['año']}"
                periodo_anterior = f"{filtros_periodo_anterior['año']}"
            else:
                # Mes = Todos y Año = Todos
                periodo_actual = "Todos"
                periodo_anterior = "Todos"

        elif filtros.get('año') is not None:
            if filtros['año'] != "Todos":
                periodo_actual = f"{filtros['año']}"
                periodo_anterior = f"{filtros_periodo_anterior['año']}"
            else:
                periodo_actual = "Todos"
                periodo_anterior = "Todos"
        else:
            # Caso muy raro: no hay nada
            periodo_actual = "Todos"
            periodo_anterior = "Todos"

            
        # Mostrar mensaje con insight principal
        # IMPORTANTE: Lo ponemos en el mismo contenedor para evitar espacios adicionales
        mensaje_insight = None
        
        #if tendencia_donaciones == 'up' and tendencia_gastos != 'up':
        #    mensaje_insight = f"🎉 ¡Excelente! Las donaciones aumentaron un {pct_donaciones} mientras que los gastos se mantuvieron controlados."
        #elif total_donaciones > total_gastos:
        #    mensaje_insight = f"✅ Balance positivo: Las donaciones superan a los gastos por ${total_donaciones - total_gastos:,.0f}"
        #elif tendencia_adoptados == 'up' and pct_adoptados and float(pct_adoptados.replace('%', '')) > 10:
        #    mensaje_insight = f"🏠 ¡Gran trabajo! Las adopciones aumentaron un {pct_adoptados} en este período."
        #
        ## Solo mostrar los mensajes si existe algún insight real
        #if mensaje_insight:
        #    st.success(mensaje_insight)
 


def crear_grafico_distribucion_tipo(df_mascotas):
    """
    Crea el gráfico de distribución por tipo de animal.
    
    Args:
        df_mascotas (pd.DataFrame): DataFrame de mascotas filtrado
    """
    try:
        if df_mascotas.empty or 'TipoAnimal' not in df_mascotas.columns:
            st.warning("No hay datos suficientes para mostrar la distribución por tipo de animal.")
            return
            
        # Calcular distribución por tipo
        type_counts = df_mascotas['TipoAnimal'].value_counts().reset_index()
        type_counts.columns = ['TipoAnimal', 'Cantidad']
        
        # Crear gráfico de torta con diseño mejorado
        fig_pie = px.pie(
            type_counts,
            values='Cantidad',
            names='TipoAnimal',
            hole=0.4,
            color_discrete_sequence=[COLORES['primario'], COLORES['adopcion'], COLORES['rescate'], COLORES['alerta']],
        )
        
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color=COLORES['fondo'], width=2))
        )
        
        fig_pie.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            font=dict(family="Arial", size=12),
            paper_bgcolor=COLORES['fondo'],
            plot_bgcolor=COLORES['fondo']
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Mostrar estadísticas adicionales
        total_animales = type_counts['Cantidad'].sum()
        adoptados = df_mascotas[df_mascotas['EstadoActual'] == 'Adoptado'].shape[0] 
  
    except Exception as e:
        st.error(f"Error al crear gráfico de distribución: {str(e)}")

def crear_grafico_gastos_donaciones(df_gastos, df_donaciones):
    """
    Crea el gráfico de comparación entre gastos y donaciones.
    
    Args:
        df_gastos (pd.DataFrame): DataFrame de gastos filtrado
        df_donaciones (pd.DataFrame): DataFrame de donaciones filtrado
    """
    try:
        if (df_gastos.empty or 'Monto' not in df_gastos.columns or 
            df_donaciones.empty or 'Monto' not in df_donaciones.columns):
            st.warning("No hay datos suficientes para mostrar el gráfico de gastos y donaciones.")
            return
        
        # Preparar datos de gastos mensuales
        gastos_mensuales = df_gastos.groupby(['año', 'mes']).agg(
            total_gastos=('Monto', 'sum'),
            num_registros=('Monto', 'count')
        ).reset_index()
        
        # Preparar datos de donaciones mensuales
        donaciones_mensuales = df_donaciones.groupby(['año', 'mes']).agg(
            total_donaciones=('Monto', 'sum')
        ).reset_index()
        
        # Crear columna de fecha para ordenamiento y visualización
        gastos_mensuales['fecha'] = pd.to_datetime(
            gastos_mensuales['año'].astype(str) + '-' + 
            gastos_mensuales['mes'].astype(str) + '-01'
        )
        gastos_mensuales = gastos_mensuales.sort_values('fecha')
        gastos_mensuales['mes_año'] = gastos_mensuales['fecha'].dt.strftime('%b %Y')
        
        donaciones_mensuales['fecha'] = pd.to_datetime(
            donaciones_mensuales['año'].astype(str) + '-' + 
            donaciones_mensuales['mes'].astype(str) + '-01'
        )
        donaciones_mensuales = donaciones_mensuales.sort_values('fecha')
        donaciones_mensuales['mes_año'] = donaciones_mensuales['fecha'].dt.strftime('%b %Y')
        
        # Crear figura para ambas líneas
        fig = go.Figure()
        
        # Agregar línea de gastos
        fig.add_trace(go.Scatter(
            x=gastos_mensuales['fecha'],
            y=gastos_mensuales['total_gastos'],
            mode='lines+markers',
            name='Gastos',
            line=dict(color=COLORES['gastos'], width=3),
            marker=dict(size=8, line=dict(width=2, color=COLORES['fondo']))
        ))
        
        # Agregar línea de donaciones
        fig.add_trace(go.Scatter(
            x=donaciones_mensuales['fecha'],
            y=donaciones_mensuales['total_donaciones'],
            mode='lines+markers',
            name='Donaciones',
            line=dict(color=COLORES['donaciones'], width=3),
            marker=dict(size=8, line=dict(width=2, color=COLORES['fondo']))
        ))
        
        # Configurar diseño del gráfico
        fig.update_layout(
            title='',
            xaxis_title='Mes',
            yaxis_title='Monto ($)',
            xaxis=dict(
                tickformat='%b %Y', 
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(gridcolor=COLORES['borde']),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            template='plotly_white',
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor=COLORES['fondo'],
            plot_bgcolor=COLORES['fondo']
        )
        
        # Añadir área sombreada para déficit (cuando gastos > donaciones)
        for i in range(len(gastos_mensuales)):
            if i < len(donaciones_mensuales):
                fecha = gastos_mensuales.iloc[i]['fecha']
                gasto = gastos_mensuales.iloc[i]['total_gastos']
                
                # Encontrar la donación correspondiente al mismo mes/año
                donacion_mismo_periodo = donaciones_mensuales[
                    (donaciones_mensuales['año'] == gastos_mensuales.iloc[i]['año']) & 
                    (donaciones_mensuales['mes'] == gastos_mensuales.iloc[i]['mes'])
                ]
                
                if not donacion_mismo_periodo.empty:
                    donacion = donacion_mismo_periodo.iloc[0]['total_donaciones']
                    
                    # Si hay déficit, añadir área sombreada
                    if gasto > donacion:
                        fig.add_trace(go.Scatter(
                            x=[fecha, fecha],
                            y=[donacion, gasto],
                            fill='tonexty',
                            fillcolor='rgba(231, 76, 60, 0.2)',
                            line=dict(color='rgba(0,0,0,0)'),
                            showlegend=False,
                            hoverinfo='none'
                        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error al crear gráfico de gastos y donaciones: {str(e)}")

def detalle_gastos_donaciones(filtered_gastos, filtered_donaciones):
            # Preparar datos de gastos
        gastos_mensuales = filtered_gastos.groupby(['año', 'mes']).agg(
            total_gastos=('Monto', 'sum'),
            num_registros=('Monto', 'count')
        ).reset_index()

        donaciones_mensuales = (
            filtered_donaciones
            .groupby(['año','mes'])['Monto']
            .agg(total_donaciones='sum')
            .reset_index()
        )

        gastos_mensuales['fecha'] = pd.to_datetime(gastos_mensuales['año'].astype(str) + '-' + 
                                                gastos_mensuales['mes'].astype(str) + '-01')
        gastos_mensuales = gastos_mensuales.sort_values('fecha')
        gastos_mensuales['mes_año'] = gastos_mensuales['fecha'].dt.strftime('%b %Y')
        
        donaciones_mensuales['fecha'] = pd.to_datetime(
            donaciones_mensuales['año'].astype(str)
            + '-' + donaciones_mensuales['mes'].astype(str)
            + '-01'
        )
        donaciones_mensuales = donaciones_mensuales.sort_values('fecha') 
        donaciones_mensuales['mes_año'] = donaciones_mensuales['fecha'].dt.strftime('%b %Y')
 # 1) Prepara los dos DataFrames
        g = gastos_mensuales[['mes_año','total_gastos']]
        d = donaciones_mensuales[['mes_año','total_donaciones']]
            # 1) Fusiona gastos y donaciones por mes_año (ya en formato string 'Feb 2025')
        resumen = pd.merge(g, d, on='mes_año', how='outer').fillna(0)

        # 2) Crea la columna de diferencia numérica
        resumen['diferencia'] = resumen['total_donaciones'] - resumen['total_gastos']

        # 3) Crea columna datetime para ordenar
        resumen['periodo'] = pd.to_datetime(resumen['mes_año'], format='%b %Y')

        # 4) Ordena cronológicamente
        resumen = ( resumen.sort_values('periodo', ascending=False).reset_index(drop=True))
        # 5) Renombra todas las columnas de una vez, incluyendo la diferencia
        resumen = resumen.rename(columns={
            'mes_año':            'Mes‑Año',
            'total_gastos':       'Total Gastos ($)',
            'total_donaciones':   'Total Donaciones ($)',
            'diferencia':         'Diferencia ($)'
        })

        # 6) Selecciona el orden definitivo de columnas para mostrar
        resumen = resumen[[
            'Mes‑Año',
            'Total Gastos ($)',
            'Total Donaciones ($)',
            'Diferencia ($)'
        ]]

# Otra solución: HTML puro con estilos inline
def mostrar_tabla_html(df_gastos, df_donaciones):
    """Solución con HTML puro para evitar problemas de color"""
    # Agrupar y calcular como antes...
    
    # Luego, en lugar de usar st.dataframe, creamos HTML directamente:
    html = """
    <div style="color: #000000;">  <!-- Forzar color negro para el texto -->
        <h3>Resumen de Gastos y Donaciones</h3>
        <table style="width:100%; border-collapse:collapse; margin:20px 0; color:#000000;">
            <tr style="background-color:#f0f0f0;">
                <th style="padding:10px; text-align:left; border:1px solid #ddd;">Período</th>
                <th style="padding:10px; text-align:left; border:1px solid #ddd;">Gastos ($)</th>
                <th style="padding:10px; text-align:left; border:1px solid #ddd;">Donaciones ($)</th>
                <th style="padding:10px; text-align:left; border:1px solid #ddd;">Diferencia ($)</th>
            </tr>
    """
    
    # Añadir cada fila con colores inline (esto garantiza que se vean)
    for _, row in resumen.iterrows():
        # Determinar color para diferencia
        if row['diferencia'] > 0:
            dif_color = "#2ecc71"  # Verde
        elif row['diferencia'] < 0:
            dif_color = "#e74c3c"  # Rojo
        else:
            dif_color = "#000000"  # Negro
            
        html += f"""
        <tr style="border:1px solid #ddd;">
            <td style="padding:8px; border:1px solid #ddd;">{row['mes_año']}</td>
            <td style="padding:8px; border:1px solid #ddd;">${row['total_gastos']:,.0f}</td>
            <td style="padding:8px; border:1px solid #ddd;">${row['total_donaciones']:,.0f}</td>
            <td style="padding:8px; border:1px solid #ddd; color:{dif_color};">${row['diferencia']:,.0f}</td>
        </tr>
        """
    
    html += """
        </table>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
  
def crear_grafico_actividad(df_mascotas, filtros):
    """
    Crea el gráfico de actividad (rescates y adopciones).
    
    Args:
        df_mascotas (pd.DataFrame): DataFrame de mascotas filtrado
        filtros (dict): Filtros aplicados
    """
    try:
        if df_mascotas.empty:
            st.warning("No hay datos suficientes para mostrar el gráfico de actividad.")
            return
            
        año_sel = filtros.get('año', "Todos")
        
        if año_sel == "Todos":
            # Mostrar agrupado por año
            actividad_anual = df_mascotas.groupby('año').agg(
                Rescates=('Nombre', 'count'),
                Adopciones=('FechaAdopcion', lambda x: x.notna().sum())
            ).reset_index()
            
            actividad_anual['Periodo'] = actividad_anual['año'].astype(str)
            
            df_plot = pd.melt(
                actividad_anual,
                id_vars=['Periodo'],
                value_vars=['Rescates', 'Adopciones'],
                var_name='Tipo',
                value_name='Cantidad'
            )
            
            # Ordenar por período
            df_plot['Periodo'] = pd.to_datetime(df_plot['Periodo'], format='%Y').dt.year.astype(str)
            df_plot = df_plot.sort_values('Periodo')
            
        else:
            # Mostrar agrupado por mes dentro del año seleccionado
            actividad_mensual = df_mascotas.groupby('mes').agg(
                Rescates=('Nombre', 'count'),
                Adopciones=('FechaAdopcion', lambda x: x.notna().sum())
            ).reset_index()
            
            # Convertir número de mes a nombre (e.g. 1 → Ene)
            actividad_mensual['Periodo'] = actividad_mensual['mes'].apply(
                lambda m: pd.to_datetime(f'2023-{m}-01').strftime('%b')
            )
            
            df_plot = pd.melt(
                actividad_mensual,
                id_vars=['Periodo', 'mes'],
                value_vars=['Rescates', 'Adopciones'],
                var_name='Tipo',
                value_name='Cantidad'
            )
            
            # Ordenar por mes
            meses_orden = {pd.to_datetime(f'2023-{i}-01').strftime('%b'): i for i in range(1, 13)}
            df_plot['mes_num'] = df_plot['Periodo'].map(meses_orden)
            df_plot = df_plot.sort_values('mes_num')
            
        # Crear gráfico de barras
        fig = px.bar(
            df_plot,
            x='Periodo',
            y='Cantidad',
            color='Tipo',
            barmode='group',
            labels={'Periodo': 'Período', 'Cantidad': 'Cantidad', 'Tipo': ''},
            color_discrete_map={'Rescates': COLORES['rescate'], 'Adopciones': COLORES['adopcion']}
        )
        
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(tickangle=0),
            paper_bgcolor=COLORES['fondo'],
            plot_bgcolor=COLORES['fondo'],
            yaxis=dict(gridcolor=COLORES['borde'])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Añadir insights sobre la actividad
        if año_sel != "Todos":
            # Calcular tasa de adopción (adopciones/rescates)
            total_rescates = df_plot[df_plot['Tipo'] == 'Rescates']['Cantidad'].sum()
            total_adopciones = df_plot[df_plot['Tipo'] == 'Adopciones']['Cantidad'].sum()
            
            if total_rescates > 0:
                tasa_adopcion = (total_adopciones / total_rescates) * 100
                
                if tasa_adopcion >= 80:
                    st.success(f"🌟 Excelente tasa de adopción del {tasa_adopcion:.1f}% en {año_sel}!")
                elif tasa_adopcion >= 50:
                    st.info(f"👍 Buena tasa de adopción del {tasa_adopcion:.1f}% en {año_sel}.")
                else:
                    st.warning(f"⚠️ La tasa de adopción es del {tasa_adopcion:.1f}% en {año_sel}. Hay oportunidad de mejora.")
        
    except Exception as e:
        st.error(f"Error al crear gráfico de actividad: {str(e)}")

def crear_mapa_calor_adopcion(df_mascotas):
    """
    Crea el mapa de calor de adopción por tipo y color de animal.
    
    Args:
        df_mascotas (pd.DataFrame): DataFrame de mascotas filtrado
    """
    try:
        # Filtrar sólo animales adoptados
        adoption_data = df_mascotas[df_mascotas['FechaAdopcion'].notna()].copy()
        
        if adoption_data.empty:
            st.warning("No hay datos de adopción disponibles para crear el mapa de calor.")
            return
            
        # Calcular días hasta adopción
        adoption_data['DiasHastaAdopcion'] = (adoption_data['FechaAdopcion'] - adoption_data['Fecha']).dt.days
        
        # Si existe ColorPelo como JSON, extraer color principal
        if 'ColorPelo' in adoption_data.columns and adoption_data['ColorPelo'].dtype == object:
            def extract_primary_color(color_json):
                try:
                    if pd.isna(color_json) or color_json == '':
                        return 'No especificado'
                    
                    # Si es un JSON como string
                    if isinstance(color_json, str) and ('[' in color_json or '{' in color_json):
                        colors = json.loads(color_json.replace("'", "\""))
                        if isinstance(colors, list) and len(colors) > 0:
                            # Tomar el color con mayor porcentaje
                            max_percentage = 0
                            primary_color = ""
                            for color_info in colors:
                                if color_info.get("porcentaje", 0) > max_percentage:
                                    max_percentage = color_info.get("porcentaje", 0)
                                    primary_color = color_info.get("color", "")
                            return primary_color
                        return "No especificado"
                    
                    # Si es un string simple
                    return color_json if isinstance(color_json, str) else "No especificado"
                except (json.JSONDecodeError, AttributeError, TypeError):
                    # Si no es un JSON válido, devolver el valor original o No especificado
                    return color_json if isinstance(color_json, str) else "No especificado"
            
            adoption_data['ColorPrimario'] = adoption_data['ColorPelo'].apply(extract_primary_color)
        elif 'ColorPrincipal' in adoption_data.columns:
            adoption_data['ColorPrimario'] = adoption_data['ColorPrincipal']
        else:
            adoption_data['ColorPrimario'] = 'No especificado'
        
        # Crear pivot table para el mapa de calor
        pivot = adoption_data.pivot_table(
            values='DiasHastaAdopcion',
            index='TipoAnimal',
            columns='ColorPrimario',
            aggfunc='mean'
        )
        
        # Verificar conteo para cada combinación
        counts_pivot = adoption_data.pivot_table(
            values='DiasHastaAdopcion',
            index='TipoAnimal',
            columns='ColorPrimario',
            aggfunc='count'
        )
        
        # Aplicar máscara para celdas con menos de 2 animales (para evitar outliers)
        mask = counts_pivot < 2
        pivot = pivot.mask(mask)
        
        if not pivot.empty and pivot.notna().sum().sum() > 0:
            # Crear y mostrar el heatmap
            fig_heat = px.imshow(
                pivot,
                labels=dict(x="Color", y="Tipo", color="Días promedio"),
                color_continuous_scale='YlOrRd_r',  # Escala invertida: amarillo (rápido) a rojo (lento)
                aspect="auto",
                text_auto='.0f'  # Mostrar valores enteros
            )
            
            # Añadir anotaciones con el conteo de animales
            annotations = []
            for i, index in enumerate(pivot.index):
                for j, column in enumerate(pivot.columns):
                    count = counts_pivot.loc[index, column] if pd.notna(counts_pivot.loc[index, column]) else 0
                    if count >= 2:  # Solo mostrar conteo para celdas válidas
                        annotations.append(
                            dict(
                                x=column,
                                y=index,
                                text=f"({int(count)})",
                                showarrow=False,
                                font=dict(size=8, color="black")
                            )
                        )
            
            fig_heat.update_layout(
                height=400,
                margin=dict(l=10, r=10, t=10, b=10),
                annotations=annotations,
                paper_bgcolor=COLORES['fondo'],
                plot_bgcolor=COLORES['fondo']
            )
            
            st.plotly_chart(fig_heat, use_container_width=True)
            
            # Encontrar combinaciones más rápidas
            min_days = pivot.min().min()
            if pd.notna(min_days):
                # Encontrar combinación tipo-color con menor tiempo de adopción
                min_idx = pivot.stack().idxmin()
                if isinstance(min_idx, tuple) and len(min_idx) == 2:
                    min_type, min_color = min_idx
                    
                    # Mostrar insight sobre combinación más rápida
                    st.info(f"💡 La combinación que se adopta más rápido es: **{min_type}** con color **{min_color}** ({min_days:.0f} días)")
                    
                    # Mostrar las 3 combinaciones más rápidas
                    tipo_color_datos = adoption_data.groupby(['TipoAnimal', 'ColorPrimario'])['DiasHastaAdopcion'].agg(['mean', 'count']).reset_index()
                    tipo_color_datos.columns = ['TipoAnimal', 'ColorPelo', 'DiasPromedio', 'Cantidad']
                    
                    # Filtrar para mostrar solo combinaciones con al menos 2 animales
                    tipo_color_datos = tipo_color_datos[tipo_color_datos['Cantidad'] >= 2].sort_values('DiasPromedio')
                    
                    top_combinaciones = tipo_color_datos.nsmallest(3, 'DiasPromedio')
                    if len(top_combinaciones) > 0:
                        st.markdown("**Combinaciones más rápidas de adopción:**")
                        for i, row in enumerate(top_combinaciones.itertuples(), 1):
                            st.markdown(f"**{i}.** {row.TipoAnimal} de color **{row.ColorPelo}**: **{row.DiasPromedio:.0f} días** ({row.Cantidad} animales)")
        else:
            st.info("No hay suficientes datos para crear un mapa de calor significativo.")
            
    except Exception as e:
        st.error(f"Error al crear mapa de calor de adopción: {str(e)}")

def crear_mapa_rescates(df_mascotas):
    """
    Crea un mapa de los lugares de rescate.
    
    Args:
        df_mascotas (pd.DataFrame): DataFrame de mascotas filtrado
    """
    try:
        if df_mascotas.empty or 'Latitud' not in df_mascotas.columns or 'Longitud' not in df_mascotas.columns:
            st.warning("No hay datos de ubicación disponibles para crear el mapa.")
            return
            
        # Crear mapa base centrado en Buenos Aires
        m = folium.Map(
            location=[-34.6037, -58.3816],
            zoom_start=11,
            tiles='CartoDB positron'  # Estilo más limpio
        )
        
        # Agrupar por ubicación para contar rescates
        location_counts = df_mascotas.groupby(['Ubicacion', 'Latitud', 'Longitud']).size().reset_index(name='count')
        
        # Añadir marcadores con información
        for idx, row in location_counts.iterrows():
            # Calcular el tamaño del círculo según la cantidad (mínimo 5, máximo 15)
            radius = min(15, max(5, row['count'] * 1.5))
            
            # Definir el color según la cantidad (más intenso para mayor cantidad)
            color = COLORES['rescate']
            
            # Crear HTML personalizado para el popup
            popup_html = f"""
            <div style="font-family: Arial; width: 150px;">
                <h4 style="margin: 5px 0; color: {COLORES['texto']};">{row['Ubicacion']}</h4>
                <p style="margin: 3px 0;">Animales: <b>{row['count']}</b></p>
            </div>
            """
            
            # Crear el popup
            popup = folium.Popup(popup_html, max_width=200)
            
            # Añadir marcador
            folium.CircleMarker(
                location=[row['Latitud'], row['Longitud']],
                radius=radius,
                popup=popup,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                weight=2
            ).add_to(m)
        
        # Añadir control de escala
        folium.plugins.MeasureControl(position='bottomleft', primary_length_unit='meters').add_to(m)
        
        # Añadir mini mapa
        folium.plugins.MiniMap(toggle_display=True).add_to(m)
        
        # Mostrar el mapa
        folium_static(m)
        
        # Mostrar información adicional
        st.markdown(f"""
        <div class="insight-card">
            <h4>Distribución geográfica de rescates</h4>
            <p>El mapa muestra la concentración de los {len(df_mascotas)} animales rescatados en diferentes zonas. 
            Las áreas con círculos más grandes indican mayor cantidad de rescates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error al crear mapa de rescates: {str(e)}")

def crear_edad_tipo_adopcion(df_mascotas):
    adoption_data = df_mascotas[df_mascotas['FechaAdopcion'].notna()].copy()
    adoption_data['DiasHastaAdopcion'] = (adoption_data['FechaAdopcion'] - adoption_data['Fecha']).dt.days

    if not adoption_data.empty:
        # Crear tabla pivote para el heatmap
        pivot_tipo_edad = adoption_data.pivot_table(
            values='DiasHastaAdopcion',
            index='TipoAnimal',      # Eje Y: Tipo de Animal
            columns='Edad',          # Eje X: Edad
            aggfunc='mean'           # Valor: Días promedio
        ).fillna(0)                  # Rellenar valores ausentes con 0

        # Crear y mostrar el heatmap
        fig_heatmap = px.imshow(
            pivot_tipo_edad,
            title='Días hasta adopción',
            labels=dict(x="Edad", y="Tipo", color="Días promedio"),
            color_continuous_scale='YlOrRd_r',  # Escala invertida: amarillo (rápido) a rojo (lento)
            aspect="auto",
            text_auto='.0f'  # Mostrar valores sin decimales para mejor visualización
        )
        fig_heatmap.update_layout(height=350, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Identificar las combinaciones más rápidas
        if pivot_tipo_edad.size > 0:  # Verificar que el pivot no esté vacío
            min_idx = pivot_tipo_edad.values.argmin()
            min_tipo = pivot_tipo_edad.index[min_idx // len(pivot_tipo_edad.columns)]
            min_edad = pivot_tipo_edad.columns[min_idx % len(pivot_tipo_edad.columns)]
            min_dias = pivot_tipo_edad.values.min()

            if min_dias > 0:  # Solo mostrar si hay datos válidos
                st.info(f"💡 Más rápido: **{min_tipo}** de edad **{min_edad}** ({min_dias:.0f} días)")
    else:
        st.info("No hay datos de adopción disponibles")

# ------------------------------------
# FUNCIÓN PRINCIPAL DEL DASHBOARD
# ------------------------------------

def main():
    """
    Función principal que ejecuta el dashboard.
    """
    # Aplicar estilo general
    aplicar_estilo_general()
    
    # Crear título personalizado
    st.markdown('<div class="custom-title">🐾 Dashboard de @101_Rescataditos</div>', unsafe_allow_html=True)    
   
    # ---- SIDEBAR: FILTROS ----
    with st.sidebar:
        st.markdown('<hr style="margin: 15px 0 15px 0; border-color: #ddd;">', unsafe_allow_html=True)
        st.header("📅 Período de tiempo")
        
        # Cargar datos iniciales para establecer opciones de filtros
        df_mascotas_init = cargar_datos("Datos")
        df_mascotas_init = procesar_datos_mascotas(df_mascotas_init)
        df_gastos_init = cargar_datos("Gastos")
      
        
        # Sección 1: Filtros principales (año y mes)
        with st.container():
            #st.markdown('<div class="filtro-titulo">📅 Período de tiempo</div>', unsafe_allow_html=True)
            
            # Determinar años disponibles
            if not df_mascotas_init.empty and 'año' in df_mascotas_init.columns:
                años = ["Todos"] + sorted(df_mascotas_init['año'].unique().tolist(), reverse=True)
            else:
                años = ["Todos", datetime.now().year, datetime.now().year - 1]
            
            # Selector de año (principal)
            año_sel = st.selectbox(
                "Año",
                años,
                key="año_sel"
                #,help="Selecciona un año específico o 'Todos' para ver datos de todos los años"
            )
            
            # Selector de mes (secundario, dependiente del año)
            meses = ["Todos"] + [f"{i} - {calendar.month_name[i]}" for i in range(1, 13)]
            mes_sel = st.selectbox(
                "Mes",
                meses,
                key="mes_sel"
                #,help="Selecciona un mes específico o 'Todos' para ver datos de todos los meses del año seleccionado"
            )
            
            # Rango de fechas (solo visible si se selecciona "Todos" en año y mes)
            if año_sel == "Todos" and mes_sel == "Todos":
                #st.markdown('<div class="filtro-subtitulo">Rango de fechas personalizado:</div>', unsafe_allow_html=True)
                
                if not df_mascotas_init.empty and 'Fecha' in df_mascotas_init.columns:
                    min_date = df_mascotas_init['Fecha'].min().date()
                    max_date = df_mascotas_init['Fecha'].max().date()
                else:
                    min_date = datetime.now().date() - timedelta(days=365)
                    max_date = datetime.now().date()
                
                # Selector de rango de fechas (ahora secundario)
                #start_date, end_date = st.date_input(
                #    "Filtrar por rango de fechas específico",
                #    [min_date, max_date],
                #    min_value=min_date,
                #    max_value=max_date,
                #    key="rango_fechas",
                #    help="Este filtro se aplica solo cuando no se selecciona un año o mes específico"
                #)
            else:
                # Valores por defecto para el rango de fechas cuando se usa año/mes
                if not df_mascotas_init.empty and 'Fecha' in df_mascotas_init.columns:
                    min_date = df_mascotas_init['Fecha'].min().date()
                    max_date = df_mascotas_init['Fecha'].max().date()
                else:
                    min_date = datetime.now().date() - timedelta(days=365)
                    max_date = datetime.now().date()
                #start_date, end_date = min_date, max_date
            start_date, end_date = min_date, max_date
        #st.markdown('<hr style="margin: 15px 0 15px 0; border-color: #ddd;">', unsafe_allow_html=True)
        
        # Sección 2: Filtros secundarios
        #with st.container():
        #    st.markdown('<div class="filtro-titulo">🔍 Filtros adicionales</div>', unsafe_allow_html=True)
        #    
        #    # Cargar lista de mascotas para filtro
        #    if not df_mascotas_init.empty and 'Nombre' in df_mascotas_init.columns:
        #        mascotas = ["Todas"] + sorted(df_mascotas_init['Nombre'].unique().tolist())
        #    else:
        #        mascotas = ["Todas"]
        #        
        #    # Selector de mascota
        #    mascota_sel = st.selectbox(
        #        "Mascota",
        #        mascotas,
        #        key="mascota_sel",
        #        help="Filtra datos para una mascota específica"
        #    )
        #    
        #    # Cargar tipos de gasto para filtro
        #    if not df_gastos_init.empty and 'TIPO DE GASTO' in df_gastos_init.columns:
        #        tipo_gastos = ["Todos"] + sorted(df_gastos_init['TIPO DE GASTO'].unique().tolist())
        #    else:
        #        tipo_gastos = ["Todos"]
        #        
        #    # Selector de tipo de gasto
        #    tipo_sel = st.selectbox(
        #        "Tipo de Gasto",
        #        tipo_gastos,
        #        key="tipo_sel",
        #        help="Filtra gastos por categoría"
        #    )
        
        #st.markdown('<hr style="margin: 15px 0 15px 0; border-color: #ddd;">', unsafe_allow_html=True)
        
        # Checkbox para activar la lluvia de animales
        lluvia_animales = st.checkbox(
            "🌧️ Lluvia de animales felices",
            value=False,
            key="rain_animals",
            help="Activa una animación de lluvia de emojis de animales"
        )
        
        if lluvia_animales:
            # Inyecta el HTML+JS dentro de un iframe
            html(
                """
                <style>
                  .falling-animal {
                    position: fixed;
                    top: -40px;
                    font-size: 2rem;
                    pointer-events: none;
                    user-select: none;
                    animation: fall linear infinite;
                  }
                  @keyframes fall {
                    to { transform: translateY(110vh) rotate(360deg); }
                  }
                </style>
                <script>
                  const chars = ["🐶","🐱","😺","🐕","🐈","🐾","🏠","💖"];
                  function dropChar() {
                    const c = chars[Math.floor(Math.random() * chars.length)];
                    const el = document.createElement("div");
                    el.textContent = c;
                    el.className = "falling-animal";
                    el.style.left = (Math.random()*100) + "vw";
                    const dur = 3 + Math.random()*4;
                    el.style.animationDuration = dur + "s";
                    el.style.animationDelay = Math.random()*1 + "s";
                    document.body.appendChild(el);
                    setTimeout(() => el.remove(), (dur+1)*1000);
                  }
                  // iniciar la lluvia
                  const rainInterval = setInterval(dropChar, 200);
                </script>
                """,
                height=50
            )
    
    # ---- PREPARAR DATOS FILTRADOS ----
    
    # Crear diccionario de filtros (priorizando año y mes)
# Crear diccionario de filtros (mantener "Todos" como string)
    filtros = {
        'fecha_inicio': start_date,
        'fecha_fin': end_date,
        'año': año_sel,  # No convertir a None
        'mes': mes_sel  # No convertir a None
        #,'mascota': mascota_sel,  # No convertir a None
        #'tipo_gasto': tipo_sel  # No convertir a None
    }
    # Cargar y procesar datos completos
    df_mascotas = cargar_datos("Datos")
    df_gastos = cargar_datos("Gastos") 
    df_donaciones = cargar_datos("Transaccion donaciones")
    
    # Procesar los datos
    df_mascotas = procesar_datos_mascotas(df_mascotas)
 
    # Filtrar los datos según los filtros seleccionados
    filtered_mascotas = filtrar_datos(df_mascotas, filtros)
    filtered_gastos = filtrar_datos(df_gastos, filtros)
    filtered_donaciones = filtrar_datos(df_donaciones, filtros)
  
    # Guardar en session_state para compartir entre páginas
    st.session_state.df_gastos = df_gastos
    st.session_state.df_donaciones = df_donaciones
    st.session_state.df_mascotas = df_mascotas
    st.session_state.filtered_df = filtered_gastos
    st.session_state.filtered_don = filtered_donaciones
    
    # ---- CONTENIDO PRINCIPAL ----
    #mostrar_filtros_activos(filtros)
    
    # Contenedor único para métricas y mensajes de insights
    with st.container():
        # Sección 1: Métricas principales
        crear_seccion_metricas(filtered_mascotas, filtered_gastos, filtered_donaciones, df_mascotas , df_gastos , df_donaciones ,filtros)    
    # Sección 2: Gráficos principales (distribución, gastos/donaciones, y actividad)
    col1, col2, col3 = st.columns([2.5, 3.75, 3.75])
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Distribución por Tipo de Animal")
        crear_grafico_distribucion_tipo(filtered_mascotas)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Gastos y Donaciones")
        crear_grafico_gastos_donaciones(filtered_gastos, filtered_donaciones)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Actividad")
        crear_grafico_actividad(filtered_mascotas, filtros)
        st.markdown('</div>', unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    
    with col1:
        # Sección 3: Mapa de calor de adopción
        st.header("Tiempo de adopcion por Tipo y Color")
        crear_mapa_calor_adopcion(filtered_mascotas)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.header("Tiempo de adopcion por Tipo y Edad")
        crear_edad_tipo_adopcion(df_mascotas)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
    # Sección 4: Mapa de rescates
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.header("🗺️ Mapa de Rescates")
    crear_mapa_rescates(filtered_mascotas)
    st.markdown('</div>', unsafe_allow_html=True)

    #st.subheader("Resumen de Gastos y Donaciones")
    detalle_gastos_donaciones(filtered_gastos, filtered_donaciones)

    
    # Footer con información y créditos
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 10px; color: #7f8c8d; font-size: 0.8em;">
        Dashboard de @101_Rescataditos - Versión 2.0 | Última actualización: Abril 2025
    </div>
    """, unsafe_allow_html=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()