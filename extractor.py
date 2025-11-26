import httpx
import re

async def get_profile_id(username: str) -> str | None:
    username = username.lstrip("@")
    url = f"https://commentpicker.com/twitter-id.php?username={username}"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(url)
            if r.status_code == 200:
                text = r.text
                # Parse the ID from HTML (e.g., "Twitter ID: 44196397" or meta tag)
                match = re.search(r'Twitter ID:\s*(\d+)', text) or re.search(r'user_id["\']?\s*:\s*["\']?(\d+)', text)
                if match:
                    return match.group(1)
        except Exception as e:
            print(f"Error: {e}")
    return None
