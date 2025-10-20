from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class Vote:
    def __init__(
        self,
        feature_id: UUID,
        user_identifier: str,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.feature_id = feature_id
        self.user_identifier = user_identifier
        self.created_at = created_at or datetime.utcnow()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vote):
            return False
        return (
            self.feature_id == other.feature_id
            and self.user_identifier == other.user_identifier
        )

    def __hash__(self) -> int:
        return hash((self.feature_id, self.user_identifier))

    def __repr__(self) -> str:
        return f"Vote(feature_id={self.feature_id}, user={self.user_identifier})"
