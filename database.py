import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("scraped_data.db")
        self.create_table()

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraped_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    data TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating table:", str(e))

    def insert_data(self, url, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO scraped_data (url, data)
                VALUES (?, ?)
            """, (url, data))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error inserting data:", str(e))

    def close_connection(self):
        self.conn.close()