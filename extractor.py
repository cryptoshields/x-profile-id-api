import httpx
import re   # this is built-in, no need to install

async def get_profile_id(username: str) -> str | None:
    username = username.lstrip("@")
    url = f"https://commentpicker.com/twitter-id.php?username={username}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(url)
            if r.status_code == 200:
                match = re.search(r'Twitter ID:\s*(\d+)', r.text)
                if match:
                    return match.group(1)
        except Exception as e:
            print("Error:", e)
    return None
