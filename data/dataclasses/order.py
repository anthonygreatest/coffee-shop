from dataclasses import dataclass
from typing import List


@dataclass
class ListProducts:
    id: int
    quantity: int

@dataclass
class Order:
    customerName: str
    products: List[ListProducts]

