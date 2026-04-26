import sqlite3
from datetime import datetime
# Create tables if they don't exist
def init_db():
    conn = sqlite3.connect("flight_data.db")
    c = conn.cursor()

    # Services table
    c.execute("""
        CREATE TABLE IF NOT EXISTS services (
            key TEXT PRIMARY KEY,
            time TEXT,
            staff TEXT
        )
    """)

    # Archive table
    c.execute("""
        CREATE TABLE IF NOT EXISTS archive (
            flight TEXT,
            reg TEXT,
            date TEXT,
            key TEXT,
            time TEXT,
            staff TEXT
        )
    """)

    conn.commit()
    conn.close()

# Initialize DB on import
init_db()

  
