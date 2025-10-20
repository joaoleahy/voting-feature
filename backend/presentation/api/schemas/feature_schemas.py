from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateFeatureRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    author_name: str = Field(..., min_length=1, max_length=100)


class FeatureResponse(BaseModel):
    id: UUID
    title: str
    description: str
    author_name: str
    votes_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VoteRequest(BaseModel):
    user_identifier: str = Field(..., min_length=1, max_length=100)
