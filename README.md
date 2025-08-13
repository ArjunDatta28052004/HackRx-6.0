# 🛡️ Insurance Query Processing System

This tool intelligently analyzes natural language insurance queries, extracts relevant details (age, gender, procedure, location, policy duration), searches insurance policy documents semantically, and provides decisions regarding claim eligibility.

---

## 📌 Features

- ✅ Natural language query processing
- ✅ Extracts key details like age, gender, procedure, etc.
- ✅ Semantic search over policy documents using FAISS + HuggingFace embeddings
- ✅ Automatic decision engine with justifications
- ✅ Streamlit-based UI for interactive usage
- ✅ REST API with JWT auth, per-user uploads and per-user FAISS indices

---

## 🗂 Project Structure

```bash
insurance-query-processor/
│
├── app.py # Flask REST API with JWT auth, upload, and query endpoints
├── main.py # Backend logic (embedding, parsing, decision, FAISS retrieval)
├── build_index.py # Index builder utilities (global and per-directory)
├── requirements.txt # All required Python packages
├── README.md # Project documentation
├── data/ # Example insurance policy PDFs
└── frontend/ # Static frontend (login, upload, query)
```

---

## 🚀 Installation and Usage

### ✅ Step 1: Install Required Packages
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### ✅ Step 2: (Optional) Build Global Index from `data/`
```bash
python build_index.py
```

### ✅ Step 3: Run the API
```bash
export FLASK_APP=app.py
export JWT_SECRET_KEY="change-me"
python app.py
# or
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

### ✅ Step 4: Static Frontend (optional)
Serve the contents of `frontend/` (any static server) or open `frontend/index.html` directly for local testing.

---

## 🔐 API Endpoints

- POST `/auth/register` -> `{ email, password }` => `{ access_token }`
- POST `/auth/login` -> `{ email, password }` => `{ access_token }`
- GET `/me` (Bearer token) => `{ user_id }`
- POST `/documents/upload` (Bearer token, multipart/form-data) -> `files: [pdf/docx...]`
- POST `/query` (Bearer token) -> `{ query: "..." }` => parsed info, decision, justification, clauses

Example curl usage:

```bash
# Register
curl -s -X POST http://localhost:5000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"pass1234"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"pass1234"}' | jq -r .access_token)

# Upload files
curl -s -X POST http://localhost:5000/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@data/BAJHLIP23020V012223.pdf" \
  -F "files=@data/ICIHLIP22012V012223.pdf"

# Query
curl -s -X POST http://localhost:5000/query \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query":"57-year-old male had knee surgery after 12 months"}' | jq
```

---

## 🧠 How It Works
1. Users authenticate and upload documents. A per-user FAISS index is built.
2. Queries are parsed to extract age, gender, procedure, location, and policy duration.
3. The user-specific index is searched for relevant clauses.
4. A rule-based decision engine returns Approved/Rejected with justification.




