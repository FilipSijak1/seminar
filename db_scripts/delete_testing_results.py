import sqlite3


conn = sqlite3.connect('../shepherd.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM test_results')
conn.commit()
conn.close()

print("Svi testovi su obrisani iz baze podataka.")
