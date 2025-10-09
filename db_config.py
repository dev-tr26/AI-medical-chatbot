import mysql.connector 
from mysql.connector import Error
import os 
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DB")


def get_connection():
    try:
        conn = mysql.connector.connect(
            host = DB_HOST,
            user = DB_USER,
            password = DB_PASSWORD,
            database = DB_NAME,
            auth_plugin='mysql_native_password'
        )
        return conn 
    except Error as e:
        print("Error in connecting to MySQL: ", e)
        return None


def init_db():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(255),
            role ENUM('user','bot'),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()


def fetch_all_chat_history():
    """Example function to fetch all chat messages"""
    conn = get_connection()
    messages = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chat_history ORDER BY created_at ASC")
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
    return messages


if __name__ == "__main__":
    init_db()
    rows = fetch_all_chat_history()
    print("Current chat history:", rows)