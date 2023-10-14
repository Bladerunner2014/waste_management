from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

model_config = {"form_name": "vehicle", "form_id": "None", "action": "add, update, delete, get", "payload": "None"}


def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "photo": user["photo"],
        "verified": user["verified"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


class UserBaseSchema(BaseModel):
    name: str
    email: str
    photo: str
    role: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


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


user_sign_in = {"username": "mohammad", "company": "pars", "full_name": "heidary", "disabled": False,
                "password": "qwerty67",
                "email": "mohammad@gmail.com", "role": "user"}


class UserInDB(BaseModel):
    username: str
    company: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str
    email: str | None = None
    role: str


class FormInfo(BaseModel):
    form_name: str
    form_group: str
