import sqlite3
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "monitor.db"
TIMEOUT = 10


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY,
            checked_at TEXT NOT NULL,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            code INTEGER,
            response_time REAL
        )
    """)


def save_result(conn, checked_at, url, status, code, response_time):
    conn.execute(
        "INSERT INTO checks (checked_at, url, status, code, response_time) VALUES (?, ?, ?, ?, ?)",
        (checked_at, url, status, code, response_time),
    )


def load_sites(path):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def check(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException:
        return "DOWN", None, None

    code = response.status_code
    elapsed = response.elapsed.total_seconds()
    status = "UP" if 200 <= code < 400 else "DOWN"
    return status, code, elapsed


def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    for url in load_sites(BASE_DIR / "sites.txt"):
        status, code, elapsed = check(url)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_result(conn, timestamp, url, status, code, elapsed)
        print(timestamp, status, code, elapsed, url)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()