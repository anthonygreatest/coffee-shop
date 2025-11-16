from pydantic import EmailStr
from dataclasses import dataclass


@dataclass
class Client:
    email: str = None