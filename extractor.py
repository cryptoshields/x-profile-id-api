import httpx

RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY_HERE"  # From rapidapi.com signup

async def get_profile_id(username: str) -> str | None:
    url = "https://twitter-user-id-username-converter.p.rapidapi.com/twitter-user-id"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "twitter-user-id-username-converter.p.rapidapi.com"
    }
    params = {"username": username}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(url, params=params, headers=headers)
            if r.status_code == 200:
                data = r.json()
                return data.get("id")
        except Exception as e:
            print(f"Error: {e}")
    return None
