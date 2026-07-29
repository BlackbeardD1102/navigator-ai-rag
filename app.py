import streamlit as st

st.set_page_config(page_title="Navigator AI", page_icon="🧭")

st.title("🧭 Navigator AI")
st.write("Asistente RAG del Plan Trading Navigator")

pregunta = st.text_input("Escribe tu pregunta")

if st.button("Consultar"):
    try:
        from rag import preguntar

        respuesta, fuentes = preguntar(pregunta)

        st.subheader("Respuesta")
        st.write(respuesta)

        st.subheader("Fuentes")
        if fuentes:
            for f in fuentes:
                st.write("•", f)
        else:
            st.write("No se encontraron fuentes.")

    except Exception as e:
        st.error(f"ERROR REAL: {e}")
        st.exception(e)
