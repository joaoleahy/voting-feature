from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos import CreateFeatureDTO, VoteDTO
from application.use_cases import (
    CreateFeatureUseCase,
    GetFeatureUseCase,
    ListFeaturesUseCase,
    UpvoteFeatureUseCase,
)
from domain.exceptions import (
    DuplicateVoteException,
    FeatureNotFoundException,
    InvalidFeatureDataException,
)
from infrastructure.database.connection import get_db
from infrastructure.database.repositories import FeatureRepositoryImpl, VoteRepositoryImpl
from presentation.api.schemas import CreateFeatureRequest, FeatureResponse, VoteRequest

router = APIRouter(prefix="/api/v1/features", tags=["features"])


@router.post("", response_model=FeatureResponse, status_code=201)
async def create_feature(
    request: CreateFeatureRequest,
    session: AsyncSession = Depends(get_db),
):
    try:
        feature_repo = FeatureRepositoryImpl(session)
        use_case = CreateFeatureUseCase(feature_repo)

        dto = CreateFeatureDTO(
            title=request.title,
            description=request.description,
            author_name=request.author_name,
        )

        result = await use_case.execute(dto)
        return FeatureResponse(**result.__dict__)
    except InvalidFeatureDataException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("", response_model=List[FeatureResponse])
async def list_features(
    sort_by: str = Query("created_at", regex="^(votes|created_at)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    try:
        feature_repo = FeatureRepositoryImpl(session)
        use_case = ListFeaturesUseCase(feature_repo)

        results = await use_case.execute(sort_by, order, limit)
        return [FeatureResponse(**result.__dict__) for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{feature_id}", response_model=FeatureResponse)
async def get_feature(
    feature_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    try:
        feature_repo = FeatureRepositoryImpl(session)
        use_case = GetFeatureUseCase(feature_repo)

        result = await use_case.execute(feature_id)
        return FeatureResponse(**result.__dict__)
    except FeatureNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{feature_id}/vote", response_model=FeatureResponse)
async def upvote_feature(
    feature_id: UUID,
    request: VoteRequest,
    session: AsyncSession = Depends(get_db),
):
    try:
        feature_repo = FeatureRepositoryImpl(session)
        vote_repo = VoteRepositoryImpl(session)
        use_case = UpvoteFeatureUseCase(feature_repo, vote_repo)

        dto = VoteDTO(user_identifier=request.user_identifier)
        result = await use_case.execute(feature_id, dto)
        return FeatureResponse(**result.__dict__)
    except FeatureNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateVoteException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
