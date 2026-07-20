from pydantic import BaseModel
from typing import Literal


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"

