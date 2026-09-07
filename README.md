📚 Research Paper Assistant

An AI-powered research paper assistant that uses Retrieval-Augmented Generation (RAG) to help users understand academic research papers quickly.

🎯 Problem

Researchers and students often spend a significant amount of time reading lengthy research papers to find important information such as the research problem, methodology, contributions, limitations, and future work.

This project provides an interactive AI assistant that allows users to upload a research paper and ask questions about its content.

💡 Solution

The application uses RAG (Retrieval-Augmented Generation).

The workflow is:

Research Paper PDF
        ↓
Text Extraction
        ↓
Text Chunking
        ↓
Embeddings
        ↓
ChromaDB
        ↓
Semantic Search
        ↓
Relevant Context
        ↓
Prompt Engineering
        ↓
Google Gemini
        ↓
Answer


The system retrieves relevant sections of the uploaded paper and provides them as context to Gemini before generating the response.

🏗️ Architecture
                    📄 PDF
                      │
                      ▼
               PDF Processing
                      │
                      ▼
                Text Chunks
                      │
                      ▼
              Embedding Model
                      │
                      ▼
                  ChromaDB
              Vector Database
                      │
                      │
User ───────► Question
                      │
                      ▼
               Semantic Search
                      │
                      ▼
               Relevant Chunks
                      │
                      ▼
              Prompt Engineering
                      │
                      ▼
                Gemini LLM
                      │
                      ▼
                  Response

✨ Features
📄 PDF Upload

Users can upload research papers in PDF format.

🧩 Text Chunking

The extracted paper text is divided into smaller chunks for efficient retrieval.

🔎 Semantic Search

The application searches the vector database for chunks relevant to the user's question.

🧠 RAG Question Answering

Retrieved paper content is provided to Gemini as context to generate grounded answers.

📝 Paper Summary

Generates a structured summary containing:

Research problem
Motivation
Proposed approach
Methodology
Main results
Conclusion
🎯 Key Contributions

Identifies the major contributions of the research paper.

⚠️ Limitations

Identifies limitations mentioned by the authors and potential limitations that can be inferred from the paper.

🚀 Future Work

Identifies future research directions mentioned or suggested by the paper.

📚 Source References

The application displays the relevant page numbers used during retrieval.

🛠️ Technologies
Technology	Purpose
Python	Main programming language
Streamlit	Web application
PyMuPDF	PDF text extraction
Sentence Transformers	Text embeddings
ChromaDB	Vector database
Google Gemini	Large Language Model
python-dotenv	API key management
📁 Project Structure
LLM PROJECT/
│
├── app.py
├── rag.py
├── pdf_processor.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── data/
│   └── papers/
│
└── venv/

Important

The following files/folders should not be uploaded to GitHub:

.env
venv/
__pycache__/
data/chroma_db/


They are excluded using .gitignore.

⚙️ Installation
1. Create a virtual environment
python -m venv venv

2. Activate it on Windows
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

🔑 API Configuration

Create a .env file in the project directory:

GEMINI_API_KEY=your_api_key_here


Replace your_api_key_here with your Gemini API key.

Never upload .env to GitHub.

▶️ Run the Application

Start Streamlit using:

streamlit run app.py


The application will open in your browser.

🧪 Example

Upload a research paper such as:

Attention Is All You Need


Then ask:

What is the main contribution of this paper?


The system retrieves relevant sections from the paper and generates an answer using Gemini.

Users can also generate:

Summary
Key Contributions
Limitations
Future Work

🧠 Prompt Engineering

The application uses different prompts for different tasks.

For question answering, the model is instructed to:

Use the retrieved paper context.
Avoid making up information.
Answer clearly and concisely.
State when the answer cannot be found in the uploaded paper.
Provide relevant page references when possible.

Different prompts are used for:

Task	Purpose
Summary	Understand the complete paper
Key Contributions	Identify major contributions
Limitations	Identify research limitations
Future Work	Identify future research directions
📊 Evaluation

The system can be evaluated using factual questions about the uploaded research paper.

Example:

Question	Expected Information
What is the main contribution?	Transformer architecture
Why use self-attention?	Efficient dependency modeling and parallelization
What tasks were evaluated?	Machine translation and parsing
What are the key contributions?	Attention-based architecture and related mechanisms

The generated answers can be manually compared with the original paper for correctness and relevance.

⚠️ Challenges
PDF Processing

Research papers can have complex formatting, which can make text extraction difficult.

Chunking

Choosing an appropriate chunk size is important for retrieving useful context.

Retrieval Quality

The quality of the final answer depends on retrieving the correct chunks.

Hallucination

LLMs can sometimes generate unsupported information. The prompts therefore instruct Gemini to rely on the retrieved paper context.

API Quotas

The Gemini API is subject to usage and quota limits, particularly when using the free tier.

🚀 Future Enhancements

Possible improvements include:

Multi-paper comparison
Multiple document collections
Chat history
Exact text citations
OCR support for scanned papers
Improved retrieval techniques
Research-paper comparison tables
User authentication
Advanced evaluation metrics
🎓 Project Objective

The objective of this project is to reduce the time researchers spend reading and understanding academic papers by providing an AI-powered assistant based on Retrieval-Augmented Generation.

The project demonstrates the integration of:

PDF Processing
      +
Text Embeddings
      +
Vector Database
      +
Semantic Search
      +
RAG
      +
Prompt Engineering
      +
Large Language Model

📌 Project Status
Core Features
 PDF Upload
 PDF Text Extraction
 Text Chunking
 Embeddings
 ChromaDB
 Semantic Search
 RAG Question Answering
 Gemini Integration
 Prompt Engineering
 Summary
 Key Contributions
 Limitations
 Future Work
Bonus
 Multi-Paper Comparison
👨‍💻 Conclusion

The Research Paper Assistant demonstrates how RAG, vector databases, embeddings, prompt engineering, and large language models can be combined to create a practical AI-powered research tool.

The application enables users to interact with academic papers using natural language and quickly obtain relevant answers and structured research insights.

:::

