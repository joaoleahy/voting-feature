from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class Feature:
    def __init__(
        self,
        title: str,
        description: str,
        author_name: str,
        id: Optional[UUID] = None,
        votes_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.author_name = author_name
        self.votes_count = votes_count
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def increment_vote(self) -> None:
        self.votes_count += 1
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"Feature(id={self.id}, title={self.title}, votes={self.votes_count})"
