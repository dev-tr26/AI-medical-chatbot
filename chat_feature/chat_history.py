# chat_history.py
from ..db_config import get_connection

def save_message(session_id, role, message):
    """
    Save a message to the chat history table.
    """
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (session_id, role, message) VALUES (%s, %s, %s)",
            (session_id, role, message)
        )
        conn.commit()
        cursor.close()
        conn.close()

def get_history(session_id):
    """
    Retrieve chat history for a specific session_id.
    """
    conn = get_connection()
    messages = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT role, message FROM chat_history WHERE session_id=%s ORDER BY created_at ASC",
            (session_id,)
        )
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
    return messages

def get_recent_history(session_id, limit=10):
    """
    Get the most recent few messages (for faster contextual retrieval).
    """
    conn = get_connection()
    messages = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT role, message FROM chat_history WHERE session_id=%s ORDER BY created_at DESC LIMIT %s",
            (session_id, limit)
        )
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
    # Reverse order to chronological
    return list(reversed(messages))
