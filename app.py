
import streamlit as st

st.set_page_config(
    page_title="Navigator AI",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 Navigator AI")

st.write("Asistente RAG para consultar el Plan Trading Navigator")

pregunta = st.text_input("Haz una pregunta")

if st.button("Consultar"):
    st.success(f"Pregunta recibida: {pregunta}")
