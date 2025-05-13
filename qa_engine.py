import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["openrouter_api_key"]
)

MODEL = st.secrets.get("model_name", "mistralai/mistral-7b-instruct:free")
SYSTEM_PROMPT = "Ты ИИ-ассистент QubitAI. Помоги пользователю разобраться в чат-ботах."

FAISS_PATH = "faiss_index"

# Загружаем FAISS и эмбеддер
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)


def ask_question(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""{SYSTEM_PROMPT}

Контекст:
{context}

Вопрос: {query}

Ответ:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content
