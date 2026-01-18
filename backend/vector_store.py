"""
ChromaDB vector store setup and management with LlamaIndex
"""
import os
import chromadb
from chromadb.config import Settings
from llama_index.core import VectorStoreIndex, Document, StorageContext, Settings as LlamaSettings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalVectorStore:
    """Manage ChromaDB vector store for medical data"""
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.persist_dir = persist_dir
        self.collection_name = "medical_wikidoc"
        
        # Initialize embedding model (using HuggingFace for local embeddings)
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        # Initialize LLM (OpenAI GPT)
        self.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=512
        )
        
        # Set up LlamaIndex settings
        LlamaSettings.embed_model = self.embed_model
        LlamaSettings.llm = self.llm
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.index = None
        self.query_engine = None
        
    def create_index(self, documents: List[Dict[str, str]]) -> None:
        """
        Create vector store index from documents
        
        Args:
            documents: List of documents with text and metadata
        """
        try:
            logger.info(f"Creating index with {len(documents)} documents")
            
            # Create collection
            collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name
            )
            
            # Create vector store
            vector_store = ChromaVectorStore(chroma_collection=collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            # Convert to LlamaIndex documents
            llama_docs = []
            for doc in documents:
                llama_doc = Document(
                    text=doc["text"],
                    metadata=doc.get("metadata", {})
                )
                llama_docs.append(llama_doc)
            
            # Create index
            self.index = VectorStoreIndex.from_documents(
                llama_docs,
                storage_context=storage_context,
                show_progress=True
            )
            
            # Create query engine
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=3,
                response_mode="compact"
            )
            
            logger.info("Index created successfully")
            
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            raise
    
    def load_index(self) -> bool:
        """
        Load existing index from disk
        
        Returns:
            True if index loaded successfully, False otherwise
        """
        try:
            logger.info("Loading existing index")
            
            collection = self.chroma_client.get_collection(
                name=self.collection_name
            )
            
            vector_store = ChromaVectorStore(chroma_collection=collection)
            
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store
            )
            
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=3,
                response_mode="compact"
            )
            
            logger.info("Index loaded successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Could not load existing index: {e}")
            return False
    
    def query(self, query_text: str) -> str:
        """
        Query the vector store
        
        Args:
            query_text: User query
            
        Returns:
            Response from the query engine
        """
        if not self.query_engine:
            raise ValueError("Query engine not initialized. Create or load an index first.")
        
        try:
            response = self.query_engine.query(query_text)
            return str(response)
        except Exception as e:
            logger.error(f"Error querying: {e}")
            raise
    
    def reset(self) -> None:
        """Reset the vector store"""
        try:
            self.chroma_client.reset()
            logger.info("Vector store reset")
        except Exception as e:
            logger.error(f"Error resetting vector store: {e}")
            raise


if __name__ == "__main__":
    # Test vector store
    store = MedicalVectorStore()
    
    # Try loading existing index
    if not store.load_index():
        print("No existing index found. Create one using the main app.")
