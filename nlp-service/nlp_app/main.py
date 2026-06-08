from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from nlp_app.db.database import Base, engine

from nlp_app.api.sentence import router as sentence_router

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
    title="NLP Service",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(sentence_router)


@app.get("/")
def root():
    return {
        "message": "nlp services running"
    }