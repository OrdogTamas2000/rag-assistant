# 🚀 AI Document Assistant (RAG)

A professional, fully functional **Retrieval-Augmented Generation (RAG)** web application built with Python. This assistant allows users to upload PDF or Word documents and ask questions about their content in real-time. 

Built with the modern **LangChain Expression Language (LCEL)** architecture, it ensures fast, context-aware answers without hallucinating beyond the provided document.

## ✨ Features
* **Multi-Format Document Processing:** Seamlessly extracts text from PDFs (`PyMuPDF`) and Word documents (`docx2txt`).
* **Advanced Vector Search:** Utilizes local HuggingFace embeddings (`all-MiniLM-L6-v2`) and **ChromaDB** to intelligently chunk and search through large documents without hitting LLM context limits.
* **Smart QA:** Powered by the state-of-the-art **Llama 3.3 70B** model via the lightning-fast Groq API.
* **Modern Architecture:** Built strictly using LangChain's latest `langchain_core` LCEL pipelines (bypassing legacy/deprecated chains).
* **Interactive UI:** A clean, responsive web interface powered by Streamlit.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Framework:** [LangChain (v0.3+)](https://python.langchain.com/)
* **LLM:** Meta Llama 3.3 70B (via [Groq](https://groq.com/))
* **Embeddings:** HuggingFace (`sentence-transformers`)
* **Vector Database:** ChromaDB

## 💻 How to Run It Locally

Follow these steps to test the application on your own machine.

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/ai-document-assistant.git](https://github.com/YOUR_USERNAME/ai-document-assistant.git)
cd ai-document-assistant
```

### 2. Create a virtual environment
Keep your global Python environment clean by creating a virtual bubble:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
Install the exact, tested versions of the required packages:
```bash
pip install -r requirements.txt
```

### 4. Set up your API Key
You will need a free Groq API key to power the language model. 
👉 **[Click here to get your free Groq API Key](https://console.groq.com/keys)**

* Create a file named `.env` in the root directory.
* Add your key like this:
  ```env
  GROQ_API_KEY=your_groq_api_key_here
  ```

### 5. Run the application
```bash
streamlit run main.py
```
The application will automatically open in your default web browser at `http://localhost:8501`.

---
*Note: On the first run, the local HuggingFace embedding model will download a small package (~100MB) to process text vectors. Subsequent runs will be instantaneous.*