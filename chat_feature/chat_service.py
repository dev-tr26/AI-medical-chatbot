# chat_service.py
import os
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain, create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hf_embeddings
from src.prompt import system_prompt
from chat_history import save_message, get_history

# -----------------------------
# Pinecone and LLM setup (unchanged)
# -----------------------------
embeddings = download_hf_embeddings()
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 4})

chat_model = ChatGroq(
    grok_api_key=os.getenv("GROK_API_KEY"),
    model="qwen/qwen3-32b",
    max_tokens=512,
    reasoning_format="parsed",
    max_retries=3,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """
Previous conversation context:
{chat_history}

Current question: {input}

Please provide a response considering the conversation history above.
""")
])

# Chain setup
que_ans_chain = create_stuff_documents_chain(chat_model, prompt)
rag_chain = create_retrieval_chain(retriever, que_ans_chain)

# -----------------------------
# In-memory session cache for performance
# -----------------------------
session_cache = {}  # {session_id: [{"role": "user", "message": "hi"}, ...]}

def get_response(session_id, user_input):
    """
    Generate a chatbot response using RAG + session history.
    Keeps history in memory and also logs to MySQL.
    """

    # Load from memory cache or DB
    if session_id not in session_cache:
        session_cache[session_id] = get_history(session_id)

    # Add user message to cache & DB
    session_cache[session_id].append({"role": "user", "message": user_input})
    save_message(session_id, "user", user_input)

    # Prepare chat context text
    chat_context = "\n".join(
        [f"{m['role']}: {m['message']}" for m in session_cache[session_id]]
    )

    # Generate response via LangChain RAG
    try:
        response = rag_chain.invoke({"input": user_input, "chat_history": chat_context})
        bot_message = response.get("answer", "Sorry, I couldn’t generate a response.")
    except Exception as e:
        print("Error generating response:", e)
        bot_message = "I'm having trouble processing that right now. Please try again."

    # Save bot reply to cache & DB
    session_cache[session_id].append({"role": "bot", "message": bot_message})
    save_message(session_id, "bot", bot_message)

    return bot_message


def clear_session_cache(session_id):
    """
    Clear only the in-memory session data (frontend-level clear chat).
    Does NOT delete anything from the database.
    """
    if session_id in session_cache:
        session_cache.pop(session_id, None)
