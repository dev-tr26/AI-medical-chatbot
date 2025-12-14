from src import helper
from unittest.mock import MagicMock

class DummyDoc:
    def __init__(self, text):
        self.page_content = text
        self.metadata = {}

def test_split_text(monkeypatch):
    docs = [DummyDoc("a"*1200)]
    chunks = helper.split_text(docs)
    assert len(chunks) > 1

def test_download_embeddings(monkeypatch):
    monkeypatch.setattr(helper, "HuggingFaceEmbeddings", lambda model_name, model_kwargs: "embedding_vector")
    embeddings = helper.download_embeddings()
    assert embeddings == "embedding_vector"

def test_load_pdf_files(monkeypatch):
    # Mock DirectoryLoader
    monkeypatch.setattr(helper, "DirectoryLoader", lambda data, **kwargs: MagicMock(load=lambda: ["doc1", "doc2"]))
    docs = helper.load_pdf_files("data")
    assert docs == ["doc1", "doc2"]
