import sqlite3
import json
import numpy as np
from typing import List, Tuple


def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            source  TEXT NOT NULL,
            text    TEXT NOT NULL,
            vector  TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def is_empty(db_path: str) -> bool:
    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()
    return count == 0


def insert_chunks(db_path: str, sources: List[str], texts: List[str], vectors: np.ndarray):
    conn = sqlite3.connect(db_path)
    rows = [
        (source, text, json.dumps(vec.tolist()))
        for source, text, vec in zip(sources, texts, vectors)
    ]
    conn.executemany("INSERT INTO chunks (source, text, vector) VALUES (?, ?, ?)", rows)
    conn.commit()
    conn.close()


def fetch_all(db_path: str) -> List[Tuple[str, str, np.ndarray]]:
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT source, text, vector FROM chunks").fetchall()
    conn.close()
    return [(r[0], r[1], np.array(json.loads(r[2]))) for r in rows]
