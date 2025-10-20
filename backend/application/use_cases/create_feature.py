from application.dtos import CreateFeatureDTO, FeatureResponseDTO
from application.interfaces.repositories import FeatureRepository
from domain.entities import Feature
from domain.exceptions import InvalidFeatureDataException


class CreateFeatureUseCase:
    def __init__(self, feature_repository: FeatureRepository):
        self.feature_repository = feature_repository

    async def execute(self, dto: CreateFeatureDTO) -> FeatureResponseDTO:
        if not dto.title or len(dto.title) > 200:
            raise InvalidFeatureDataException("Title must be between 1 and 200 characters")

        if not dto.description:
            raise InvalidFeatureDataException("Description is required")

        if not dto.author_name or len(dto.author_name) > 100:
            raise InvalidFeatureDataException("Author name must be between 1 and 100 characters")

        feature = Feature(
            title=dto.title,
            description=dto.description,
            author_name=dto.author_name,
        )

        created_feature = await self.feature_repository.create(feature)

        return FeatureResponseDTO(
            id=created_feature.id,
            title=created_feature.title,
            description=created_feature.description,
            author_name=created_feature.author_name,
            votes_count=created_feature.votes_count,
            created_at=created_feature.created_at,
            updated_at=created_feature.updated_at,
        )
