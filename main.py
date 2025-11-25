from fastapi import FastAPI, HTTPException
from extractor import get_profile_id

app = FastAPI(title="X Profile ID API")

@app.get("/")
async def home():
    return {"info": "Use /id/username"}

@app.get("/id/{username}")
async def get_id(username: str):
    profile_id = await get_profile_id(username)
    if not profile_id:
        raise HTTPException(404, f"Profile not found or blocked: @{username}")
    return {"username": username.lstrip("@"), "profile_id": profile_id}
