from typing import Optional

from pydantic import BaseModel, UUID4

class User(BaseModel):
    id: Optional[UUID4] = None
    name: str
    email: str

class CreateUser(BaseModel):
    name: str
    email: str


class UpdateUser(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class File(BaseModel):
    id: Optional[UUID4] = None
    filename: str
    path: str
    user_id: UUID4


class AddFile(BaseModel):
    filename: str
    path: str
    user_id: UUID4