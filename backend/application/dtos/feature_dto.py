from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateFeatureDTO:
    title: str
    description: str
    author_name: str


@dataclass
class FeatureResponseDTO:
    id: UUID
    title: str
    description: str
    author_name: str
    votes_count: int
    created_at: datetime
    updated_at: datetime


@dataclass
class VoteDTO:
    user_identifier: str
