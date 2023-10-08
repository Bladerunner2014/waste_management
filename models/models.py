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
    apn: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    company: str
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str


class UserInDB(User):
    hashed_password: str
