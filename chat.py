import streamlit as st
import ollama


def mostrar_chat(data):
    if "chat_historial" not in st.session_state:
        st.session_state.chat_historial = []

    col_vacio, col_chat = st.columns([5, 1])
    with col_chat:
        with st.popover("💬 Chat", use_container_width=True):
            for msg in st.session_state.chat_historial:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            pregunta_app = st.chat_input("Pregunta algo...", key="chat_app")

            if pregunta_app:
                st.session_state.chat_historial.append({"role": "user", "content": pregunta_app})
                with st.chat_message("user"):
                    st.write(pregunta_app)

                contexto = "\n".join([
                    f"- Empresa: {d.get('empresa')}, Puesto: {d.get('puesto')}, Score: {d.get('score')}, "
                    f"Estado: {d.get('estado')}, Plataforma: {d.get('plataforma')}, "
                    f"Modalidad: {d.get('modalidad')}, Ubicación: {d.get('ubicacion')}, Notas: {d.get('notas')}"
                    for d in data
                ])

                prompt = f"""Tienes esta información de vacantes de trabajo de Mariana:

{contexto}

Pregunta: {pregunta_app}

Reglas importantes:
- Responde en español, de forma breve y directa.
- Usa ÚNICAMENTE los datos de arriba, no inventes nada.
- Si el dato exacto (como un número de teléfono) no aparece tal cual en las notas de arriba, responde: "No tengo ese dato registrado, revisa la columna de notas."
- No adivines ni asumas información que no esté escrita exactamente ahí."""

                with st.chat_message("assistant"):
                    with st.spinner("Pensando..."):
                        respuesta = ollama.chat(
                            model="llama3.2",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        texto_respuesta = respuesta["message"]["content"]
                        st.write(texto_respuesta)

                st.session_state.chat_historial.append({"role": "assistant", "content": texto_respuesta})
