from pydantic import BaseModel, EmailStr


class AllProductResponseSchema(BaseModel):
    id: int
    category: str
    name: str
    isAvailable: bool

class TokenValidatorSchema(BaseModel):
    token: EmailStr