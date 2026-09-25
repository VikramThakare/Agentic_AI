import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Use an open-source, local embedding model via HuggingFace.
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./vectorstore")

_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)
    return _embeddings

def get_vector_store() -> Chroma:
    """
    Returns the Chroma vector store instance. 
    It will load the existing database from CHROMA_DB_DIR if it exists,
    or create a new empty one in that directory.
    """
    return Chroma(
        collection_name="clinical_protocols",
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DB_DIR
    )
