"""
Everything that talks directly to the SQLite database file.

The app does NOT create the database: you build database/app.db yourself
with the sqlite3 command (see README.md, section 3). The app only connects to it.

You normally do NOT need to edit this file.
"""
import re
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "database" / "app.db"
BUILD_COMMAND = 'sqlite3 -bail :memory: ".read database/build.sql"'
QUERY_SECONDS = 5


def exists():
    return DB_PATH.exists() and DB_PATH.stat().st_size > 0


def connect():
    """A READ-ONLY connection: the app only runs queries, it never changes app.db."""
    conn = sqlite3.connect(DB_PATH.as_uri() + "?mode=ro", uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def limit_time(conn, seconds=QUERY_SECONDS):
    """Stop any statement on this connection that runs longer than `seconds`."""
    deadline = time.monotonic() + seconds
    conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 10000)


_STRING = re.compile(r"'(?:[^']|'')*'")


def without_strings(sql):
    return _STRING.sub("''", sql)
