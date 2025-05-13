import streamlit as st
from qa_engine import ask_question
import uuid
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


if not os.path.exists("faiss_index/index.faiss"):
    import ingest
    ingest.ingest()


st.set_page_config(page_title="Чат-бот QubitAI", layout="wide")


# 💅 Подключаем кастомный стиль
style_path = "styles.css"
with open(style_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


WELCOME_MESSAGE = """👋 Привет! Я ИИ-ассистент QubitAI.  
Я помогу вам разобраться в возможностях чат-ботов, сроках, этапах, интеграциях и стоимости.

Просто напишите вопрос — я отвечу на основе документации проекта."""

# Инициализация сессии
if "chats" not in st.session_state:
    st.session_state["chats"] = {}

if "active_chat" not in st.session_state or st.session_state["active_chat"] not in st.session_state["chats"]:
    chat_id = str(uuid.uuid4())[:8]
    st.session_state["chats"][chat_id] = [{
        "user": None,
        "bot": WELCOME_MESSAGE
    }]
    st.session_state["active_chat"] = chat_id

# === SIDEBAR ===
st.sidebar.title("💬 Ваши чаты")

# Кнопка: Новый чат
if st.sidebar.button("Новый чат"):
    if len(st.session_state["chats"]) >= 3:
        oldest_chat = list(st.session_state["chats"].keys())[0]
        del st.session_state["chats"][oldest_chat]

    new_id = str(uuid.uuid4())[:8]
    st.session_state["chats"][new_id] = [{
        "user": None,
        "bot": WELCOME_MESSAGE
    }]
    st.session_state["active_chat"] = new_id

# Переключение между чатами
for cid in st.session_state["chats"]:
    if st.sidebar.button(f"💭 Чат {cid}", key=f"select_{cid}"):
        st.session_state["active_chat"] = cid

# === MAIN CHAT ZONE ===
st.title("🤖 QubitAI Ассистент")

active_id = st.session_state["active_chat"]
chat_history = st.session_state["chats"][active_id]

# Вывод истории
for entry in chat_history:
    if entry["user"]:
        with st.chat_message("user"):
            st.write(entry["user"])
    if entry["bot"]:
        with st.chat_message("assistant"):
            st.write(entry["bot"])

# Ввод нового сообщения
query = st.chat_input("Введите ваш вопрос...")

if query:
    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Обработка..."):
        answer = ask_question(query)

    with st.chat_message("assistant"):
        st.write(answer)

    # Сохраняем в историю
    st.session_state["chats"][active_id].append({
        "user": query,
        "bot": answer
    })
