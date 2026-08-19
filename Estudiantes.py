import streamlit as st  
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard de Estudiantes", page_icon="🎓", layout="wide")

# 2. Cargar los datos del DataFrame (Formato alternativo a prueba de fallos)
@st.cache_data
def cargar_datos():
    # Listas independientes para evitar recortes del sistema de formato
    estudiantes = ['Carlos Pérez', 'Ana Gómez', 'Luis Martínez', 'María Rodríguez', 'Juan Posada', 'Sofía López', 'Diego Fernádez', 'Laura Gaviria', 'Andrés Castro', 'Valentina Ruiz', 'Mateo Villa', 'Camila Toro', 'Santiago Arango', 'Isabella Meía', 'Alejandro Ortiz', 'Gabriela Cano', 'Samuel Restrepo', 'Mariana Henao', 'Nicolás Jaramillo', 'Luciana Marín']
    
    edades = [18, 19, 21, 20, 22, 19, 18, 20, 23, 21, 22, 19, 20, 21, 18, 22, 20, 19, 21, 20]
    
    niveles = ['Grado 12', 'Universidad', 'Universidad', 'Universidad', 'Postgrado', 'Universidad', 'Grado 12', 'Universidad', 'Postgrado', 'Universidad', 'Postgrado', 'Universidad', 'Universidad', 'Universidad', 'Grado 12', 'Postgrado', 'Universidad', 'Universidad', 'Universidad', 'Universidad']
    
    indices = [3.8, 4.2, 3.5, 4.8, 4.5, 3.9, 3.2, 4.1, 4.6, 3.7, 4.3, 4.0, 3.6, 4.7, 3.4, 4.9, 3.8, 4.3, 3.9, 4.2]
    
    datos = {
        'Estudiante': estudiantes,
        'Edad': edades,
        'Nivel Académico': niveles,
        'Índice Acumulado': indices
    }
    return pd.DataFrame(datos)

df = cargar_datos()

# 3. Título del Dashboard
st.title("🎓 Dashboard de Rendimiento Estudiantil Avanzado")
st.markdown("Análisis interactivo con filtros demográficos y académicos avanzados.")

# 4. Barra lateral para Filtros (Sidebar)
st.sidebar.header("🔍 Panel de Filtros")

# Filtro 1: Buscador de texto por nombre
buscar_nombre = st.sidebar.text_input("Buscar Estudiante por Nombre:", value="")

# Filtro 2: Rango de edad (Slider)
edad_min, edad_max = int(df['Edad'].min()), int(df['Edad'].max())
rango_edad = st.sidebar.slider("Filtrar por Rango de Edad:", edad_min, edad_max, (edad_min, edad_max))

# Filtro 3: Selección de Nivel Académico
lista_niveles = df['Nivel Académico'].unique().tolist()
niveles_seleccionados = st.sidebar.multiselect("Selecciona el Nivel Académico:", options=lista_niveles, default=lista_niveles)

# Filtro 4: Control dinámico del Top-N
activar_top = st.sidebar.checkbox("🏆 Activar Filtro de Mejores Índices", value=False)
cantidad_top = st.sidebar.number_input("Cantidad de alumnos en el Top:", min_value=1, max_value=20, value=5, step=1, disabled=not activar_top)

# --- APLICACIÓN DE FILTROS EN PANDAS ---
df_filtrado = df.copy()

# Aplicar búsqueda por nombre
if buscar_nombre:
    df_filtrado = df_filtrado[df_filtrado['Estudiante'].str.contains(buscar_nombre, case=False)]

# Aplicar rango de edad utilizando desempaquetado de tupla para Streamlit
df_filtrado = df_filtrado[(df_filtrado['Edad'] >= rango_edad[0]) & (df_filtrado['Edad'] <= rango_edad[1])]

# Aplicar niveles académicos
df_filtrado = df_filtrado[df_filtrado['Nivel Académico'].isin(niveles_seleccionados)]

# Aplicar corte de mejores índices si está activo
if activar_top and not df_filtrado.empty:
    df_filtrado = df_filtrado.nlargest(cantidad_top, 'Índice Acumulado')


# 5. Métricas Clave (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Estudiantes Visualizados", value=len(df_filtrado))
with col2:
    if not df_filtrado.empty:
        promedio_indice = df_filtrado['Índice Acumulado'].mean()
        st.metric(label="Índice Promedio", value=f"{promedio_indice:.2f}")
    else:
        st.metric(label="Índice Promedio", value="0.00")
with col3:
    if not df_filtrado.empty:
        promedio_edad = df_filtrado['Edad'].mean()
        st.metric(label="Edad Promedio", value=f"{promedio_edad:.1f} años")
    else:
        st.metric(label="Edad Promedio", value="0 años")

st.markdown("---")


# 6. Gráficos Interactivos
if not df_filtrado.empty:
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Índice Acumulado por Estudiante")
        fig_barras = px.bar(
            df_filtrado, 
            x='Estudiante', 
            y='Índice Acumulado', 
            color='Nivel Académico',
            text_auto=True,
            title="Calificaciones del segmento seleccionado"
        ).update_layout(xaxis={'categoryorder':'total descending'})
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
else:
    st.warning("Ningún estudiante coincide con los filtros seleccionados actualmente.")


# 7. Tabla de Datos Dinámica
st.subheader("📋 Vista de Datos General")
st.dataframe(df_filtrado.sort_values(by='Índice Acumulado', ascending=False), use_container_width=True)
