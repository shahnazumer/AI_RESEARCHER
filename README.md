# 📚 Research AI Agent with LangGraph, Gemini & arXiv

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Streamlit](https://img.shields.io/badge/Streamlit-frontend-red)](https://streamlit.io/)  
[![uv](https://img.shields.io/badge/Package-uv-yellow)](https://github.com/astral-sh/uv) 

An **AI-powered research assistant** that helps you **search, read, analyze, and write research papers**.  
Built with **LangChain, LangGraph, and Google Generative AI (Gemini)**, this agent provides an end-to-end workflow for academic research.

---

## 🚀 Features

- 🔍 **Search arXiv** – Find the latest research papers by topic.  
- 📖 **Read PDFs** – Extract and analyze text from scientific papers.  
- 🧠 **Reasoning Agent** – ReAct architecture + Gemini for deep analysis.  
- ✍️ **Write Papers** – Generate structured LaTeX research content.  
- 📄 **Export as PDF** – Render LaTeX into professional-quality PDFs.  

---

## 🛠 Installation

This project uses **[uv](https://github.com/astral-sh/uv)** for dependency management.

### 1. Clone the repository
```bash
git clone https://github.com/shahnazumer/AI_RESEARCHER.git
```

### 2. Create & Activate Environment
```bash
# Create virtual environment
uv venv

# Activate (Linux/Mac)
source .venv/bin/activate  

# Activate (Windows)
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv add requirements.txt
```

### 4. Install Tectonic (LaTeX → PDF)

 - Download from Tectonic Releases
 - Ensure tectonic is available in your system PATH.
 - Or update TECTONIC_PATH in write_pdf.py.

### 5. Set Up Environment Variables
```bash
Create a .env file and add your API key:
GOOGLE_API_KEY=your_google_api_key_here
```

▶️ Usage
```bash
Run the Streamlit frontend:
uv run streamlit run frontend.py
```

This will launch a chat-based interface to interact with the research AI.

⚡ Quickstart Example

Try with a sample topic as an example:
```bash
Write me research paper on quantum computing
```
The agent will:
 - Fetch recent arXiv papers
 - Summarize key findings
 - Suggest future research directions
 - Write a LaTeX research paper
 - Render it as a PDF in the output/ directory

📂 Project Structure
```bash
.
├── ai_researcher.py     # Main CLI entrypoint
├── arxiv_tool.py        # arXiv search integration
├── read_pdf.py          # PDF reading utility
├── write_pdf.py         # LaTeX → PDF rendering
├── frontend.py          # Streamlit chat interface
├── requirements.txt     # Dependencies
└── .env                 # API keys (ignored by git)
```

⚠️ Notes

 - Requires a valid Google Generative AI API Key.
 - Tectonic must be installed for LaTeX → PDF rendering.
 - Intended for research and educational purposes only.

📜 License

MIT License – free to use and modify.

✨ With this assistant, you can go from idea → literature review → paper draft → polished PDF.
