import sqlite3

conn = sqlite3.connect('../shepherd.db')  # Zamijenite 'ime_baze.db' sa stvarnim imenom vaše baze
cursor = conn.cursor()
cursor.execute("SELECT * FROM korisnici")
rows = cursor.fetchall()
for row in rows:
    print(row)
cursor.close()
conn.close()
