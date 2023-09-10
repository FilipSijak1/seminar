import sqlite3

class database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS korisnici (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print("Greška prilikom kreiranja tablice:", str(e))
        finally:
            cursor.close()

    def close(self):
        self.conn.close()

# Inicijalizacija baze
db = database('shepherd.db')
