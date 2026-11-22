import sqlite3

from fastapi import FastAPI

from checker import DB_PATH

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "broken"}


@app.get("/status")
def status():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT url, status, code, response_time, checked_at
        FROM checks
        WHERE id IN (SELECT MAX(id) FROM checks GROUP BY url)
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]