from dataclasses import dataclass

@dataclass
class Products:
    category: str = None
    limit: int = None
    page: int = None