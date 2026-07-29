import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Leer API desde Streamlit Secrets (Cloud) o entorno local
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else os.getenv("GOOGLE_API_KEY")

MODEL_NAME = "gemini-3.6-flash"
EMBEDDING_MODEL = "models/gemini-embedding-001"
INDEX_PATH = "faiss_index"
TOP_K = 3

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

# Cargar índice FAISS
vectorstore = FAISS.load_local(
    INDEX_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

# Modelo Gemini
llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

def preguntar(pregunta):
    try:
        documentos = retriever.invoke(pregunta)

        contexto = "\n\n".join([doc.page_content for doc in documentos])

        prompt = f"""
Eres Navigator AI.
Responde únicamente usando el contexto proporcionado.
Si la respuesta no está en el contexto responde exactamente:
No encontré esa información en los documentos disponibles.

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:
"""

        respuesta = llm.invoke(prompt)

        texto = getattr(respuesta, "content", str(respuesta))

        if isinstance(texto, list):
            partes = []
            for item in texto:
                if isinstance(item, dict) and item.get("type") == "text":
                    partes.append(item.get("text", ""))
            texto = "\n".join(partes)

        fuentes = []
        for doc in documentos:
            fuente = f"{doc.metadata['source']} (Página {doc.metadata['page']+1})"
            if fuente not in fuentes:
                fuentes.append(fuente)

        return texto, fuentes

    except Exception as e:
        return f"ERROR: {e}", []
