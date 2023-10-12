from pydantic import BaseModel

model_config = {"form_name": "vehicle", "form_id": "None", "action": "add, update, delete, get", "payload": "None"}


class Request(BaseModel):
    form_name: str
    form_id: str
    action: str
    payload: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    company: str
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str


class UserSignIn(BaseModel):
    username: str
    company: str
    full_name: str | None = None
    disabled: bool | None = None
    password: str


user_sign_in = {"username": "mohammad", "password": "qwerty67", "email": "mohammad@gmail.com"}


class UserInDB(User):
    hashed_password: str
