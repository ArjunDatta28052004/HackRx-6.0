import streamlit as st
from main import process_query  # This imports your logic

st.set_page_config(page_title="🛡️ Insurance Query System", layout="wide")
st.title("🛡️ Insurance Query Processing System")

st.markdown("This tool analyzes insurance queries, retrieves relevant clauses, and provides approval decisions.")

with st.form("query_form"):
    query = st.text_area(
        "📝 Enter your insurance query:",
        placeholder="E.g., I am a 45-year-old male from Delhi. I want to claim for a gallbladder surgery after 6 months of policy coverage.",
        height=200
    )
    submit = st.form_submit_button("🔍 Process Query")

if submit and query.strip():
    with st.spinner("Processing..."):
        result = process_query(query)

        st.subheader("🔍 Parsed Query")
        st.json(result["Parsed Query"])

        st.subheader("📄 Retrieved Clauses")
        for idx, clause in enumerate(result["Top Retrieved Clauses"], 1):
            st.markdown(f"**Clause {idx}:** {clause}")

        st.subheader("✅ Decision")
        st.json(result["Decision"])
