import uuid
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from validate_docbr import CPF
from app.core.exceptions import UnderageUserException
from app.core.security import validate_password_strength

cpf_validator = CPF()

class UserCreate(BaseModel):
    nickname: str = Field(min_length=3)
    email: EmailStr
    cpf: str = Field(min_length=11, max_length=11)
    password: str = Field(min_length=8, max_length=255)
    date_of_birth: date

    model_config = ConfigDict(from_attributes=True)

    @field_validator('cpf')
    @classmethod
    def check_cpf(cls, value: str):
        clean_cpf = "".join(filter(str.isdigit, value))

        if not cpf_validator.validate(clean_cpf):
            raise ValueError("CPF inválido")

        return clean_cpf

    @field_validator("date_of_birth")
    @classmethod
    def check_age(cls, value: date):
        today = date.today()
            # ano atual - ano informado     mes e dia atual for menor que mes e dia informado (subtraio para pegar a idade real)
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise UnderageUserException("O usuário deve ser maior de 18 anos", 400)
        return value

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str) -> str:
        validate_password_strength(value)
        return value


class UserResponse(BaseModel):
    id: uuid.UUID
    nickname: str
    email: str
    points: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Usar SecretStr
class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

    model_config = ConfigDict(from_attributes=True)
