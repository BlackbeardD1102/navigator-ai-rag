
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# API de Google AI Studio
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Modelo LLM
MODEL_NAME = "gemini-3.5-flash"

# Modelo de embeddings
EMBEDDING_MODEL = "models/gemini-embedding-001"

# PDF
PDF_PATH = "plan_trading_navigator.pdf"

# Carpeta del índice FAISS
INDEX_PATH = "faiss_index"

# Configuración del chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Cantidad de documentos recuperados
TOP_K = 3
