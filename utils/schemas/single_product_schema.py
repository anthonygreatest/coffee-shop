from pydantic import Field, BaseModel


class SingleProductSchema(BaseModel):

    id: int
    category: str
    name: str
    isAvailable: bool
    product_description: str = Field(alias='product-description')
    additional_text: str = Field(alias='additionalText')