import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path
import openai
from openai import OpenAI
import os

class ChromaDBRAGSystem:

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.persistentclient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.collections = {}


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
        
        return self.collections[collection_name]
    
    def _generate_embeddings(self, texts: List[str],embedding_config_model) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using the configured embedding model.
        
        This method handles both OpenAI and local embedding generation with proper
        error handling and batch processing for efficiency.
        
        Args:
            texts (List[str]): List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        print(f"🔄 Generating embeddings for {len(texts)} texts...")
        
        try:
                # Use OpenAI embeddings API
            response = self.openai_client.embeddings.create(
                model=embedding_config_model,
                input=texts
            )

            embeddings = [embedding.embedding for embedding in response.data]
            print(f"✅ Generated {len(embeddings)} OpenAI embeddings")
            return embeddings
                
        except Exception as e:
            print(f"❌ Error generating embeddings: {str(e)}")
            raise

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

        # TODO
        embedding_config_model = ''

        try: 
            query_embeddings = self._generate_embeddings(self,[query],embedding_config_model)

            results = self.collections.query(
                query_embeddings=query_embeddings,
                n_results = n_results,
                where = my_filter if my_filter else mission_filter,
                include=["documents", "distances", "metadatas"]
            )

            print(f"✅ Found {len(results['documents'][0])} relevant documents")

            # TODO: Return query results to caller
            # Format results for better readability
            formatted_results = {
                "query": query,
                "n_results": len(results['documents'][0]),
                "results": []
            }
                
            for i in range(len(results['documents'][0])):
                formatted_results["results"].append({
                    "document": results['documents'][0][i],
                    "similarity_score": 1 - results['distances'][0][i],  # Convert distance to similarity
                    "metadata": results['metadatas'][0][i]
                })
            return formatted_results
        except Exception as e:
            print(f"❌ Error searching documents: {str(e)}")
            return {"documents": [], "distances": [], "metadatas": []}

    def format_context(documents: List[str], metadatas: List[Dict]) -> str:
        """Format retrieved documents into context"""
        if not documents:
            return ""
        
        # TODO: Initialize list with header text for context section
        context_documents = []
        for result in documents["results"]:
            context_documents.append({
                "content": result["document"],
                "similarity": result["similarity_score"],
                "source": result["metadata"].get("source", "Unknown")
            })
        
        # Step 3: Create prompt with context
        context_text = "\n\n".join([
            f"Document {i+1} (Similarity: {doc['similarity']:.3f}):\n{doc['content']}"
            for i, doc in enumerate(context_documents)
        ])
        return context_text

        # TODO: Loop through paired documents and their metadata using enumeration
            # TODO: Extract mission information from metadata with fallback value
            # TODO: Clean up mission name formatting (replace underscores, capitalize)
            # TODO: Extract source information from metadata with fallback value  
            # TODO: Extract category information from metadata with fallback value
            # TODO: Clean up category name formatting (replace underscores, capitalize)
            
            # TODO: Create formatted source header with index number and extracted information
            # TODO: Add source header to context parts list
            
            # TODO: Check document length and truncate if necessary
            # TODO: Add truncated or full document content to context parts list

        # TODO: Join all context parts with newlines and return formatted string