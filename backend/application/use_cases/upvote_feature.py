from uuid import UUID

from application.dtos import FeatureResponseDTO, VoteDTO
from application.interfaces.repositories import FeatureRepository, VoteRepository
from domain.exceptions import DuplicateVoteException, FeatureNotFoundException
from domain.value_objects import Vote


class UpvoteFeatureUseCase:
    def __init__(
        self, feature_repository: FeatureRepository, vote_repository: VoteRepository
    ):
        self.feature_repository = feature_repository
        self.vote_repository = vote_repository

    async def execute(self, feature_id: UUID, dto: VoteDTO) -> FeatureResponseDTO:
        feature = await self.feature_repository.get_by_id(feature_id)

        if not feature:
            raise FeatureNotFoundException(str(feature_id))

        vote_exists = await self.vote_repository.exists(
            feature_id, dto.user_identifier
        )

        if vote_exists:
            raise DuplicateVoteException(str(feature_id), dto.user_identifier)

        vote = Vote(feature_id=feature_id, user_identifier=dto.user_identifier)
        await self.vote_repository.create(vote)

        feature.increment_vote()
        updated_feature = await self.feature_repository.update(feature)

        return FeatureResponseDTO(
            id=updated_feature.id,
            title=updated_feature.title,
            description=updated_feature.description,
            author_name=updated_feature.author_name,
            votes_count=updated_feature.votes_count,
            created_at=updated_feature.created_at,
            updated_at=updated_feature.updated_at,
        )
