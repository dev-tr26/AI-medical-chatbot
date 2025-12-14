import time
import logging

logging.basicConfig(
    filename="tests/logs/performance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def test_response_time(mock_chat_service):
    session_id = "perf_test"
    user_input = "What triggers migraines?"
    start = time.time()
    resp = mock_chat_service.get_response(session_id, user_input)
    duration = time.time() - start
    logging.info(f"Query: {user_input} | Duration: {duration:.2f}s | Response: {resp}")
    assert resp == "Mocked response"
    assert duration < 2.0
