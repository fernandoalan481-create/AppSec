"""Base Collector class for plugin system."""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseCollector(ABC):
    """Abstract base for all OSINT collectors."""
    
    name: str = "base"
    
    def __init__(self):
        self.errors: list[str] = []
        self.data: list[dict] = []

    
    @abstractmethod
    def collect(self, nome: str, user: str) -> dict[str, Any]:
        """
        Collect OSINT data for target. 
        Must return standardized dict: {'data': list[dict], 'errors': list[str]}
        """
        pass

