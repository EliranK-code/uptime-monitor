from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent
TIMEOUT = 10


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
    for url in load_sites(BASE_DIR / "sites.txt"):
        status, code, elapsed = check(url)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp, status, code, elapsed, url)


if __name__ == "__main__":
    main()