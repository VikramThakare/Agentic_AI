from rag.vector_store import get_vector_store
from typing import List
from langchain_core.documents import Document

def retrieve_protocol_evidence(query: str, category: str, k: int = 3) -> List[Document]:
    """
    Retrieves the top-k relevant chunks from Chroma, perfectly filtered 
    by the protocol category that the trend engine matched.
    """
    vector_store = get_vector_store()
    
    # Filter strictly by the category metadata we injected during indexing
    # This prevents searching the Sepsis protocol when the patient has a Respiratory issue.
    search_kwargs = {
        "k": k,
        "filter": {"category": category}
    }
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )
    
    # Execute the retrieval
    docs = retriever.invoke(query)
    return docs
