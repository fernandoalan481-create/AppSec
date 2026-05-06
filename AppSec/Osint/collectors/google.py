"""Google Dorks Collector - PDF/OSINT Optimized."""

import time
from googlesearch import search
from core.base import BaseCollector
from config.settings import SLEEP_INTERVAL


class GoogleCollector(BaseCollector):
    name = "google"

    def collect(self, nome: str, user: str) -> dict:
        self.data = []
        self.errors = []
        seen = set()

        queries = [
            f'"{nome}"',
            f'"{nome}" filetype:pdf',
            f'"{nome}" site:linkedin.com',
            f'"{nome}" site:github.com',
            f'"{nome}" site:scribd.com',
            f'"{nome}" filetype:pdf "{user}"'
        ]

        print(f"[LOG] GoogleCollector: {len(queries)} queries")

        for q in queries:
            try:
                results = search(q, num_results=8, advanced=True)

                for res in results:
                    url = getattr(res, "url", None)
                    if not url or url in seen:
                        continue

                    seen.add(url)

                    title = getattr(res, "title", "N/A")
                    desc = getattr(res, "description", "")[:200]

                    is_pdf = ".pdf" in url.lower()

                    # =========================
                    # SCORE ENGINE (NOVO)
                    # =========================
                    score = 0

                    if is_pdf:
                        score += 3

                    if nome.lower() in title.lower():
                        score += 2

                    if user.lower() in url.lower():
                        score += 2

                    if "linkedin" in url.lower():
                        score += 1

                    if "github" in url.lower():
                        score += 1

                    self.data.append({
                        "query": q,
                        "title": title,
                        "url": url,
                        "description": desc,
                        "filetype": "PDF" if is_pdf else "Web",
                        "score": score
                    })

                time.sleep(SLEEP_INTERVAL)

            except Exception as e:
                self.errors.append(f"Query error '{q}': {str(e)}")

        # 🔥 ranking por relevância (score)
        self.data.sort(key=lambda x: x.get("score", 0), reverse=True)

        return {
            "data": self.data[:20],
            "errors": self.errors
        }