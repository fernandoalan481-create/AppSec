from playwright.sync_api import sync_playwright

class BrowserManager:
    _instance = None
    _playwright = None
    _browser = None

    @classmethod
    def start(cls):
        if cls._browser is None:
            cls._playwright = sync_playwright().start()
            cls._browser = cls._playwright.chromium.launch(
                headless=True,
                args=["--no-sandbox"]
            )
        return cls._browser

    @classmethod
    def stop(cls):
        if cls._browser:
            cls._browser.close()
            cls._playwright.stop()
            cls._browser = None
            cls._playwright = None