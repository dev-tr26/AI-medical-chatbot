from flask import Flask, request, redirect,render_template
from src.helper import download_hf_embeddings 
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain 
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain 
from langchain_pinecone import PineconeVectorStore
from flask import jsonify 
from src.prompt import *
from dotenv import load_dotenv
import os

app =Flask(__name__)

load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY 
os.environ['GROK_API_KEY'] = GROK_API_KEY

embeddings = download_hf_embeddings()



index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name = index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 4})

chat_model = ChatGroq(
    grok_api_key = GROK_API_KEY,
    model="qwen/qwen3-32b",
    max_tokens= 512,
    reasoning_format="parsed",
    max_retries=3,
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human","""
Previous conversation context:
{chat_history}

Current question: {input}

Please provide a response considering the conversation history above.       

""")    
])

que_ans_chain = create_stuff_documents_chain(chat_model, prompt)
rag_chain = create_retrieval_chain(retriever, que_ans_chain)

@app.rote("/")
def index():
    return render_template("chatbot.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    