from fastapi import FastAPI, HTTPException
from extractor import get_profile_id

app = FastAPI(title="X Profile ID API — Always On")

@app.get("/")
async def home():
    return {"message": "Use /id/username → example: /id/elonmusk"}

@app.get("/id/{username}")
async def get_id(username: str):
    username = username.removeprefix("@")
    profile_id = await get_profile_id(username)
    if not profile_id:
        raise HTTPException(404, f"User @{username} not found or blocked")
    return {"username": username, "profile_id": profile_id}
