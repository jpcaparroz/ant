from pydantic import BaseModel


class BaseLoginSchema(BaseModel):
    acess_token: str
    bearer: str


class HttpDetail(BaseModel):
    detail: str