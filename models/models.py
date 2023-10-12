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


