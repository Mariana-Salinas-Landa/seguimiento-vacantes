from config import supabase

data = {
    "empresa": "Empresa de prueba",
    "puesto": "Desarrollador",
    "link": "https://ejemplo.com",
    "score": 85,
    "estado": "aplicado",
    "plataforma": "LinkedIn"
}

response = supabase.table("Vacantes").insert(data).execute()
print(response)