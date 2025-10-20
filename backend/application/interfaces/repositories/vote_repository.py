from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.value_objects import Vote


class VoteRepository(ABC):
    @abstractmethod
    async def create(self, vote: Vote) -> Vote:
        pass

    @abstractmethod
    async def get_by_feature_and_user(
        self, feature_id: UUID, user_identifier: str
    ) -> Optional[Vote]:
        pass

    @abstractmethod
    async def exists(self, feature_id: UUID, user_identifier: str) -> bool:
        pass
