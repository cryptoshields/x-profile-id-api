from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="X Profile ID API — FINAL")

@app.get("/")
async def root():
    return {"info": "Use /id/username"}

@app.get("/id/{username}")
async def get_id(username: str):
    username = username.lstrip("@")
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(f"https://api.vante.me/twitter/id/{username}")
            if r.status_code == 200 and r.text.strip().isdigit():
                return {"username": username, "profile_id": r.text.strip()}
        except:
            pass
    raise HTTPException(404, f"User @{username} not found")
