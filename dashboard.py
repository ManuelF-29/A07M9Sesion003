# dashboard.py — Sesión 2: Streamlit Widgets y Layouts
# Corre con: streamlit run dashboard.py
#
# Instrucciones Copilot:
# En las secciones marcadas con "# ✏️ COPILOT" escribe el comentario sugerido
# y deja que Copilot complete el código.

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Configuración ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Crédito",
    page_icon="💳",
    layout="wide"
)

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    df = pd.read_csv('credit_dataset.csv').rename(columns={
        'loan_amnt':             'monto',
        'loan_int_rate':         'tasa',
        'loan_status':           'incumplimiento',
        'loan_grade':            'grado',
        'person_income':         'ingreso',
        'person_home_ownership': 'vivienda',
        'loan_intent':           'proposito',
        'person_age':            'edad',
    }).dropna()
    ## Forzar columna monto a numérica
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
    # Forzar columna tasa a numérica
    df['tasa'] = pd.to_numeric(df['tasa'], errors='coerce')
    return df

df = cargar_datos()

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Filtros
# ════════════════════════════════════════════════════════════════════════════
st.sidebar.header("🔧 Filtros")

# ✏️ COPILOT — Escribe el comentario y deja que Copilot genere el widget:
# Agregar multiselect en sidebar para filtrar por grado, con todos los grados seleccionados por defecto
grados_sel = st.sidebar.multiselect(
    "Grado de crédito",
    options=sorted(df['grado'].unique()),
    default=sorted(df['grado'].unique())
)

# ✏️ COPILOT:
# Agregar multiselect en sidebar para filtrar por proposito, con todos seleccionados por defecto
propositos_sel = st.sidebar.multiselect(
    "Propósito del crédito",
    options=sorted(df['proposito'].unique()),
    default=sorted(df['proposito'].unique())
)

# ✏️ COPILOT:
# Agregar slider en sidebar para filtrar rango de monto entre el mínimo y máximo del dataset
monto_rango = st.sidebar.slider(
    "Rango de monto",
    min_value=int(df['monto'].min()),
    max_value=int(df['monto'].max()),
    value=(int(df['monto'].min()), int(df['monto'].max()))
)


# ── Aplicar filtros ──────────────────────────────────────────────────────────
df_f = df[df['grado'].isin(grados_sel)]
df_f = df_f[df_f['proposito'].isin(propositos_sel)]
df_f = df_f[(df_f['monto'] >= monto_rango[0]) & (df_f['monto'] <= monto_rango[1])]

# ════════════════════════════════════════════════════════════════════════════
# MÉTRICAS — Fila de KPIs
# ════════════════════════════════════════════════════════════════════════════
st.title("💳 Dashboard de Crédito")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de créditos",   f"{len(df_f):,}")
col2.metric("Monto promedio",       f"${df_f['monto'].mean():,.0f}")
col3.metric("Tasa promedio",        f"{df_f['tasa'].mean():.1f}%")
col4.metric("Tasa de incumplimiento", f"{df_f['incumplimiento'].mean()*100:.1f}%")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# TABS — Secciones de gráficas
# ════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["📊 Riesgo", "📦 Distribución", "🥧 Composición", "📋 Datos"])

# ── Tab 1: Riesgo ────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Monto vs Tasa de Interés")

    # ✏️ COPILOT:
    # Scatter plot con plotly express: x=monto, y=tasa, color=grado, opacity=0.4
    # scatter plot con plotly express: x=monto, y=tasa, color=grado, opacity=0.4
    fig_scatter = px.scatter(df_f, x="monto", y="tasa", color="grado", opacity=0.4)
    st.plotly_chart(fig_scatter)

    st.subheader("Tasa de Incumplimiento por Propósito")

    # ✏️ COPILOT:
    # Calcular tasa de incumplimiento por proposito y graficar con px.bar ordenado de mayor a menor
    tasa_incumplimiento = df_f.groupby('proposito')['incumplimiento'].mean().sort_values(ascending=False)
    fig_bar = px.bar(x=tasa_incumplimiento.index, y=tasa_incumplimiento.values)
    st.plotly_chart(fig_bar)


# ── Tab 2: Distribución ──────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Monto por Grado")
        # ✏️ COPILOT:
        # Box plot: x=grado, y=monto, color=grado
        fig_box = px.box(x="grado", y="monto", color="grado", data_frame=df_f)
        st.plotly_chart(fig_box)


    with col_b:
        st.subheader("Tasa por Tipo de Vivienda")
        # ✏️ COPILOT:
        # Violin plot: x=vivienda, y=tasa, color=vivienda, box=True
        fig_violin = px.violin(x="vivienda", y="tasa", color="vivienda", box=True, data_frame=df_f)
        st.plotly_chart(fig_violin)


# ── Tab 3: Composición ───────────────────────────────────────────────────────
with tab3:
    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Distribución por Propósito")
        conteo = df_f['proposito'].value_counts().reset_index()
        conteo.columns = ['proposito', 'cantidad']
        # ✏️ COPILOT:
        # Pie chart con px.pie: values=cantidad, names=proposito, hole=0.3
        fig_pie = px.pie(data_frame=conteo, values='cantidad', names='proposito', hole=0.3)
        st.plotly_chart(fig_pie)


    with col_d:
        st.subheader("Histograma de Monto")
        # ✏️ COPILOT:
        # Histograma: x=monto, nbins=40, color=grado
        fig_hist = px.histogram(df_f, x="monto", nbins=40, color="grado")
        st.plotly_chart(fig_hist)


# ── Tab 4: Datos crudos ───────────────────────────────────────────────────────
with tab4:
    st.subheader("Datos filtrados")
    st.write(f"{len(df_f):,} registros")
    st.dataframe(df_f, use_container_width=True)

    # ✏️ COPILOT:
    # Botón de descarga que permita descargar df_f como CSV
    csv = df_f.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name='credit_dataset_filtrado.csv',
        mime='text/csv',
    )


# ── Formulario de reporte ─────────────────────────────────────────────────────
st.divider()
st.subheader("📄 Generar reporte")

with st.form("reporte"):
    nombre_reporte = st.text_input("Nombre del reporte", value="Análisis de crédito")
    incluir_outliers = st.checkbox("Incluir outliers en el análisis", value=True)
    enviado = st.form_submit_button("Generar")

if enviado:
    st.success(f"✅ Reporte '{nombre_reporte}' generado con {len(df_f):,} registros.")
