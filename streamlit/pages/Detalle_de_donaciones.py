import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
import locale
import numpy as np 
import plotly.express as px
import streamlit as st

# Configurar la localización para mostrar los meses en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except:
        pass  # Si no se puede configurar la localización, usaremos la predeterminada

 
 # Estilizar la aplicación
st.markdown("""
    <style>
    /* Ajustar el espacio en la parte superior de la página */
    .block-container {
        padding-top: 1rem !important;
    }
    
    /* Reducir el espacio entre elementos */
    h1 {
        margin-top: -10px !important;
        margin-bottom: 20px !important;
    }
    
    /* Ajustar encabezados secundarios */
    h2 {
        margin-top: 5px !important;
    }
    
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #3498db;
    }
    .metric-title {
        font-size: 16px;
        color: #7f8c8d;
    }        
    /* Estilo para el título personalizado */
    .custom-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4a4a4a;
        padding: 10px 0;
        margin-top: -1px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)
# Crear tu título personalizado donde desees
st.markdown('<div class="custom-title">Donaciones</div>', unsafe_allow_html=True)
 
df_donaciones = st.session_state.df_donaciones
filtered_don = st.session_state.filtered_don
año_sel = st.session_state.get("año_sel", "Todos")
mes_sel = st.session_state.get("mes_sel", "Todos")
df_donaciones["MES_AÑO"] = df_donaciones["Fecha"].dt.strftime("%b %Y")
# Filtros laterales
with st.sidebar:
        st.header("Filtros")

        # 1) Rango de fechas
        if 'Fecha' in df_donaciones.columns:
            min_date = df_donaciones['Fecha'].min().date()
            max_date = df_donaciones['Fecha'].max().date()
            start_date, end_date = st.date_input(
                "Rango de fechas",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date,
                key="don_start_end"
            )
        else:
            # Si no hay 'Fecha', definimos defaults de todos los datos
            start_date, end_date = None, None

       
        # 2) Año
        años = ["Todos"] + sorted(df_donaciones['año'].unique().tolist())
         
        default_año_index = años.index(año_sel) if año_sel in años else 0
        año_sel = st.selectbox( "Filtrar por año",
            options=años,                  # aquí van las opciones
            index=default_año_index,       # aquí el índice por defecto
            key="año_sel"     )  
      
    

        # 3) Mes
        meses = ["Todos"] + [f"{i} - {calendar.month_name[i]}" for i in range(1,13)]
        default_mes_index = meses.index(mes_sel) if mes_sel in meses else 0
        mes_sel = st.selectbox(
            "Filtrar por mes",
            options=meses,
            index=default_mes_index,
            key="mes_sel"
        )

        # 4) Medio de pago
        if 'MEDIO DE PAGO' in df_donaciones.columns:
            medios_pago = ["Todos"] + sorted(df_donaciones['MEDIO DE PAGO'].unique().tolist())
            medio_sel = st.selectbox(
                "Filtrar por Medio de Pago",
                medios_pago,
                key="don_medio_sel"
            )
        else:
            medio_sel = "Todos"

# AQUÍ ES DONDE APLICAMOS LOS FILTROS
filtered_don = df_donaciones.copy()

# Filtro de rango de fechas
if start_date and end_date:
    filtered_don = filtered_don[(filtered_don['Fecha'].dt.date >= start_date) & 
                               (filtered_don['Fecha'].dt.date <= end_date)]

# Filtro de año
if año_sel != "Todos":
    filtered_don = filtered_don[filtered_don['año'] == año_sel]

# Filtro de mes
if mes_sel != "Todos":
    mes_num = int(mes_sel.split(" - ")[0])
    filtered_don = filtered_don[filtered_don['Fecha'].dt.month == mes_num]

# Filtro de medio de pago
if medio_sel != "Todos" and 'MEDIO DE PAGO' in df_donaciones.columns:
    filtered_don = filtered_don[filtered_don['MEDIO DE PAGO'] == medio_sel]


# AHORA USAMOS FILTERED_DON PARA LAS MÉTRICAS
if not filtered_don.empty:
    # Mostrar datos básicos con el dataframe filtrado
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        total = filtered_don["Monto"].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${total:,.2f}</div>
                <div class="metric-title">Total de Donaciones ($)</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        count = len(filtered_don)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{count:,}</div>
                <div class="metric-title">Número de Donaciones</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        if "DONANTE" in filtered_don.columns:
            uniques = filtered_don["DONANTE"].nunique()
            val = f"{uniques:,}"
        else:
            val = "N/A"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-title">Donantes únicos</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        avg = filtered_don["Monto"].mean()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${avg:,.2f}</div>
                <div class="metric-title">Donación Promedio ($)</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No hay donaciones que coincidan con los filtros seleccionados.")
    # Mostrar datos en pestañas

#tab1, tab2, tab3  = st.tabs(["Análisis", "Principales Donantes", "Tendencias"])
col1, col2  = st.columns(2)
    
with col1:
    # Crea columna con nombre de mes y día para agrupaciones
    filtered_don["NOMBRE_MES"] = filtered_don["Fecha"].dt.month_name(locale="es_ES")
    filtered_don["día"] = filtered_don["Fecha"].dt.day

    # Decide nivel de agregación según tus filtros
    if año_sel == "Todos":
        df_plot = (
            filtered_don
            .groupby("año")["Monto"]
            .sum()
            .reset_index()
            .rename(columns={"año": "Periodo", "Monto": "Total Donaciones"})
        )
        # Convertir a string para categoría y ordenar
        df_plot["Periodo"] = df_plot["Periodo"].astype(str)
        custom_order = sorted(df_plot["Periodo"].unique(), reverse=True)
        category_orders = {"Periodo": custom_order}
        x = "Periodo"
        title_txt = "Donaciones por Año"

    elif mes_sel == "Todos":
        # Agregar por mes del año seleccionado
        df_plot = (
            filtered_don
            .groupby(["mes", "NOMBRE_MES"])["Monto"]
            .sum()
            .reset_index()
            .sort_values("mes")
            .rename(columns={"NOMBRE_MES": "Periodo", "Monto": "Total Donaciones"})
        )
        x = "Periodo"
        title_txt = f"Donaciones por Mes — {año_sel}"
        custom_order = None  # No hay ordenamiento personalizado en este caso

    else:
        mes_num = int(mes_sel.split(" - ")[0])
        # Agregar por día del mes seleccionado
        df_plot = (
            filtered_don
            .groupby("día")["Monto"]
            .sum()
            .reset_index()
            .rename(columns={"día": "Periodo", "Monto": "Total Donaciones"})
        )
        x = "Periodo"
        title_txt = f"Donaciones Diarias — {calendar.month_name[mes_num]} {año_sel}"
        custom_order = None  # No hay ordenamiento personalizado en este caso

    # Gráfico único de barras
    fig = px.bar(
        df_plot,
        x=x,
        y="Total Donaciones",
        title=title_txt,
        labels={"Total Donaciones": "Donaciones ($)", x: ""},
        color="Total Donaciones",
        color_continuous_scale="Viridis",
        # Aplicar ordenamiento personalizado si existe
        **({"category_orders": {"Periodo": custom_order}} if custom_order else {})
    )

    # Actualizar ejes y diseño
    if custom_order:
        fig.update_xaxes(categoryorder='array', categoryarray=custom_order)
    
    fig.update_layout(
        xaxis_tickangle=-45,
        coloraxis_showscale=False,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    
with col2:
 

    if 'DONANTE' in filtered_don.columns and 'Monto' in filtered_don.columns:
        # 1) Agrupar por DONANTE usando el df ya filtrado
        df_donantes = (
            filtered_don
            .groupby('DONANTE')['Monto']
            .agg(total_donado='sum', numero_donaciones='count')
            .reset_index()
        )
        # Calcular promedio
        df_donantes['donacion_promedio'] = (
            df_donantes['total_donado'] / df_donantes['numero_donaciones']
        )
        # Ordenar y quedarnos con el top 10
        df_donantes = df_donantes.sort_values('total_donado', ascending=False)
        top_donantes = df_donantes.head(10)

        # 2) Gráfico de barras
        fig_donantes = px.bar(
            top_donantes,
            x='DONANTE',
            y='total_donado',
            title='🏆Top 10 Donantes',
            labels={
                'DONANTE': 'Donante',
                'total_donado': 'Monto Total Donado'
            },
            color='total_donado',
            color_continuous_scale='Viridis'
        )
        fig_donantes.update_layout(coloraxis_showscale=False, template='plotly_white')
        st.plotly_chart(fig_donantes, use_container_width=True)

    else:
        st.warning("No hay datos suficientes sobre donantes para mostrar.")


# 3) Tabla con detalles
st.subheader("Detalles de Principales Donantes")
display = top_donantes.copy()
display['total_donado']       = display['total_donado'].map('${:,.2f}'.format)
display['donacion_promedio']  = display['donacion_promedio'].map('${:,.2f}'.format)
display = display.rename(columns={
    'DONANTE': 'Donante',
    'total_donado': 'Total Donado',
    'numero_donaciones': 'Número de Donaciones',
    'donacion_promedio': 'Donación Promedio'
})
st.dataframe(display, use_container_width=True)
# 4) Mayor contribuyente
max_d = df_donantes.iloc[0]
st.subheader("Mayor Contribuyente")
st.info(
    f"**{max_d['DONANTE']}** ha donado **${max_d['total_donado']:,.2f}** en "
    f"**{int(max_d['numero_donaciones'])}** ocasiones "
    f"(promedio: **${max_d['donacion_promedio']:,.2f}**)."
)


st.header("Tendencias y Patrones")
        
# Verificar si hay datos para el análisis de tendencias
if 'MES_AÑO' in df_donaciones.columns and 'Monto' in df_donaciones.columns:
    # Tendencia temporal de donaciones
    df_tendencia = df_donaciones.groupby('MES_AÑO')['Monto'].sum().reset_index()
    df_tendencia['MES_AÑO'] = pd.to_datetime(df_tendencia['MES_AÑO'])
    df_tendencia = df_tendencia.sort_values('MES_AÑO')
    
    # Gráfico de línea para tendencia temporal
    fig_tendencia = px.line(
        df_tendencia,
        x='MES_AÑO',
        y='Monto',
        title='Tendencia de Donaciones a lo Largo del Tiempo',
        labels={'Monto': 'Monto Total', 'MES_AÑO': 'Fecha'},
        markers=True
    )
    st.plotly_chart(fig_tendencia, use_container_width=True)
    
    # Análisis por medio de pago si está disponible
    if 'MEDIO DE PAGO' in df_donaciones.columns:
        st.subheader("Distribución por Medio de Pago")
        df_medio_pago = df_donaciones.groupby('MEDIO DE PAGO')['Monto'].sum().reset_index()
        df_medio_pago = df_medio_pago.sort_values('Monto', ascending=False)
        
        # Gráfico de pastel para medios de pago
        fig_medio_pago = px.pie(
            df_medio_pago,
            values='Monto',
            names='MEDIO DE PAGO',
            title='Distribución de Donaciones por Medio de Pago'
        )
        st.plotly_chart(fig_medio_pago, use_container_width=True)
    
    # Análisis por tipo de identificación si está disponible
    if 'TIPO DE IDENTIFICACIÓN DEL DONANTE' in df_donaciones.columns:
        st.subheader("Distribución por Tipo de Identificación")
        df_tipo_id = df_donaciones.groupby('TIPO DE IDENTIFICACIÓN DEL DONANTE')['Monto'].sum().reset_index()
        df_tipo_id = df_tipo_id.sort_values('Monto', ascending=False)
        
        # Gráfico de pastel para tipos de identificación
        fig_tipo_id = px.pie(
            df_tipo_id,
            values='Monto',
            names='TIPO DE IDENTIFICACIÓN DEL DONANTE',
            title='Distribución de Donaciones por Tipo de Identificación'
        )
        st.plotly_chart(fig_tipo_id, use_container_width=True)
else:
    st.warning("No hay datos suficientes para análisis de tendencias.")


 

# Información al pie
st.sidebar.markdown("---")
st.sidebar.info("""
**Análisis de Donaciones Dashboard**  
Desarrollado con Streamlit y Python 
por @glaraarteaga
""")