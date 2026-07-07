import uuid
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

class UserCreate(BaseModel):
    nickname: str = Field()
    email: EmailStr
    cpf: str = Field(max_length=11)
    password: str = Field(min_length=8, max_length=255)
    date_of_birth: date

    model_config = ConfigDict(from_attributes=True)

# TODO: Onde fica o field validator do CPF, e como fazer a senha strong?
class UserResponse(BaseModel):
    id: uuid.UUID
    nickname: str
    email: str
    points: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

    model_config = ConfigDict(from_attributes=True)
