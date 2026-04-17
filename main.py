import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load API keys from .env
load_dotenv()

# --- Page Setup ---
st.set_page_config(page_title="AI RAG Assistant", layout="centered")
st.title("🚀 AI Document Assistant")
st.write("Ask questions about your documents using RAG (Llama 3.3 + ChromaDB)")

# --- Initialize AI Models ---
llm = ChatGroq(temperature=0.6, model_name="llama-3.3-70b-versatile")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- UI: File Uploader ---
uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    if uploaded_file.name.endswith(".pdf"):
        loader = PyMuPDFLoader(tmp_file_path)
    else:
        loader = Docx2txtLoader(tmp_file_path)
    
    data = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    st.success(f"Document '{uploaded_file.name}' analyzed and indexed!")

    # --- Chat Interface ---
    user_question = st.text_input("Ask a question about the document:")
    
    if user_question:
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "Use three sentences maximum and keep the answer concise."
            "\n\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        # Format the retrieved documents into a single text string
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Build the logic flow directly
        rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        with st.spinner("Thinking..."):
            # Execute the flow
            response = rag_chain.invoke(user_question)
            st.write("### Answer:")
            st.write(response)

    os.remove(tmp_file_path)