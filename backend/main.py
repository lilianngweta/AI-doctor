"""
FastAPI backend for AI Doctor wellness app
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import logging

from data_loader import WikidocDataLoader
from vector_store import MedicalVectorStore

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Doctor - Wellness Advice API",
    description="AI-powered wellness advice using medical knowledge from Wikidoc",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vector store instance
vector_store: Optional[MedicalVectorStore] = None


class QueryRequest(BaseModel):
    """Request model for health queries"""
    question: str
    

class QueryResponse(BaseModel):
    """Response model for health queries"""
    answer: str
    success: bool
    

class StatusResponse(BaseModel):
    """System status response"""
    status: str
    index_loaded: bool
    message: str


@app.on_event("startup")
async def startup_event():
    """Initialize the vector store on startup"""
    global vector_store
    
    try:
        logger.info("Starting up AI Doctor API...")
        
        # Check for OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY not found in environment variables")
        
        # Initialize vector store
        chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        vector_store = MedicalVectorStore(persist_dir=chroma_db_path)
        
        # Try to load existing index
        if not vector_store.load_index():
            logger.info("No existing index found. Use /initialize endpoint to create one.")
        else:
            logger.info("Vector store index loaded successfully")
            
    except Exception as e:
        logger.error(f"Error during startup: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Doctor - Wellness Advice API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "initialize": "/initialize",
            "query": "/query"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status"""
    global vector_store
    
    if vector_store is None:
        return StatusResponse(
            status="error",
            index_loaded=False,
            message="Vector store not initialized"
        )
    
    index_loaded = vector_store.index is not None
    
    return StatusResponse(
        status="ok" if index_loaded else "not_ready",
        index_loaded=index_loaded,
        message="System ready" if index_loaded else "Index not loaded. Use /initialize to create index."
    )


@app.post("/initialize")
async def initialize_index(max_samples: Optional[int] = 1000):
    """
    Initialize the vector store with data from HuggingFace
    
    Args:
        max_samples: Maximum number of samples to load (default: 1000)
    """
    global vector_store
    
    try:
        logger.info(f"Initializing index with max {max_samples} samples...")
        
        # Load data
        loader = WikidocDataLoader()
        documents = loader.load_data(max_samples=max_samples)
        
        # Create index
        vector_store.create_index(documents)
        
        return {
            "success": True,
            "message": f"Index initialized with {len(documents)} documents",
            "documents_count": len(documents)
        }
        
    except Exception as e:
        logger.error(f"Error initializing index: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_health(request: QueryRequest):
    """
    Query the AI doctor for wellness advice
    
    Args:
        request: QueryRequest with user question
        
    Returns:
        AI-generated wellness advice
    """
    global vector_store
    
    if vector_store is None or vector_store.query_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store not initialized. Use /initialize endpoint first."
        )
    
    try:
        logger.info(f"Processing query: {request.question}")
        
        # Query the vector store
        answer = vector_store.query(request.question)
        
        return QueryResponse(
            answer=answer,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_index():
    """Reset the vector store (use with caution)"""
    global vector_store
    
    try:
        if vector_store:
            vector_store.reset()
            
        return {
            "success": True,
            "message": "Vector store reset successfully"
        }
        
    except Exception as e:
        logger.error(f"Error resetting index: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(app, host=host, port=port)
