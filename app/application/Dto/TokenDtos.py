from pydantic import BaseModel

class Token(BaseModel):
    username: str | None = None
    access_token: str
    token_type: str
