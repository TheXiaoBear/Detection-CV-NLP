from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from cv_app.db.database import Base, engine

from cv_app.api.detect import router as detect_router

from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from infra.nacos.registry import (
    register_service,
    unregister_service
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    await asyncio.to_thread(
        Base.metadata.create_all,
        bind=engine
    )

    await register_service(
        "cv-service",
        8001
    )

    yield

    await unregister_service(
        "cv-service",
        8001
    )

    engine.dispose()


app = FastAPI(
    title="CV Service",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(detect_router)


@app.get("/")
def root():
    return {
        "message": "cv services running"
    }