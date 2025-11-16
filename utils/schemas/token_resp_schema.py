from pydantic import BaseModel


class TokenValidationSchema(BaseModel):
    token: str