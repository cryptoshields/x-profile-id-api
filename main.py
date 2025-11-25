from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="X Profile ID API – FINAL WORKING VERSION")

@app.get("/")
async def home():
    return {"info": "Use /id/username"}

@app.get("/id/{username}")
async def get_id(username: str):
    username = username.lstrip("@")
    url = f"https://api.vante.me/twitter/id/{username}"
    
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(url)
            if r.status_code == 200 and r.text.isdigit():
                return {"username": username, "profile_id": r.text}
        except:
            pass
    
    raise HTTPException(404, f"User @{username} not found")
