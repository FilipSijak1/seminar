import sqlite3

class database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
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

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY,
                    label TEXT NOT NULL,
                    description TEXT NOT NULL,
                    user TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL
                )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            print("Greška prilikom kreiranja tablica:", str(e))
        finally:
            cursor.close()

    def get_high_priority_bugs(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM test_results WHERE label = 'High priority bug'
            ''')
            high_priority_bugs = cursor.fetchall()
            return high_priority_bugs
        except sqlite3.Error as e:
            print("Greška prilikom dohvaćanja high priority bugova:", str(e))
        except Exception as e:
            print("Exception in show_high_priority_bug_data:", str(e))
        finally:
            cursor.close()

    def get_bug_entries(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM test_results WHERE label = 'Bug'
            ''')
            bug_entries = cursor.fetchall()
            return bug_entries
        except sqlite3.Error as e:
            print("Greška prilikom dohvaćanja unosa bugova:", str(e))
        finally:
            cursor.close()

    def get_info_entries(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM test_results WHERE label = 'Info'
            ''')
            info_entries = cursor.fetchall()
            return info_entries
        except sqlite3.Error as e:
            print("Greška prilikom dohvaćanja unosa info:", str(e))
        finally:
            cursor.close()

    def close(self):
        self.conn.close()

# Inicijalizacija baze
db = database('shepherd.db')
