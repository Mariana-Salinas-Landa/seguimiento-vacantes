import streamlit as st
import pandas as pd
import math
from config import supabase, PERSONA

column_config = {
    "favorito": st.column_config.CheckboxColumn("Favorito"),
    "notas": st.column_config.TextColumn("Notas"),
    "link": st.column_config.LinkColumn("Link", display_text="Ver vacante"),
    "fecha_aplicacion": st.column_config.DateColumn("Fecha de aplicación", format="YYYY-MM-DD"),
    "estado": st.column_config.SelectboxColumn(
        "Estado",
        options=["nueva", "aplicado", "entrevista", "rechazada", "descartada"]
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
                row_clean["persona"] = PERSONA
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


def guardar_cambios_automaticos(df, key_suffix):
    editor_key = f"editor_{key_suffix}"
    estado_editor = st.session_state[editor_key]

    filas_a_guardar = []

    for idx_str, cambios in estado_editor.get("edited_rows", {}).items():
        idx = int(idx_str)
        fila = df.iloc[idx].to_dict()
        fila.update(cambios)
        filas_a_guardar.append(fila)

    for fila_nueva in estado_editor.get("added_rows", []):
        if fila_nueva:
            filas_a_guardar.append(fila_nueva)

    if not filas_a_guardar:
        return

    for row in filas_a_guardar:
        if pd.notna(row.get("fecha_aplicacion")):
            row["fecha_aplicacion"] = str(row["fecha_aplicacion"])[:10]
        else:
            row["fecha_aplicacion"] = None

    guardar_cambios(filas_a_guardar)


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

    st.data_editor(
        df,
        column_config=column_config,
        num_rows="dynamic",
        key=f"editor_{key_suffix}",
        height=600,
        use_container_width=True,
        on_change=guardar_cambios_automaticos,
        args=(df, key_suffix)
    )
