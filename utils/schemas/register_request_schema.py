from pydantic import BaseModel


class RegisterRequestSchema(BaseModel):

    email: str