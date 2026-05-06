"""OSINT Framework Settings."""
from pathlib import Path

DATA_DIR = Path("output")
DATA_DIR.mkdir(exist_ok=True)

SLEEP_INTERVAL = 1.5
TIMEOUT_PLAYWRIGHT = 20000
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

