from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import FeatureRepository, VoteRepository
from application.use_cases import (
    CreateFeatureUseCase,
    GetFeatureUseCase,
    ListFeaturesUseCase,
    UpvoteFeatureUseCase,
)
from infrastructure.database.connection import get_db
from infrastructure.database.repositories import FeatureRepositoryImpl, VoteRepositoryImpl


async def get_feature_repository(
    session: AsyncSession = next(get_db()),
) -> FeatureRepository:
    return FeatureRepositoryImpl(session)


async def get_vote_repository(
    session: AsyncSession = next(get_db()),
) -> VoteRepository:
    return VoteRepositoryImpl(session)


async def get_create_feature_use_case(
    session: AsyncSession = next(get_db()),
) -> CreateFeatureUseCase:
    feature_repo = FeatureRepositoryImpl(session)
    return CreateFeatureUseCase(feature_repo)


async def get_list_features_use_case(
    session: AsyncSession = next(get_db()),
) -> ListFeaturesUseCase:
    feature_repo = FeatureRepositoryImpl(session)
    return ListFeaturesUseCase(feature_repo)


async def get_get_feature_use_case(
    session: AsyncSession = next(get_db()),
) -> GetFeatureUseCase:
    feature_repo = FeatureRepositoryImpl(session)
    return GetFeatureUseCase(feature_repo)


async def get_upvote_feature_use_case(
    session: AsyncSession = next(get_db()),
) -> UpvoteFeatureUseCase:
    feature_repo = FeatureRepositoryImpl(session)
    vote_repo = VoteRepositoryImpl(session)
    return UpvoteFeatureUseCase(feature_repo, vote_repo)
