import streamlit as st
import json
from main import process_insurance_query

st.set_page_config(page_title="Insurance Query Decision System", layout="wide")
st.title("🛡️ Insurance Eligibility Checker")
st.markdown("Enter a natural language query to check if the procedure is eligible under your insurance policy.")

query = st.text_area("📝 Enter your query here:", height=150)

if st.button("🔍 Evaluate Query"):
    if not query.strip():
        st.warning("Please enter a query to evaluate.")
    else:
        with st.spinner("Processing your query..."):
            try:
                result = process_insurance_query(query)
                
                st.success("✅ Decision Completed")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🔍 Parsed Information")
                    st.json(result["parsed_info"])
                with col2:
                    st.subheader("📋 Decision")
                    st.write(f"**Decision:** {result['decision']}")
                    st.write(f"**Justification:** {result['justification']}")

                st.subheader("📄 Policy Clauses Retrieved")
                for i, clause in enumerate(result["policy_clauses"], 1):
                    st.markdown(f"**Clause {i}:** {clause}")

            except Exception as e:
                st.error(f"❌ Error: {e}")
