from typing import List

from application.dtos import FeatureResponseDTO
from application.interfaces.repositories import FeatureRepository


class ListFeaturesUseCase:
    def __init__(self, feature_repository: FeatureRepository):
        self.feature_repository = feature_repository

    async def execute(
        self, sort_by: str = "created_at", order: str = "desc", limit: int = 50
    ) -> List[FeatureResponseDTO]:
        valid_sort_fields = ["votes", "created_at"]
        valid_orders = ["asc", "desc"]

        if sort_by not in valid_sort_fields:
            sort_by = "created_at"

        if order not in valid_orders:
            order = "desc"

        if limit < 1 or limit > 100:
            limit = 50

        features = await self.feature_repository.list_all(sort_by, order, limit)

        return [
            FeatureResponseDTO(
                id=feature.id,
                title=feature.title,
                description=feature.description,
                author_name=feature.author_name,
                votes_count=feature.votes_count,
                created_at=feature.created_at,
                updated_at=feature.updated_at,
            )
            for feature in features
        ]
