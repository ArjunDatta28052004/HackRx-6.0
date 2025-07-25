import os
import re
import spacy
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Load and process documents
def load_documents(file_paths):
    documents = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            continue
        documents.extend(loader.load())
    return documents

# Split documents into chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

# Embed and store documents in FAISS
def embed_and_store_documents(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

# Query processing using SpaCy
def parse_query(query):
    doc = nlp(query)
    parsed = {
        "age": "N/A",
        "gender": "N/A",
        "procedure": "N/A",
        "location": "N/A",
        "policy_duration": "N/A"
    }

    # Extract entities using SpaCy
    for ent in doc.ents:
        if ent.label_ == "AGE":
            parsed["age"] = ent.text.split()[0]
        elif ent.label_ == "GPE":  # Geopolitical entity
            parsed["location"] = ent.text
        elif "month" in ent.text.lower() or "year" in ent.text.lower():
            parsed["policy_duration"] = ent.text

    # ✅ Age fallback: e.g., "52-year-old"
    if parsed["age"] == "N/A":
        age_match = re.search(r'(\d{2})[- ]?year[- ]?old', query, re.IGNORECASE)
        if age_match:
            parsed["age"] = age_match.group(1)

    # ✅ Gender detection (supports F, M, female, male)
    gender_match = re.search(r'\b(female|f|male|m)\b', query.lower())
    if gender_match:
        gender = gender_match.group(1)
        if gender in ["female", "f"]:
            parsed["gender"] = "female"
        elif gender in ["male", "m"]:
            parsed["gender"] = "male"

    # ✅ Location fallback: "from Pune"
    if parsed["location"] == "N/A":
        location_match = re.search(r'from ([A-Za-z ]+)', query, re.IGNORECASE)
        if location_match:
            parsed["location"] = location_match.group(1).strip()

    # ✅ Procedure extraction: "back surgery", "heart operation", etc.
    if parsed["procedure"] == "N/A":
        proc_match = re.search(r'\b(\w+ (surgery|operation|procedure|treatment))\b', query, re.IGNORECASE)
        if proc_match:
            parsed["procedure"] = proc_match.group(1).strip()

    return parsed


# Semantic search
def semantic_search(vector_store, query_embedding):
    results = vector_store.similarity_search(query_embedding, k=5)
    return results


# Helper function to extract total months from policy duration text
def extract_months(duration_text):
    duration_text = duration_text.lower()
    months = 0

    year_match = re.search(r'(\d+)\s*year', duration_text)
    month_match = re.search(r'(\d+)\s*month', duration_text)

    if year_match:
        months += int(year_match.group(1)) * 12
    if month_match:
        months += int(month_match.group(1))

    return months

# Decision evaluation
def evaluate_decision(retrieved_clauses, parsed_query):
    duration_months = extract_months(parsed_query["policy_duration"])

    if "surgery" in parsed_query['procedure'].lower() and duration_months < 24:
        return {
            "Decision": "Rejected",
            "Amount": "N/A",
            "Justification": f"{parsed_query['procedure'].capitalize()} is subject to a 24-month waiting period."
        }

    return {
        "Decision": "Approved",
        "Amount": "10000",
        "Justification": f"{parsed_query['procedure'].capitalize()} is covered under the policy."
    }

# Main function to process the query
def process_query(query):
    # Load documents
    documents = load_documents(['data/BAJHLIP23020V012223.pdf', 'data/CHOTGDP23004V012223.pdf', 
                                'data/EDLHLGA23009V012223.pdf', 'data/HDFHLIP23024V072223.pdf',
                                'data/ICIHLIP22012V012223.pdf'])
    
    # Split documents into chunks
    document_chunks = split_documents(documents)
    
    # Embed and store documents
    vector_store = embed_and_store_documents(document_chunks)
    
    # Parse the query
    parsed_query = parse_query(query)
    
    # Perform semantic search
    retrieved_clauses = semantic_search(vector_store, query)
    
    # Evaluate decision
    decision = evaluate_decision(retrieved_clauses, parsed_query)
    
    return {
        "Parsed Query": parsed_query,
        "Top Retrieved Clauses": [doc.page_content for doc in retrieved_clauses],
        "Decision": decision
    }


# Example usage with user input
# if __name__ == "__main__":
#     print("Welcome to the Insurance Query Processing System!")
#     while True:
#         query = input("Please enter your query (or type 'exit' to quit): ")
#         if query.lower() == 'exit':
#             print("Exiting the system. Goodbye!")
#             break
#         response = process_query(query)
#         print("\nParsed Query:")
#         print(response["Parsed Query"])
#         print("\nTop Retrieved Clauses:")
#         for i, clause in enumerate(response["Top Retrieved Clauses"], 1):
#             print(f"Clause {i}: {clause}\n")
#         print("Decision:")
#         print(response["Decision"])
#         print("=" * 80)

