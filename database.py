import sqlite3

conn = sqlite3.connect("database/phishing.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email_text TEXT,

    prediction TEXT,

    confidence REAL,

    risk_score INTEGER,

    risk_level TEXT,

    threats TEXT,

    analysis TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database Created")