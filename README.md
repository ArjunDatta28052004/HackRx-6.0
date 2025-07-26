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
├── build_index.py
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
sentence-transformers
faiss-cpu
unstructured
pypdf
python-docx
```
#### Install Them: 
```bash
pip install -r requirements.txt
```
### ✅ Step 3: Download SpaCy Language Model
```bash
python -m spacy download en_core_web_sm
```
### ✅ Step 4: Run build_index.py
```bash
python build_index.py
```
### ✅ Step 5: Launch the App
```bash
streamlit run app.py
```


## 🧪 Example Query
```bash
A 57-year-old male underwent knee surgery after 12 months
```
### Parsed Output:
```bash
{
"age":"57"
"gender":"male"
"procedure":"knee surgery"
"location":"N/A"
"policy_duration":"12 months"
}
```

### Decision Output:
```bash
Decision: Rejected

Justification: Knee surgery is subject to a 24-month waiting period.
```

### Policy Clauses Retrieved
```bash
Clause 1: 75 Rotational Arc Therapy 275 Testicular biopsy
76 Tele gamma therapy 276 laparoscopic cardiomyotomy( Hellers) 77 FSRT-Fractionated SRT 277 Sentinel node biopsy malignant melanoma 78 VMAT-Volumetric Modulated Arc Therapy 278 laparoscopic pyloromyotomy( Ramstedt) 79 SBRT-Stereotactic Body Radiotherapy Orthopedics 80 Helical Tomotherapy 279 Arthroscopic Repair of ACL tear knee 81 SRS-Stereotactic Radiosurgery 280 Closed reduction of minor Fractures 82 X-Knife SRS 281 Arthroscopic repair of PCL tear knee 83 Gammaknife SRS 282 Tendon shortening 84 TBI- Total Body Radiotherapy 283 Arthroscopic Meniscectomy - Knee 85 intraluminal Brachytherapy 284 Treatment of clavicle dislocation 86 Electron Therapy 285 Arthroscopic meniscus repair 87 TSET-Total Electron Skin Therapy 286 Haemarthrosis knee- lavage 88 Extracorporeal Irradiation of Blood Products 287 Abscess knee joint drainage
89 Telecobalt Therapy 288 Carpal tunnel release

Clause 2: 88 Extracorporeal Irradiation of Blood Products 287 Abscess knee joint drainage
89 Telecobalt Therapy 288 Carpal tunnel release 90 Telecesium Therapy 289 Closed reduction of minor dislocation 91 External mould Brachytherapy 290 Repair of knee cap tendon 92 Interstitial Brachytherapy 291 ORIF with K wire fixation- small bones 93 Intracavity Brachytherapy 292 Release of midfoot joint 94 3D Brachytherapy 293 ORIF with plating- Small long bones 95 Implant Brachytherapy 294 Implant removal minor 96 Intravesical Brachytherapy 295 K wire removal 97 Adjuvant Radiotherapy 296 POP application 98 Afterloading Catheter Brachytherapy 297 Closed reduction and external fixation 99 Conditioning Radiothearpy for BMT 298 Arthrotomy Hip joint
100 Extracorporeal Irradiation to the Homologous Bone grafts 299 Syme's amputation 101 Radical chemotherapy 300 Arthroplasty 102 Neoadjuvant radiotherapy 301 Partial removal of rib
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

    6.2 Justification (referencing policy clause logic)




