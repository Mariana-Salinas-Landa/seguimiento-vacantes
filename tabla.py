import streamlit as st
import pandas as pd
import math
from config import supabase

column_config = {
    "favorito": st.column_config.CheckboxColumn("Favorito"),
    "notas": st.column_config.TextColumn("Notas"),
    "link": st.column_config.LinkColumn("Link", display_text="Ver vacante"),
    "fecha_aplicacion": st.column_config.DateColumn("Fecha de aplicación", format="YYYY-MM-DD"),
    "estado": st.column_config.SelectboxColumn(
        "Estado",
        options=["nueva", "aplicado", "entrevista", "descartada"]
    ),
    "plataforma": st.column_config.SelectboxColumn(
        "Plataforma",
        options=["LinkedIn", "Indeed", "OCC", "Computrabajo", "Bumeran"]
    ),
    "modalidad": st.column_config.SelectboxColumn(
        "Modalidad",
        options=["Presencial", "Híbrido", "Remoto"]
    ),
    "rango_salarial": st.column_config.TextColumn("Rango salarial"),
    "cv_ingeniero_datos": st.column_config.CheckboxColumn("CV Ing. Datos"),
    "cv_maestro": st.column_config.CheckboxColumn("CV Maestro"),
    "cv_especial": st.column_config.CheckboxColumn("CV Especial"),
}


def limpiar_valor(v):
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def guardar_cambios(edited_data):
    errores = []
    for row in edited_data:
        row_id = row.get("id")
        row_clean = {k: limpiar_valor(v) for k, v in row.items() if k not in ("id", "created_at")}

        if row_clean.get("score") is not None:
            row_clean["score"] = int(row_clean["score"])

        try:
            if row_id:
                supabase.table("Vacantes").update(row_clean).eq("id", row_id).execute()
            else:
                row_clean["persona"] = "mariana"
                supabase.table("Vacantes").insert(row_clean).execute()
        except Exception as e:
            errores.append(str(e))

    if errores:
        st.error("Hubo errores al guardar:")
        for e in errores:
            st.code(e)
    else:
        st.success("Cambios guardados correctamente")
        st.rerun()


def mostrar_tabla(datos, key_suffix):
    st.subheader(f"Total: {len(datos)}")
    df = pd.DataFrame(datos)
    if "fecha_aplicacion" in df.columns:
        df["fecha_aplicacion"] = pd.to_datetime(df["fecha_aplicacion"], errors="coerce")

    busqueda = st.text_input("🔎 Buscar empresa o puesto", key=f"buscar_{key_suffix}")
    if busqueda:
        mask = (
            df["empresa"].astype(str).str.contains(busqueda, case=False, na=False)
            | df["puesto"].astype(str).str.contains(busqueda, case=False, na=False)
        )
        df = df[mask]

    edited = st.data_editor(
        df,
        column_config=column_config,
        num_rows="dynamic",
        key=f"editor_{key_suffix}",
        height=600,
        use_container_width=True
    )

    edited = edited.where(pd.notnull(edited), None)

    if st.button("Guardar cambios", key=f"guardar_{key_suffix}"):
        edited_records = edited.to_dict(orient="records")
        for row in edited_records:
            if pd.notna(row.get("fecha_aplicacion")):
                row["fecha_aplicacion"] = str(row["fecha_aplicacion"])[:10]
            else:
                row["fecha_aplicacion"] = None
        guardar_cambios(edited_records)
