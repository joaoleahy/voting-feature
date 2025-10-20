from uuid import UUID

from application.dtos import FeatureResponseDTO
from application.interfaces.repositories import FeatureRepository
from domain.exceptions import FeatureNotFoundException


class GetFeatureUseCase:
    def __init__(self, feature_repository: FeatureRepository):
        self.feature_repository = feature_repository

    async def execute(self, feature_id: UUID) -> FeatureResponseDTO:
        feature = await self.feature_repository.get_by_id(feature_id)

        if not feature:
            raise FeatureNotFoundException(str(feature_id))

        return FeatureResponseDTO(
            id=feature.id,
            title=feature.title,
            description=feature.description,
            author_name=feature.author_name,
            votes_count=feature.votes_count,
            created_at=feature.created_at,
            updated_at=feature.updated_at,
        )
