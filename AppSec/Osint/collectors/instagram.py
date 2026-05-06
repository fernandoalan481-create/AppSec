from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, Error
from core.base import BaseCollector
from core.browser import BrowserManager
from config.settings import USER_AGENT, TIMEOUT_PLAYWRIGHT
import json


class InstagramCollector(BaseCollector):
    name = "instagram"

    def collect(self, nome: str, user: str) -> dict:
        base_url = f"https://www.instagram.com/{user}/"

        dados = {
            "status": "Analyzing...",
            "nome_publico": "N/A",
            "bio": "-",
            "seguidores": "-",
            "url": base_url
        }

        self.data = []
        self.errors = []

        print(f"[LOG] InstagramCollector: Starting analysis for {user}")

        try:
            # 🔥 PLAYWRIGHT GLOBAL (CORREÇÃO PRINCIPAL)
            browser = BrowserManager.start()
            page = browser.new_page()

            page.set_extra_http_headers({"User-Agent": USER_AGENT})
            page.goto(base_url, timeout=TIMEOUT_PLAYWRIGHT)
            page.wait_for_timeout(3000)

            html = page.content()

            # perfil inexistente
            if "Sorry, this page isn't available" in html:
                dados["status"] = "Profile private/non-existent"

            else:
                # JSON-LD parsing robusto
                scripts = page.locator('script[type="application/ld+json"]').all()

                for script in scripts:
                    try:
                        content = script.inner_text().strip()
                        ld_data = json.loads(content)

                        if isinstance(ld_data, list):
                            ld_data = ld_data[0] if ld_data else {}

                        if isinstance(ld_data, dict):
                            dados["nome_publico"] = ld_data.get("name", dados["nome_publico"])
                            dados["bio"] = ld_data.get("description", dados["bio"])
                            break

                    except Exception:
                        continue

                # fallback OG meta
                try:
                    desc = page.locator('meta[property="og:description"]').first
                    if desc.count() > 0:
                        og = desc.get_attribute("content")
                        if og:
                            dados["bio"] = og.split(" • ")[0]
                except:
                    pass

                dados["status"] = "Public data collected"

            page.close()

        except PlaywrightTimeoutError:
            dados["status"] = "Timeout - blocked/slow"
            self.errors.append("timeout")

        except Error as e:
            dados["status"] = f"Playwright error: {str(e)[:100]}"
            self.errors.append(str(e))

        except Exception as e:
            dados["status"] = f"Unexpected: {str(e)[:100]}"
            self.errors.append(str(e))

        self.data = [dados]

        print(f"[LOG] InstagramCollector: Status {dados['status']}")

        return {
            "data": self.data,
            "errors": self.errors
        }