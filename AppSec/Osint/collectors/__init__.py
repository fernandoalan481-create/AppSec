"""
Collectors registry for explicit loading.
"""

from collectors.github import GithubCollector
from collectors.google import GoogleCollector
from collectors.instagram import InstagramCollector

__all__ = [
    "GithubCollector",
    "GoogleCollector",
    "InstagramCollector",
]