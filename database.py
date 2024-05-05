import sqlite3
from PyQt5.QtCore import QObject, pyqtSignal

class Database(QObject):
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
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
            self.error_occurred.emit("Error creating table: {}".format(str(e)))

    def insert_data(self, url, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO scraped_data (url, data)
                VALUES (?, ?)
            """, (url, data))
            self.conn.commit()
        except sqlite3.Error as e:
            self.error_occurred.emit("Error inserting data: {}".format(str(e)))

    def close_connection(self):
        self.conn.close()
