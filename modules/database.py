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

DB_FILE = "flight_data.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
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

def save_service(key, time, staff):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO services (key, time, staff) VALUES (?, ?, ?)", (key, time, staff))
    conn.commit()
    conn.close()

def load_services():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT key, time, staff FROM services")
    rows = c.fetchall()
    conn.close()
    return {r[0]: {"time": r[1], "staff": r[2]} for r in rows}

def clear_services():
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM services")
    conn.commit()
    conn.close()

def archive_services(flight, reg):
    conn = get_connection()
    c = conn.cursor()
    date = datetime.now().strftime("%d/%m/%Y")

    # Check if already archived
    c.execute("SELECT COUNT(*) FROM archive WHERE flight=? AND reg=? AND date=?", (flight, reg, date))
    exists = c.fetchone()[0]

    if exists > 0:
        conn.close()
        return False

    services = load_services()
    for k, v in services.items():
        c.execute(
            "INSERT INTO archive (flight, reg, date, key, time, staff) VALUES (?, ?, ?, ?, ?, ?)",
            (flight, reg, date, k, v['time'], v['staff'])
        )

    conn.commit()
    conn.close()
    return True

def load_archive():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT flight, reg, date, key, time, staff FROM archive ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows
