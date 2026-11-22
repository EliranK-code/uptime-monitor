import sqlite3

from checker import init_db, load_sites, save_result


def test_load_sites_skips_empty_lines(tmp_path):
    sites_file = tmp_path / "sites.txt"
    sites_file.write_text("https://a.com\n\n   \nhttps://b.com\n")
    assert load_sites(sites_file) ==["https://a.com", "https://b.com"]

def test_save_result_stores_row():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    save_result(conn, "2026-01-01 00:00:00", "https://a.com", "UP", 200, 0.1)
    rows = conn.execute("SELECT url, status, code FROM checks").fetchall()
    assert rows == [("https://a.com", "UP", 200)]