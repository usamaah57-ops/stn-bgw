import sqlite3
import datetime

DB_NAME = "flight_data.db"


# -----------------------------
# Database initialization
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Table for current flight services
    c.execute("""
        CREATE TABLE IF NOT EXISTS services (
            key TEXT PRIMARY KEY,
            time TEXT,
            staff TEXT
        )
    """)

    # Table for archived flights
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


# -----------------------------
# Services table operations
# -----------------------------
def save_service(key, time, staff):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        INSERT OR REPLACE INTO services (key, time, staff)
        VALUES (?, ?, ?)
        """,
        (key, time, staff)
    )

    conn.commit()
    conn.close()


def load_services():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT key, time, staff FROM services")
    rows = c.fetchall()

    conn.close()

    services = {}
    for key, time, staff in rows:
        services[key] = {
            "time": time,
            "staff": staff
        }

    return services


def clear_services():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM services")

    conn.commit()
    conn.close()


# -----------------------------
# Archive table operations
# -----------------------------
def archive_services(flight, reg):
    """
    Archive current services for a given flight/registration.
    Returns:
        True  -> archived successfully
        False -> already archived today
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Use today's date
    today = datetime.date.today().strftime("%d/%m/%Y")

    # Check if this flight is already archived today
    c.execute(
        """
        SELECT 1 FROM archive
        WHERE flight = ? AND reg = ? AND date = ?
        LIMIT 1
        """,
        (flight, reg, today)
    )
    exists = c.fetchone()

    if exists:
        conn.close()
        return False

    # Load current services
    c2 = conn.cursor()
    c2.execute("SELECT key, time, staff FROM services")
    services = c2.fetchall()

    # Insert into archive
    for key, time, staff in services:
        c.execute(
            """
            INSERT INTO archive (flight, reg, date, key, time, staff)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (flight, reg, today, key, time, staff)
        )

    conn.commit()
    conn.close()
    return True


def load_archive():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        SELECT flight, reg, date, key, time, staff
        FROM archive
        ORDER BY date DESC
        """
    )
    rows = c.fetchall()

    conn.close()
    return rows
