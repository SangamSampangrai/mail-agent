import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# Always use the database located in the same directory as this file.
DB_PATH = Path(__file__).resolve().parent / "checkpoints.db"


def initialize_database():
    """
    Create the conversations table if it does not already exist.
    """
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                thread_id TEXT PRIMARY KEY,
                title TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        connection.commit()


def create_conversation(thread_id: str):
    """
    Create a new conversation.
    """
    # Make sure the table exists before inserting.
    initialize_database()

    now = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO conversations (
                thread_id,
                title,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (thread_id, None, now, now),
        )

        connection.commit()


def update_conversation_title(thread_id: str, title: str):
    """
    Update the title and updated time of a conversation.
    """
    now = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            UPDATE conversations
            SET title = ?, updated_at = ?
            WHERE thread_id = ?
            """,
            (title, now, thread_id),
        )

        # IMPORTANT: commit must be inside the with block.
        connection.commit()


def get_conversation_title(thread_id: str) -> str | None:
    """
    Return the title of a conversation.
    """
    with sqlite3.connect(DB_PATH) as connection:
        result = connection.execute(
            """
            SELECT title
            FROM conversations
            WHERE thread_id = ?
            """,
            (thread_id,),
        ).fetchone()

    if result is None:
        return None

    return result[0]


def list_conversations() -> list[tuple[str, str | None]]:
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute("""
    SELECT thread_id, title
    FROM conversations
    ORDER BY updated_at DESC
    
    """).fetchall()
    return rows
