import httpx

async def get_profile_id(username: str) -> str | None:
    username = username.lstrip("@").lower()
    
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Twitter-Active-User": "yes",
        "X-Twitter-Client-Language": "en",
        "Content-Type": "application/json",
    }

    params = {
        "variables": '{"screen_name":"' + username + '","withSafetyModeUserFields":true}',
        "features": '{"hidden_profile_likes_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}'
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(
            "https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjMg/UserByScreenName",
            params=params,
            headers=headers
        )
        try:
            data = r.json()
            return data["data"]["user"]["rest_id"]
        except:
            return None
