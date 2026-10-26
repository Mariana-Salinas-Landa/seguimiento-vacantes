import streamlit as st
from config import supabase, PLATAFORMAS, SUPABASE_STORAGE_URL, PERSONA
from chat import mostrar_chat
from tabla import mostrar_tabla

st.set_page_config(layout="wide", page_title="Seguimiento de vacantes", page_icon="💼")

st.markdown("""
<style>
div[data-testid="stPopoverBody"] {
    width: 800px !important;
    min-height: 600px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("💼 Seguimiento de vacantes")
st.caption("Tu centro de control para la búsqueda de empleo")

response = supabase.table("Vacantes").select("*").eq("persona", PERSONA).execute()
data = response.data

mostrar_chat(data)

if "vista" not in st.session_state:
    st.session_state.vista = "nuevas"

with st.sidebar:
    st.header("🔍 Filtros")
    plataforma_seleccionada = st.radio("Plataforma", PLATAFORMAS)
    st.divider()

    total_nuevas = len([d for d in data if d.get("estado") == "nueva"])
    total_postuladas = len([d for d in data if d.get("estado") == "aplicado" and d.get("empresa") is not None])
    total_descartadas = len([d for d in data if d.get("estado") == "descartada"])
    total_favoritos = len([d for d in data if d.get("favorito") is True])

    if st.button(f"🆕 Nuevas ({total_nuevas})", use_container_width=True):
        st.session_state.vista = "nuevas"
    if st.button(f"✅ Postuladas ({total_postuladas})", use_container_width=True):
        st.session_state.vista = "postuladas"
    if st.button(f"🗑️ Descartadas ({total_descartadas})", use_container_width=True):
        st.session_state.vista = "descartadas"
    if st.button(f"⭐ Favoritas ({total_favoritos})", use_container_width=True):
        st.session_state.vista = "favoritas"

vista_actual = st.session_state.vista

contenedor = st.container(key=f"contenedor_{vista_actual}")

with contenedor:
    if vista_actual == "nuevas":
        st.header("🆕 Nuevas")
        filtrado = [d for d in data if d.get("estado") == "nueva"]
    elif vista_actual == "postuladas":
        st.header("✅ Postuladas")
        filtrado = [d for d in data if d.get("estado") == "aplicado" and d.get("empresa") is not None]
    elif vista_actual == "descartadas":
        st.header("🗑️ Descartadas")
        filtrado = [d for d in data if d.get("estado") == "descartada"]
    else:
        st.header("⭐ Favoritas")
        filtrado = [d for d in data if d.get("favorito") is True]

    if plataforma_seleccionada != "Todas":
        filtrado = [d for d in filtrado if d.get("plataforma") == plataforma_seleccionada]

    mostrar_tabla(filtrado, vista_actual)

st.divider()
st.subheader("📄 Panel de CVs enviados")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("CV Ingeniero de Datos", len([d for d in data if d.get("cv_ingeniero_datos") is True]))
    st.link_button("Ver PDF", f"{SUPABASE_STORAGE_URL}/cv_ingeniero_datos.pdf", use_container_width=True)
with col2:
    st.metric("CV Maestro", len([d for d in data if d.get("cv_maestro") is True]))
    st.link_button("Ver PDF", f"{SUPABASE_STORAGE_URL}/cv_maestro.pdf", use_container_width=True)
with col3:
    st.metric("CV Especial", len([d for d in data if d.get("cv_especial") is True]))
    st.caption("Se genera por vacante — sin archivo fijo")
