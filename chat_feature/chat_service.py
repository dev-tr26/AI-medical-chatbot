import os
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain, LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from src.helper import download_embeddings
from src.prompt import system_prompt
from chat_feature.chat_history import save_message, get_history
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY 
os.environ['GROK_API_KEY'] = GROK_API_KEY

embeddings = download_embeddings()
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

chat_model = ChatGroq(
    api_key=GROK_API_KEY,
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

# Create the chains
llm_chain = LLMChain(llm=chat_model, prompt=prompt)
que_ans_chain = create_stuff_documents_chain(llm=chat_model,prompt=prompt)
rag_chain = create_retrieval_chain(retriever, que_ans_chain)


# {session_id: [{"role":"user","message":"..."}, {"role":"bot","message":"..."}]}
session_cache = {}



def get_response(session_id: str, user_input: str) -> str:
    """
    Generate a chatbot response using RAG + session history.
    Stores history in memory for context and also logs all messages to DB.
    """
    # Load history from memory or DB
    if session_id not in session_cache:
        session_cache[session_id] = get_history(session_id)

    # Add user message to memory & DB
    session_cache[session_id].append({"role": "user", "message": user_input})
    save_message(session_id, "user", user_input)

    # Prepare chat context
    chat_context = "\n".join([f"{m['role']}: {m['message']}" for m in session_cache[session_id]])

    # Generate response
    try:
        response = rag_chain.invoke({"input": user_input, "chat_history": chat_context})
        bot_message = response.get("answer", "Sorry, I couldn't generate a response.")
    except Exception as e:
        print("Error generating response:", e)
        bot_message = "I'm having trouble processing that right now. Please try again."

    # Save bot response to memory & DB
    session_cache[session_id].append({"role": "bot", "message": bot_message})
    save_message(session_id, "bot", bot_message)

    return bot_message


def clear_session_cache(session_id: str):
    """
    Clear only the in-memory session data (frontend-level clear chat).
    Does NOT delete anything from the database.
    """
    if session_id in session_cache:
        session_cache.pop(session_id, None)


def get_recent_history(session_id: str, limit: int = 10):
    """
    Get the most recent messages for a session.
    Useful for quick context or displaying recent conversation.
    """
    if session_id in session_cache:
        return session_cache[session_id][-limit:]
    return get_history(session_id)[-limit:]
