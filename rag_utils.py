import os
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class RAGUtils:
    def __init__(self, pdf_paths):
        docs = []
        for path in pdf_paths:
            if os.path.exists(path):
                loader = PyPDFLoader(path)
                docs.extend(loader.load())
            else:
                print(f"Arquivo {path} não encontrado.", file=sys.stderr)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=200)
        split = text_splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = FAISS.from_documents(documents=split, embedding=embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        print("RAGUtils inicializado com sucesso.", file=sys.stderr)

    def buscar_contexto(self, query):
        docs = self.retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])