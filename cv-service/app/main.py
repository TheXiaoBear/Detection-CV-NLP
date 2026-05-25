from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.db.database import Base, engine

from app.api.detect import router as detect_router

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):

    await asyncio.to_thread(
        Base.metadata.create_all,
        bind=engine
    )

    yield

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