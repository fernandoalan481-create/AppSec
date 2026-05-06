"""GitHub Profile Collector - Real implementation."""
from core.base import BaseCollector
import requests

class GithubCollector(BaseCollector):
    name = "github"
    
    def collect(self, nome: str, user: str) -> dict:
        self.data = []
        url = f"https://github.com/{user}"
        
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 404:
                data_item = {
                    "status": "Profile not found",
                    "url": url,
                    "error": "404 - User does not exist"
                }
            elif resp.status_code == 200:
                data_item = {
                    "status": "Profile found",
                    "url": url,
                    "name": nome,
                    "repos": "Available" 
                }
            else:
                data_item = {
                    "status": f"Suspended/Private ({resp.status_code})",
                    "url": url
                }
        except Exception:
            data_item = {
                "status": "Error accessing GitHub",
                "url": url
            }
        
        self.data = [data_item]
        print(f"[LOG] GithubCollector: {data_item['status']} for {user}")
        return {
            "data": self.data,
            "errors": self.errors
        }

