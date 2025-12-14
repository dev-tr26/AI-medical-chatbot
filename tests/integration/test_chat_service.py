import logging

logging.basicConfig(
    filename="tests/logs/chat_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def test_get_response(mock_chat_service):
    session_id = "test123"
    user_input = "What are flu symptoms?"
    response = mock_chat_service.get_response(session_id, user_input)
    logging.info(f"Query: {user_input} | Response: {response}")
    assert response == "Mocked response"
    assert session_id in mock_chat_service.session_cache
    assert len(mock_chat_service.session_cache[session_id]) == 2

def test_clear_session_cache(mock_chat_service):
    session_id = "test_clear"
    mock_chat_service.session_cache[session_id] = [{"role":"user","message":"hi"}]
    mock_chat_service.clear_session_cache(session_id)
    assert session_id not in mock_chat_service.session_cache

def test_get_recent_history(mock_chat_service):
    session_id = "test_history"
    mock_chat_service.session_cache[session_id] = [{"role":"user","message":"msg1"}]
    recent = mock_chat_service.get_recent_history(session_id, limit=1)
    assert recent == [{"role":"user","message":"msg1"}]
