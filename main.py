from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

RAPIDAPI_KEY = "7670518617msh346fc08c9defbdep1ac659jsnfb52401ae2e7"

@app.get("/")
async def home():
    return {"message": "Use /id/username"}

@app.get("/id/{username}")
async def get_id(username: str):
    username = username.removeprefix("@")
    
    url = "https://twitter-user-id-username-converter.p.rapidapi.com/user-id"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "twitter-user-id-username-converter.p.rapidapi.com"
    }
    params = {"username": username}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, params=params, timeout=10.0)
        if r.status_code == 200:
            data = r.json()
            if "id" in data:
                return {"username": username, "profile_id": data["id"]}
    
    raise HTTPException(404, f"User @{username} not found")
