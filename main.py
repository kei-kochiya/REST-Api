from fastapi import FastAPI
from database.connection import init_db
from routers import character

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(character.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Proseka API! Visit /docs for the interactive API documentation."}