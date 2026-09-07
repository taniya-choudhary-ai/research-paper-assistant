import os
import time

import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


# ==========================================
# GEMINI CLIENT
# ==========================================

client_gemini = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# EMBEDDING MODEL
# ==========================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# CHROMADB
# ==========================================

chroma_client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="research_papers"
)


# ==========================================
# ADD CHUNKS TO DATABASE
# ==========================================

def add_chunks_to_database(chunks, paper_name):

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):

        text = chunk["text"]

        embedding = embedding_model.encode(
            text
        ).tolist()

        documents.append(text)
        embeddings.append(embedding)

        metadatas.append({
            "paper": paper_name,
            "page": chunk["page"]
        })

        ids.append(
            f"{paper_name}_{i}"
        )

    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


# ==========================================
# SEARCH CHUNKS
# ==========================================

def search_chunks(query, n_results=5):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results


# ==========================================
# GEMINI REQUEST WITH RETRY
# ==========================================

def generate_gemini_response(prompt):

    for attempt in range(3):

        try:

            response = client_gemini.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            # Retry temporary server errors
            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:

                    time.sleep(5)

                else:

                    raise e

            else:

                raise e


# ==========================================
# GENERATE ANSWER
# ==========================================

def generate_answer(question):

    results = search_chunks(
        question,
        n_results=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = ""

    for i, document in enumerate(documents):

        page = metadatas[i]["page"]

        context += (
            f"\n\n--- Page {page} ---\n"
            f"{document}"
        )


    # ======================================
    # RAG PROMPT
    # ======================================

    prompt = f"""
You are an expert research paper assistant.

Answer the user's question using ONLY
the information provided in the research paper
context below.

Do not make up information.

If the answer cannot be found in the context,
say:

"The answer cannot be found in the uploaded paper."

Give a clear and concise answer.

Mention relevant page numbers when possible.

--------------------------------
RESEARCH PAPER CONTEXT
--------------------------------

{context}

--------------------------------
USER QUESTION
--------------------------------

{question}

--------------------------------
ANSWER
--------------------------------
"""


    # ======================================
    # GEMINI
    # ======================================

    answer = generate_gemini_response(
        prompt
    )

    return answer, metadatas


# ==========================================
# ANALYZE PAPER
# ==========================================

def analyze_paper(analysis_type):

    results = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    documents = results["documents"]
    metadatas = results["metadatas"]


    # ======================================
    # LIMIT CONTEXT
    # ======================================

    documents = documents[:30]
    metadatas = metadatas[:30]


    context = ""

    for i, document in enumerate(documents):

        page = metadatas[i]["page"]

        context += (
            f"\n\n--- Page {page} ---\n"
            f"{document}"
        )


    # ======================================
    # PROMPT ENGINEERING
    # ======================================

    if analysis_type == "Summary":

        prompt = f"""
You are an expert research assistant.

Analyze the research paper below.

Create a structured summary containing:

### 1. Research Problem
Explain what problem the paper addresses.

### 2. Motivation
Explain why the problem is important.

### 3. Proposed Approach
Explain the proposed solution.

### 4. Methodology
Explain how the authors conducted the research.

### 5. Main Results
Explain the major findings.

### 6. Conclusion
Summarize the overall conclusion.

Use only information from the paper.

Do not invent information.

--------------------------------
RESEARCH PAPER
--------------------------------

{context}
"""


    elif analysis_type == "Key Contributions":

        prompt = f"""
You are an expert research assistant.

Identify the most important contributions
of this research paper.

Give 4-6 clear bullet points.

For each contribution, briefly explain
why it is important.

Use only information supported by the paper.

Do not invent information.

--------------------------------
RESEARCH PAPER
--------------------------------

{context}
"""


    elif analysis_type == "Limitations":

        prompt = f"""
You are an expert research assistant.

Analyze the limitations of this research paper.

Separate your answer into:

### Limitations explicitly mentioned by the authors

List limitations directly stated by the authors.

### Potential limitations

List reasonable limitations that can be inferred
from the paper.

Clearly label inferred limitations.

Do not present inferred limitations as facts.

Do not invent information.

--------------------------------
RESEARCH PAPER
--------------------------------

{context}
"""


    elif analysis_type == "Future Work":

        prompt = f"""
You are an expert research assistant.

Identify future research directions
related to this paper.

Separate the answer into:

### Future Work Mentioned by the Authors

List future work explicitly mentioned
or suggested by the authors.

### Possible Future Directions

Suggest reasonable directions based
on the paper.

Clearly label these as suggestions.

Do not invent information.

--------------------------------
RESEARCH PAPER
--------------------------------

{context}
"""


    else:

        return "Invalid analysis type."


    # ======================================
    # GEMINI WITH RETRY
    # ======================================

    analysis = generate_gemini_response(
        prompt
    )

    return analysis
