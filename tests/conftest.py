# tests/conftest.py
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure project root is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import chat_feature.chat_service as chat_service

@pytest.fixture
def mock_chat_service():
    # Patch RAG chain to avoid API calls
    chat_service.rag_chain = MagicMock()
    chat_service.rag_chain.invoke = MagicMock(return_value={"answer": "Mocked response"})

    # Patch DB functions in chat_history
    patch_conn = patch("chat_feature.chat_history.get_connection")
    mock_conn_func = patch_conn.start()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn_func.return_value = mock_conn

    patch_save = patch("chat_feature.chat_history.save_message", MagicMock())
    patch_save.start()
    patch_get_history = patch("chat_feature.chat_history.get_history", MagicMock(return_value=[]))
    patch_get_history.start()

    yield chat_service

    patch_conn.stop()
    patch_save.stop()
    patch_get_history.stop()
