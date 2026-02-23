import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path
import openai
from openai import OpenAI
import os


def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path("./data_text")
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)

    for root, dirs, files in os.walk(current_dir):
        for dir in dirs:
            print("------")
            print(dir)
            try:
                client = chromadb.PersistentClient(
                    path=dir,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=True
                    )
                )
                collection = client.get_or_create_collection(
                    name=dir,
                    metadata={"description": "NASA space mission documents with OpenAI Embeddings"}
                )
                # for collection in collections:
                collection_info = {}
                collection_info['path'] =  os.path.join(root, dir)
                collection_info['name'] = collection.name
                collection_info['documentCount'] = collection.count() if collection.count() else 0
                display_name = os.path.join(root, dir) + collection.name
                backends[display_name] = collection_info
            except Exception as e:
                print(f"❌ Error connecting db while scanning directory: {str(e)}")
                    # return {"documents": [], "distances": [], "metadatas": []}
    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # TODO: Create a chomadb persistentclient ???????
    client = chromadb.PersistentClient(
        path=chroma_dir,
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )
    
    return client.get_collection(name=collection_name)


def retrieve_documents(collection, query: str, n_results: int = 3, 
                    mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""
    my_filter = {}
    if mission_filter:
        print(f"Filters: {mission_filter}")
        for x in mission_filter:
            if x != 'all':
                my_filter["category"]=x

    try:

        results = collection.query(
            query_texts=[query],
            n_results = n_results,
            where = my_filter if my_filter else mission_filter
        )

        print(f"✅ Found {len(results['documents'][0])} relevant documents")
        return results
    except Exception as e:
        print(f"❌ Error searching documents: {str(e)}")
        return {"documents": [], "distances": [], "metadatas": []}

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    contexts = []
    
    for i, document in enumerate(documents):
        mission = metadatas[i]['mission'].replace('_', '').capitalize() if metadatas[i]['mission'] else 'unknown source'
        source =  metadatas[i]['source'] if metadatas[i]['source'] else 'unknown source'
        category = metadatas[i]['document_category'].replace('_', '').capitalize() if metadatas[i]['document_category'] else 'unknown category'
        document_header = f"""DOC {i} - ${mission} - ${source} - ${category}"""
        contexts.append("\n\n".join(
            f"Document {document_header} :\n{document['content']}"
        ))
    return "\n".join(contexts)