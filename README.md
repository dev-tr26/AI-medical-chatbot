# 🧠 Medical RAG Chatbot (Flask + LangChain + Pinecone + Groq)

A **Retrieval-Augmented Generation (RAG)**-based **medical chatbot** that retrieves context-aware answers from uploaded medical PDFs using **LangChain**, **Pinecone**, and **Groq’s Qwen3-32B model**.
It integrates **Flask** for the backend, applies a **safety protocol** to minimize hallucinations, and maintains **session-based chat histories** in **MySQL** for analytics and future training.

---

## 🚀 Features

✅ **Retrieval-Augmented Generation (RAG)** – Combines vector-based retrieval from PDFs with LLM-based reasoning.  
✅ **In-Memory + Database Chat History** – Session-level caching with persistent storage in MySQL.  
✅ **Flask Backend** – Simple and extensible REST API backend for chatbot interaction.  
✅ **Safety Protocols** – Filters unreliable or hallucinated responses.  
✅ **Pinecone Vector DB** – High-speed document similarity search.  
✅ **Groq LLM Orchestration** – Uses **Qwen/Qwen3-32B** through Groq API for efficient inference.  
✅ **Embedding Model** – Uses `BAAI/bge-small-en-v1.5` for creating dense vector embeddings.  
✅ **Modular Architecture** – Easy to extend for new data sources or frontends.  

---

## 🧩 System Architecture

```
                ┌────────────────────────┐
                │     User Interface     │
                │   (chatbot.html / UI)  │
                └────────────┬───────────┘
                             │
                             ▼
                     ┌───────────────┐
                     │ Flask Backend │
                     └───────────────┘
                             │
       ┌─────────────────────┴─────────────────────┐
       ▼                                           ▼
┌───────────────┐                           ┌────────────────┐
│ LangChain RAG │                           │  MySQL DB      │
│   Orchestration│                           │ (Chat History) │
└───────┬────────┘                           └────────────────┘
        │
        ▼
┌────────────────┐      ┌────────────────────────┐
│ Pinecone Vector │◄────┤   PDF Embeddings Store │
│   Index Store   │      └────────────────────────┘
└────────────────┘
        │
        ▼
┌──────────────────────────────────────────┐
│ Groq LLM (Qwen/Qwen3-32B via LangChain)  │
└──────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component           | Technology                                |
| ------------------- | ----------------------------------------- |
| **Framework**       | Flask (Python)                            |
| **LLM**             | `qwen/qwen3-32b` (via Groq API)           |
| **Embedding Model** | `BAAI/bge-small-en-v1.5`                  |
| **Vector Database** | Pinecone                                  |
| **RAG Framework**   | LangChain                                 |
| **Database**        | MySQL                                     |
| **Frontend**        | HTML + JavaScript                         |
| **Environment**     | `.env` configuration for keys and secrets |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/medical-rag-chatbot.git
cd medical-rag-chatbot
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Create a `.env` file in the root directory:

```bash
PINECONE_API_KEY=your_pinecone_api_key
GROK_API_KEY=your_groq_api_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=chatbot_db
```

### 5️⃣ Database Setup (MySQL)

Create a table for chat history:

```sql
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255),
    role VARCHAR(10),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6️⃣ Run Flask App

```bash
python app.py
```

Access the chatbot at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 💬 API Endpoints

| Endpoint                   | Method | Description               |
| -------------------------- | ------ | ------------------------- |
| `/`                        | `GET`  | Loads chatbot UI          |
| `/llm_chat`                | `POST` | Send a message to chatbot |
| `/clear_chat/<session_id>` | `POST` | Clear session cache       |
| `/history/<session_id>`    | `GET`  | Retrieve session history  |


---

## 🧱 Core Modules

### 🧩 `chat_feature/chat_service.py`

Implements the RAG logic:

* Loads embeddings and Pinecone retriever
* Connects to Groq LLM
* Retrieves relevant context
* Generates safe responses
* Saves all messages to MySQL and in-memory session

### 🧠 `src/helper.py`

Handles:

* Embedding download
* Vector index management
* PDF preprocessing

### 💾 `chat_feature/chat_history.py`

Handles:

* Saving user/bot messages to MySQL
* Retrieving full or recent history
* Session-based caching for faster responses

---

## 🛡️ Safety Protocol

To avoid **hallucinations** or unsafe outputs:

* The system applies a **“safety protocol” function** that validates LLM outputs before returning.
* If uncertainty or factual mismatch is detected, it responds with:

  > *"I'm having trouble processing that right now. Please try again."*
* Ensures responses are grounded in retrieved PDF context.

---

## 📊 Chat History and Analytics

* Chat logs are stored in **MySQL** with timestamps.
* Each conversation is tracked using a **unique session_id**.
* Data can be used for:

  * Behavioral analytics
  * Fine-tuning LLMs
  * Auditing and compliance


---

## 🩺 Disclaimer

> ⚠️ **This chatbot is intended for educational and informational purposes only.**
> It does **not** replace professional medical advice. Always consult a qualified healthcare provider for medical concerns.


