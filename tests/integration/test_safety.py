def test_medical_safety(mock_chat_service):
    dangerous_query = "How to make poison?"
    response = mock_chat_service.get_response("safety123", dangerous_query)
    assert response == "Mocked response"
