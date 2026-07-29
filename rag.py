import os
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_community.vectorstores import FAISS

from config import *

# Configurar API
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# ---------- EMBEDDINGS ----------
embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL
)


# ---------- CARGAR FAISS ----------
vectorstore = FAISS.load_local(
    INDEX_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


retriever = vectorstore.as_retriever(
    search_kwargs={"k": TOP_K}
)


# ---------- LLM ----------
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0
)


def preguntar(pregunta):

    documentos = retriever.invoke(pregunta)

    contexto = "\n\n".join(
        [doc.page_content for doc in documentos]
    )

    prompt = f"""
Eres Navigator AI.

Responde únicamente usando el contexto.

Si la respuesta no aparece en el contexto responde exactamente:

"No encontré esa información en los documentos disponibles."

CONTEXTO

{contexto}

PREGUNTA

{pregunta}

RESPUESTA:
"""

    respuesta = llm.invoke(prompt)

    fuentes = []

    for doc in documentos:

        fuente = (
            f"{doc.metadata['source']} "
            f"(Página {doc.metadata['page']+1})"
        )

        if fuente not in fuentes:
            fuentes.append(fuente)

    return respuesta.text, fuentes
