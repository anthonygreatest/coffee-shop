from pydantic import BaseModel


class GetAllOrdersSchema(BaseModel):
    id: str
    created: str
    customerName: str