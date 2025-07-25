# 🛡️ Insurance Query Processing System

This tool intelligently analyzes natural language insurance queries, extracts relevant details (age, gender, procedure, location, policy duration), searches insurance policy documents semantically, and provides decisions regarding claim eligibility.

---

## 📌 Features

- ✅ Natural language query processing
- ✅ Extracts key details like age, gender, procedure, etc.
- ✅ Semantic search over policy documents using FAISS + HuggingFace embeddings
- ✅ Automatic decision engine with justifications
- ✅ Streamlit-based UI for interactive usage

---

## 🗂 Project Structure

```bash
insurance-query-processor/
│
├── app.py # Streamlit frontend application
├── main.py # Backend logic (embedding, parsing, decision)
├── requirements.txt # All required Python packages
├── README.md # Project documentation
├── data/ # Folder containing insurance policy PDFs
│ ├── BAJHLIP23020V012223.pdf
│ ├── CHOTGDP23004V012223.pdf
│ └── ...

```

---

## 🚀 Installation and Usage

### ✅ Step 1: Clone the Repository

```bash
git clone https://github.com/ArjunDatta28052004/HackRx-6.0.git
cd HackRx-6.0
```
### ✅ Step 2: Install Required Packages
#### Dependencies:
```bash
streamlit

spacy

langchain

langchain-community

langchain-huggingface

unstructured

pypdf

faiss-cpu

sentence-transformers
```
#### Install Them: 
```bash
pip install -r requirements.txt
```
### ✅ Step 3: Download SpaCy Language Model
```bash
python -m spacy download en_core_web_sm
```
### ✅ Step 4: Launch the App
```bash
streamlit run app.py
```


## 🧪 Example Query
```bash
I am a 57-year-old female from Kolkata. I recently had knee surgery. My policy has been active for 10 months.
```
### Parsed Output:
```bash
{
  "age": "57",
  "gender": "female",
  "procedure": "knee surgery",
  "location": "Kolkata",
  "policy_duration": "10 months"
}
```

### Decision Output:
```bash
{
  "Decision": "Rejected",
  "Amount": "N/A",
  "Justification": "Knee surgery is subject to a 24-month waiting period."
}
```

## 🧠 How It Works

1. User enters a natural language insurance query.

2. Query is parsed with SpaCy to extract:

    2.1 Age

    2.2 Gender

    2.3 Medical Procedure

    2.4 Location

    2.5 Policy Duration

3. Preloaded insurance policy documents are embedded using sentence-transformers and indexed with FAISS.

4. The query is semantically matched to the top relevant policy clauses.

5. A rule-based engine evaluates if the procedure is eligible based on extracted details.

6. The system returns a structured JSON response including:

    6.1 Decision (Approved/Rejected)

    6.2 Amount (if applicable)

    6.3 Justification (referencing policy clause logic)




