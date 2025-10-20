from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import FeatureRepository
from domain.entities import Feature
from infrastructure.database.models import FeatureModel


class FeatureRepositoryImpl(FeatureRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, feature: Feature) -> Feature:
        feature_model = FeatureModel(
            id=feature.id,
            title=feature.title,
            description=feature.description,
            author_name=feature.author_name,
            votes_count=feature.votes_count,
            created_at=feature.created_at,
            updated_at=feature.updated_at,
        )
        self.session.add(feature_model)
        await self.session.flush()
        await self.session.refresh(feature_model)
        return self._to_entity(feature_model)

    async def get_by_id(self, feature_id: UUID) -> Optional[Feature]:
        result = await self.session.execute(
            select(FeatureModel).where(FeatureModel.id == feature_id)
        )
        feature_model = result.scalar_one_or_none()
        return self._to_entity(feature_model) if feature_model else None

    async def list_all(
        self, sort_by: str = "created_at", order: str = "desc", limit: int = 50
    ) -> List[Feature]:
        sort_column = (
            FeatureModel.votes_count if sort_by == "votes" else FeatureModel.created_at
        )
        order_func = sort_column.desc() if order == "desc" else sort_column.asc()

        result = await self.session.execute(
            select(FeatureModel).order_by(order_func).limit(limit)
        )
        feature_models = result.scalars().all()
        return [self._to_entity(model) for model in feature_models]

    async def update(self, feature: Feature) -> Feature:
        result = await self.session.execute(
            select(FeatureModel).where(FeatureModel.id == feature.id)
        )
        feature_model = result.scalar_one_or_none()

        if feature_model:
            feature_model.votes_count = feature.votes_count
            feature_model.updated_at = feature.updated_at
            await self.session.flush()
            await self.session.refresh(feature_model)
            return self._to_entity(feature_model)

        return feature

    def _to_entity(self, model: FeatureModel) -> Feature:
        return Feature(
            id=model.id,
            title=model.title,
            description=model.description,
            author_name=model.author_name,
            votes_count=model.votes_count,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
