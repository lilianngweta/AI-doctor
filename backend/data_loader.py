"""
Data loader for medical datasets from HuggingFace
"""
import os
from datasets import load_dataset
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikidocDataLoader:
    """Load and process medical data from HuggingFace"""
    
    def __init__(self, dataset_name: str = None):
        self.dataset_name = dataset_name or os.getenv(
            "DATASET_NAME",
            "lavita/ChatDoctor-HealthCareMagic-100k"
        )
        self.dataset = None

    def _detect_fields(self, item: Dict[str, str]):
        candidates = [
            ("input", "output"),
            ("instruction", "output"),
            ("question", "answer"),
            ("prompt", "response"),
            ("query", "response"),
        ]
        for question_field, answer_field in candidates:
            if question_field in item and answer_field in item:
                return question_field, answer_field
        if "text" in item:
            return "text", None

        string_fields = [
            key for key, value in item.items()
            if isinstance(value, str) and value.strip()
        ]
        if string_fields:
            question_field = string_fields[0]
            answer_field = string_fields[1] if len(string_fields) > 1 else None
            return question_field, answer_field
        return None, None
        
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
            def _truncate(value: str, max_len: int = 200) -> str:
                if not value:
                    return ""
                if len(value) <= max_len:
                    return value
                return value[:max_len - 3] + "..."

            if len(self.dataset) == 0:
                return []

            question_field, answer_field = self._detect_fields(self.dataset[0])
            if not question_field:
                raise ValueError("Could not detect text fields in dataset items.")

            documents = []
            for idx, item in enumerate(self.dataset):
                question_text = item.get(question_field, "")
                answer_text = item.get(answer_field, "") if answer_field else ""

                if answer_field:
                    text = f"Question: {question_text}\n\nAnswer: {answer_text}"
                else:
                    text = question_text

                documents.append({
                    "text": text,
                    "metadata": {
                        "source": "huggingface",
                        "dataset": self.dataset_name,
                        "doc_id": f"{self.dataset_name}_{idx}",
                        "question_field": question_field,
                        "answer_field": answer_field or "",
                        "question": _truncate(question_text),
                        "answer": _truncate(answer_text)
                    }
                })

            # Add small curated set for common conditions to improve coverage.
            documents.extend(self._curated_documents())
            
            logger.info(f"Processed {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise

    def _curated_documents(self) -> List[Dict[str, str]]:
        curated = [
            {
                "id": "flu_symptoms",
                "title": "Flu symptoms overview",
                "text": (
                    "Common flu symptoms include fever or chills, cough, sore throat, "
                    "runny or stuffy nose, muscle or body aches, headaches, fatigue, "
                    "and sometimes vomiting or diarrhea (more common in children)."
                ),
            },
            {
                "id": "flu_when_seek_help",
                "title": "Flu when to seek care",
                "text": (
                    "Seek medical care for flu if you have trouble breathing, chest "
                    "pain, persistent dizziness, confusion, severe weakness, or if "
                    "symptoms improve then return with fever and worse cough."
                ),
            },
            {
                "id": "cold_vs_flu",
                "title": "Cold vs flu basics",
                "text": (
                    "Colds usually start gradually with milder symptoms like sneezing "
                    "and runny nose, while flu often starts suddenly with fever, "
                    "body aches, and marked fatigue."
                ),
            },
            {
                "id": "fever_overview",
                "title": "Fever basics",
                "text": (
                    "Fever is a body temperature higher than normal, commonly above "
                    "100.4 F (38 C). It can occur with infections and usually improves "
                    "with rest, fluids, and fever-reducing medicines."
                ),
            },
            {
                "id": "hydration_tips",
                "title": "Hydration tips",
                "text": (
                    "For viral illnesses, rest and hydration can help recovery. "
                    "Drink water or oral rehydration fluids, and monitor for signs "
                    "of dehydration such as dark urine or dizziness."
                ),
            },
            {
                "id": "sore_throat_home_care",
                "title": "Sore throat home care",
                "text": (
                    "Home care for a mild sore throat: warm fluids, honey in tea "
                    "(avoid in children under 1 year), saltwater gargles, throat "
                    "lozenges, and rest. Seek care if severe pain, trouble breathing "
                    "or swallowing, high fever, or symptoms last longer than a week."
                ),
            },
            {
                "id": "cough_home_care",
                "title": "Cough home care",
                "text": (
                    "For a mild cough: stay hydrated, use warm drinks, honey for adults "
                    "and children over 1 year, and consider humidified air. Seek care "
                    "if cough lasts more than 2-3 weeks, blood in mucus, chest pain, "
                    "or shortness of breath."
                ),
            },
            {
                "id": "runny_nose_home_care",
                "title": "Runny nose home care",
                "text": (
                    "For runny or stuffy nose: saline nasal spray or rinse, steam "
                    "inhalation, fluids, and rest. Seek care if severe sinus pain, "
                    "high fever, or symptoms last more than 10 days."
                ),
            },
            {
                "id": "headache_home_care",
                "title": "Headache home care",
                "text": (
                    "For mild headaches: rest in a quiet room, hydrate, apply a cool "
                    "or warm compress, and avoid triggers. Seek care for sudden severe "
                    "headache, weakness, confusion, or after head injury."
                ),
            },
            {
                "id": "indigestion_home_care",
                "title": "Indigestion home care",
                "text": (
                    "For indigestion: eat smaller meals, avoid lying down after eating, "
                    "limit spicy or fatty foods, and sip water. Seek care if severe "
                    "abdominal pain, vomiting blood, or black stools."
                ),
            },
            {
                "id": "constipation_home_care",
                "title": "Constipation home care",
                "text": (
                    "For constipation: drink water, increase fiber (fruits, vegetables, "
                    "whole grains), and stay active. Seek care if severe pain, blood "
                    "in stool, or constipation lasts more than 2 weeks."
                ),
            },
            {
                "id": "nausea_home_care",
                "title": "Mild nausea home care",
                "text": (
                    "For mild nausea: small sips of water, bland foods like crackers, "
                    "ginger tea, and rest. Seek care if persistent vomiting, signs of "
                    "dehydration, or severe abdominal pain."
                ),
            },
            {
                "id": "diarrhea_home_care",
                "title": "Mild diarrhea home care",
                "text": (
                    "For mild diarrhea: oral rehydration fluids, bland foods, and rest. "
                    "Avoid dairy and fatty foods for a day or two. Seek care for blood "
                    "in stool, high fever, or dehydration."
                ),
            },
            {
                "id": "muscle_strain_home_care",
                "title": "Muscle strain home care",
                "text": (
                    "For a mild muscle strain: rest the area, apply ice for 10-20 minutes "
                    "several times daily for the first 48 hours, then heat as needed. "
                    "Seek care if severe pain, swelling, or inability to use the limb."
                ),
            },
            {
                "id": "minor_burns_home_care",
                "title": "Minor burn home care",
                "text": (
                    "For minor burns: cool the area under running water for several minutes, "
                    "cover with a clean non-stick dressing, and avoid breaking blisters. "
                    "Seek care for large burns, face or hand burns, or signs of infection."
                ),
            },
            {
                "id": "insect_bite_home_care",
                "title": "Insect bite home care",
                "text": (
                    "For insect bites: wash with soap and water, apply a cold compress, "
                    "and avoid scratching. Seek care for spreading redness, fever, or "
                    "signs of allergic reaction (trouble breathing, facial swelling)."
                ),
            },
            {
                "id": "seasonal_allergies_home_care",
                "title": "Seasonal allergies home care",
                "text": (
                    "For seasonal allergies: rinse nasal passages with saline, keep windows "
                    "closed during high pollen, and shower after being outside. Seek care "
                    "if symptoms are severe or causing breathing problems."
                ),
            },
            {
                "id": "mild_rash_home_care",
                "title": "Mild rash home care",
                "text": (
                    "For a mild rash: keep skin clean and dry, avoid new products, and use "
                    "cool compresses. Seek care if rash spreads rapidly, is painful, "
                    "or you have fever."
                ),
            },
            {
                "id": "oral_cold_sore_home_care",
                "title": "Cold sore home care",
                "text": (
                    "For cold sores: keep the area clean, avoid picking, and use cold "
                    "compresses for discomfort. Seek care if sores are severe, frequent, "
                    "or accompanied by high fever."
                ),
            },
            {
                "id": "earache_home_care",
                "title": "Mild earache home care",
                "text": (
                    "For mild ear discomfort: warm compresses and rest may help. Seek care "
                    "if severe pain, fever, drainage from the ear, or symptoms in young "
                    "children."
                ),
            },
        ]

        documents: List[Dict[str, str]] = []
        for item in curated:
            documents.append({
                "text": f"{item['title']}\n\n{item['text']}",
                "metadata": {
                    "source": "curated",
                    "doc_id": f"curated_{item['id']}",
                    "topic": item["title"],
                },
            })

        return documents


if __name__ == "__main__":
    # Test data loading
    loader = WikidocDataLoader()
    docs = loader.load_data(max_samples=100)
    print(f"Loaded {len(docs)} documents")
    if docs:
        print(f"\nSample document:\n{docs[0]['text'][:500]}...")
