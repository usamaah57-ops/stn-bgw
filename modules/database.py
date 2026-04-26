import sqlite3

# -----------------------------------
# Initialize database
# -----------------------------------
def init_db():
    conn = sqlite3.connect("services.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS services (
            flight TEXT,
            reg TEXT,
            date TEXT,
            service TEXT,
            start TEXT,
            end TEXT,
            PRIMARY KEY (flight, reg, date, service)
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------------
# Save service (Start / End)
# -----------------------------------
def save_service(flight, reg, date, service, time, mode):
    conn = sqlite3.connect("services.db")
    c = conn.cursor()

    # Check if record exists
    c.execute("SELECT * FROM services WHERE flight=? AND reg=? AND date=? AND service=?",
              (flight, reg, date, service))
    row = c.fetchone()

    if row:
        if mode == "start":
            c.execute("UPDATE services SET start=? WHERE flight=? AND reg=? AND date=? AND service=?",
                      (time, flight, reg, date, service))
        elif mode == "end":
            c.execute("UPDATE services SET end=? WHERE flight=? AND reg=? AND date=? AND service=?",
                      (time, flight, reg, date, service))
    else:
        if mode == "start":
            c.execute("INSERT INTO services (flight, reg, date, service, start, end) VALUES (?, ?, ?, ?, ?, ?)",
                      (flight, reg, date, service, time, None))
        elif mode == "end":
            c.execute("INSERT INTO services (flight, reg, date, service, start, end) VALUES (?, ?, ?, ?, ?, ?)",
                      (flight, reg, date, service, None, time))

    conn.commit()
    conn.close()

# -----------------------------------
# Load services
# -----------------------------------
def load_services(flight, date):
    conn = sqlite3.connect("services.db")
    c = conn.cursor()
    c.execute("SELECT service, start, end FROM services WHERE flight=? AND date=?", (flight, date))
    rows = c.fetchall()
    conn.close()

    data = {}
    for service, start, end in rows:
        data[service] = {"start": start, "end": end}
    return data
