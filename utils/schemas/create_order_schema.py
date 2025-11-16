from pydantic import Field, BaseModel


class InsideProductsSchema(BaseModel):
    id: int
    quantity: int

class CreateOrderSchema(BaseModel):

    customerName: str
    products: list