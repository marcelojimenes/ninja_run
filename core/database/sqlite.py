import sqlite3
from core.database.db import Database

class SQLiteDatabase(Database):
    def __init__(self, db="ninja_run.db"):
        self.db = db
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_score(self, player_name, score):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (player_name, score))
        conn.commit()
        conn.close()

    def fetch_scores(self, limit=5):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 5")
        scores = cursor.fetchall()
        conn.close()
        return scores