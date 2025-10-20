from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import VoteRepository
from domain.value_objects import Vote
from infrastructure.database.models import VoteModel


class VoteRepositoryImpl(VoteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, vote: Vote) -> Vote:
        vote_model = VoteModel(
            id=vote.id,
            feature_id=vote.feature_id,
            user_identifier=vote.user_identifier,
            created_at=vote.created_at,
        )
        self.session.add(vote_model)
        await self.session.flush()
        await self.session.refresh(vote_model)
        return self._to_value_object(vote_model)

    async def get_by_feature_and_user(
        self, feature_id: UUID, user_identifier: str
    ) -> Optional[Vote]:
        result = await self.session.execute(
            select(VoteModel).where(
                VoteModel.feature_id == feature_id,
                VoteModel.user_identifier == user_identifier,
            )
        )
        vote_model = result.scalar_one_or_none()
        return self._to_value_object(vote_model) if vote_model else None

    async def exists(self, feature_id: UUID, user_identifier: str) -> bool:
        vote = await self.get_by_feature_and_user(feature_id, user_identifier)
        return vote is not None

    def _to_value_object(self, model: VoteModel) -> Vote:
        return Vote(
            id=model.id,
            feature_id=model.feature_id,
            user_identifier=model.user_identifier,
            created_at=model.created_at,
        )
