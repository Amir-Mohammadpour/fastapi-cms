from fastapi import FastAPI
from app.api.endpoints import auth, posts
from app.database import engine, Base
import asyncio

app = FastAPI(
    title="Simple CMS API (Async)",
    description="A simple asynchronous CMS API with FastAPI",
    version="1.0.0",
)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Async CMS API!"}
