import os
import glob
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from rag.vector_store import get_vector_store

PROTOCOLS_DIR = Path(__file__).parent.parent / "data" / "protocols"

def build_index():
    """
    Reads markdown protocols, chunks them using semantic headers, 
    injects category metadata, and stores them in Chroma.
    """
    vector_store = get_vector_store()
    
    # Define how to split markdown by semantic sections
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    # Secondary splitter for large chunks to fit LLM context perfectly
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    
    all_chunks = []
    
    for md_file in PROTOCOLS_DIR.glob("*.md"):
        category = md_file.stem  # e.g., "sepsis", "respiratory"
        
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Semantic markdown split
        md_docs = markdown_splitter.split_text(content)
        
        # Inject metadata and further split if necessary
        for doc in md_docs:
            doc.metadata["category"] = category
            doc.metadata["source"] = md_file.name
            
        final_docs = text_splitter.split_documents(md_docs)
        all_chunks.extend(final_docs)
        
    if all_chunks:
        print(f"Indexing {len(all_chunks)} protocol chunks into Chroma...")
        vector_store.add_documents(all_chunks)
        print("Indexing complete.")

if __name__ == "__main__":
    build_index()
