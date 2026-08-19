import streamlit as pd
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard de Estudiantes", page_icon="🎓", layout="wide")

# 2. Cargar los datos del DataFrame
@st.cache_data
def cargar_datos():
    datos = {
        'Estudiante': [
            'Carlos Pérez', 'Ana Gómez', 'Luis Martínez', 'María Rodríguez', 'Juan Posada',
            'Sofía López', 'Diego Fernádez', 'Laura Gaviria', 'Andrés Castro', 'Valentina Ruiz',
            'Mateo Villa', 'Camila Toro', 'Santiago Arango', 'Isabella Meía', 'Alejandro Ortiz',
            'Gabriela Cano', 'Samuel Restrepo', 'Mariana Henao', 'Nicolás Jaramillo', 'Luciana Marín'
        ],
        'Edad':,
        'Nivel Académico': [
            'Grado 12', 'Universidad', 'Universidad', 'Universidad', 'Postgrado',
            'Universidad', 'Grado 12', 'Universidad', 'Postgrado', 'Universidad',
            'Postgrado', 'Universidad', 'Universidad', 'Universidad', 'Grado 12',
            'Postgrado', 'Universidad', 'Universidad', 'Universidad', 'Universidad'
        ],
        'Índice Acumulado': [3.8, 4.2, 3.5, 4.8, 4.5, 3.9, 3.2, 4.1, 4.6, 3.7, 4.3, 4.0, 3.6, 4.7, 3.4, 4.9, 3.8, 4.3, 3.9, 4.2]
    }
    return pd.DataFrame(datos)

df = cargar_datos()

# 3. Título del Dashboard
st.title("🎓 Dashboard de Rendimiento Estudiantil")
st.markdown("Análisis interactivo del índice acumulado y niveles académicos.")

# 4. Barra lateral para Filtros (Sidebar)
st.sidebar.header("Filtros de Búsqueda")
niveles = df['Nivel Académico'].unique().tolist()
niveles_seleccionados = st.sidebar.multiselect("Selecciona el Nivel Académico:", opciones=niveles, default=niveles)

# Filtrar el DataFrame según la selección
df_filtrado = df[df['Nivel Académico'].isin(niveles_seleccionados)]

# 5. Métricas Clave (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Estudiantes", value=len(df_filtrado))
with col2:
    promedio_indice = df_filtrado['Índice Acumulado'].mean()
    st.metric(label="Índice Promedio", value=f"{promedio_indice:.2f}")
with col3:
    promedio_edad = df_filtrado['Edad'].mean()
    st.metric(label="Edad Promedio", value=f"{promedio_edad:.1f} años")

st.markdown("---")

# 6. Gráficos Interactivos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Índice Acumulado por Estudiante")
    fig_barras = px.bar(
        df_filtrado, 
        x='Estudiante', 
        y='Índice Acumulado', 
        color='Nivel Académico',
        text_auto=True,
        title="Calificaciones por Alumno"
    )
    st.plotly_chart(fig_barras, use_container_width=True)

with col_graf2:
    st.subheader("Distribución de Estudiantes por Nivel")
    fig_pastel = px.pie(
        df_filtrado, 
        names='Nivel Académico', 
        title="Porcentaje por Nivel Académico",
        hole=0.4
    )
    st.plotly_chart(fig_pastel, use_container_width=True)

# 7. Tabla de Datos Dinámica
st.subheader("📋 Vista de Datos General")
st.dataframe(df_filtrado, use_container_width=True)
