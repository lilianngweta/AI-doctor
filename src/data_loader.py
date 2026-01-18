from datasets import load_dataset

def load_medical_qa_dataset():
    """
    Loads the medical_meadow_wikidoc dataset from Hugging Face.
    """
    print("Loading medical_meadow_wikidoc dataset...")
    dataset = load_dataset("medalpaca/medical_meadow_wikidoc")
    print("Dataset loaded successfully.")
    return dataset

def simple_keyword_search(query: str, dataset):
    """
    Performs a simple keyword search on the dataset's 'input' field.
    Returns the 'output' of the first matching entry (case-insensitive).
    """
    query_lower = query.lower()
    for entry in dataset['train']:
        if query_lower in entry['input'].lower():
            return entry['output']
    return "No information found for your query."

if __name__ == "__main__":
    medical_dataset = load_medical_qa_dataset()
    print(f"Dataset structure: {medical_dataset}")
    print(f"First entry in train split: {medical_dataset['train'][0]}")

    # Demonstrate the simple search functionality
    print("\n--- Testing simple keyword search ---")
    test_query_1 = "lung's squamous cell carcinoma"
    result_1 = simple_keyword_search(test_query_1, medical_dataset)
    print(f"Query: '{test_query_1}'")
    print(f"Result: {result_1}")

    test_query_2 = "What causes diabetes?"
    result_2 = simple_keyword_search(test_query_2, medical_dataset)
    print(f"Query: '{test_query_2}'")
    print(f"Result: {result_2}")

    test_query_3 = "non-existent medical condition"
    result_3 = simple_keyword_search(test_query_3, medical_dataset)
    print(f"Query: '{test_query_3}'")
    print(f"Result: {result_3}")

