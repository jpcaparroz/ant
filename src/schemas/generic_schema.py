from pydantic import BaseModel


class BaseLoginSchema(BaseModel):
    access_token: str
    bearer: str


class HttpDetail(BaseModel):
    detail: str