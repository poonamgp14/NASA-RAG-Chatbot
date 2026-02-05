import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path
import openai
from openai import OpenAI
import os


def discover_chroma_backends(self) -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)

    # TODO: Loop through each discovered directory
        # TODO: Wrap connection attempt in try-except block for error handling
        
            # TODO: Initialize database client with directory path and configuration settings
            
            # TODO: Retrieve list of available collections from the database
            
            # TODO: Loop through each collection found
                # TODO: Create unique identifier key combining directory and collection names
                # TODO: Build information dictionary containing:
                    # TODO: Store directory path as string
                    # TODO: Store collection name
                    # TODO: Create user-friendly display name
                    # TODO: Get document count with fallback for unsupported operations
                # TODO: Add collection information to backends dictionary
        
        # TODO: Handle connection or access errors gracefully
            # TODO: Create fallback entry for inaccessible directories
            # TODO: Include error information in display name with truncation
            # TODO: Set appropriate fallback values for missing information

    # TODO: Return complete backends dictionary with all discovered collections

def initialize_rag_system(self,chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # TODO: Create a chomadb persistentclient ???????
    client = chromadb.persistentclient(
        path=chroma_dir,
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )
    
    return client.get_collection(name=collection_name)


def retrieve_documents(self,collection, query: str, n_results: int = 3, 
                    mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""



    # TODO: Initialize filter variable to None (represents no filtering)

    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs
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

        # TODO: Return query results to caller
        # Format results for better readability
        # formatted_results = {
        #     "query": query,
        #     "n_results": len(results['documents'][0]),
        #     "results": []
        # }
            
        # for i in range(len(results['documents'][0])):
        #     formatted_results["results"].append({
        #         "document": results['documents'][0][i],
        #         "similarity_score": 1 - results['distances'][0][i],  # Convert distance to similarity
        #         "metadata": results['metadatas'][0][i]
        #     })
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