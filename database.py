"""Store and retrieve tickets in SQLite using explicit SQL statements."""

import sqlite3
from contextlib import closing
from pathlib import Path

# Keep the database beside this file, regardless of the working directory.
DB_PATH = Path(__file__).resolve().parent / "tickets.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    # closing closes the connection; the inner context commits or rolls back.
    with closing(connect()) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                    description TEXT NOT NULL CHECK (length(trim(description)) > 0),
                    status TEXT NOT NULL DEFAULT 'open'
                        CHECK (status IN ('open', 'in_progress', 'closed'))
                )
            """)


def create_ticket(title, description):
    with closing(connect()) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO tickets (title, description) VALUES (?, ?)",
                (title, description),
            )
            row = connection.execute(
                "SELECT id, title, description, status FROM tickets WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return dict(row)


def list_tickets():
    with closing(connect()) as connection:
        rows = connection.execute(
            "SELECT id, title, description, status FROM tickets ORDER BY id"
        ).fetchall()

        tickets = []
        for row in rows:
            tickets.append(dict(row))
        return tickets


def get_ticket(ticket_id):
    with closing(connect()) as connection:
        row = connection.execute(
            "SELECT id, title, description, status FROM tickets WHERE id = ?",
            (ticket_id,),
        ).fetchone()

        if row is None:
            return None
        return dict(row)


def update_ticket(ticket_id, new_status):
    with closing(connect()) as connection:
        with connection:
            cursor = connection.execute(
                "UPDATE tickets SET status = ? WHERE id = ?",
                (new_status, ticket_id),
            )
            if cursor.rowcount == 0:
                return None

            row = connection.execute(
                "SELECT id, title, description, status FROM tickets WHERE id = ?",
                (ticket_id,),
            ).fetchone()
        return dict(row)


def delete_ticket(ticket_id):
    with closing(connect()) as connection:
        with connection:
            cursor = connection.execute(
                "DELETE FROM tickets WHERE id = ?", (ticket_id,)
            )
        return cursor.rowcount > 0
