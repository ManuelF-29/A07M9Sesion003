# ── 06_layouts.py ───────────────────────────────────────────────────────────
# Este script muestra los tres layouts principales de Streamlit:
#   1. Sidebar  — panel lateral siempre visible
#   2. Columns  — divide la página en columnas lado a lado
#   3. Tabs     — pestañas para organizar contenido en secciones
#
# Corre con: streamlit run 06_layouts.py
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st

# layout="wide" aprovecha todo el ancho de la pantalla
st.set_page_config(page_title="Layouts en Streamlit", layout="wide")

st.title("Layouts en Streamlit")

# ════════════════════════════════════════════════════════════════════════════
# 1. SIDEBAR
# El sidebar es el panel lateral izquierdo que permanece visible en toda la app.
# Es ideal para poner filtros o controles globales.
# ════════════════════════════════════════════════════════════════════════════

st.sidebar.header("Sidebar")
st.sidebar.write("Aquí van los filtros o controles globales.")

# Cualquier widget creado con st.sidebar.widget() aparece en el panel lateral
grado = st.sidebar.selectbox("Grado del crédito:", ["A", "B", "C", "D", "E", "F", "G"])
st.sidebar.write(f"Grado seleccionado: **{grado}**")

# ════════════════════════════════════════════════════════════════════════════
# 2. COLUMNS
# st.columns divide el espacio horizontal en columnas independientes.
# Puedes poner cualquier widget o texto dentro de cada columna.
# ════════════════════════════════════════════════════════════════════════════

st.subheader("Columns")

# st.columns(3) crea 3 columnas de igual ancho
# También puedes pasar proporciones: st.columns([2, 1, 1])
col1, col2, col3 = st.columns(3)

# Cada columna es un contenedor independiente
col1.metric(label="Total de créditos", value="32,591")
col2.metric(label="Monto promedio", value="$9,589")
col3.metric(label="Tasa de incumplimiento", value="21.8%")

# Separamos las secciones visualmente con una línea horizontal
st.divider()

# Ejemplo con dos columnas y texto
st.subheader("Columns con texto")

col_izq, col_der = st.columns(2)

# "with col_izq:" es la forma más cómoda cuando hay varios elementos en la columna
with col_izq:
    st.write("**Columna izquierda**")
    st.write("Aquí puede ir una gráfica, una tabla o cualquier widget.")

with col_der:
    st.write("**Columna derecha**")
    st.write("Cada columna es completamente independiente de la otra.")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# 3. TABS
# st.tabs organiza el contenido en pestañas.
# El usuario ve solo una pestaña a la vez y puede cambiar haciendo clic.
# Es útil para separar temas sin hacer la página demasiado larga.
# ════════════════════════════════════════════════════════════════════════════

st.subheader("Tabs")

# st.tabs recibe una lista con los nombres de cada pestaña
tab1, tab2, tab3 = st.tabs(["Pestaña 1", "Pestaña 2", "Pestaña 3"])

with tab1:
    # Todo lo que escribas dentro de "with tab1:" aparece solo en esa pestaña
    st.write("Contenido de la Pestaña 1.")
    st.write("Aquí podría ir una gráfica de distribución de montos.")

with tab2:
    st.write("Contenido de la Pestaña 2.")
    st.write("Aquí podría ir un mapa o un pie chart.")

with tab3:
    st.write("Contenido de la Pestaña 3.")
    st.write("Aquí podría ir una tabla con los datos crudos.")
