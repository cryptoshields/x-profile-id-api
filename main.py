from fastapi import FastAPI, HTTPException
from extractor import get_profile_id

app = FastAPI(title="X Profile ID Extractor")

@app.get("/")
def home():
    return {"message": "Use /id/{username} → e.g. /id/elonmusk"}

@app.get("/id/{username}")
@app.get("/id")
async def get_id(username: str = None):
    if not username:
        raise HTTPException(400, "Missing username")
    username = username.lstrip("@")
    profile_id = get_profile_id(username)
    if profile_id:
        return {"username": username, "profile_id": profile_id}
    raise HTTPException(404, f"Profile not found or blocked: @{username}")