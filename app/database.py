import psycopg2
from .config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city VARCHAR(100),
        temperature FLOAT,
        humidity FLOAT,
        weather VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()