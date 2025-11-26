from fastapi import FastAPI, HTTPException
from extractor import get_profile_id

app = FastAPI(title="X Profile ID API — CommentPicker Version")

@app.get("/")
async def home():
    return {"message": "Use /id/username (e.g., /id/elonmusk)"}

@app.get("/id/{username}")
async def get_id(username: str):
    username = username.removeprefix("@")
    profile_id = await get_profile_id(username)
    if not profile_id:
        raise HTTPException(404, f"User @{username} not found")
    return {"username": username, "profile_id": profile_id}
