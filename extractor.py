import httpx
import json

async def get_profile_id(username: str) -> str | None:
    url = "https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjMg/UserByScreenName"
    variables = json.dumps({
        "screen_name": username,
        "withSafetyModeUserFields": True
    })
    features = json.dumps({
        "hidden_profile_likes_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True
    })
    params = {"variables": variables, "features": features}
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Twitter-Active-User": "yes",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                user = data.get("data", {}).get("user", {})
                profile_id = user.get("rest_id") or user.get("id_str")
                if profile_id:
                    return profile_id
        except Exception as e:
            print(f"Error: {e}")
    return None
