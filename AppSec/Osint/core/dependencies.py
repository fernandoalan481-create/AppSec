"""Dependency checker for OSINT Framework."""
import importlib.util
import sys
import subprocess
from pathlib import Path

DEPS_MAP = {
    'colorama': 'colorama',
    'pyfiglet': 'pyfiglet',
    'playwright': 'playwright.sync_api',
    'googlesearch-python': 'googlesearch'
}

def check_dependencies():
    """Check if all required dependencies are installed."""
    missing = []
    for pip_name, module_path in DEPS_MAP.items():
        spec = importlib.util.find_spec(module_path.split('.')[0])
        if spec is None:
            missing.append(pip_name)
    
    if missing:
        print(f"[!] Missing dependencies: {', '.join(missing)}")
        print(f"[!] Install: pip install {' '.join(missing)}")
        print("[!] For Playwright: python -m playwright install chromium")
        sys.exit(1)

def playwright_browser_check():
    """Verify Playwright browser is installed and launchable."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            browser.close()
        return True
    except Exception as e:
        print(f"[!] Playwright browser issue: {str(e)}")
        print("[!] Fix: python -m playwright install chromium")
        return False

