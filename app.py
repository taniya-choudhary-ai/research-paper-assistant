import streamlit as st
import os

from pdf_processor import extract_text, create_chunks

from rag import (
    add_chunks_to_database,
    generate_answer,
    analyze_paper
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Research Paper Assistant",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("📚 Research Paper Assistant")

st.write(
    "Upload a research paper, ask questions, "
    "and generate an AI-powered analysis."
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("📚 Research Paper Assistant")

    st.write("### Features")

    st.write("📄 PDF Upload")
    st.write("🧩 Text Chunking")
    st.write("🔎 Semantic Search")
    st.write("🧠 RAG Question Answering")
    st.write("📝 Paper Summary")
    st.write("🎯 Key Contributions")
    st.write("⚠️ Limitations")
    st.write("🚀 Future Work")

    st.divider()

    st.write(
        "Built using Python, Streamlit, "
        "ChromaDB, Sentence Transformers "
        "and Google Gemini."
    )


# ==========================================
# PDF UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "📄 Upload your research paper",
    type=["pdf"]
)


# ==========================================
# PROCESS PDF
# ==========================================

if uploaded_file:

    # --------------------------------------
    # Save PDF
    # --------------------------------------

    os.makedirs(
        "data/papers",
        exist_ok=True
    )

    pdf_path = os.path.join(
        "data/papers",
        uploaded_file.name
    )

    with open(
        pdf_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    st.success(
        "PDF uploaded successfully! ✅"
    )


    # --------------------------------------
    # Extract Text
    # --------------------------------------

    with st.spinner(
        "Extracting text from PDF..."
    ):

        pages = extract_text(
            pdf_path
        )

    st.success(
        f"Extracted {len(pages)} pages! 📄"
    )


    # --------------------------------------
    # Create Chunks
    # --------------------------------------

    with st.spinner(
        "Creating text chunks..."
    ):

        chunks = create_chunks(
            pages
        )

    st.success(
        f"Created {len(chunks)} chunks! 🧩"
    )


    # --------------------------------------
    # Store Chunks in ChromaDB
    # --------------------------------------

    with st.spinner(
        "Adding paper to knowledge base..."
    ):

        add_chunks_to_database(
            chunks,
            uploaded_file.name
        )

    st.success(
        "Paper added to knowledge base! 🧠"
    )


    # ======================================
    # PAPER INFORMATION
    # ======================================

    st.subheader("📊 Paper Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Pages",
            len(pages)
        )

    with col2:

        st.metric(
            "Text Chunks",
            len(chunks)
        )

    with col3:

        st.metric(
            "File Type",
            "PDF"
        )


    st.info(
        f"📄 Current paper: **{uploaded_file.name}**"
    )


    # ======================================
    # EXTRACTED TEXT
    # ======================================

    st.subheader(
        "📄 Extracted Text"
    )

    for page in pages:

        with st.expander(
            f"Page {page['page']}"
        ):

            st.write(
                page["text"]
            )


    # ======================================
    # CHUNKS
    # ======================================

    st.subheader(
        "🧩 Text Chunks"
    )

    st.write(
        f"Total chunks: {len(chunks)}"
    )

    for i, chunk in enumerate(chunks):

        with st.expander(
            f"Chunk {i + 1} — Page {chunk['page']}"
        ):

            st.write(
                chunk["text"]
            )


    # ======================================
    # QUESTION ANSWERING
    # ======================================

    st.divider()

    st.subheader(
        "🔎 Ask About the Paper"
    )

    question = st.text_input(
        "Enter your question",
        placeholder=(
            "Example: What is the main "
            "contribution of this paper?"
        )
    )


    if question:

        with st.spinner(
            "Searching the paper and "
            "generating an answer..."
        ):

            try:

                answer, sources = generate_answer(
                    question
                )


                # --------------------------
                # ANSWER
                # --------------------------

                st.subheader(
                    "💡 Answer"
                )

                st.write(
                    answer
                )


                # --------------------------
                # SOURCES
                # --------------------------

                st.subheader(
                    "📚 Sources"
                )

                shown_pages = set()

                for source in sources:

                    page = source["page"]

                    if page not in shown_pages:

                        st.write(
                            f"📄 Page {page}"
                        )

                        shown_pages.add(
                            page
                        )


            except Exception as e:

                st.error(
                    f"❌ Error generating answer: {e}"
                )


    # ======================================
    # PAPER ANALYSIS
    # ======================================

    st.divider()

    st.subheader(
        "📊 Paper Analysis"
    )

    st.write(
        "Use prompt engineering to generate "
        "different types of research paper analysis."
    )


    analysis_type = st.selectbox(
        "Choose an analysis type:",
        [
            "Summary",
            "Key Contributions",
            "Limitations",
            "Future Work"
        ]
    )


    if st.button(
        "🚀 Generate Analysis"
    ):

        with st.spinner(
            f"Generating {analysis_type}..."
        ):

            try:

                analysis = analyze_paper(
                    analysis_type
                )


                st.subheader(
                    f"📌 {analysis_type}"
                )

                st.markdown(
                    analysis
                )


            except Exception as e:

                st.error(
                    f"❌ Error generating analysis: {e}"
                )


# ==========================================
# ABOUT PROJECT
# ==========================================

st.divider()

st.subheader(
    "ℹ️ About This Project"
)

st.write(
    """
### 📚 Research Paper Assistant

This application uses **Retrieval-Augmented Generation (RAG)**
to help researchers understand academic papers.

### 🔧 Technologies Used

- Python
- Streamlit
- PyMuPDF
- Sentence Transformers
- ChromaDB
- Google Gemini

### 🔄 Project Workflow

PDF
→ Text Extraction
→ Chunking
→ Embeddings
→ ChromaDB
→ Semantic Search
→ Gemini
→ Final Answer

### ✨ Features

- 📄 Research paper upload
- 🔎 Question answering
- 🧠 RAG-based retrieval
- 📝 Automatic paper summary
- 🎯 Key contribution extraction
- ⚠️ Limitation analysis
- 🚀 Future work identification
- 📚 Source page references

### 🎯 Purpose

The goal of this project is to reduce the time researchers
spend reading and understanding academic papers by providing
an AI-powered research assistant.
"""
)