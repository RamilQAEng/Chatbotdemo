from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from PyPDF2 import PdfReader
import os
import pickle

DATA_PATH = "data"
FAISS_PATH = "faiss_index"

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def ingest():
    texts = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(os.path.join(DATA_PATH, filename))
            texts.append(text)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts, embeddings)

    vectorstore.save_local(FAISS_PATH)
    print("✅ Индексация завершена.")

if __name__ == "__main__":
    ingest()
