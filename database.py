import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        request_data VARCHAR(255),
        response_data TEXT,
        status_code INT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    connection.commit()
    cursor.close()
    connection.close()