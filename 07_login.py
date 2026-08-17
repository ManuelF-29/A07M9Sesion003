# ── 07_login.py ─────────────────────────────────────────────────────────────
# Muestra cómo proteger una app Streamlit con usuario y contraseña,
# sin instalar librerías extra.
#
# La clave es st.session_state: un diccionario que Streamlit mantiene en memoria
# mientras el navegador está abierto. Usamos una variable "autenticado" para
# recordar si el usuario ya inició sesión.
#
# Corre con: streamlit run 07_login.py
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st

# ── Credenciales ─────────────────────────────────────────────────────────────
# En un proyecto real estas irían en .streamlit/secrets.toml, no aquí.
USUARIO_CORRECTO   = "Mferreras29"
CONTRASENA_CORRECTA = "Ferreras29"

# ── Inicializar session_state ────────────────────────────────────────────────
# st.session_state es un diccionario que persiste entre interacciones.
# Si la clave "autenticado" no existe todavía, la creamos con False.
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# ── Función de login ─────────────────────────────────────────────────────────
def mostrar_login():
    st.title("Iniciar sesión")

    # st.form agrupa los campos para que Streamlit no reaccione hasta que
    # el usuario presione el botón "Entrar"
    with st.form("form_login"):
        usuario    = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")  # type="password" oculta el texto
        enviado    = st.form_submit_button("Entrar")

    # Este bloque solo se ejecuta cuando el usuario presiona "Entrar"
    if enviado:
        if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:
            # Guardamos en session_state que el usuario ya se autenticó
            st.session_state["autenticado"] = True
            # st.rerun() vuelve a ejecutar el script desde arriba,
            # ahora con autenticado=True, lo que mostrará el contenido real
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

# ── Lógica principal ─────────────────────────────────────────────────────────
if not st.session_state["autenticado"]:
    # Si el usuario NO está autenticado, mostramos solo el formulario
    mostrar_login()
    st.stop()   # st.stop() evita que el resto del script se ejecute

# A partir de aquí solo llega código si el usuario ya inició sesión
st.title("Dashboard de Crédito")
st.write("Bienvenido. Esta sección solo es visible después del login.")

# Botón para cerrar sesión
if st.sidebar.button("Cerrar sesión"):
    st.session_state["autenticado"] = False
    st.rerun()
