from chat_feature.chat_history import save_message, get_history, get_recent_history
from unittest.mock import MagicMock

def test_save_and_get_history(monkeypatch):
    # Properly mock DB connection & cursor
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr("chat_feature.chat_history.get_connection", lambda: mock_conn)

    save_message("sess1", "user", "Hello")
    messages = get_history("sess1")
    assert messages == []

def test_get_recent_history(monkeypatch):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr("chat_feature.chat_history.get_connection", lambda: mock_conn)

    recent = get_recent_history("sess1", limit=5)
    assert recent == []
