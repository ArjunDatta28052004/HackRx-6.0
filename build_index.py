import os
from main import load_documents, split_documents, embed_documents
from langchain_community.vectorstores import FAISS

def build_and_save_index():
    os.makedirs("data", exist_ok=True)

    file_paths = [os.path.join("data", f) for f in os.listdir("data") if f.endswith((".pdf", ".docx"))]
    if not file_paths:
        print("❌ No valid documents found in 'data/'. Please add PDF or DOCX files.")
        return

    print(f"📄 Loading {len(file_paths)} documents:")
    for f in file_paths:
        print(f"   - {f}")

    documents = load_documents(file_paths)
    chunks = split_documents(documents)
    embeddings, _ = embed_documents(chunks)
    
    faiss_index = FAISS.from_documents(chunks, embeddings)
    faiss_index.save_local("faiss_index")

    print("✅ FAISS index saved successfully to faiss_index/")

if __name__ == "__main__":
    build_and_save_index()
