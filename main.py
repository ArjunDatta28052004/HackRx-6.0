import os
import re
import spacy
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceHub

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define known data
known_procedures = [
    "knee surgery", "back surgery", "eye surgery", "heart surgery", "brain surgery",
    "neck surgery", "shoulder surgery", "hip replacement", "bypass surgery",
    "dental treatment", "appendix removal", "chemotherapy", "dialysis"
]
known_locations = [
    "pune", "delhi", "kolkata", "mumbai", "chennai", "bangalore", "hyderabad",
    "lucknow", "ahmedabad", "jaipur"
]

# Load FAISS index and embedder
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)

# Load documents
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

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

def embed_documents(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings, documents

# ------------------------------------
# 🔍 Query Parsing
# ------------------------------------
def parse_query(text):
    text = text.lower()

    # Age
    age_match = re.search(r'aged\s+(\d+)|(\d+)[-\s]?year[-\s]?old|^(\d+)\s*[fm]\b|(\d+)\s*[fm]\b', text)
    age = next((g for g in age_match.groups() if g), "N/A") if age_match else "N/A"

    # Gender
    if re.search(r'\b(female|wife|mother|she|f\b)\b', text):
        gender = "female"
    elif re.search(r'\b(male|husband|father|he|m\b)\b', text):
        gender = "male"
    else:
        gender = "N/A"

    # Procedure
    procedure = "N/A"
    for proc in known_procedures:
        if proc in text:
            procedure = proc
            break
    if procedure == "N/A":
        match = re.search(r'(knee|eye|back|heart|brain|neck|hip|shoulder|lung|spine|liver|skin)\s+(surgery|treatment)', text)
        if match:
            procedure = f"{match.group(1)} {match.group(2)}"

    # Location
    location = "N/A"
    for loc in known_locations:
        if loc in text:
            location = loc.capitalize()
            break
    if location == "N/A":
        loc_match = re.search(r"(in|from)\s+([a-z]+)", text)
        if loc_match:
            location = loc_match.group(2).capitalize()

    # Policy Duration
    duration_match = re.search(r'(\d+)\s*(months|month|years|year)', text)
    policy_duration = f"{duration_match.group(1)} {duration_match.group(2)}" if duration_match else "N/A"

    return {
        "age": age,
        "gender": gender,
        "procedure": procedure,
        "location": location,
        "policy_duration": policy_duration
    }

# ------------------------------------
# ✅ Decision Logic
# ------------------------------------
def evaluate_decision(parsed_query):
    try:
        months = int(re.search(r'\d+', parsed_query["policy_duration"]).group())
        if "year" in parsed_query["policy_duration"].lower():
            months *= 12
    except:
        months = 0

    if "surgery" in parsed_query['procedure'].lower() and months < 24:
        return {
            "Decision": "Rejected",
            "Justification": f"{parsed_query['procedure'].capitalize()} is subject to a 24-month waiting period."
        }
    return {
        "Decision": "Approved",
        "Justification": f"{parsed_query['procedure'].capitalize()} is covered under the policy."
    }

# ------------------------------------
# 📑 Clause Retrieval from FAISS
# ------------------------------------
def retrieve_clauses(query, k=2):
    vectorstore = load_vector_store()
    matches = vectorstore.similarity_search(query, k=k)
    return [doc.page_content.strip() for doc in matches]

# ------------------------------------
# 🎯 Main Function: Full Pipeline
# ------------------------------------
def process_insurance_query(user_text):
    parsed = parse_query(user_text)
    decision = evaluate_decision(parsed)
    clauses = retrieve_clauses(parsed["procedure"] or "surgery")

    return {
        "parsed_info": parsed,
        "decision": decision["Decision"],
        "justification": decision["Justification"],
        "policy_clauses": clauses
    }
