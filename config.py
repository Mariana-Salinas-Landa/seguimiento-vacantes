import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
SUPABASE_STORAGE_URL = f"{SUPABASE_URL}/storage/v1/object/public/cvs"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PLATAFORMAS = ["Todas", "LinkedIn", "Indeed", "OCC", "Computrabajo", "Bumeran"]
