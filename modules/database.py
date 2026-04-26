import sqlite3
import os
import json

DB_PATH = "database.db"

# -------------------------------------------------
# Create database and tables if not exist
# -------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Services table
    c.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight TEXT,
            reg TEXT,
            date TEXT,
            service TEXT,
            time TEXT,
            staff TEXT
        )
    """)

    # Documents table
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight TEXT,
            date TEXT,
            service TEXT,
            filename TEXT
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------------------------
# Save service
# -------------------------------------------------
def save_service(flight, reg, date, service, time, staff):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Delete old record for same service
    c.execute("""
        DELETE FROM services 
        WHERE flight=? AND date=? AND service=?
    """, (flight, date, service))

    # Insert new record
    c.execute("""
        INSERT INTO services (flight, reg, date, service, time, staff)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (flight, reg, date, service, time, staff))

    conn.commit()
    conn.close()


# -------------------------------------------------
# Load services
# -------------------------------------------------
def load_services(flight, date):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT service, time, staff 
        FROM services 
        WHERE flight=? AND date=?
    """, (flight, date))

    rows = c.fetchall()
    conn.close()

    data = {}
    for service, time, staff in rows:
        data[service] = {"time": time, "staff": staff}

    return data


# -------------------------------------------------
# Save document
# -------------------------------------------------
def save_document(flight, date, service, filename):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Delete old document for same service
    c.execute("""
        DELETE FROM documents 
        WHERE flight=? AND date=? AND service=?
    """, (flight, date, service))

    # Insert new document
    c.execute("""
        INSERT INTO documents (flight, date, service, filename)
        VALUES (?, ?, ?, ?)
    """, (flight, date, service, filename))

    conn.commit()
    conn.close()


# -------------------------------------------------
# Load documents
# -------------------------------------------------
def load_documents(flight, date):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT service, filename 
        FROM documents 
        WHERE flight=? AND date=?
    """, (flight, date))

    rows = c.fetchall()
    conn.close()

    data = {}
    for service, filename in rows:
        data[service] = filename

    return data
