import sqlite3


conn = sqlite3.connect('../shepherd.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM korisnici')
conn.commit()
conn.close()

print("Svi korisnici su obrisani iz baze podataka.")
