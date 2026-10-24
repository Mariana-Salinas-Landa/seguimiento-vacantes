from supabase import create_client

SUPABASE_URL = "https://ivmewysnzxbjnqlkcuul.supabase.co"
SUPABASE_KEY = "sb_publishable_rHPuhTdHZvxOZ8RawuxtLg_wsHgyuvm"
SUPABASE_STORAGE_URL = "https://ivmewysnzxbjnqlkcuul.supabase.co/storage/v1/object/public/cvs"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PLATAFORMAS = ["Todas", "LinkedIn", "Indeed", "OCC", "Computrabajo", "Bumeran"]
