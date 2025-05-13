import os
import chromadb
from openai import OpenAI
import streamlit as st

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["openrouter_api_key"]
)

MODEL = st.secrets.get("model_name", "mistralai/mistral-7b-instruct:free")


# Загружаем системный промт из markdown-файла
with open(os.path.join(os.path.dirname(__file__), "system_prompt.md"), "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# ChromaDB
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_or_create_collection(name="docs")

def is_strategic_query(q: str) -> bool:
    keywords = ["что такое", "ИИ", "LLM", "бот", "польза", "зачем", "как помогает"]
    return any(kw.lower() in q.lower() for kw in keywords)

def ask_question(query: str) -> str:
    results = collection.query(query_texts=[query], n_results=3)
    context = "\n".join(results["documents"][0])

    strategy_prompt = (
        "\n\nТакже объясни, что такое ИИ и LLM, как они применяются в бизнесе, и какую выгоду это даёт клиенту."
        if is_strategic_query(query) else ""
    )

    prompt = f"""{SYSTEM_PROMPT}

Контекст:
{context}

Вопрос: {query}
{strategy_prompt}

Ответ:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content
