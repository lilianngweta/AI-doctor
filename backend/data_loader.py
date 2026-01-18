"""
Data loader for medical_meadow_wikidoc dataset from HuggingFace
"""
import os
from datasets import load_dataset
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikidocDataLoader:
    """Load and process medical data from HuggingFace"""
    
    def __init__(self, dataset_name: str = "medalpaca/medical_meadow_wikidoc"):
        self.dataset_name = dataset_name
        self.dataset = None
        
    def load_data(self, split: str = "train", max_samples: int = None) -> List[Dict[str, str]]:
        """
        Load dataset from HuggingFace
        
        Args:
            split: Dataset split to load (default: "train")
            max_samples: Maximum number of samples to load (None for all)
            
        Returns:
            List of documents with text content
        """
        try:
            logger.info(f"Loading dataset: {self.dataset_name}")
            self.dataset = load_dataset(self.dataset_name, split=split)
            
            if max_samples:
                self.dataset = self.dataset.select(range(min(max_samples, len(self.dataset))))
            
            logger.info(f"Loaded {len(self.dataset)} samples")
            
            # Process documents
            documents = []
            for idx, item in enumerate(self.dataset):
                # The dataset has 'input' and 'output' fields
                # Combine them for better context
                text = f"Question: {item.get('input', '')}\n\nAnswer: {item.get('output', '')}"
                
                documents.append({
                    "text": text,
                    "metadata": {
                        "source": "wikidoc",
                        "doc_id": f"wikidoc_{idx}",
                        "input": item.get('input', ''),
                        "output": item.get('output', '')
                    }
                })
            
            logger.info(f"Processed {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise


if __name__ == "__main__":
    # Test data loading
    loader = WikidocDataLoader()
    docs = loader.load_data(max_samples=100)
    print(f"Loaded {len(docs)} documents")
    if docs:
        print(f"\nSample document:\n{docs[0]['text'][:500]}...")
