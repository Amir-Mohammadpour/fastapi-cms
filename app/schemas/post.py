from datetime import datetime

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, min_length=1)

    model_config = {"extra": "forbid"}


class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    author_id: int

    model_config = {"from_attributes": True}
