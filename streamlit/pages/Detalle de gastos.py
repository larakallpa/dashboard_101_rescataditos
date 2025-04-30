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
from utils.data_loader import cargar_datos
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
        padding: 15px 0;
        margin-top: -1px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)
# Crear tu título personalizado donde desees
st.markdown('<div class="custom-title">Gastos</div>', unsafe_allow_html=True)
 
df_gastos = st.session_state.df_gastos
año_sel = st.session_state.get("año_sel", "Todos")
mes_sel = st.session_state.get("mes_sel", "Todos")
df_gastos["MES_AÑO"] = df_gastos["Fecha"].dt.strftime("%b %Y")
 
# Filtros laterales
with st.sidebar:
        st.header("Filtros")

        # 1) Rango de fechas
        if 'Fecha' in df_gastos.columns:
            min_date = df_gastos['Fecha'].min().date()
            max_date = df_gastos['Fecha'].max().date()
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
        años = ["Todos"] + sorted(df_gastos['año'].unique().tolist())
         
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
        if 'MEDIO DE PAGO' in df_gastos.columns:
            medios_pago = ["Todos"] + sorted(df_gastos['MEDIO DE PAGO'].unique().tolist())
            medio_sel = st.selectbox(
                "Filtrar por Medio de Pago",
                medios_pago,
                key="don_medio_sel"
            )
        else:
            medio_sel = "Todos"
         # 3) Mascota y tipo de gasto
        mascotas   = ["Todas"] + sorted(df_gastos.get('MASCOTA', pd.Series()).unique().tolist())
        tipo_gastos = ["Todos"] + sorted(df_gastos.get('TIPO DE GASTO', pd.Series()).str.upper().unique().tolist())
        mascota_sel = st.selectbox("Filtrar por Mascota", mascotas, key="mascota_sel")
        tipo_sel    = st.selectbox("Filtrar por Tipo de Gasto", tipo_gastos, key="tipo_sel")
        
# Aplicar filtros desde cero
filtered_df = df_gastos.copy()

# Fecha
filtered_df = filtered_df[
    (filtered_df['Fecha'].dt.date >= start_date) &
    (filtered_df['Fecha'].dt.date <= end_date)
]

# Año
if año_sel != "Todos":
    filtered_df = filtered_df[filtered_df['año'] == año_sel]
 
# Filtro de mes, solo si no es "Todos"
if mes_sel != "Todos":
    # Extraer el número de mes y filtrar
    mes_num = int(mes_sel.split(" - ")[0])
    filtered_df = filtered_df[filtered_df['mes'] == mes_num]
 
# Mascota
if mascota_sel != "Todas":
    filtered_df = filtered_df[filtered_df["MASCOTA"] == mascota_sel]

# Tipo de Gasto
if tipo_sel != "Todos":
    filtered_df = filtered_df[filtered_df['TIPO DE GASTO'] == tipo_sel]

st.session_state.filtered_df = filtered_df
# Columnas para los siguientes gráficos
col1, col2 = st.columns(2)

with col1:
    # Gráfico de gastos por Mascota (Top 10)
    gastos_Mascota = filtered_df.groupby('MASCOTA').agg(
        total_gastos=('Monto', 'sum'),
        num_registros=('Monto', 'count')
    ).reset_index().sort_values('total_gastos', ascending=False).head(10)
    gastos_Mascota = gastos_Mascota.rename(columns={'MASCOTA': 'Mascota'})
    fig_Mascotas = px.bar(
        gastos_Mascota,
        x='Mascota',
        y='total_gastos',
        color='total_gastos',
        labels={'total_gastos': 'Gasto Total ($)', 'Mascota': 'MASCOTA'},
        title='Top 10 Mascotas con Mayor Gasto',
        template='plotly_white',
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    fig_Mascotas.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_Mascotas, use_container_width=True)

with col2:
    # Gráfico de distribución de gastos por tipo
    gastos_tipo = filtered_df.groupby('TIPO DE GASTO').agg(
        total_gastos=('Monto', 'sum')
    ).reset_index().sort_values('total_gastos', ascending=False)
    gastos_tipo = gastos_tipo.rename(columns={"TIPO DE GASTO": "Tipo de Gasto"})
    fig_tipos = px.pie(
        gastos_tipo,
        values='total_gastos',
        names='Tipo de Gasto',
        title='Distribución de Gastos por Tipo',
        template='plotly_white',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig_tipos.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_tipos, use_container_width=True)

# Gastos por Proveedor
st.header("🏥 Análisis por Proveedor")

gastos_Proveedor = filtered_df.groupby('PROVEEDOR').agg(
    total_gastos=('Monto', 'sum'),
    num_registros=('Monto', 'count'),
    promedio=('Monto', 'mean')
).reset_index().rename(columns={'PROVEEDOR': 'Proveedor'}).sort_values('total_gastos', ascending=False)

col1, col2 = st.columns(2)

with col1:
    # Top Proveedores por gasto total
    fig_Proveedores = px.bar(
        gastos_Proveedor.head(10),
        x='Proveedor',
        y='total_gastos',
        color='total_gastos',
        labels={'total_gastos': 'Gasto Total ($)', 'Proveedor': 'Proveedor'},
        title='Top 10 Proveedores',
        template='plotly_white',
        color_continuous_scale=px.colors.sequential.Greens
    )
    
    fig_Proveedores.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_Proveedores, use_container_width=True)

with col2:
    # Burbujas de Proveedores (tamaño = cantidad de visitas, color = gasto promedio)
    fig_bubble = px.scatter(
        gastos_Proveedor.head(10),
        x='num_registros',
        y='total_gastos',
        size='promedio',
        color='promedio',
        hover_name='Proveedor',
        labels={
            'num_registros': 'Cantidad de Visitas',
            'total_gastos': 'Gasto Total ($)',
            'promedio': 'Gasto Promedio ($)'
        },
        title='Relación entre Visitas y Gastos por Proveedor',
        template='plotly_white',
        color_continuous_scale=px.colors.sequential.Greens
    )
    
    st.plotly_chart(fig_bubble, use_container_width=True)


