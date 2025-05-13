import os
import chromadb
from PyPDF2 import PdfReader
from tqdm import tqdm

CHROMA_PATH = "db"
DATA_PATH = "data"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="docs")

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def ingest():
    for filename in tqdm(os.listdir(DATA_PATH)):
        if filename.endswith(".pdf"):
            path = os.path.join(DATA_PATH, filename)
            text = extract_text_from_pdf(path)
            collection.add(documents=[text], ids=[filename])
    print("✅ Индексация завершена.")

if __name__ == "__main__":
    ingest()
