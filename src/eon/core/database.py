import sqlite3
from pathlib import Path


class ConversationStore:
    
    def __init__(self, db_path=None):
        if db_path is None:
            data_dir = Path.home() / ".local" / "share" / "eon"
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = data_dir / "eon.db"

        self.db_path = str(db_path)
        self._initialize_database()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize_database(self):
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK (
                        role IN ('user', 'assistant')
                    ),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id)
                        REFERENCES conversations(id)
                        ON DELETE CASCADE
                )
            """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_conversation
                ON messages(conversation_id, id)
            """)

    def create_conversation(self, title="New conversation"):
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO conversations (title) VALUES (?)",
                (title,),
            )
            return cursor.lastrowid

    def add_message(self, conversation_id, role, content):
        if role not in ("user", "assistant"):
            raise ValueError("Role must be 'user' or 'assistant'.")

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO messages (conversation_id, role, content)
                VALUES (?, ?, ?)
                """,
                (conversation_id, role, content),
            )

            connection.execute(
                """
                UPDATE conversations
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (conversation_id,),
            )

    def get_messages(self, conversation_id):
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, role, content, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id
                """,
                (conversation_id,),
            ).fetchall()

            return [dict(row) for row in rows]

    def list_conversations(self):
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    c.id,
                    c.title,
                    c.created_at,
                    c.updated_at,
                    COUNT(m.id) AS message_count
                FROM conversations c
                LEFT JOIN messages m
                    ON m.conversation_id = c.id
                GROUP BY c.id
                ORDER BY c.updated_at DESC, c.id DESC
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def delete_conversation(self, conversation_id):
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM conversations WHERE id = ?",
                (conversation_id,),
            )
