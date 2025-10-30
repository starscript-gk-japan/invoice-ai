import sqlite3
import os

class ExampleDB:
    def __init__(self, db_path="examples.db"):
        self.db_path = db_path
        # Create directory if path contains folders
        os.makedirs(os.path.dirname(db_path), exist_ok=True) if "/" in db_path else None
        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        """Create the examples table if it does not exist"""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS examples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL
                )
            """)

    def insert_example(self, text):
        """Insert a single example sentence"""
        with self.conn:
            self.conn.execute("INSERT INTO examples (text) VALUES (?)", (text,))

    def get_all_examples(self):
        """Retrieve all example sentences"""
        cur = self.conn.cursor()
        cur.execute("SELECT text FROM examples")
        return [row[0] for row in cur.fetchall()]

    def close(self):
        """Close the database connection"""
        self.conn.close()
