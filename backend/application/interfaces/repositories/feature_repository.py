from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities import Feature


class FeatureRepository(ABC):
    @abstractmethod
    async def create(self, feature: Feature) -> Feature:
        pass

    @abstractmethod
    async def get_by_id(self, feature_id: UUID) -> Optional[Feature]:
        pass

    @abstractmethod
    async def list_all(
        self, sort_by: str = "created_at", order: str = "desc", limit: int = 50
    ) -> List[Feature]:
        pass

    @abstractmethod
    async def update(self, feature: Feature) -> Feature:
        pass
