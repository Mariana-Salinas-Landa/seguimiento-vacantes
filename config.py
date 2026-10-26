import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
PERSONA = st.secrets.get("PERSONA", "mariana")
SUPABASE_STORAGE_URL = f"{SUPABASE_URL}/storage/v1/object/public/cvs/{PERSONA}"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PLATAFORMAS = ["Todas", "LinkedIn", "Indeed", "OCC", "Computrabajo", "Bumeran"]