# Calendario de gastos
st.header("📅 Calendario de Gastos")

# Seleccionar año y mes para el calendario
col1, col2 = st.columns(2)

with col1:
    año_calendario = st.selectbox(
        "Año",
        sorted(filtered_df['año'].unique()),
        index=0
    )

with col2:
    mes_calendario = st.selectbox(
        "Mes",
        [f"{i} - {calendar.month_name[i]}" for i in sorted(filtered_df[filtered_df['año'] == año_calendario]['mes'].unique())],
        index=0
    )

mes_num_calendario = int(mes_calendario.split(" - ")[0])

# Filtrar datos para el calendario
df_calendario = filtered_df[(filtered_df['año'] == año_calendario) & (filtered_df['mes'] == mes_num_calendario)]

# Obtener días del mes seleccionado
año_mes = f"{año_calendario}-{mes_num_calendario:02d}"
dias_mes = pd.date_range(
    start=f"{año_mes}-01",
    end=pd.Timestamp(f"{año_mes}-01") + pd.offsets.MonthEnd(),
    freq='D'
)

# Crear DataFrame de todos los días
dias_mes_df = pd.DataFrame({'fecha': dias_mes})
dias_mes_df['dia'] = dias_mes_df['fecha'].dt.day

# Añadir día a los registros filtrados
df_calendario["dia"] = df_calendario["Fecha"].dt.day

# Agrupar gastos por día
gastos_diarios = (
    df_calendario
      .groupby('dia')
      .agg(total_gastos=('Monto','sum'), num_registros=('Monto','count'))
      .reset_index()
)

# Unir con todos los días del mes
calendario_completo = dias_mes_df.merge(
    gastos_diarios, on='dia', how='left'
)
calendario_completo['total_gastos'].fillna(0, inplace=True)
calendario_completo['num_registros'].fillna(0, inplace=True)

# Construir la matriz del calendario
dia_semana_inicio = dias_mes[0].weekday()  # 0 = Lunes
total_dias = len(dias_mes)
semanas_necesarias = (dia_semana_inicio + total_dias + 6) // 7

matriz_calendario = np.zeros((semanas_necesarias, 7), dtype=int)
matriz_valores   = np.zeros((semanas_necesarias, 7))

for i, dia in enumerate(range(1, total_dias + 1)):
    fila    = (dia_semana_inicio + i) // 7
    columna = (dia_semana_inicio + i) % 7
    matriz_calendario[fila, columna] = dia
    
    gasto = calendario_completo.loc[
        calendario_completo['dia']==dia, 'total_gastos'
    ].values
    if gasto.size:
        matriz_valores[fila, columna] = gasto[0]

# Dibujar heatmap tipo calendario
dias_semana = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']
fig_calendario = go.Figure(
    data=go.Heatmap(
        z=matriz_valores,
        text=[
            [
                f"{int(matriz_calendario[i,j])}<br>${matriz_valores[i,j]:,.0f}"
                if matriz_calendario[i,j]!=0 else ""
                for j in range(7)
            ] for i in range(semanas_necesarias)
        ],
        x=dias_semana,
        y=[f"Semana {i+1}" for i in range(semanas_necesarias)],
        hoverongaps=False,
        colorscale='Blues',
        showscale=False,
        texttemplate="%{text}",
        textfont={"size":12}
    )
)

fig_calendario.update_layout(
    title=f"Calendario de Gastos - {calendar.month_name[mes_num_calendario]} {año_calendario}",
    height=400,
    template='plotly_white'
)

st.plotly_chart(fig_calendario, use_container_width=True)

# Mapa de calor de Mascotas vs Tipo de Gasto
st.header("🔍 Análisis Detallado")
 
# 1) Pivot y reset_index para pasar Mascota a columna
pivot_Mascota_tipo = pd.pivot_table(
    filtered_df, 
    values='Monto',
    index='MASCOTA',
    columns='TIPO DE GASTO',
    aggfunc='sum',
    fill_value=0
).rename_axis(columns='Tipo de Gasto') \
 .reset_index() \
 .rename(columns={'MASCOTA': 'Mascota'})

# 2) Top 10 mascotas
top_Mascotas = (
    filtered_df
      .groupby('MASCOTA')['Monto']
      .sum()
      .nlargest(10)
      .index
)

# 3) Filtrar usando isin en la columna Mascota
pivot_filtrado = pivot_Mascota_tipo[
    pivot_Mascota_tipo['Mascota'].isin(top_Mascotas)
]

# 4) Graficar
fig_heatmap = px.imshow(
    pivot_filtrado.set_index('Mascota'),  # px.imshow quiere índice
    labels=dict(x="Tipo de Gasto", y="Mascota", color="Monto ($)"),
    title="Distribución de Gastos por Mascota y Categoría",
    color_continuous_scale='Blues',
    aspect="auto",
    text_auto='.0f'
)
st.plotly_chart(fig_heatmap, use_container_width=True)


# Tabla de datos detallados
st.header("📋 Registros Detallados")

# Mostrar datos filtrados
if st.checkbox("Mostrar tabla de datos detallados"):
    print("gastos",filtered_df)
    st.dataframe(
        filtered_df.sort_values('Fecha', ascending=False)[
            ['Fecha', 'MASCOTA', 'TIPO DE GASTO', 'PROVEEDOR', 'DETALLE', 'Monto', 'RESPONSABLE']
        ].reset_index(drop=True),
        height=400
    )