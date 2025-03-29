from typing import Optional

from pydantic import BaseModel, UUID4

class User(BaseModel):
    id: Optional[UUID4] = None
    name: str
    email: str

class CreateUser(BaseModel):
    name: str
    email: str
