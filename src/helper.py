from langchain_community.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
import torch


def download_embeddings():
    model_name = "BAAI/bge-small-en-v1.5"
    embedding_vectors = HuggingFaceEmbeddings(
        model_name = model_name,
        model_kwargs={
            "device":"cuda" if torch.cuda.is_available() else "cpu"
        }
    )
    return embedding_vectors


def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls = PyPDFLoader
    )
    
    documents = loader.load()
    return documents



def split_text(minimal_docs):
    text_splitter  = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap = 40
    )
    texts_chunks = text_splitter.split_documents(minimal_docs)
    return texts_chunks

