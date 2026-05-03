import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_listings (
                id          TEXT PRIMARY KEY,
                keyword     TEXT NOT NULL,
                title       TEXT,
                url         TEXT,
                first_seen  TEXT NOT NULL
            )
        """)
        conn.commit()


def is_new(listing_id: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM seen_listings WHERE id = ?", (listing_id,)
        ).fetchone()
    return row is None


def mark_seen(listing: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO seen_listings (id, keyword, title, url, first_seen)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                listing["id"],
                listing.get("keyword", ""),
                listing.get("title", ""),
                listing.get("url", ""),
                datetime.now().isoformat(),
            ),
        )
        conn.commit()


def mark_seen_batch(listings: list[dict]) -> None:
    now = datetime.now().isoformat()
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO seen_listings (id, keyword, title, url, first_seen)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (l["id"], l.get("keyword", ""), l.get("title", ""), l.get("url", ""), now)
                for l in listings
            ],
        )
        conn.commit()
