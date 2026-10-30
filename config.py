import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
PERSONA = st.secrets.get("PERSONA", "mariana")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PLATAFORMAS = ["Todas", "LinkedIn", "Indeed", "OCC", "Computrabajo", "Bumeran"]


def url_cv(nombre_archivo):
    """Genera un link temporal (1 hora) para un CV en el bucket privado 'cvs'.
    Si el archivo no existe para esta persona, regresa None en vez de tronar."""
    try:
        resultado = supabase.storage.from_("cvs").create_signed_url(
            f"{PERSONA}/{nombre_archivo}", 3600
        )
        return resultado["signedURL"]
    except Exception:
        return None
