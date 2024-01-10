from datetime import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr
from fastapi_users import schemas


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    # image: str

    class Config:
        orm_mode = True


class FilteredUserResponse(UserBaseSchema):
    id: int


class PostBaseSchema(BaseModel):
    id: int | None
    user_id: int | None
    title: str
    content: str
    image: str | None
    created_at: datetime | None
    updated_at: datetime | None
    likes_count: int | None
    comments_count: int | None
    categories: List | None
    username: str | None

    class Config:
        orm_mode = True


class CreatePostSchema(PostBaseSchema):
    pass


class PostResponse(PostBaseSchema):
    pass


class UpdatePostSchema(BaseModel):
    id: int | None = None
    user_id: int | None = None
    title: str | None = None
    content: str | None = None
    image: str | None = None
    # created_at: datetime | None = None
    updated_at: datetime | None = None
    likes_count: int | None = None
    comments_count: int | None = None

    class Config:
        orm_mode = True

class ListPostResponse(BaseModel):
    status: str
    results: int
    posts: List[PostResponse]
