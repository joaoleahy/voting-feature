from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.config.settings import get_settings
from infrastructure.database.models import Base
from infrastructure.database.connection import engine
from presentation.api.routes import features_router, health_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Feature Voting System API",
    description="A RESTful API for voting on feature requests",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(features_router)
app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "message": "Feature Voting System API",
        "docs": "/docs",
        "health": "/api/health",
    }
