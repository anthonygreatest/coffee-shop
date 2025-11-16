from _pydatetime import datetime

from pydantic import BaseModel


class InsideOrderCreatedSchema(BaseModel):
    id: int
    quantity: int


class OrderCreatedSchema(BaseModel):
    id: str
    clientId: str
    created: str
    customerName: str
    products: list