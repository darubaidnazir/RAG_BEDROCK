import streamlit as st
from bedrock_service import query_knowledge_base

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Enterprise RAG System",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    .card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info(
        "This is an Enterprise RAG (Retrieval-Augmented Generation) system "
        "powered by AWS Bedrock.\n\n"
        "Ask questions from your internal knowledge base."
    )
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.success("Developed by **Dar Ubaid Nazir**")

# ---------------- HEADER ---------------- #
st.markdown("""
<div style="text-align:center;">
    <h1>🧠 Enterprise Knowledge Base</h1>
    <p style="color:gray;">AI-powered Q&A over internal documents</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ---------------- #
st.markdown("### 🔍 Ask your question")

query = st.text_input(
    "Enter your question", 
    placeholder="e.g. What are the company policies for remote work?",
    label_visibility="collapsed"
)
# ---------------- BUTTON ---------------- #
if st.button("🚀 Ask Question") and query:

    with st.spinner("🤖 Thinking... Retrieving relevant documents..."):
        answer, citations = query_knowledge_base(query)

    # ---------------- ANSWER CARD ---------------- #
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💡 Answer")
    st.write(answer)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- CITATIONS CARD ---------------- #
    if citations:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📚 Sources")
        for i, c in enumerate(citations, 1):
            st.markdown(f"**{i}.** {c}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.markdown(
    "<center style='color:gray;'>Built with ❤️ using Streamlit | © 2026 Dar Ubaid Nazir</center>",
    unsafe_allow_html=True
)