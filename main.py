from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="X Profile ID API — RapidAPI Version")

# Your RapidAPI key
RAPIDAPI_KEY = "7670518617msh346fc08c9defbdep1ac659jsnfb52401ae2e7"

@app.get("/")
async def home():
    return {"message": "Use /id/username (e.g., /id/elonmusk)"}

@app.get("/id/{username}")
async def get_id(username: str):
    username = username.removeprefix("@")
    url = "https://twitter-user-id-username-converter.p.rapidapi.com/user-id"
    headers = {
        "x-rapidapi-host": "twitter-user-id-username-converter.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {"username": username}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(url, params=params, headers=headers)
            if r.status_code == 200:
                data = r.json()
                profile_id = data.get("id")
                if profile_id:
                    return {"username": username, "profile_id": profile_id}
        except Exception as e:
            print(f"Error: {e}")
    
    raise HTTPException(404, f"User @{username} not found")
