import sqlite3

conn = sqlite3.connect("cvs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cvs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo TEXT,
    es_valido INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Tabla 'cvs' creada (o ya existía).")
