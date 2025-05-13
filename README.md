# 🤖 QubitAI Ассистент

**QubitAI Ассистент** — это AI-чат-бот, реализованный на [Streamlit](https://streamlit.io/), который отвечает на вопросы пользователей на основе встроенной базы знаний и OpenRouter (LLM API).  
Идеально подходит для демонстрации возможностей ИИ в сфере поддержки, консалтинга и информационных сервисов.

[🧪 Попробовать онлайн](https://chatbotdemo-qubitai.streamlit.app/)

---

## 📦 Возможности

- 💬 Многоразовые диалоги с историей чатов.
- 🧠 Ответы на основе собственной документации (векторная база ChromaDB).
- 🔗 Интеграция с OpenRouter (модель Mistral 7B или любая другая).
- 🚀 Быстрый деплой через Streamlit Cloud.
- 🛡️ Безопасное хранение ключей через `secrets.toml`.

---

## 🧰 Стек технологий

- **Python 3.10+**
- **Streamlit** — UI и логика взаимодействия
- **FAISS** — локальное векторное хранилище
- **OpenRouter API** — языковая модель
- **dotenv / secrets.toml** — управление ключами
- **PyPDF2** — загрузка и индексация PDF-файлов

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/RamilQAEng/Streamlitdemo.git
cd Streamlitdemo
```
### Установка зависимостей

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Добавить переменные в .streamlit/secrets.toml

```bash
openrouter_api_key = "sk-ваш_ключ"
model_name = "mistralai/mistral-7b-instruct:free"
```
### Запуск приложения

```bash
streamlit run main.py   
```
