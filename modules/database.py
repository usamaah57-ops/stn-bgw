import sqlite3

def init_db():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            flight TEXT,
            reg TEXT,
            date TEXT,
            service TEXT,
            start TEXT,
            end TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_service(flight, reg, date, service, time, action):
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    if action == "start":
        cursor.execute("UPDATE services SET start=? WHERE flight=? AND date=? AND service=?",
                       (time, flight, date, service))
    elif action == "end":
        cursor.execute("UPDATE services SET end=? WHERE flight=? AND date=? AND service=?",
                       (time, flight, date, service))
    conn.commit()
    conn.close()

def load_services(flight, date):
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("SELECT service, start, end FROM services WHERE flight=? AND date=?", (flight, date))
    rows = cursor.fetchall()
    conn.close()
    data = {}
    for service, start, end in rows:
        data[service] = {"start": start, "end": end}
    return data

def load_archive():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("SELECT flight, reg, date, service, start, end FROM services")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ✅ الدالة الجديدة لمسح كل الخدمات
def clear_services():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services")
    conn.commit()
    conn.close()
