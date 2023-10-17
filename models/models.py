from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

model_config = {"form_name": "vehicle", "form_id": "None", "action": "add, update, delete, get", "payload": "None"}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSignIn(BaseModel):
    username: str
    company: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    password: str
    email: str | None = None
    role: str
    verified: bool | None = None
    passwordConfirm: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


user_sign_in = {"username": "mohammad", "company": "pars", "full_name": "heidary", "disabled": False,
                "password": "qwerty67",
                "email": "mohammad@gmail.com", "role": "user"}


class UserInDB(BaseModel):
    username: str
    company: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    password: str | None = None
    email: str | None = None
    role: str | None = None
    verified: bool | None = None
    passwordConfirm: str | None = None
    verification_code: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True

class FormInfo(BaseModel):
    form_name: str
    form_group: str
