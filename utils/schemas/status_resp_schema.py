from pydantic import BaseModel

class StatusResponseSchema(BaseModel):
    status: str