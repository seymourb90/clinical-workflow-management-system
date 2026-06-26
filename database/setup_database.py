import sqlite3

conn = sqlite3.connect("clinical_workflow.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    phone_number TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS visits (
    visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    department TEXT NOT NULL,
    provider TEXT NOT NULL,
    status TEXT NOT NULL,
    check_in_time TEXT NOT NULL,
    discharge_time TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS visit_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id INTEGER NOT NULL,
    note_type TEXT NOT NULL,
    note_text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
)
""")

conn.commit()
conn.close()

print("Database created successfully.")