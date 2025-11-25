from fastapi import FastAPI, HTTPException
from extractor import get_profile_id
import os

app = FastAPI(title="X Profile ID → Works 2025")

@app.get("/")
async def root():
    return {"message": "Use /id/username  •  Example: /id/elonmusk"}

@app.get("/id/{username}")
async def profile_id(username: str):
    result = await get_profile_id(username)
    if not result:
        raise HTTPException(status_code=404, detail=f"User @{username} not found or blocked")
    return {"username": username.removeprefix("@"), "profile_id": result}
